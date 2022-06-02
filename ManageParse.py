#ManageParse
#Chloe Farr
#April 13, 2022
#For LING590 / HLCS

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import re
import csv

#import LexemeInfo as lexemeInfo

CATEGORIES = ['=PL','=DIM', '=PROG', '=DUR', '=STA', '=RDP', '=STAT', '=IMP']
PROCESS_INDICES = []
grammatical_categories = []

#Returns list of grammatical processes of PL, PROG, DIM
def get_grammatical_categories(parse):
    '''
    Takes the parse and returns a list of the grammatical categories listed. Returns an empty list if no grammatical categories are indicated in the parse.
    Preconditions:
    - This assumes that CATEGORIES is an exhaustive list of any grammatical category that would be indicated in the parse. 
    >>>get_grammatical_categories('shhw=√ne’=m=PL')
    ['=PL']
    >>>get_grammatical_categories('shhw=√ne’=m')
    []
    '''
    grammatical_categories = []
    
    for i in CATEGORIES:
        if i in parse:
            grammatical_categories.append(i)
            #print(PROCESS_INDICES)
    #print(grammatical_categories)
    return grammatical_categories


def get_clean_grammatical_categories(parse):
    '''
    Takes the parse and returns a list of the grammatical categories listed. Returns an empty list if no grammatical categories are indicated in the parse but without '='.
    Preconditions:
    - This assumes that CATEGORIES is an exhaustive list of any grammatical category that would be indicated in the parse. 
    >>>get_grammatical_categories('shhw=√ne’=m=PL')
    ['PL']
    >>>get_grammatical_categories('shhw=√ne’=m')
    []
    '''
    grammatical_categories = get_grammatical_categories(parse)
    l = []
    for i in grammatical_categories:

        l.append(i[1:])
    return l
    
def strip_grammatical_categories_from_parse(parse):
    '''
    Takes the parse string and returns the parse string excluding grammatical markers
    >>>strip_grammatical_categories_from_parse('shhw=√ne’=m=PL')
    shhw=√ne’=m
    '''
    grammatical_categories = get_grammatical_categories(parse)
    parse_without_GC = parse
    for i in grammatical_categories:
        parse_without_GC = parse_without_GC.replace(i, '')
    return parse_without_GC

def get_category_indices(parse):
    '''
    Takes the parse string and returns the category and the index at which the category string began in the parse. assumes each indices is a char, not a grapheme.
    >>>get_category_indices('shhw=√ne’=m=PL')
    [['=PL', 11]]
    '''
    grammatical_categories = get_grammatical_categories(parse)
    GC_Indices = []
    for i in grammatical_categories:
        GC_Indices.append([i, parse.find(i)])
    return GC_Indices   


#returns the list of prefixes from the parsed form
def get_prefixes(parse):
    '''
    Takes the parse string and returns a list of the prefixes listed
    Preconditions: 
    - Assumes that there is a prefix and the '√' symbol in the parse.
    NOTE: this should be modified to return an empty list if there're no prefixes and an error if there's no '√' in the parse.
    >>>get_prefixes('shhw=√ne’=m')
    ['shhw']
    '''
    prefixes = parse.split('√')
    prefix_list = prefixes[0].split('=')
    for i in prefix_list:
        i = i + '='
    prefix_list = prefix_list[:-1]
    #print(prefix_list)
    #lexemeInfo.LEXEME_INFO.append(['prefixes' , prefix_list])
    return prefix_list

def strip_prefixes_from_parse(parse:str, prefixes:list) -> str:
    '''
    Takes the parse and prefix list and parse string and returns the parse string without prefixes.
    Precondition:
    - Assumes that the parse has prefixes.. works if there aren't any though, unless the prefix char exists somewhere other than the beginning of the parse, so... be careful.
    NOTE: simplify so this calls get_prefixes rather than taking prefixes as a parameter.
    >>>strip_prefixes_from_parse('shhw=√ne’=m', ['shhw'])
    √ne’=m
    '''
    parse_without_prefixes = parse
    for i in prefixes:
        i = i + '='
        parse_without_prefixes = parse_without_prefixes.replace(i,'')
    return parse_without_prefixes

