#CheckForRegex
#Chloe Farr
#April 15, 2022
#For LING590 / HLCS

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import ManageParse as parser
import LexemeInfo as lexemeInfo
import re


'''THIS FILENAME IS MISLEADING AND SHOULD BE RENAMED'''

'''REGEX STRINGS'''
SOUNDS = "(kw’|kw|k’|k|m’|m|n’|n|qw’|qw|q’|q|ch’|ch|hw|th|sh|lh|tth’|tth|ts’|ts|tl’|xw|x|l’|l|h|s|w’|w|y’|y|p’|p|t’|t|aa|ee|oo|ou|ii|o|u|i|e|a|’)"

CONSONANTS = "(kw’|kw|k’|k|m’|m|n’|n|qw’|qw|q’|q|ch’|ch|hw|th|sh|lh|tth’|tth|ts’|ts|tl’|xw|x|l’|l|h|s|w’|w|y’|y|p’|p|t’|t|’)"
CONSONANTS_NO_L = "(kw’|kw|k’|k|m’|m|n’|n|qw’|qw|q’|q|ch’|ch|hw|th|sh|lh|tth’|tth|ts’|ts|tl’|xw|x|h|s|w’|w|y’|y|p’|p|t’|t|’)"
CONSONANTS_NO_H = "(kw’|kw|k’|k|m’|m|n’|n|qw’|qw|q’|q|ch’|ch|hw|th|sh|lh|tth’|tth|ts’|ts|tl’|xw|x|l’|l|s|w’|w|y’|y|p’|p|t’|t|’)"
CONSONANTS_UNUHW = CONSONANTS = "(kw’|k’|m’|n’|qw’|q’|ch’|tth’|ts’|tl’|l’|w’|y’|p’|t’|h’|’)"

RESONANTS = "(l’|l|m’|m|n’|n|w’|w|y’|y)"
SCHWA = "u"
UNUHW = "’"
#doesn't consider diphthongs
VOWELS = "(aa|ee|oo|ou|o|i|e|a)"
VOWELS_SCHWA = "(aa|ee|oo|ou|o|u|i|e|a)"
L = "(l’|l)"
H = "(h’|h)"
VOWELS_LIST = ['aa', 'ee', 'oo', 'ou', 'o', 'u', 'i', 'e', 'a']




'''------SLICING AND INDEXING------'''

def slice_string_graphemes(word:str) -> list:
    '''
    Takes a string and splits it by graphemes using regex and the SOUNDS string
    >>>slice_string_graphemes('ts’i’ts’umiil’')
    ['ts’', 'i', '’', 'ts’', 'u', 'm', 'ii', 'l’']
    >>>slice_string_graphemes('ts’uli’ts’umiil’')
    ['ts’', 'u', 'l', 'i', '’', 'ts’', 'u', 'm', 'ii', 'l’']
    '''
    split_lexeme = []
    
    while len(word) > 0:
        onset_span = re.match(SOUNDS, word).span()
        split_lexeme.append(word[:onset_span[1]])
        word = word[onset_span[1]:]
    return split_lexeme

def join_split_graphemes(grapheme_list:list) -> str:
    '''
    Takes a list of strings and joins them in a for loop to return a string
    >>>join_split_graphemes(['ts’', 'i', '’', 'ts’', 'u', 'm', 'ii', 'l’'])
    ts’i’ts’umiil’
    '''
    w = ''
    for i in grapheme_list:
        w += i
    return w

def get_root(parse:str) -> str: 
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
#print(get_root('qul'))

def index_vowel_morpheme(morpheme:str) -> int:
    '''
    Takes the string and returns the first vowel string found.
    >>>index_vowel_morpheme('huy', 'hay')
    (1, 2)
    >>>index_vowel_morpheme('hee’wi’wuqus')
    1
    >>>index_vowel_morpheme('q’apq’upthut')
    1
    >>>index_vowel_morpheme('qp’apq’upthut')
    2
    '''
    morpheme_graphemes = slice_string_graphemes(morpheme)
    
    #print(morpheme_graphemes)
    i_vowel = 0
    
    for i in range(len(morpheme_graphemes)):
        for j in range(len(VOWELS_LIST)):        
            #print(morpheme_graphemes[i], VOWELS_LIST[j])
            if morpheme_graphemes[i] == VOWELS_LIST[j] and i_vowel == 0:
                i_vowel = i
                #print(vowels[0])
                break
    return i_vowel

def get_vowels_copy_copied_root(copy:str, copied:str, root:str) -> list:
    '''
    Takes the copy morpheme, copied morpheme and the root morpheme and find the vowels in each. Returns the vowels in a list of len 3
    >>>get_vowels_copy_copied_root('qp’a', 'q’pu','q’pu')
    ['a', 'u', 'u']
    >>>get_vowels_copy_copied_root('qap’up','qp’u', 'q’pu')
    ['a', 'u', 'u']
    >>>get_vowels_copy_copied_root('qpa’ap','qpa', 'q’pu')
    ['a', 'a', 'u']
    >>>get_vowels_copy_copied_root('qp’ap','q’pa', 'q’pa')
    ['a', 'a', 'a']
    >>>get_vowels_copy_copied_root('qp’aap','q’paa', 'q’pa')
    ['aa', 'aa', 'a']
    >>>get_vowels_copy_copied_root('qp’oup','q’pou', 'q’pu')
    ['ou', 'ou', 'u']
    '''
    copy_graphemes = slice_string_graphemes(copy)
    copied_graphemes = slice_string_graphemes(copied)
    root_graphemes = slice_string_graphemes(root)
    vowels = ['', '', '']
    
    try:
        for i in range(len(copy_graphemes)):
            for j in range(len(VOWELS_LIST)):  
                if copy_graphemes[i] == VOWELS_LIST[j] and vowels[0] == '':
                    vowels[0] = copy_graphemes[i]
                    break
    except:
        print("error: no vowel in copy!")
    
    try:
        for i in range(len(copied_graphemes)):
            for j in range(len(VOWELS_LIST)):
                        
                if copied_graphemes[i] == VOWELS_LIST[j] and vowels[1] == '':
                    vowels[1] = copied_graphemes[i]
                    break  
    except:
        print("error: no vowel in copied!")
    
    try:            
        for i in range(len(root_graphemes)):
            for j in range(len(VOWELS_LIST)):
                if root_graphemes[i] == VOWELS_LIST[j] and vowels[2] == '':
                    vowels[2] = root_graphemes[i]
                    break       
    except:
        print("error: no vowel in root!")
    return vowels


