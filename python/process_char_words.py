"""
process_char_words.py

Author: Alan Burwell
Last updated: 13 Jan 22

DPI691MA, Group A4, Game of Thrones

This script processes a JSON database of the number of words each character has
spoken in chronological order written by episode, then generates for each 
character a dict that includes name, total words spoken, an array of words 
spoken per episode, an array of cumulative words spoken per episode, and an 
array of words spoken per season, then exports that new dataset into a JSON.

Input data file taken from Jeffrey Lancaster Game of Thrones Github repository
at https://github.com/jeffreylancaster/game-of-thrones

Input: char_words.json
    JSON database of every character's number of spoken words of every episode
            
Output: all_char_word_counts.json
   example list of dicts 
       [dict, dict, dict]
       
       example dict:
           name: 'jon snow'
           episode_words: [0, 1, 2, 1, 5, 5...]
           cum_episode_words: [0, 1, 3, 4, 9, 14...]
           word_tot: 14
           season_word_tots: [100, 100, 100, 100...]
    
"""



import json
#import matplotlib.pyplot as plt
#import numpy as np

#load chat info from json file
f = open("../data/char_words.json", "r")
data = json.loads(f.read())
f.close()

episode_list = []
all_char_list = []

episode_info_list = data['count']

#first generate list of episodes and list of all characters
for episode_info in episode_info_list:
    
    #add episode string to list
    episode_list.append(episode_info['episodeAlt'])

    #iterate through episode text to come up with sums for each character
    for sentence in episode_info['text']:
        
        if sentence['name'] not in all_char_list:
            
            #add the character to our list of names
            all_char_list.append(sentence['name'])

#alphabetize
all_char_list.sort()

#now create data structure for each character
all_char_list_info = []

for name in all_char_list:

    #temporary char dict
    char = {}
    char['name'] = name
    char['word_tot'] = 0
    char['episode_words'] = [0] * len(episode_list)
    char['cum_episode_words'] = [0] * len(episode_list)
    
    #add this dict to our list
    all_char_list_info.append(char)
    
    
#search through data to build number of words spoken in each episode
for episode_info in episode_info_list:

    #find which element this episode is in our total list
    episode_el = episode_list.index(episode_info['episodeAlt'])
    
    #iterate through each sentence and start adding values for episode
    for sentence in episode_info['text']:

        #find char_el for who is talking
        char_el = all_char_list.index(sentence['name'])

        all_char_list_info[char_el]['episode_words'][episode_el] += sentence['count']

#search each char in all_char_list_info to build cumulative word totals
for i in range(len(all_char_list)):
    
    #set first cumulative for the character
    all_char_list_info[i]['cum_episode_words'][0] = all_char_list_info[i]['episode_words'][0] 
    
    #search through each episode for this character and build cumulative list
    #start at episode 2
    for j in range(1, len(episode_list)):
    
        all_char_list_info[i]['cum_episode_words'][j] = all_char_list_info[i]['cum_episode_words'][j - 1] + all_char_list_info[i]['episode_words'][j]

#add total number of words based on max of cumulative
for i in range(len(all_char_list)):

    all_char_list_info[i]['word_tot'] = all_char_list_info[i]['cum_episode_words'][-1]


#for each character, add up how many words per season into new 8 array.
for i in range(len(all_char_list)):

    temp_epi_tot = [0,0,0,0,0,0,0,0]
    #search through each episode to tally up
    for j in range(len(episode_list)):
    
        #to do, look at case switching to minimize code ... works fine though
        if episode_list[j][1] == '1': 
            temp_epi_tot[0] += int(all_char_list_info[i]['episode_words'][j])
            
        elif episode_list[j][1] == '2': 
            temp_epi_tot[1] += int(all_char_list_info[i]['episode_words'][j])
        
        elif episode_list[j][1] == '3': 
            temp_epi_tot[2] += int(all_char_list_info[i]['episode_words'][j])
            
        elif episode_list[j][1] == '4': 
            temp_epi_tot[3] += int(all_char_list_info[i]['episode_words'][j])
            
        elif episode_list[j][1] == '5': 
            temp_epi_tot[4] += int(all_char_list_info[i]['episode_words'][j])
            
        elif episode_list[j][1] == '6': 
            temp_epi_tot[5] += int(all_char_list_info[i]['episode_words'][j])
        
        elif episode_list[j][1] == '7': 
            temp_epi_tot[6] += int(all_char_list_info[i]['episode_words'][j])
            
        elif episode_list[j][1] == '8': 
            temp_epi_tot[7] += int(all_char_list_info[i]['episode_words'][j])
    
    all_char_list_info[i]['season_word_tots'] = temp_epi_tot