def get_suffixes(parse):
    '''
    Takes the parse string and returns a list of the suffixes listed
    Preconditions: 
    - Assumes that there is a prefix and the '√' symbol in the parse.
    NOTE: this should be modified to return an empty list if there're no prefixes and an error if there's no '√' in the parse.
    >>>get_suffixes('shhw=√ne’=m')
    ['m']
    '''
    if any(ele in parse for ele in CATEGORIES):
        #print('categories still in parse when getting suffixes')
        grammatical_categories = get_grammatical_categories(parse)
        parse = strip_grammatical_categories_from_parse(parse)
        
    almost_suffixes = parse.split('√')
    suffix_list = almost_suffixes[1].split('=')
    
    for i in suffix_list:
        i = '=' + i
    suffix_list = suffix_list[1:]
    #print(suffix_list)
    #lexemeInfo.LEXEME_INFO.append(['suffixes' , suffix_list])
    return suffix_list

def get_suffix_indices(lexeme, suffixes):
    '''
    Takes the parse string and returns the prefix and the index at which the category string began in the parse. Assumes each indices is a char, not a grapheme.
    NOTES: 
    - This doesn't include indices of any inserted vowels or whatnot. It needs to.
    - This should probably return the start and end indices though.
    - This should probably index by grapheme, not character
    >>>get_suffix_indices('shhw=√ne’=m', ['shhw'])
    >>>get_suffix_indices('shhw=√ne’=m', ['m'])
    [['m', '10']]
    '''
    suffix_indices = []
    new_lexeme = lexeme
    for i in reversed(suffixes):
        suffix_indices.append([i, str(new_lexeme.rfind(i[0]))])
        #print(len(new_lexeme[new_lexeme.rfind(i)]))
        
        new_lexeme = new_lexeme[:new_lexeme.rfind(i)]
        
    return suffix_indices
        
def get_prefix_indices(lexeme, prefixes):
    '''
    Takes the parse string and returns the prefix and the index at which the category string began in the parse. Assumes each indices is a char, not a grapheme.
    NOTES: 
    - This doesn't include indices of any inserted vowels or whatnot. It needs to.
    - This should probably return the start and end indices though.
    - This should probably index by grapheme, not character
    >>>get_suffix_indices('shhw=√ne’=m', ['shhw'])
    [['shhw', '0']]
    '''
    prefix_indices = []
    new_lexeme = lexeme
    for i in prefixes:
        prefix_indices.append([i, str(new_lexeme.find(i[0]))])
        #print(len(new_lexeme[new_lexeme.rfind(i)]))
        
        new_lexeme = new_lexeme[:new_lexeme.rfind(i)]
        
    return prefix_indices


def strip_suffixes_from_parse(parse, suffixes):
    '''
    Takes the parse and suffix list and parse string and returns the parse string without suffixes.
    Precondition:
    - Assumes that the parse has suffixes.. works if there aren't any though, unless the suffix char exists somewhere other than the beginning of the parse, so... be careful.
    NOTE: simplify so this calls get_suffixes rather than taking suffixes as a parameter.
    >>>strip_suffixes_from_parse('shhw=√ne’=m', ['m'])
    shhw=√ne’
    '''    
    parse_without_suffixes = parse
    for i in suffixes:
        i = '=' + i
        parse_without_suffixes = parse_without_suffixes.replace(i,'')
    return parse_without_suffixes


def get_root(parse):    
    '''
    Strips all characters of the parse prior to and including '√', and after and including the first '=' found after the root has been stripped
    >>>get_root('s=√meent=PL')
    meent
    >>>get_root('√mun’u=DIM=PL')
    mun’u
    >>>get_root('shhw=√ne’=m=PL')
    ne’
    >>>get_root('√qul')
    qul
    '''
    root = ''
    root_end = 0
    if re.search('√', parse):
        root = parse[re.search('√', parse).start()+1:]
    else:
        root = parse        
    if re.search('=',root):
        root_end = re.search('=',root).start()
    else: 
        root_end = len(root)
    return root[:root_end]