def where_vowels_copy_copied_root(copy:str, copied:str, root:str) -> list:
    '''
    Takes the copy morpheme, copied morpheme and the root morpheme and find the vowels in each. Returns a list of the indices of the vowel in each... that each indices is a sound as per slice_string_graphemes, not a char
    >>>where_vowels_copy_copied_root('qp’a', 'q’pu','q’pu')
    [2, 2, 2]
    >>>where_vowels_copy_copied_root('qap’up','qp’u', 'q’pu')
    [1, 2, 2]
    >>>where_vowels_copy_copied_root('qpa’ap','qpa', 'q’pu')
    [2, 2, 2]
    >>>where_vowels_copy_copied_root('qp’ap','q’pa', 'q’pa')
    [2, 2, 2]
    >>>where_vowels_copy_copied_root('qp’aap','q’paa', 'q’pa')
    [2, 2, 2]
    >>>where_vowels_copy_copied_root('qp’oup','q’pou', 'q’pu')
    [2, 2, 2]
    '''
    copy_graphemes = slice_string_graphemes(copy)
    copied_graphemes = slice_string_graphemes(copied)
    root_graphemes = slice_string_graphemes(root)
    #print(root_graphemes)
    vowels = [0,0,0]
    
    try:
        for i in range(len(copy_graphemes)):
            for j in range(len(VOWELS_LIST)):        
                #print(copy_graphemes[i], VOWELS_LIST[j])
                if copy_graphemes[i] == VOWELS_LIST[j] and vowels[0] == 0:
                    vowels[0] = i
                    #print(vowels[0])
                    break
        
    except:
        print("error: no vowel in copy!")
    
    try:
        for i in range(len(copied_graphemes)):
            for j in range(len(VOWELS_LIST)):
                #print(copied_graphemes[i],VOWELS_LIST[j])    
                if copied_graphemes[i] == VOWELS_LIST[j] and vowels[1]  == 0:
                    vowels[1] = i
                    #print(vowels[0])
                    break  
    except:
        print("error: no vowel in copied!")
    
    try:            
        for i in range(len(root_graphemes)):
            for j in range(len(VOWELS_LIST)):
                #print(root_graphemes[i],VOWELS_LIST[j])
                if root_graphemes[i] == VOWELS_LIST[j] and vowels[2] == 0:
                    vowels[2] = i
                    #print(vowels[0])            
        
    except:
        print("error: no vowel in root!")
    
    return vowels


def where_copy(lexeme:str, root:str) -> list:
    '''
    Takes the lexeme and the root strings and returns a list of the start and end indices of the copy morpheme... that each indices is a sound as per slice_string_graphemes, not a char
    Precondition:
    - lexeme must be stripped of prefixes.
    NOTE: This will always return a string, even if there isn't actually a copy. Make sure to use the 'has_copy' function to check that there's both a copy and a copied segment.
    >>>where_copy('tsul’tsa’luqw','tsa’luqw')
    [0, 3]
    >>>where_copy('lhul’lhul’q','lhul’q')
    [0, 3]
    >>>where_copy('hi’huy’u','huye’')
    [0, 3]
    >>>where_copy('ts’uy’ts’eey’u','ts’eey’u')
    [0, 3]
    >>>where_copy('t’ult’ulq','t’ulq')
    [0, 3]
    >>>where_copy('m’umun’lh' , 'm’un’')
    [0, 2]
    >>>where_copy('q’epq’up’utum’','q’ep’')
    [0, 3]
    '''
    split1 = slice_string_graphemes(lexeme)
    split2 = slice_string_graphemes(root)
    #print(split1,split2)    
    l = []
    for i in range(len(split2)):
        l1 = str(split1[i])
        l2 = str(split2[i])      
        #print("l1, l2" + str(l1) + str(l2))
        if l1 in l2 or l2 in l1 or (re.search(VOWELS_SCHWA,l1) and re.search(VOWELS_SCHWA,l2)) or l1 == UNUHW or l2 == UNUHW:
            l.append(i)
            #print('l1: ' +l1)
        else:
            break
    #print(l)
    k = [l[0]]
    last = l[len(l)-1] + 1
    k.append(last)
    return k

def get_copy(lexeme:str, root:str) -> str:
    '''
    Takes the lexeme and the root strings and returns the copied morpheme in the lexeme as a string
    Precondition:
    - lexeme must be stripped of prefixes.
    >>>get_copy('tsul’tsa’luqw','tsa’luqw')
    tsul’
    >>> get_copy('lhul’lhul’q','lhul’q')
    lhul’
    >>>get_copy('hi’huy’u','huye’')
    hi’
    >>>get_copy('ts’uy’ts’eey’u','ts’eey’u')
    ts’uy’
    >>>get_copy('t’ult’ulq','t’ulq')
    t’ul
    >>>get_copy('m’umun’lh' , 'm’un’')
    m’u
    >>>get_copy('q’epq’up’utum’','q’ep’')
    q’ep
    '''
    #print(lexeme, root)
    split1 = slice_string_graphemes(lexeme)
    iRed = where_copy(lexeme, root)
    l = []
    for i in range(iRed[0],iRed[1]):
        l.append(split1[i])
    
    w = join_split_graphemes(l)
    return w

#print(get_copy('tsul’tsa’luqw','tsa’luqw'))


