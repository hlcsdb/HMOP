#LexemeInfo
#Chloe Farr
#April 13, 2022
#For LING590 / HLCS

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import ManageParse as parser
import re

'''In reality, this entire script is dumb and obsolete, I just need to fix the strip affixes functions/move them to CheckForRegex'''

'''all of these lists are obsolete if I use regex with the strings in CheckForRegex'''
LEXEME_INFO = []
PROCESSES = []
CONSONANTS = [['p','p’'],['t','t’'],['k','kw’','kw'],['l','l’'],['m','m’'],['n','n’'],['q','q’','qw','qw’'],['w','w’'],['y','y’'],['ch','ch’'],['l','l’'],['s'],['h','hw'],['th'],['sh'],['lh'],['tth','tth’'],['ts','ts’'],['tl’'],['x','xw']]
RESONANTS = [['l','l’'],['m','m’'],['n','n’'],['w','w’'],['y','y’']]
SCHWA = 'u'
UNUHW = '’'
VOWELS = ['a','e','u','i','ee','aa','oo','ou']

def strip_lexeme_affixes(lexeme, parse):
    '''This is way too complicated. it should take the lexeme and parse and go 'stripped = strip_lexeme_prefixes, then stripped = strip_lexeme_suffices and voila.
    >>>strip_lexeme_affixes('slhunlheni’','s=√lheni’=PL')
    lhunlheni’
    '''
    without_prefixes = strip_lexeme_prefixes(lexeme,parse)
    without_affixes = strip_lexeme_suffixes(without_prefixes,parse)
    i_last = (len(without_affixes))-1
    without_affixes_or_schwa = without_affixes
    root = parser.get_root(parse)
    return without_affixes_or_schwa


def strip_lexeme_prefixes(lexeme, parse):
    '''This should be done with regex. redo it. pretty self explanatory what it's supposed to do'''
    new_lexeme = lexeme
    prefixes = parser.get_prefixes(parse)
    LEXEME_INFO.append(['prefixes',prefixes])
    for p in prefixes:
        length_affix = len(p)
        if lexeme.find(p) is 0:
            index_2 = new_lexeme.find(p[length_affix-1])+1
            new_lexeme = lexeme[index_2:]
    return new_lexeme


def strip_lexeme_suffixes(lexeme, parse):
    '''This should be done with regex. redo it. pretty self explanatory what it's supposed to do'''
    new_lexeme = lexeme
    suffixes = parser.get_suffixes(parse)
    suffix_indices = []
    
    if(len(suffixes) > 0):
        new_p_consonant = get_other_consonant(suffixes[0], new_lexeme)
        lexeme_i_suffix = new_lexeme.rfind(new_p_consonant)
        suffix_indices.append([suffixes[0], lexeme_i_suffix])
        new_lexeme = new_lexeme[:lexeme_i_suffix]
    LEXEME_INFO.append(['suffixes',suffix_indices])
    return new_lexeme        
   
   
def get_consonant_coarticulations(consonant):
    '''literally no idea what this is. it's being used by get_other_consonant which is also dumb so eventually they'll both go'''
    for i in CONSONANTS:
        if consonant in i:
            return i
    return consonant
        
        
def compare_consonant_coarticulations(other_consonant, coarticulations):
    '''literally no idea what this is. it uses get_consonant_coarticulations which is also dumb so eventually it'll also go'''
    if other_consonant in coarticulations:
        return True
    else:
        return False

def get_other_consonant(consonant, lexeme):
    '''
    THIS IS A DUMB FUNCTION. It only exists because it's used by strip_lexeme_suffixes, which really should be using regex but I'm not going to change it now.
    '''
    consonant_coarticulations = get_consonant_coarticulations(consonant)
    for i in consonant_coarticulations:
        possible_suffix = lexeme[lexeme.rfind(i):]        
        return possible_suffix
        
def get_lexeme_info(lexeme, parse):
    '''EW. This is obsolete now with GetWordObjects but I don't quite want to get rid of it yet'''
    LEXEME_INFO = []
    parser.grammatical_category_indices = []
    
    #PROCESSES = []
    LEXEME_INFO.append(['lexeme',lexeme])
    LEXEME_INFO.append(['parse',parse])
    #lexeme_info = []
    suffixes = parser.get_suffixes(parse)
    suffix_indices = parser.get_suffix_indices(lexeme, suffixes)
    prefixes = parser.get_prefixes(parse)
    prefix_indices = parser.get_prefix_indices(lexeme, prefixes)

    #categories = parser.get_grammatical_categories(parse)
    root = parser.get_root(parse)
    stripped = strip_lexeme_affixes(lexeme,parse)
    #lexeme_info.append(['parse', parse])
    #lexeme_info.append(['lexeme', lexeme])
    LEXEME_INFO.append(['root', root])
    LEXEME_INFO.append(['stripped',stripped])
    #LEXEME_INFO.append(['suffixes',suffixes])

    LEXEME_INFO.append(['suffix indices',suffix_indices])    
    LEXEME_INFO.append(['prefix indices',prefix_indices])
    #LEXEME_INFO.append(['prefixes',prefixes])
    LEXEME_INFO.append(['categories', parser.get_category_indices(parse, parser.get_grammatical_categories(parse))])
    LEXEME_INFO.append(['processes',PROCESSES])
    
    #print(LEXEME_INFO)
    return LEXEME_INFO
    
    
#get_consonant_tuple_index('t')
#compare_consonant_coarticulations('t',('t','t’'))
#get_other_consonant('t', 'muqw’muqw’u’t’')
#print(strip_lexeme_affixes('tsmuq’muq’um','ts=√muq’u=m=PL')) #this is a predicted word-final schwa
#print(strip_lexeme_affixes('muqw’muqw’ut‘','√muqw’=t=PL')) #this has an unpredicted word-final schwa
#strip_lexeme_affixes('hwkwunkwunlhnenum','hw=√kwun=lhnen=m=PL')
#get_lexeme_info('muqw’muqw’ut‘','√muqw’=t=PL') #this has an unpredicted word-final schwa
#get_lexeme_info('tsmuq’muq’um','ts=√muq’u=m=PL') #this is a predicted word-final schwa
#get_lexeme_info('hwkwunkwunlhnenum','hw=√kwun=lhnen=m=PL')
#has_h_copying('huniqum','√nuq=m=PL')
#replace_h_copying('hulixwtun', '√luxw=ten=PL')