'''
ABOUT AFFIXES
csv columns: pronoun	affix	person	tense	alternations (stem_og stem_new affix_og affix_new affix_cond)
'''
PRONOUN = 0
AFFIX = 1
PERSON = 2
TENSE = 3
ALTERNATIONS = 4
# in alternations...(stem_og stem_new affix_og affix_new affix_cond)
stem_og = 0
stem_new = 1
affix_og = 2
affix_new = 3
affix_cond = 4
stem = "stem"
vowels = ["aa","ee","oo","ou","o","i","e","a"]


def format_affix_conditions(row):
    '''
    the Pronoun.csv has a column for alternation conditions (column E) formatted as a weird string to avoid weird csv comma parsing
    formats it to return a list or 2d list
    >>>format_affix_conditions(v u _stuhw _stuhw none|u u _stuhw _stehw none|none none _stuhw _st-hw _us)
    [["v", "u", "_stuhw", "_stuhw", "none"],["u","u", "_stuhw", "_stehw", "none"], ["none", "none", "_stuhw", "_st-hw", "_us"]]
    '''
    try:
        print(row[ALTERNATIONS])
        x = row[ALTERNATIONS].replace(' ', ',').split('|')
        for i in range(len(x)-1):
            x[i]=x[i].split(',')
        if len(x[0]) == 0:
            print("no conditions")
            return None
        
        return x
    
    except:
        print("no conditions")
        return None
    
def get_affix_meaning(affix:str)-> list:
    '''
    takes csv with columns : pronoun,affix,person,tense,alternations (stem_og stem_new affix_og affix_new affix_cond)
    finds and returns the row as a list that corresponds with the searched affix... affix would be passed through from an affix list for example
    >>>get_affix_meaning('stuhw')
    ['causative', '_stuhw', 'Third person singular', 'Active Objects', [['v', 'u', '_stuhw', '_stuhw', 'none'], ['u', 'u', '_stuhw', '_stehw', 'none'], 'none,none,_stuhw,_st-hw,_us']]
    '''
    prefix = affix + "_"
    suffix = "_" + affix
    csv_file = csv.reader(open('Pronouns.csv', "r"), delimiter=",")
    affix_row = []
    for row in csv_file:
        #if current rows 2nd value is equal to input, print that row
        if row[1] == (prefix or suffix):
            print(row)
            affix_row = row
            affix_row[ALTERNATIONS] = format_affix_conditions(affix_row)
            return affix_row
    #csv_file.close()
    return False

#print(get_affix_meaning('stuhw'))


def has_alternations(affix):
    '''
    takes in the content of Pronoun.csv row n[4] alternations and returns true if the list isn't empty
    >>>format_affix_conditions([["v", "u", "_stuhw", "_stuhw", "none"],["u","u", "_stuhw", "_stehw", "none"], ["none", "none", "_stuhw", "_st-hw", "_us"]])
    True
    >>>format_affix_conditions([""])
    False
    >>>format_affix_conditions()
    False
    '''
    try:
        affix_meaning = get_affix_meaning(affix)
        if affix_meaning[ALTERNATIONS] == None:
            return False
        else:
            return True   
    except:
        return False
    

def schwa_in_last_syllable(graphemes):
    '''
    returns true if the last vowel in the grapheme list is a schwa, returns false if the last vowel is not a schwa... ignores consonants through traverse
    >>>schwa_in_last_syllable(['ts’', 'i', '’', 'ts’', 'u', 'm', 'ii', 'l’'])
    False
    >>>schwa_in_last_syllable(['ts’', 'i', '’', 'ts’', 'u', 'm', 'u', 'l’'])
    True
    '''
    for i in reversed(graphemes):
        if i == 'u':
            return True
        elif any(ext in i for ext in ["aa","ee","oo","ou","o","i","e","a"]):
            return False