def where_copied(lexeme:str, root:str) -> list:
    '''
    Takes the lexeme and the root strings and returns a list of the start and end indices of the copied morpheme...  each indices is a sound as per slice_string_graphemes, not a char
    Precondition:
    - lexeme must be stripped of prefixes.
    NOTE: This most likely won't return a string if there isn't a copy. Best be sure to use the 'has_copy' function to check that there's both a copy and a copied segment.
    >>>where_copied('hi’huy’u','huye’')
    [3, 6] ~treating uy as separate vowels.. idk what to do with that unuhw though...
    >>>where_copied('ts’uy’ts’eey’u','ts’eey’u')
    [3, 6]
    >>>where_copied('t’ult’ulq','t’ulq')
    [3, 6]
    >>>where_copied('m’umun’lh' , 'm’un’')
    [2, 4]
    >>>where_copied('tsul’tsa’luqw','tsa’luqw')
    [3, 6] ~~error: should be [3, 7] . probably an indexing issue cause of the glottal metathesis
    >>>where_copied('q’epq’up’utum’','q’ep’')
    [3, 6]
    '''
    try:
        reduplicant_index = where_copy(lexeme, root)
        #print(reduplicant_index)
        #print(lexeme[reduplicant_index[0]:reduplicant_index[1]])
        split1 = slice_string_graphemes(lexeme)
        split2 = slice_string_graphemes(root)
        split3 = slice_string_graphemes(get_copy(lexeme, root))
        #print(split1,split2, split3)
        l = []
        j=reduplicant_index[1]
        h = 0
        #print(reduplicant_index[1],(reduplicant_index[1]+len(split2)))
        for i in range(len(split3)):
            l1 = split1[j]
            l2 = split2[i]
            l3 = split3[h]  
            #print(i,j, h)
            #print(len(l))
            #print(l1 + ' ' + l2 + ' ' + l3)
            #print(l1 + ' ' + split2[i+1])
            if l1 in l2 or l2 in l1 or ((re.search(VOWELS_SCHWA,l1) and re.search(VOWELS_SCHWA,l2))) or l1 == UNUHW or l2 == UNUHW:
                #print('yes')
                if l2 in l3 or l3 in l2 or ((re.search(VOWELS_SCHWA,l2) and re.search(VOWELS_SCHWA,l3))) or l2 == UNUHW or l3 == UNUHW:
                    #print('yes')
                    l.append(j)
            elif len(l) > 0 and len(l) < len(split2):
                #print(split2[i])
                if lexeme[i] == '’' and l2 in [split2[i-1]]:
                    ##print('yes')
                    l.append(j)
                if lexeme[i] == '’' and l2 in [split2[i-1]]:
                    ##print('yes')
                    l.append(j)                
            elif l1 in [split2[i+1]] or [split2[i+1]] in l1:
                #print('yes')
                l.append(i)
            elif re.search(VOWELS_SCHWA, l1) and re.search(VOWELS_SCHWA, [split2[i+1]]):
                #print(split2[i])
                l.append(i)
            j+=1
            h+=1
        k=[]
        
        try:    
            k = [reduplicant_index[1]]
            last = l[len(l)-1] + 1
            k.append(last)
            return k
        except:
            return k
    except:
        return None
    
#print(where_copied('kwa’kwti’','kwaty'))

def get_copied(lexeme:str, root:str) -> str:
    '''
    Takes the lexeme and root strings and returns the copied morpheme as a string.
    Precondition:
    ~!!!! lexeme cannot contain a reduplicant with an l onset
    - lexeme must be stripped of prefixes.
    Note: doesn't take into account ablaut. To get the underlying copied morpheme, pass through 'reverse_copied_ablaut' first.
    >>>get_copied('lhul’lhul’q','lhul’q')
    lhul’
    >>>get_copied('hi’huy’u','huye’')
    hu
    >>>get_copied('q’eq’up’utum’','q’ep’')
    q’u
    >>>get_copied('tsul’tsa’luqw','tsa’luqw')
    tsa’ ~~error: should be tsa’l . probably an indexing issue cause of the glottal metathesis
    '''
    
    split1 = slice_string_graphemes(lexeme)
    #print(split1)
    iRed = where_copied(lexeme, root)
    #print(iRed)
    l = []
    try:
        for i in range(iRed[0],iRed[1]):
            l.append(split1[i])
        
        w = join_split_graphemes(l)
        return w    
    except:
        return None

def has_copy(lexeme, root):
    copy = ''
    copied = ''
    try:
        copy = get_copy(lexeme, root)
        copied = get_copied(lexeme, root)        
        if copied == None or copy == None:
            return False
        try:
            if copied != None and copy != None:
                return True
        except:
            return False
    except:
        return False
    return False

'''------L STUFF------'''
def has_l_infixation(lexeme:str, root:str) -> bool:
    '''
    Takes the lexeme and root strings and determines if there's l-infixation based on the number of Ls in the root and lexeme. Returns True if there's l-infixation.
    Precondition:
    - lexeme must be stripped of prefixes.
    >>>has_l_infixation('kwul’a’kwti’','kwaty')
    True
    >>>has_l_infixation('ts’i’ts’umiil’','ts’umiil’')
    False
    >>>has_l_infixation('le’lum’stum’' , 'lem')
    False
    >>>has_l_infixation('lul’ul’kwut','lukwa'))
    True
    '''
    num_l_word = len(re.findall(L, lexeme))
    num_l_root = len(re.findall(L, root))
    #print(num_l_root, num_l_word)
    #why is there a criterion that there can't be an l-onset if there's only 1 l in the copy?
    if num_l_word == 1 and num_l_root == 0:
        return True
    elif num_l_word == num_l_root:
        return False
    elif num_l_root == 1 and num_l_word == 2:
        return False
    elif num_l_root == 1 and num_l_word == 3:
        return True
    else:
        return False


#print(has_l_infixation('kwekwul’sh','kweel'))

def where_l_infixation(lexeme:str, root:str):
    '''
    Takes the lexeme and the root strings and returns a list of the start and end indices of the L infix... 
    Precondition:
    - lexeme must be stripped of prefixes.
    ~~this is currently wrong because it assumes each indices is a char, not a grapheme
    >>>where_l_infixation('kwul’a’kwti’','kwaty')
    [2, 5]
    >>>where_l_infixation('lul’ul’kwut','lukwa')
    [1, 4]
    >>>where_l_infixation('ts’i’ts’umiil’','ts’umiil’')
    None
    '''
    if has_l_infixation(lexeme, root):
        indices_all_L = [i.span() for i in re.finditer(("(ul’|ul|l’|l)"), lexeme)]
        if indices_all_L[0][0] == 0:
            return list(indices_all_L[1])
        else:
            return list(indices_all_L[0])
    else: 
        return None


