#MorphologicalProcesses
#Chloe Farr
#April 13, 2022
#For LING590 / HLCS

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import ManageParse as parser
import LexemeInfo as lexemeInfo
import re
import CheckForRegex as regCheck

CONSONANTS = "(kw’|kw|k’|k|m’|m|n’|n|qw’|qw|q’|q|ch’|ch|hw|th|sh|lh|tth’|tth|ts’|ts|tl’|xw|x|l’|l|h|s|w’|w|y’|y|p’|p|t’|t|’)"
CONSONANTS_NO_L = "(kw’|kw|k’|k|m’|m|n’|n|qw’|qw|q’|q|ch’|ch|hw|th|sh|lh|tth’|tth|ts’|ts|tl’|xw|x|h|s|w’|w|y’|y|p’|p|t’|t|’)"
CONSONANTS_NO_H = "(kw’|kw|k’|k|m’|m|n’|n|qw’|qw|q’|q|ch’|ch|hw|th|sh|lh|tth’|tth|ts’|ts|tl’|xw|x|l’|l|s|w’|w|y’|y|p’|p|t’|t|’)"

RESONANTS = "(l’|l|m’|m|n’|n|w’|w|y’|y)"
SCHWA = "u"
UNUHW = "’"
VOWELS = "(aa|ee|oo|ou|o|i|e|a)"
VOWELS_SCHWA = "(aa|ee|oo|ou|o|u|i|e|a)"
L = "(l’|l)"
H = "(h’|h)"

ROOT = 2
STRIPPED = 3
UNUHW = '’'
LEXEME_INFO = []
OG_lexeme=''
PROCESSES_INDEX = 7;


def find_reduplicant(OG_lexeme, lexeme, root):
    ''' 'm’umun’lh' , '√m’un’=lh=PL' '''
    #print(OG_lexeme)
    lexeme = replace_h_copying(lexeme, root)
    OG_indices = [i.start() for i in re.finditer(root[0], OG_lexeme)]
    indices = [i.start() for i in re.finditer(root[0], lexeme)] # indices in string of each occurence of the first char in string 
    reduplicant = lexeme[indices[0]:indices[1]] # string up to second occurence of the first char in string
    reduplicant_info = []
    
    reduplicant_info.append(['underlying reduplicant',lexeme[indices[0]:indices[1]]])
    #print('reduplicant: ' + lexeme[indices[0]:indices[1]])
    return reduplicant_info
            

def return_no_infixation_or_h(lexeme, parse):
    OG_lexeme = lexeme;
    lexemeInfo.PROCESSES = []
    LEXEME_INFO = lexemeInfo.get_lexeme_info(lexeme, parse)
    lexeme = LEXEME_INFO[STRIPPED][1]
    root = LEXEME_INFO[ROOT][1]
    temp_lexeme = lexeme
    #print('lexeme: ' + lexeme+'; root: ' + root)
    #if has_h_copying(lexeme, root):
        #temp_lexeme = replace_h_copying(lexeme, root)
        ##print('replaced h: ' + replaced_h)
        #LEXEME_INFO.append(['replaced h', temp_lexeme])
    #if index_l_infixation(temp_lexeme, root):
        #temp_lexeme= remove_l_infixation(temp_lexeme, root)
        #LEXEME_INFO.append(['without l', temp_lexeme])
    ##print('removed l : ' + removed_l)
    print('stripped: ', temp_lexeme)
    temp_lexeme = regCheck.get_to_underlying(temp_lexeme,root)
    print(temp_lexeme)
    reduplicant = find_reduplicant(OG_lexeme, temp_lexeme, root)
    #LEXEME_INFO.append(reduplicant)    
    
    #print('reduplicant: ' + reduplicant)    
    #print('processes: ' + str(lexemeInfo.PROCESSES) + '\n\n')
    print(str(LEXEME_INFO) + '\n\n')
    
#find_reduplicant('tsmuq’muq’um','ts=√muq’u=m=PL')
#find_reduplicant('hwkwunkwunlhnenum','hw=√kwun=lhnen=m=PL')
#find_reduplicant('ts’eyts’eyuhwum', '√ts’uy’hw=m=PL')

#find_reduplicant('huyinum', '√yun=m=PL')
#find_l_infixation('’uli’uy’mut', '√’uy’=mat=DIM=PL')
#LEXEME_INFO = lexemeInfo.get_lexeme_info('l’uli’uy’mut', '√l’uy’=mat=DIM=PL')
#remove_l_infixation('l’uli’uy’mut', '√l’uy’=mat=DIM=PL')

##LEXEME_INFO = lexemeInfo.get_lexeme_info('’uli’uy’mut', '√’uy’=mat=DIM=PL')
#return_no_infixation_or_h('’uli’uy’mut', '√’uy’=mat=DIM=PL')

##LEXEME_INFO = lexemeInfo.get_lexeme_info('la’lum’uthut', '√lem=that=PROG')
#return_no_infixation_or_h('la’lum’uthut', '√lem=that=PROG')

##LEXEME_INFO = lexemeInfo.get_lexeme_info('hiil’e’lum’ut', '√lem=t=DIM=PROG')
#return_no_infixation_or_h('hiil’e’lum’ut', '√lem=t=DIM=PROG')

#return_no_infixation_or_h('lukwlukw', '√lukwa=PL')

#return_no_infixation_or_h('hul’kwut','√lukwa=t=PROG')

#return_no_infixation_or_h('hul’ul’kwut','√lukwa=t=PROG=PL')

#return_no_infixation_or_h('munmaanta’qw','√meent=a’qw=PL')

#return_no_infixation_or_h('hum’een’', '√meen’=PROG')

#return_no_infixation_or_h('hwkwunkwunlhnenum','hw=√kwun=lhnen=m=PL')

#return_no_infixation_or_h('tsmuq’muq’um','ts=√muq’u=m=PL')