'''
Word Objects to CSV
Takes in a list of lexemes and generates a csv with mopho details, delimiter is tab because if it's comma, unity will deliminate all commas, even those where an index is holding another list
1 row per lexeme entered
'''
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys

import csv
from Words import Words

input_list = input('Enter a list of lexemes, separated by a comma (e.g. \'ha’kwush, kwuyxutth’e’t\':\n')
input_list = input_list.replace(' ', '').split(',')

# name of csv file 
filename = input('enter name of new csv (e.g. \'test_word_objects\'):\n') +'.csv'
filename.replace(' ', '').replace('\'','')

fields = ['lexeme','stripped_lexeme','root','parse','underlying','definition','word_graphemes','where_in_wrapped','grammatical_categories','suffixes','prefixes','copy','copy_indices','copied','copied_indices','h_copy', 'linfixation_indices', 'without_linfixation', 'l_copy_indices']

word_objects = []

# writing to csv file 
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile, delimiter='\t') 
        
    # writing the fields 
    csvwriter.writerow(fields) 
        
    #instantiating the word objects from input list
    for i in input_list:
        print(i)
        word_objects.append(Words(i))
   
    # writing the data rows 
    for l in word_objects:
        csvwriter.writerow(l.list_for_csv())
    
#see’likw, q’uli’q’ept,  p’utl’ul’ust