def remove_l_infixation(lexeme:str, root:str) -> str:
    '''
    Takes the lexeme and root strings and returns the lexeme string with the l infix removed.
    removes l’ or l, and its preceding schwa if one exists 
    Precondition:
    - lexeme must be stripped of prefixes.
    >>>remove_l_infixation('kwul’a’kwti’','kwaty')
    kwa’kwti’
    >>>remove_l_infixation('huli’huy’u','huye’')
    hi’huy’u
    >>>remove_l_infixation('ts’i’ts’umiil’','ts’umiil’')
    ts’i’ts’umiil’
    >>>remove_l_infixation('lul’ul’kwut','lukwa'))
    lu’l’kwut # need to deal with u metathesis or deletion
    '''
    l_infix_span = where_l_infixation(lexeme, root)
    lexeme = lexeme[:l_infix_span[0]] + lexeme[l_infix_span[1]:]
    return lexeme



def where_red_with_l(lexeme:str, root:str):
    '''
    Takes the lexeme and root and returns a list of the indices of the copy with the l infix still in place. 
    Precondition:
    - lexeme must be stripped of prefixes.
    ~~this is currently wrong because it assumes each indices is a char, not a grapheme
    >>>get_red_with_l('kwul’a’kwti’','kwaty')
    [0, 6] ~~error: should be [0, 5]
    >>>where_red_with_l('huli’huy’u','huye’')
    [0, 4]
    '''
    red_with_l = []
    if has_l_infixation(lexeme,root):
        word = lexeme
        index_l = where_l_infixation(word, root)
        temp_word = remove_l_infixation(word,root)
        index_reduplicant = where_copy(temp_word, root)
        index_reduplicated = where_copied(temp_word,root)
        
        if index_reduplicant[1] > index_l[1]:
            red_with_l = [0, index_reduplicant[1]+1]
        else:
            red_with_l = [0, index_l[1]+1]

    return red_with_l

#print(where_red_with_l('pulou’ps', 'pous'))

def get_red_with_l(lexeme:str, root:str):
    '''
    Takes the lexeme and root and returns the copy with the l infix still in place. 
    Precondition:
    - lexeme must be stripped of prefixes.
    >>>get_red_with_l('kwul’a’kwti’','kwaty')
    kwul’a
    >>>get_red_with_l('huli’huy’u','huye’')
    huli ~~error: should be huli’
    '''
    if has_l_infixation(lexeme, root):
        i = where_red_with_l(lexeme, root)
        #print(i)
        return lexeme[i[0]:i[1]]
    return None

#print(get_red_with_l('pulou’ps', 'pous'))


def starts_with_l(word:str) -> bool:
    '''
    Takes a string (can be anything) and returns True if the character is either exclusively 'l' or 'l’'
    Precondition:
    - lexeme must be stripped of prefixes.
    >>starts_with_l('l’ots')
    True
    >>starts_with_l('lots')
    True
    >>starts_with_l('tleni')
    False
    >>starts_with_l('keni')
    False
    >>starts_with_l('lheni')
    False
    '''
    if(re.match(L, word) and not re.match(CONSONANTS_NO_L, word)):
        l = re.search(L, word)
        span = l.span()
        return True
    return False


'''-------RESONANTS-------'''

def has_hRes_copying(lexeme:str, root:str) -> bool:
    '''
    Takes the lexeme and root strings and returns if the onset of the lexeme starts with h and the onset of the root starts with a resonant grapheme.
    Precondition:
    - lexeme must be stripped of prefixes.
    >>has_hRes_copying('hum’een’','meen’')
    True
     >>has_hRes_copying('heeyum’','hey’')
    False
    >>has_hRes_copying('hwsmul’mul’q','mel’q')
    False
    >>has_hRes_copying('hi’hul’ush','le’')
    True
    >>>has_hRes_copying('h’i’hul’ush','le’')
    True
    >>>has_hRes_copying('hunuw’nutst', 'nuw’')
    True
    has_hRes_copying('hunuw’nutst', 'kuw’')
    False
    '''
    if re.match(H, lexeme) and not re.match(CONSONANTS_NO_H, lexeme) and not re.match(H, root) and re.match(RESONANTS, root):
        h = re.match(H, lexeme)
        return True
    return False
#print(has_hRes_copying('hi’hul’ush','le’'))

def agree_hresonant_copy(lexeme:str, root:str) -> str:
    '''
    Takes the lexeme and root strings. Returns the string with the h replaced with the onset resonant in the root.
    Precondition:
    - lexeme must be stripped of prefixes.
    >>agree_hresonant_copy('hum’een’','meen’')
    mum’een’
    >>agree_hresonant_copy('hwsmul’mul’q','mel’q')
    hwsmul’mul’q
    >>agree_hresonant_copy('heeyum’','hey’')
    heeyum’
    >>>agree_hresonant_copy('hunuw’nutst', 'nuw’')
    nunuw’nutst
    '''
    
    if(has_hRes_copying(lexeme, root)):
        h_span = re.match(H, lexeme).span()
        r_span = re.match(CONSONANTS_NO_H, root).span()
        word_ons = lexeme[h_span[0]:h_span[1]]
        root_ons = root[r_span[0]:r_span[1]]
        lexeme = re.sub(word_ons, root_ons, lexeme)
    return lexeme

def get_hresonant_copy(lexeme:str, copy:str) -> str:
    '''
    Takes the lexeme and root strings. Returns the string with the h replaced with the onset resonant in the root.
    Precondition:
    - lexeme must be stripped of prefixes.
    >>get_hresonant_copy('mum’een’','mum')
    hum
    >>get_hresonant_copy('hwsmul’mul’q','mel’q')
    hwsmul’mul’q
    >>get_hresonant_copy('h'eeyum’','yey’')
    hey’
    '''
    lex = copy
    split_lexeme = slice_string_graphemes(lexeme)
    split_copy = slice_string_graphemes(copy)
    if re.search(H, split_lexeme[0]) and re.search(RESONANTS, split_copy[0]):
        lex = join_split_graphemes(split_lexeme[0]) + join_split_graphemes(split_copy[1:])
    return lex

#print(get_hresonant_copy('h’eeyum’','yey’'))
def starts_with_resonant(lexeme:str) -> bool:
    '''
    Takes a string (can be anything) and returns if it begins with any resonant
    >>>starts_with_resonant('l’ots')
    True
    >>>starts_with_resonant('nilh')
    True
    >>>starts_with_resonant('ya’thut')
    True
    >>>starts_with_resonant('pekw’')
    False
    >>>starts_with_resonant('y’a’thut')
    True
    '''    
    if re.match(RESONANTS, lexeme):
        #print('starts_with_resonant')
        return True
    return False    


'''------METATHESIS-----'''