#clean up
del char, char_el, data, episode_el, episode_info, episode_info_list, i, j, name, sentence, temp_epi_tot




# =============================================================================
# EXPORT DATA, good code
# 
# #export dicts with all characters and word counts
with open('../data/all_char_word_counts.json', 'w') as outfile:
    json.dump(all_char_list_info, outfile, indent = 4)
#  
# #export list of all characters
# with open('all_char_list.json', 'w') as outfile:
#     json.dump(all_char_list, outfile, indent = 4)
# 
# #export list of episodes
# with open('all_episode_list.json', 'w') as outfile:
#     json.dump(episode_list, outfile, indent = 4)
# 
# 
# 
# =============================================================================























# =============================================================================
# EXAMPLE MATPLOTLIB
# #generate an example plot
# 
# #find which element we're looking at
# name1 = "Eddard Stark"
# name1_el = next((i for i, item in enumerate(all_char_list_info) if item["name"] == name1), None)
# name1_data = all_char_list_info[name1_el]['cum_episode_words']
# 
# name2 = "Catelyn Stark"
# name2_el = next((i for i, item in enumerate(all_char_list_info) if item["name"] == name2), None)
# name2_data = all_char_list_info[name2_el]['cum_episode_words']
# 
# name3 = "Robb Stark"
# name3_el = next((i for i, item in enumerate(all_char_list_info) if item["name"] == name3), None)
# name3_data = all_char_list_info[name3_el]['cum_episode_words']
# 
# name4 = "Sansa Stark"
# name4_el = next((i for i, item in enumerate(all_char_list_info) if item["name"] == name4), None)
# name4_data = all_char_list_info[name4_el]['cum_episode_words']
# 
# name5 = "Arya Stark"
# name5_el = next((i for i, item in enumerate(all_char_list_info) if item["name"] == name5), None)
# name5_data = all_char_list_info[name5_el]['cum_episode_words']
# 
# name6 = "Bran Stark"
# name6_el = next((i for i, item in enumerate(all_char_list_info) if item["name"] == name6), None)
# name6_data = all_char_list_info[name6_el]['cum_episode_words']
# 
# name7 = "Rickon Stark"
# name7_el = next((i for i, item in enumerate(all_char_list_info) if item["name"] == name7), None)
# name7_data = all_char_list_info[name7_el]['cum_episode_words']
# 
# x_range = range(len(episode_list))
# 
# plt.plot(x_range, name1_data, x_range, name2_data, x_range, name3_data,x_range, name4_data, x_range, name5_data, x_range, name6_data, x_range, name7_data)
# plt.title('Stark Family Cumulative Words Per Episode')
# plt.xlabel('Episodes')
# plt.ylabel('Words per Episode')
# plt.legend([name1, name2, name3, name4, name5, name6, name7])
# plt.xticks(range(len(episode_list)), episode_list)
# plt.xticks(rotation = 90)
# 
# 
# =============================================================================































# =============================================================================
# OLD CODE
# 
# count_sums = {}
# episode_list = []
# 
# for episode in data['count']:
#     
#     #make a list of each episode
#     episode_list.append(episode['episodeAlt'])
#     
#     for diatribe_dict in episode['text']:
#         
#         if diatribe_dict['name'] not in count_sums.keys():
#             
#             count_sums[diatribe_dict['name']] = diatribe_dict['count']
#             
#         else:
#         
#             count_sums[diatribe_dict['name']] += diatribe_dict['count']
# 
# #select only relevant characters, more than 4000 words
# count_sums_4000 = { k: v for k, v in count_sums.items() if v >= 4000 }
# 
# #make list of important characters
# important_chars = list(count_sums_4000.keys())
# 
# 
# =============================================================================


