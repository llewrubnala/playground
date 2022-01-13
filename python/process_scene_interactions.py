#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 11:29:54 2022

@author: al
"""




import json
import itertools
#import matplotlib.pyplot as plt
import numpy as np
import csv


#load chat info from json file
f = open("../data/episodes.json", "r")
data = json.loads(f.read())
f.close()


important_characters = ['Robb Stark','Olenna Tyrell','Sandor Clegane','Brienne of Tarth','Bronn','Jorah Mormont','Theon Greyjoy','Tywin Lannister','Arya Stark','Davos Seaworth','Samwell Tarly','Lord Varys','Petyr Baelish','Sansa Stark','Jaime Lannister','Daenerys Targaryen','Jon Snow','Cersei Lannister','Tyrion Lannister','Stannis Baratheon']
important_characters.sort()

#template to push scene info to
database = [['char_1','char_2','value']]

#convert to numpy to make manipulation easier
database = np.array(database)


#database = np.append(database, [['Jon Snow', 'Tormund Giantsbane', 1]], axis=0)

for episode in data['episodes']:
    
    for scene in episode['scenes']:

        #if at least 2 characters are in the scene
        if len(scene['characters']) > 1:
            
            #find strings of characters in scene
            names = []
            for i in range(len(scene['characters'])):
                names.append(scene['characters'][i]['name'])
                
            #create permutations of characters in the scene
            permutations = list(itertools.permutations(names, 2))
            
            for permutation in permutations:
                
                #UGLY but works fine
                #check if each permutation already exists ... either increment or append
                if True in np.where(database[:,0] == permutation[0], True, False) * np.where(database[:,1] == [permutation[1]], True, False):
                    match_array = np.where(database[:,0] == permutation[0], True, False) * np.where(database[:,1] == [permutation[1]], True, False)
                    match = np.where(match_array == True)
                    match_row = match[0][0]
                    database[match_row][2] = int(database[match_row][2]) + 1
                else:
                    database = np.append(database,[[permutation[0], permutation[1], 1]], axis=0)


#sort through database and remove any unimportant characters
for i in range(len(database) - 1, 0, -1):
    
    if database[i,0] not in important_characters or database[i,1] not in important_characters:
    
        database = np.delete(database, i, axis=0)


#cleanup            
del data, episode, i, match, match_array, match_row, names, permutation, permutations, scene           
            

#export to a CSV
with open('scene_interactions.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(database)