def has_copy_metathesis(lexeme:str, root:str) -> bool:
    '''
    Takes the lexeme and root strings and determines if there's any metathesis in the copy. Returns true if the first vowels in the copy is in a different index than the first vowel in the root.
    Precondition:
    - lexeme must be stripped of prefixes.
    NOTE: this only looks at metathesis between vowels and consonants. It doesn't check if there's any metathesis of consonants or shifting of glottals. It should eventually.
    >>>has_copy_metathesis('qp’apq’upthut', 'q’pu')
    False
    >>>has_copy_metathesis('huy', 'hay')
    False
    >>>has_copy_metathesis('q’uxq’ux', 'q’ux')
    False
    >>>has_copy_metathesis('qtewustun','qit')
    True
    >>>has_copy_metathesis('kwakwma’tsiin’','kwam’')
    False
    '''
    if re.search(VOWELS_SCHWA,lexeme) and re.search(VOWELS_SCHWA, root):
        w = re.search(VOWELS_SCHWA,lexeme)
        r = re.search(VOWELS_SCHWA, root)
        if w.span()[0] == r.span()[0]:    
            return False
        else:
            #print('has metathesis')
            return True
    return False

#print(has_copy_metathesis('kwa’kwti’','kwaty'))

#def need has_copied_metathesis():


def reverse_copy_metathesis(lexeme:str, root:str) -> str:
    '''
    Takes the lexeme and root strings and reverses metathesis of consonant-vowels in the copy morpheme if it exists
    Precondition:
    - lexeme must be stripped of prefixes.
    NOTE: this only looks at metathesis between vowels and consonants. It doesn't check if there's any metathesis of consonants or shifting of glottals. It should eventually.
    >>>reverse_copy_metathesis('qp’apq’upthut', 'q’pu')
    qp’apq’upthut
    >>>reverse_copy_metathesis('huy', 'hay')
    huy
    >>>reverse_copy_metathesis('q’uxq’ux', 'q’ux')
    q’uxq’ux
    >>>reverse_copy_metathesis('qtewustun','qit')
    qetwustun
    >>>reverse_copy_metathesis('kwakwma’tsiin’','kwam’')
    kwakwma’tsiin’
    '''
    if has_metathesis:
        w_1 = lexeme
        w_span = re.search(VOWELS_SCHWA,lexeme).span()
        r_span = re.search(VOWELS_SCHWA, root).span()
        w_1 = lexeme[0:r_span[0]] + lexeme[w_span[0]:w_span[1]] + lexeme[r_span[0]:w_span[0]] + lexeme[w_span[1]:]
        return w_1
    else:
        return lexeme


'''-----ABLAUT-----'''
def has_copy_ablaut(copy:str, copied:str, root:str) -> bool:
    '''
    Takes the copy and copied morpheme strings, and the root string and returns True if the first vowel in the copy is DIFFERENT than the first vowel in the root.
    NOTE: this doesn't use the 'copied' variable. I'm keeping it in because my IDE doesn't give me parameter hints and I kept forgetting which strings to include in which ablaut functions. 
    >>>has_copy_ablaut('qp’up','q’pu', 'q’pu')
    False
    >>>has_copy_ablaut('qp’ap','q’pa', 'q’pu')
    True
    >>>has_copy_ablaut('qp’ap','q’pa', 'q’pa')
    False
    >>>has_copy_ablaut('qp’aap','q’paa', 'q’pa')
    True
    >>>has_copy_ablaut('qp’oup','q’pou', 'q’pu')
    True
    '''           
    vowels = get_vowels_copy_copied_root(copy, copied, root)
    #print(vowels[0]+" " + vowels[2])
    try:
        if vowels[0] != vowels[2]:
            return True
    except:
        print('vowels aren\'nt in all of the copy, copied, and root. check get_vowels_copy_copied_root(copy, copied, root) function') 
    return False

def has_copied_ablaut(copy:str, copied:str, root:str) -> bool:
    '''
    Takes the copy and copied morpheme strings, and the root string and returns True if the first vowel in the copied morpheme is DIFFERENT than the first vowel in the root.
    NOTE: this doesn't use the 'copy' variable. I'm keeping it in because my IDE doesn't give me parameter hints and I kept forgetting which strings to include in which ablaut functions. Also, theoretically this could be used to check if the first vowel in a lexeme is different from the root where the lexeme DOESN'T have reduplication in it... this is only possible if I remove the 'copy' parameter, so oh well.
    >>>has_copied_ablaut('qp’up','q’pu', 'q’pu')
    False
    >>>has_copied_ablaut('qp’ap','q’pa', 'q’pu')
    True
    >>>has_copied_ablaut('qp’ap','q’pa', 'q’pa')
    False
    >>>has_copied_ablaut('qp’aap','q’paa', 'q’pa')
    True
    >>>has_copied_ablaut('qp’oup','q’pou', 'q’pu')
    True
    '''         
    vowels = get_vowels_copy_copied_root(copy, copied, root)
    #print(vowels[1]+" " + vowels[2])
    try:
        if vowels[1] != vowels[2]:
            return True
    except:
        print('vowels aren\'nt in all of the copy, copied, and root. check get_vowels_copy_copied_root(copy, copied, root) function') 
    return False


def has_copy_strengthening(copy:str, copied:str, root:str) -> bool:
    '''
    Takes the copy and copied morpheme strings, and the root string and returns True if the first vowel in the copy morpheme is not a schwa and the than the first vowel in the root is a schwa.
    NOTE: this doesn't use the 'copied' variable. I'm keeping it in because my IDE doesn't give me parameter hints and I kept forgetting which strings to include in which ablaut functions.
    >>>has_copy_strengthening('qp’up','q’pu', 'q’pu')
    False
    >>>has_copy_strengthening('qp’ap','q’pu', 'q’pu')
    True
    >>>has_copy_strengthening('qp’ap','q’pu', 'q’pa')
    False
    >>>has_copy_strengthening('qp’up','q’pu', 'q’pa')
    False
    >>>has_copy_strengthening('qp’aap','q’pu', 'q’pa')
    False
    >>>has_copy_strengthening('qp’oup','q’pu', 'q’pa')
    False
    '''       
    vowels = get_vowels_copy_copied_root(copy, copied, root)
    #print(vowels[0]+" " + vowels[2])
    try:
        if re.search(VOWELS,vowels[0]) and re.search(SCHWA, vowels[2]) and not re.search(VOWELS, vowels[2]):
            return True
    except:
        print('vowels aren\'nt in all of the copy, copied, and root. check get_vowels_copy_copied_root(copy, copied, root) function') 
    return False