def whole_vowel_in_last_syllable(graphemes):
    '''
    returns true if the last vowel in the grapheme list is not a schwa, returns false if the last vowel is a schwa... ignores consonants through traverse
    >>>schwa_in_last_syllable(['ts’', 'i', '’', 'ts’', 'u', 'm', 'ii', 'l’'])
    True
    >>>schwa_in_last_syllable(['ts’', 'i', '’', 'ts’', 'u', 'm', 'u', 'l’'])
    False
    '''
    for i in reversed(graphemes):
        if i == 'u':
            return False
        elif any(ext in i for ext in ["aa","ee","oo","ou","o","i","e","a"]):
            return True
        
    
def which_segment_alternated(alternation):
    '''
    precondition: the affix has at least one alternation (var passed into function)
    takes an alternation list and returns if the stem or affix is alternated, or None if neither (this would be weird though)
    >>>which_segment_alternated([["v", "u", "_stuhw", "_stuhw", "none"])
    stem
    >>>which_segment_alternated(["u","u", "_stuhw", "_stehw", "none"])
    affix
    '''
    print(alternation)
    if alternation[stem_og] != alternation[stem_new]:
        print(stem)
        return stem
    elif (alternation[affix_og] != alternation[affix_new]) or alternation[affix_cond] != "none":
        print("affix")
        return "affix"
    print("typo")
    return "typo"

def stem_alternation(alternation):
    '''
    takes an alternation list and determines what kind of vowel shift the stem is undergoing, if any. 
    >>>stem_alternation([["v", "u", "_stuhw", "_stuhw", "none"])
    reduction
    >>>stem_alternation(["u","v", "_stuhw", "_stehw", "none"])
    strengthening
    >>>stem_alternation(["u","u", "_stuhw", "_stehw", "none"])
    None
    >>>stem_alternation(["a","e", "_stuhw", "_stehw", "none"])
    albaut
    '''
    if which_segment_alternated(alternation) == stem:
        if alternation[stem_og] != ("u" or "none") and alternation[stem_new] == "u":
            return "reduction"
        elif alternation[stem_og] == "u" and alternation[stem_new] != ("u" or "none"):
            return "strengthening"
        elif alternation[stem_og] != ("u" or "none") and alternation[stem_new] != "u" and alternation[stem_og] != alternation[stem_new]:
            return "ablaut"
    return None

#print(stem_alternation(["a","e", "_stuhw", "_stehw", "none"]))
    
def affix_reducing_stem(affix_meaning):
    '''
    takes a word object, searches through each affix, checks to see if that affix causes an alternation... if yes, and if the alternation changes the stem,
    checks if the stem vowel reduces
    returns the alternation condition list
    '''
    for j in affix_meaning[ALTERNATIONS]:
        if stem_alternation(j) == "reduction":
            print(j)
            return j
    return None


def affix_strengthening_stem(affix_meaning):
    '''
    takes a word object, searches through each affix, checks to see if that affix causes an alternation... if yes, and if the alternation changes the stem,
    checks if the alternation is strengthening, and then returns that affix
    Precondition: Only one alternation includes stem strengthening
    '''
    for j in get_affix_meaning(affix)[ALTERNATIONS]:
        if stem_alternation(j) == "strengthening":
            print(j)
            return j
    return None


def affix_ablauting_stem(affix_meaning):
    '''
    takes a word object, searches through each affix, checks to see if that affix causes an alternation... if yes, and if the alternation changes the stem,
    checks if the alternation is ablaut, and then returns that affix
    Precondition: Only one alternation includes stem ablaut 
    '''
    for j in get_affix_meaning(affix)[ALTERNATIONS]:
        if stem_alternation(j) == "ablaut":
            print(j)
            return j
    return None



