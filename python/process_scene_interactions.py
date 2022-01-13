#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
process_scene_interactions.py

Author: Alan Burwell
Last updated: 13 Jan 22

DPI691MA, Group A4, Game of Thrones

This script processes a JSON database of episode information, compares against
a list of *important* characters (listed here but determined by another script 
that calculates the numbers of total words spoken throughout the series) to
filter down to a manageable 20, then lists the number of times each permutation
of those characters actually interact with each other, then exports to a CSV 
database file for use in generating a heatmap. 

Input data file taken from Jeffrey Lancaster Game of Thrones Github repository
at https://github.com/jeffreylancaster/game-of-thrones

Input: episodes.json
    JSON database of every scene of every episode of every season listing 
    character names who participated
            
Output: scene_interactions.csv
    CSV file that lists important character pairs and the number of scene 
    interactions they have shared

    'char_a','char_b','value'
    'Jon Snow','Arya Stark',13
    ...
    
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

#iterate through each episode
for episode in data['episodes']:
    
    #iterate through each scene
    for scene in episode['scenes']:

        #only look at scenes with 2 or more characters
        if len(scene['characters']) > 1:
            
            #generate list of characters in scene as list of strings
            names = []
            for i in range(len(scene['characters'])):
                names.append(scene['characters'][i]['name'])
                
            #create permutations of characters in the scene
            permutations = list(itertools.permutations(names, 2))
            
            #for each character combination...
            for permutation in permutations:
                
                #check if each permutation already exists ... either increment or append
                #UGLY but works fine
                if True in np.where(database[:,0] == permutation[0], True, False) * np.where(database[:,1] == [permutation[1]], True, False):
                    match_array = np.where(database[:,0] == permutation[0], True, False) * np.where(database[:,1] == [permutation[1]], True, False)
                    match = np.where(match_array == True)
                    match_row = match[0][0]
                    database[match_row][2] = int(database[match_row][2]) + 1
                else:
                    database = np.append(database,[[permutation[0], permutation[1], 1]], axis=0)

#sort through new database and remove any unimportant characters ... otherwise VERY long
for i in range(len(database) - 1, 0, -1):
    
    if database[i,0] not in important_characters or database[i,1] not in important_characters:
    
        database = np.delete(database, i, axis=0)

#cleanup
del data, episode, i, match, match_array, match_row, names, permutation, permutations, scene           
            
#export to a CSV
with open('../data/scene_interactions.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(database)