def has_copy_reduction(copy:str, copied:str, root:str) -> bool:
    '''
    Takes the copy and copied morpheme strings, and the root string and returns True if the first vowel in the copy morpheme is a schwa and the than the first vowel in the root is not a schwa.
    NOTE: this doesn't use the 'copied' variable. I'm keeping it in because my IDE doesn't give me parameter hints and I kept forgetting which strings to include in which ablaut functions.
    >>>has_copy_reduction('qp’up','q’pu', 'q’pu')
    False
    >>>has_copy_reduction('qp’ap','q’pu', 'q’pu')
    False
    >>>has_copy_reduction('qp’ap','q’pu', 'q’pa')
    False
    >>>has_copy_reduction('qp’up','q’pu', 'q’pa')
    True
    >>>has_copy_reduction('qp’oup','q’pu', 'q’pa')
    False
    '''    
    vowels = get_vowels_copy_copied_root(copy, copied, root)
    #print(vowels[0]+" " + vowels[2])
    try:
        if re.search(SCHWA,vowels[0]) and not re.search(VOWELS,vowels[0]) and re.search(VOWELS, vowels[2]):
            return True
    except:
        print('vowels aren\'nt in all of the copy, copied, and root. check get_vowels_copy_copied_root(copy, copied, root) function') 
    return False

def has_copied_strengthening(copy:str, copied:str, root:str) -> bool:
    '''
    Takes the copy and copied morpheme strings, and the root string and returns True if the first vowel in the copied morpheme is not a schwa and the first vowel in the root is a schwa.
    NOTE: this doesn't use the 'copy' variable. I'm keeping it in because my IDE doesn't give me parameter hints and I kept forgetting which strings to include in which ablaut functions. Also, theoretically this could be used to check if the first vowel in a lexeme is different from the root where the lexeme DOESN'T have reduplication in it... this is only possible if I remove the 'copy' parameter, so oh well.
    >>>has_copied_strengthening('qp’up','q’pa', 'q’pu')
    True
    >>>has_copied_strengthening('qp’up','q’pu', 'q’pu')
    False
    >>>has_copied_strengthening('qp’up','q’pu', 'q’pa')
    False
    >>>has_copied_strengthening('qp’up','q’pa', 'q’pa')
    False
    '''
    vowels = get_vowels_copy_copied_root(copy, copied, root)
    #print(vowels[1]+" " + vowels[2])
    try:
        if re.search(VOWELS,vowels[1]) and re.search(SCHWA, vowels[2]) and not re.search(VOWELS, vowels[2]):
            return True
    except:
        print('vowels aren\'nt in all of the copy, copied, and root. check get_vowels_copy_copied_root(copy, copied, root) function') 
    return False


def has_copied_reduction(copy:str, copied:str, root:str) -> bool:
    '''
    Takes the copy and copied morpheme strings, and the root string and returns True if the first vowel in the copied morpheme is a schwa and the first vowel in the root is not a schwa.
    NOTE: this doesn't use the 'copy' variable. I'm keeping it in because my IDE doesn't give me parameter hints and I kept forgetting which strings to include in which ablaut functions. Also, theoretically this could be used to check if the first vowel in a lexeme is different from the root where the lexeme DOESN'T have reduplication in it... this is only possible if I remove the 'copy' parameter, so oh well.
    >>>has_copy_reduction('qp’ap','q’pu', 'q’pu')
    False
    >>>has_copy_reduction('qp’up','q’pu', 'q’pu')
    False
    >>>has_copy_reduction('qp’up','q’pu', 'q’pa')
    True
    >>>has_copy_reduction('qp’ap','q’pu', 'q’pa')
    False
    '''
    
    vowels = get_vowels_copy_copied_root(copy, copied, root)
    #print(vowels[1]+" " + vowels[2])
    try:
        if re.search(SCHWA,vowels[1]) and not re.search(VOWELS,vowels[1]) and re.search(VOWELS, vowels[2]):
            return True
    except:
        print('vowels aren\'nt in all of the copy, copied, and root. check get_vowels_copy_copied_root(copy, copied, root) function') 
    return False


def get_copy_ablaut_index_lexeme(lexeme:str, root:str) -> list:
    '''
    Takes the lexeme and root strings and returns a list of the vowel in the copy that has undergone ablaut, and the vowel in the root that was modified, and the index of the vowel in the copy.
    Precondition:
    - lexeme must be stripped of prefixes.
    NOTE: The index returned is that within the copy. To get the index of the vowel within the lexeme, it'll need to be wrapped.
    >>>get_copy_ablaut_index_lexeme('q’uq’up’utum’','q’ep’')
    ['u', 'u', '1']
    >>>get_copy_ablaut_index_lexeme('q’eq’ep’utum’','q’ep’')
    None
    >>>get_copy_ablaut_index_lexeme('q’eq’up’utum’','q’ep’')
    None
    '''
    copy = get_copy(lexeme, root)
    copied = get_copied(lexeme, root)
    copy_graphemes = slice_string_graphemes(copy)
    
    #copy
    copy_index = where_copy(lexeme, root)
    vowel_indices = where_vowels_copy_copied_root(copy, copied, root)
    if(has_copy_reduction(copy, copied, root)):
        return [copy_graphemes[vowel_indices[0]], copy_graphemes[vowel_indices[2]], str(copy_index[0] + vowel_indices[0])]
    elif(has_copy_strengthening(copy, copied, root)):
        return [copy_graphemes[vowel_indices[0]], copy_graphemes[vowel_indices[2]], str(copy_index[0]  + vowel_indices[0])]
    elif(has_copy_ablaut(copy, copied, root)):
        return [copy_graphemes[vowel_indices[0], copy_graphemes[vowel_indices[2]], str(copy_index[0]  + vowel_indices[0])]]
    else:
        return None