def find_affix_in_lexeme(word_obj, affix):
    '''
    compares the affix in the list and searches for it in the lexeme. this is currently being done in Lexeme Info but that doesn't account for any alternations whatsoever.
    returns the indices of the affix within the lexeme if it is found.
    if he lexeme isn't found, it checks the Alternations cell in row to see if there are any alternations to the affix in the stem, then looks for that.
    >>>find_affix_in_lexeme(obj~word = "yunyuntus", "us")
    [6,8]
    ~~~~~this is way incomplete. have to go through and find all the ways things can alternate to correctly identify the affix and underlying vowels in the lexeme.
    '''
    lexeme = word_obj.get_word()
    affix_meaning = []
    try:
        affix_meaning = get_affix_meaning(affix)
        i_affix = lexeme.get_word().rfind(affix)
        if lex_affix > -1:
            return [i_affix, i_affix + len(affix)]
    
        else:
            if has_alternations(affix):
                for i in affix_meaning[ALTERNATIONS]:
                    if lexeme.rfind(i[affix_new]) > -1:
                        return [lexeme.rfind(i[affix_new]), lexeme.rfind(i[affix_new]) + len(i[affix_new])]
    except:
        print("affix not found")
        
def reverse_affix_vowel_change(word_obj):
    reversed_word = word_obj.get_word()
    affixes = word_obj.get_suffix_list()+word_obj.get_prefix_list()
    if affixes!= None and len(affixes) == 0:
        return False
    else:
        for i in affixes:
            if has_alternations(i):
                s = affix_reducing_stem(i)
                t = affix_strengthening_stem(i)
                u = affix_ablauting_stem(i)
                
                if s != None:
                    reversed_word = reverse_affix_stem_reduction(word_obj, s)
                elif t != None:
                    reversed_word = reverse_affix_stem_strengthening(word_obj,t)
                elif u != None:
                    reversed_word =  reverse_affix_stem_ablaut(word_obj, u)
        return reversed_word
        #and something else to do with loop
    return None


#``````~~~~~~fixedish to here

def reverse_affix_stem_reduction(word_obj, condition):  
    affix = ''
    stripped_lex_graphemes = word_obj.get_stripped_lexeme_graphemes()
    found = False
    
    if affix_reducing_stem(word_obj) != None:
        affix = affix_reducing_stem(word_obj)
        for i in range(len(stripped_lex_graphemes)-1, -1, -1):
            if stripped_lex_graphemes[i] == "u":
                stripped_lex_graphemes[i] = get_new_last_vowel(word_obj.root_graphemes)
                return stripped_lex_graphemes
                
    return stripped_lex_graphemes


def reverse_affix_stem_strengthening(word_ob, condition):
    affix = ''
    stripped_lex_graphemes = word_obj.get_stripped_lexeme_graphemes()
    found = False
    print("fix strengthening")
    affix = affix_strengthening_stem(word_obj)
    for i in range(len(stripped_lex_graphemes)-1, -1, -1):
        for k in range(len(vowels)-1):
            if i == vowels[k]:
                stripped_lex_graphemes[i] = "u"
                found = True
                break
        if found == True:
            break
    return stripped_lex_graphemes        
        
        
        
def reverse_affix_stem_ablaut(word_obj, condition):
    affix = ''
    stripped_lex_graphemes = word_obj.get_stripped_lexeme_graphemes()
    found = False
    
    print("fix ablaut")
    affix = affix_ablauting_stem(word_obj)
    for i in reversed(stripped_lex_graphemes):
        if i == any(ext in j for ext in ["aa","ee","oo","ou","o","i","e","a"]):
            for j in reversed(word_obj.get_root_graphemes()):
                if any(ext in j for ext in ["aa","ee","oo","ou","o","i","e","a"]):
                    i = j
                    found = True
                    break
        if found == True:
            return stripped_lex_graphemes      
            
        
    return stripped_lex_graphemes
#have to traverse through affix list to strip down in order right to left for rfind to work...

def get_last_vowel_index(graphemes):
    for i in range(len(graphemes)-1, -1, -1):
        for k in range(len(vowels)-1):
            #print(graphemes[i], vowels[k])
            if graphemes[i] == vowels[k]:
                return i
    return -1

def get_new_last_vowel(graphemes):
    for i in range(len(graphemes)-1, -1, -1):
        for k in range(len(vowels)-1):
            #print(graphemes[i], vowels[k])
            if graphemes[i] == vowels[k]:
                return vowels[k]
    return -1    