def get_copied_ablaut_index_lexeme(lexeme:str, root:str) -> list:
    '''
    Takes the lexeme and root strings and returns a list of the vowel in the copied morpheme that has undergone ablaut, and the vowel in the root that was modified, and the index of the vowel in the copy.
    Precondition:
    - lexeme must be stripped of prefixes.
    NOTE: The index returned is that within the copied morpheme. To get the index of the vowel within the lexeme, it'll need to be wrapped.
    Also, theoretically this could be used to check if the first vowel in a lexeme is different from the root where the lexeme DOESN'T have reduplication in it... this is only possible if I remove the 'copy' parameter from where_vowels_copy_copied_root, so oh well.
    
    >>>get_copied_ablaut_index_lexeme('q’uq’up’utum’','q’ep’')
    ['u', 'e', '3']
    >>>get_copied_ablaut_index_lexeme('q’eq’ep’utum’','q’ep’')
    None
    >>>get_copied_ablaut_index_lexeme('q’eq’up’utum’','q’ep’')
    ['u', 'e', '3']
    '''
    copy = get_copy(lexeme, root)
    copied = get_copied(lexeme, root)
    copied_graphemes = slice_string_graphemes(copied)
    root_graphemes = slice_string_graphemes(root)
    #copy
    #print(slice_string_graphemes(lexeme))

    copied_index = where_copied(lexeme, root)
    #print(copied_index)
    vowel_indices = where_vowels_copy_copied_root(copy, copied, root)
    vowel_index_lexeme = copied_index[0] + vowel_indices[1]
    #print(vowel_index_lexeme)
    if(has_copied_reduction(copy, copied, root)):
        return [copied_graphemes[vowel_indices[1]], root_graphemes[vowel_indices[2]], str(vowel_index_lexeme)]
    elif(has_copied_strengthening(copy, copied, root)):
        return [copied_graphemes[vowel_indices[1]], root_graphemes[vowel_indices[2]], str(vowel_index_lexeme)]
    elif(has_copied_ablaut(copy, copied, root)):
        return [copied_graphemes[vowel_indices[1], root_graphemes[vowel_indices[2]], str(vowel_index_lexeme)]]

    return None


def has_weakening(lexeme:str, root:str) -> bool:
    ''' 
    Takes the lexeme and root strings and returns True if either or both of the has_copy_reduction, has_copied_reduction functions return true.
    Precondition:
    - lexeme must be stripped of prefixes.
    >>>has_weakening('huy', 'hay')
    True
    >>>has_weakening('qp’apq’upthut', 'q’pu')
    False
    >>>has_weakening('q’uxq’ux', 'q’ux')
    False
    '''
    copy = get_copy(lexeme, root)
    copied = get_copied(lexeme, root)
    if has_copy_reduction(copy, copied, root) or has_copied_reduction(copy, copied, root):
        return True
    return False

def has_strengthening(lexeme:str, root:str) -> bool:
    '''
    Takes the lexeme and root strings and returns True if either or both of the has_copy_strengthening, has_copied_strengthening functions return true
    Precondition:
    - lexeme must be stripped of prefixes.
    >>>has_strengthening('qp’apq’upthut', 'q’pu')
    True
    >>>has_strengthening('huy', 'hay')
    False
    >>>has_strengthening('q’uxq’ux', 'q’ux')
    False
    >>>has_strengthening('hay', 'huy')
    True
    '''
    copy = get_copy(lexeme, root)
    copied = get_copied(lexeme, root)
    if has_copy_strengthening(copy, copied, root) or has_copied_strengthening(copy, copied, root):
        return True
    return False

def reverse_copy_ablaut(lexeme:str, root:str) -> str:
    '''
    Takes the lexeme and root strings and returns the lexeme string with the ablauted vowel in the copy assimilated to the underlying vowel from the root.
    Precondition:
    - lexeme must be stripped of prefixes.
    >>>reverse_copy_ablaut('qp’apq’upthut', 'q’pu')
    qp’upq’upthut
    >>>reverse_copy_ablaut('tseltsulush','tselush')
    None
    >>>reverse_copy_ablaut('tsultselush','tselush')
    tseltselush
    '''
    copy = get_copy(lexeme, root)
    copied = get_copied(lexeme, root)
    vowel_indices = where_vowels_copy_copied_root(copy, copied, root)
    #print(copy + copied + root)
    if has_copy_ablaut(copy, copied ,root):
        vowel_indices = where_vowels_copy_copied_root(copy, copied, root)
        
        no_ablaut = ''
        copy_graphemes = slice_string_graphemes(get_copy(lexeme, root))
        copied_graphemes = slice_string_graphemes(get_copied(lexeme, root))
        word_graphemes = slice_string_graphemes(lexeme)
        root_graphemes = slice_string_graphemes(root)
        
        vowel_indices = where_vowels_copy_copied_root(copy, copied, root)
        
        no_ablaut = join_split_graphemes(word_graphemes[0:vowel_indices[0]]) + join_split_graphemes(root_graphemes[vowel_indices[2]]) + join_split_graphemes(word_graphemes[vowel_indices[0]+1:])
        
        return no_ablaut
    else:
        return None


def reverse_copied_ablaut(lexeme:str, root:str) -> str:
    '''
    Takes the lexeme and root strings and returns the lexeme string with the ablauted vowel in the copied morpheme assimilated to the underlying vowel from the root.
    Precondition:
    - lexeme must be stripped of prefixes.
    >>>reverse_copied_ablaut('qp’apq’upthut', 'q’pu')
    qp’upq’upthut
    reverse_copied_ablaut('tsultselush','tselush')
    None
    >>>reverse_copied_ablaut('tsultselush','tselush')
    tseltselush
    >>>reverse_copied_ablaut('tseltsulush','tselush')
    None
    '''
    copy = get_copy(lexeme, root)
    copied = get_copied(lexeme, root)   
    #print(copy + ' ' + copied + ' ' + root)
    if has_copied_ablaut(copy, copied, root):
        #print(copy, copied, root)
        copied_graphemes = slice_string_graphemes(copied)
        word_graphemes = slice_string_graphemes(lexeme)
        root_graphemes = slice_string_graphemes(root)
        
        copied_indices = where_copied(lexeme, root)
        vowel_indices = where_vowels_copy_copied_root(copy, copied, root)
        copied_new_vowel = join_split_graphemes(copied_graphemes[:vowel_indices[0]]) + join_split_graphemes(root_graphemes[vowel_indices[2]]) + join_split_graphemes(copied_graphemes[vowel_indices[1]+1:])
        no_ablaut = join_split_graphemes(word_graphemes[:copied_indices[0]])+ copied_new_vowel + join_split_graphemes(word_graphemes[copied_indices[1]:])
        #print(no_ablaut)
        return no_ablaut
    else:
        return lexeme
 
    
#print(reverse_copied_ablaut('luliqwu','luqwa'))

def wrap_stripped(lexeme:str, stripped:str, parse:str) -> str:
    '''
    Takes the original lexeme, the stripped lexeme, and the parse strings and returns the original lexeme with all of the modifications that have been applied to the stripped lexeme. 
    Preconditions: 
    - This is moot if the original lexeme contained no affixes. 
    NOTE: this currently doesn't actually work, because it excludes all of the phonological changes made to the affixes, like vowel insertion for example.
    >>>wrap_stripped('hwkwunkwunlhnenum','kwunkwun', 'hw=√kwun=lhnen=m=PL')
    hwkwunkwunlhnenm ~~error: not adding vowel back before the m suffix.
    >>>wrap_stripped('stslhaythun', 'tsl', 's=√tsilh=ay=thin')
    stslaythin ~~error: needs to pull from lexeme info where the original prefixes and suffixes were removed, to preserve phonological changes made to affixes
    >>>wrap_stripped('shchuymuna’lh','chuymun')
    [2, 9] ~~error: considering sh as 2 indices
    '''
    wrapped =''
    prefix_graphemes = parser.get_prefixes(parse)
    #print(prefix_graphemes)
    suffix_graphemes = parser.get_suffixes(parse)
    #print(suffix_graphemes)
    prefix_string = join_split_graphemes(prefix_graphemes)
    suffix_string = join_split_graphemes(suffix_graphemes)
    wrapped = prefix_string + stripped + suffix_string
    return wrapped


def span_prefix_graphemes(lexeme:str, parse:str) -> list:
    '''
    Takes the original lexeme and the parse strings and returns the start and end indices of the prefixes in the original.
    Preconditions:
    - This is moot if there're no prefixes in the original lexeme.
    NOTE: this currently doesn't work because:
    - It doesn't recognize is there's been any modifications to the prefixes. It needs to work. It's probably going to need to use something from ManageParse or LexemeInfo. 
    >>>span_prefix_graphemes('hwkwunkwunlhnenum', 'hw=√kwun=lhnen=m=PL')
    [0, 1]
    >>>span_prefix_graphemes('stslhaythun', 's=√tsilh=ay=thin')
    [0, 1]
    >>>span_prefix_graphemes('shts’a’lum’uqw', 's=hw=√ts’a’muqw=PL')
    [0, 0] ~~error: s has been added, h has been added without w, so not recognizing the characters and returning null
    >>>span_prefix_graphemes('shts’um’inus', 'shhw=√ts’um’=inus')
    [0, 0]  ~~error: sh has been added, hw has been excluded, so not recognizing the characters and returning null
    >>>span_prefix_graphemes('lhchumux', 'lh=√chumux')
    [0, 1]
    '''
    prefixes = parser.get_prefixes(parse)
    #print(prefixes)
    root = get_root(parse)
    #print(root)
    #print(lexeme)
    #print(prefixes[len(prefixes)-1])
    try:
        iPref = lexeme.find(prefixes[len(prefixes)-1])
        #print(iPref)
        stripped_graphemes = slice_string_graphemes(lexeme[:iPref+1])
        return [0,len(stripped_graphemes)]
    except:
        return [0, 0]
    


def span_suffix_graphemes(lexeme:str, parse:str) -> list:
    '''
    Takes the original lexeme and the parse strings and returns the start and end indices of the suffixes in the original.
    Preconditions:
    - This is moot if there're no suffixes in the original lexeme.
    NOTE: this currently doesn't work because:
    - It doesn't recognize is there's been any modifications to the suffixes. It needs to work. It's probably going to need to use something from ManageParse or LexemeInfo. 
    >>>span_suffix_graphemes('tsuwtelh', '√tsuwtelh')
    [6, 6]
    >>>span_suffix_graphemes('tsus', 's=√tsus')
    [3, 3]
    >>>span_suffix_graphemes('stslhaythun', 's=√tsilh=ay=thin')
    [3, 8]
    '''
    suffixes = parser.get_suffixes(parse)
    root = get_root(parse)
    lexeme_graphemes = slice_string_graphemes(lexeme)
    try:
        iSuff = lexeme.rfind(suffixes[0])
        if re.search(VOWELS_SCHWA,lexeme[iSuff-1]) and not re.search(VOWELS_SCHWA, root[len(root)-1]):
            iSuff -=1
            
        stripped_graphemes = slice_string_graphemes(lexeme[:iSuff])
        num_graph_lex = len(lexeme_graphemes)
        num_graph_no_suff = len(stripped_graphemes)
        return([num_graph_no_suff, num_graph_lex])
    except:
        return [len(lexeme_graphemes),len(lexeme_graphemes)]
    
def indices_stripped(lexeme:str, parse:str) -> list:
    '''
    Takes the original lexeme and the parse and returns the indices of the lexeme that exclude prefixes and affixes
    Precondition:
    - The lexeme must be in its original state.
    >>>indices_stripped('hwkwunkwunlhnenum', 'hw=√kwun=lhnen=m=PL')
    [1, 7]
    >>>indices_stripped('hwtsi’tsakwul’thut', 'hw=√tsel=that=PROG'
    [1, 10]
    >>>indices_stripped('stsun’ewusum', 's=√tsun’=ewus=m')
    [1, 4]
    >>>indices_stripped('tsuwtelh', '√tsuwtelh')
    [0, 6]
    '''
    indices_prefix = span_prefix_graphemes(lexeme, parse)
    indices_suffix = span_suffix_graphemes(lexeme, parse)
    return [indices_prefix[1], indices_suffix[0]]

def where_in_wrapped(lexeme:str, parse:str, indices:list) -> list:
    '''
    NOTE~~~~~ I don't actually know what's different between this function and indices_stripped
    >>>where_in_wrapped('hwkwunkwunlhnenum', 'hw=√kwun=lhnen=m=PL', [0, 4])
    [1, 5]
    >>>where_in_wrapped('tsuwtelh', '√tsuwtelh', [0, 6])
    [0, 6]
    '''
    iStripped = indices_stripped(lexeme, parse)  
    try:
        iStart = indices[0]+iStripped[0]
        iEnd = indices[1] + iStripped[0]
        return [iStart,iEnd]
    except:
        return [0,0]

