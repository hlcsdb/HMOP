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

SOUNDS = "(kw’|kw|k’|k|m’|m|n’|n|qw’|qw|q’|q|ch’|ch|hw|th|sh|lh|tth’|tth|ts’|ts|tl’|xw|x|l’|l|h|s|w’|w|y’|y|p’|p|t’|t|aa|ee|oo|ou|ii|o|u|i|e|a|’)"

CONSONANTS = "(kw’|kw|k’|k|m’|m|n’|n|qw’|qw|q’|q|ch’|ch|hw|th|sh|lh|tth’|tth|ts’|ts|tl’|xw|x|l’|l|h|s|w’|w|y’|y|p’|p|t’|t|’)"
CONSONANTS_NO_L = "(kw’|kw|k’|k|m’|m|n’|n|qw’|qw|q’|q|ch’|ch|hw|th|sh|lh|tth’|tth|ts’|ts|tl’|xw|x|h|s|w’|w|y’|y|p’|p|t’|t|’)"
CONSONANTS_NO_H = "(kw’|kw|k’|k|m’|m|n’|n|qw’|qw|q’|q|ch’|ch|hw|th|sh|lh|tth’|tth|ts’|ts|tl’|xw|x|l’|l|s|w’|w|y’|y|p’|p|t’|t|’)"

CONSONANTS_UNUHW = CONSONANTS = "(kw’|k’|m’|n’|qw’|q’|ch’|tth’|ts’|tl’|l’|w’|y’|p’|t’|h’|’)"


RESONANTS = "(l’|l|m’|m|n’|n|w’|w|y’|y)"
SCHWA = "u"
UNUHW = "’"
VOWELS = "(aa|ee|oo|ou|o|i|e|a)"
VOWELS_SCHWA = "(aa|ee|oo|ou|o|u|i|e|a)"
L = "(l’|l)"
H = "(h’|h)"
VOWELS_LIST = ['aa', 'ee', 'oo', 'ou', 'o', 'u', 'i', 'e', 'a']

#user_input = input()

def slice_string_graphemes(word):
    '''
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

def join_split_graphemes(grapheme_list):
    '''
    >>>join_split_graphemes(['ts’', 'i', '’', 'ts’', 'u', 'm', 'ii', 'l’'])
    ts’i’ts’umiil’
    '''
    w = ''
    for i in grapheme_list:
        w += i
    return w

def index_vowel_word(word, root):
    '''
    >>>index_vowel_word('huy', 'hay')
    (1,2)
    >>>index_vowel_word('hee’wi’wuqus', 'wiq')
    (1, 2)
    >>>index_vowel_word('q’apq’upthut', 'q’pu')
    None #needs metathesis first
    >>>index_vowel_word('qp’apq’upthut', 'q’pu')
    (3, 4)
    '''
    if re.search(VOWELS_SCHWA,word) and re.search(VOWELS_SCHWA, root):
        w = re.search(VOWELS_SCHWA,word)
        #print(w)
        r = re.search(VOWELS_SCHWA, root)
        #print(r)
        return w.span()

def index_vowel_root(word, root):
    '''
    >>>index_vowel_root('huy', 'hay')
    (1,2)
    >>>index_vowel_root('hee’wi’wuqus', 'wiq')
    (1, 3)
    >>>index_vowel_root('q’apq’upthut', 'q’pu')
    None #needs metathesis first
    >>>index_vowel_root('qp’apq’upthut', 'q’pu')
    (3, 4)
    '''
    if re.search(VOWELS_SCHWA,word) and re.search(VOWELS_SCHWA, root):
        w = re.search(VOWELS_SCHWA,word)
        r = re.search(VOWELS_SCHWA, root)
        return r.span()

def starts_with_l(word):
    '''
    >>starts_with_l('l’ots')
    True
    >>starts_with_l('lots')
    True
    >>starts_with_l('tleni')
    False
    >>starts_with_l('keni')
    False
    >>starts_with_l('lheni')
    false
    '''
    if(re.match(L, word) and not re.match(CONSONANTS_NO_L, word)):
        l = re.search(L, word)
        span = l.span()
        return True
    return False
        
def has_hRes_copying(word, root):
    '''
    >>has_hRes_copying('hum’een’','meen’')
    True
    >>has_hRes_copying('hwsmul’mul’q','mel’q')
    False
    >>has_hRes_copying('heeyum’','hey’')
    False
    >>has_hRes_copying('hi’hul’ush','le’')
    True
    >>>has_hRes_copying('hunuw’nutst', 'nuw’')
    True
    '''
    if re.match(H, word) and not re.match(CONSONANTS_NO_H, word) and not re.match(H, root) and re.match(RESONANTS, root):
        h = re.match(H, word)
        return True
    return False
#print(has_hRes_copying('hi’hul’ush','le’'))

def agree_hresonant_copy(word, root):
    '''
    >>agree_hresonant_copy('hum’een’','meen’')
    mum’een’
    >>agree_hresonant_copy('hwsmul’mul’q','mel’q')
    hwsmul’mul’q
    >>agree_hresonant_copy('heeyum’','hey’')
    heeyum’
    >>>agree_hresonant_copy('hunuw’nutst', 'nuw’')
    nunuw’nutst
    '''
    
    if(has_hRes_copying(word, root)):
        h_span = re.match(H, word).span()
        r_span = re.match(CONSONANTS_NO_H, root).span()
        word_ons = word[h_span[0]:h_span[1]]
        root_ons = root[r_span[0]:r_span[1]]
        word = re.sub(word_ons, root_ons, word)
    return word


def has_l_infixation(word, root):
    '''
    >>>has_l_infixation('kwul’a’kwti’','kwaty')
    True
    >>>has_l_infixation('ts’i’ts’umiil’','ts’umiil’')
    False
    >>>has_l_infixation('le’lum’stum’' , 'lem')
    False
    >>>has_l_infixation('lul’ul’kwut','lukwa'))
    True
    '''
    num_l_word = len(re.findall(L, word))
    num_l_root = len(re.findall(L, root))
    if (num_l_word == 1 and num_l_root == 0 and not re.match(L,word)) or (num_l_word > 2 and (num_l_word-2/num_l_root == 1)):
        return True
    else:
        return False


def where_l_infixation(word, root):
    '''
    >>>where_l_infixation('kwul’a’kwti’','kwaty')
    [2, 5]
    >>>where_l_infixation('lul’ul’kwut','lukwa')
    [1,4]
    >>>where_l_infixation('ts’i’ts’umiil’','ts’umiil’')
    None
    '''
    if has_l_infixation(word, root):
        indices_all_L = [i.span() for i in re.finditer(("(ul’|ul|l’|l)"), word)]
        if indices_all_L[0][0] == 0:
            return list(indices_all_L[1])
        else:
            return list(indices_all_L[0])
    else: 
        return None
    
#print(where_l_infixation('kwul’a’kwti’','kwaty'))

def remove_l_infixation(word, root):
    '''
    removes l’ or l, and its preceding schwa if one exists 
    >>>remove_l_infixation('kwul’a’kwti’','kwaty')
    kwa’kwti’
    >>>remove_l_infixation('huli’huy’u','huye’')
    hi’huy’u
    >>>remove_l_infixation('ts’i’ts’umiil’','ts’umiil’')
    ts’i’ts’umiil’
    >>>remove_l_infixation('lul’ul’kwut','lukwa'))
    lu’l’kwut # need to deal with u metathesis or deletion
    '''
    l_infix_span = where_l_infixation(word, root)
    word = word[:l_infix_span[0]] + word[l_infix_span[1]:]
    return word


def where_red_with_l(lexeme, root):
    red_with_l = ''
    if has_l_infixation(lexeme,root):
        word = lexeme
        index_l = where_l_infixation(word, root)
        temp_word = remove_l_infixation(word,root)
        index_reduplicant = where_copy(temp_word, root)
        index_reduplicated = where_copied(temp_word,temp_word,root)
        
        if index_reduplicant[1] > index_l[1]:
            red_with_l = [0, index_reduplicant[1]+1]
        elif index_reduplicant[1] < index_l[1]:
            red_with_l = [0, index_l[1]+1]

    return red_with_l

def find_red_with_l(lexeme, root):
    if has_l_infixation(lexeme, root):
        i = where_red_with_l(lexeme, root)
        return lexeme[i[0]:i[1]]
    return None



def where_copy(lexeme, root):
    '''
    >>>where_copy('ts’uy’ts’eey’u','ts’eey’u')
    [0, 6]
    >>>where_copy('hi’huy’u','huye’')
    [0, 3]
    >>>
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

def get_copy(lexeme, root):
    '''
    >>>get_copy('tsul’tsa’luqw','tsa’luqw')
    tsul’
    >>> get_copy('lhul’lhul’q','lhul’q')
    lhul’
    >>>
    '''
    split1 = slice_string_graphemes(lexeme)
    iRed = where_copy(lexeme, root)
    l = []
    for i in range(iRed[0],iRed[1]):
        l.append(split1[i])
    
    w = join_split_graphemes(l)
    return w

#print(get_copy('kwunkwunlhnenum','kwun'))

def where_copied(lexeme:str, root:str):
    '''
    >>>where_copied('hi’huy’u','huye’')
    [3, 7]
    >>>where_copied('ts’uy’ts’eey’u','ts’eey’u')
    [6, 13]
    >>>where_copied('t’ult’ulq','t’ulq')
    [4, 8]
    >>>where_copied('m’umun’lh' , 'm’un’')
    >>>where_copied('tsul’tsa’luqw','tsa’luqw')
    [3, 5]
    '''
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
        if l1 in l2 or l2 in l1 or ((re.search(VOWELS_SCHWA,l1) and re.search(VOWELS_SCHWA,l2))) or l1 == UNUHW or l2 == UNUHW:
            #print('yes')
            if l2 in l3 or l3 in l2 or ((re.search(VOWELS_SCHWA,l2) and re.search(VOWELS_SCHWA,l3))) or l2 == UNUHW or l3 == UNUHW:
                #print('yes')
                
                l.append(j)
        elif len(l) > 0 and len(l) < len(split2):
            #print(lexeme[i])
            if lexeme[i] == '’' and l2 in [split2[i-1]]:
                ##print('yes')
                l.append(j)
        elif l1 in [split2[i+1]]:
                #print('yes')
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
    
#print(where_copied('q’epq’up’utum’','q’ep’'))

def get_copied(lexeme, root):
    '''
    >>>get_copied('lhul’lhul’q','lhul’q')
    lhul’
    >>>get_copied('hi’huy’u','huye’')
    hu
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
        return ''

#print(get_copied('q’eq’up’utum’','q’ep’'))
#print(get_copied('tsul’tsa’luqw','tsa’luqw'))


def starts_with_resonant(word):
    '''
    >>>starts_with_resonant('l’ots')
    True
    >>>starts_with_resonant('nilh')
    True
    >>>starts_with_resonant('ya’thut')
    True
    >>>starts_with_resonant('pekw’')
    False
    '''    
    if re.match(RESONANTS, word):
        print('starts_with_resonant')
        return True
    return False    

def has_weakening(word, root):
    '''
    >>>has_weakening('huy', 'hay')
    True
    >>>has_weakening('qp’apq’upthut', 'q’pu')
    False
    >>>has_weakening('q’uxq’ux', 'q’ux')
    False
    '''
    word_vowel_index = index_vowel_word(word, root)
    root_vowel_index = index_vowel_root(word, root) 
    if word[word_vowel_index[0]] == SCHWA and root[root_vowel_index[0]] != SCHWA:
        #print('has weakening')
        return True;
    return False
    

def has_strengthening(word, root):
    '''
    >>>has_strengthening('qp’apq’upthut', 'q’pu')
    True
    >>>has_strengthening('huy', 'hay')
    False
    >>>has_strengthening('q’uxq’ux', 'q’ux')
    False
    '''
    word_vowel_index = index_vowel_word(word, root)
    root_vowel_index = index_vowel_root(word, root) 
    #print(word[word_vowel_index[0]])
    #print(root[root_vowel_index[0]])
    if word[word_vowel_index[0]] != SCHWA and root[root_vowel_index[0]] == SCHWA:
        #print('has strengthening')
        return True;
    return False
                                              
            
def has_metathesis(word, root):
    '''
    >>>has_metathesis('qp’apq’upthut', 'q’pu')
    False
    >>>print(has_metathesis('huy', 'hay'))
    False
    >>>has_metathesis('q’uxq’ux', 'q’ux')
    False
    >>>has_metathesis('qtewustun','qit')
    True
    '''
    if re.search(VOWELS_SCHWA,word) and re.search(VOWELS_SCHWA, root):
        w = re.search(VOWELS_SCHWA,word)
        r = re.search(VOWELS_SCHWA, root)
        if w.span()[0] == r.span()[0]:    
            return False
        else:
            print('has metathesis')
            return True
        
def reverse_metathesis(word, root):
    '''
    >>>reverse_metathesis('qp’apq’upthut', 'q’pu')
    qp’apq’upthut
    >>>reverse_metathesis('huy', 'hay')
    huy
    >>>reverse_metathesis('q’uxq’ux', 'q’ux')
    q’uxq’ux
    >>>reverse_metathesis('qtewustun','qit')
    qetwustun
    >>>reverse_metathesis('kwakwma’tsiin’','kwam’')
    ! doesn't account for stem metathesis eg 'kwakwma’tsiin’','kwam’'
    kwakwma’tsiin’
    '''
    if has_metathesis:
        w_1 = word
        w_span = re.search(VOWELS_SCHWA,word).span()
        r_span = re.search(VOWELS_SCHWA, root).span()
        w_1 = word[0:r_span[0]] + word[w_span[0]:w_span[1]] + word[r_span[0]:w_span[0]] + word[w_span[1]:]
        return w_1
    else:
        return word


def get_vowels_copy_copied_root(copy, copied, root):
    copy_graphemes = slice_string_graphemes(copy)
    copied_graphemes = slice_string_graphemes(copied)
    root_graphemes = slice_string_graphemes(root)
    vowels = ['', '', '']
    
    try:
        for i in range(len(copy_graphemes)):
            for j in range(len(VOWELS_LIST)):  
                if copy_graphemes[i] == VOWELS_LIST[j]:
                    vowels[0] = copy_graphemes[i]
                    break
    except:
        print("error: no vowel in copy!")
    
    try:
        for i in range(len(copied_graphemes)):
            for j in range(len(VOWELS_LIST)):
                        
                if copied_graphemes[i] == VOWELS_LIST[j]:
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


def where_vowels_copy_copied_root(copy, copied, root):
    '''
    >>>where_vowels_copy_copied_root('qp’a', 'q’pu','q’pu')
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
                if copy_graphemes[i] == VOWELS_LIST[j]:
                    vowels[0] = i
                    #print(vowels[0])
                    break
                
    except:
        print("error: no vowel in copy!")
    
    try:
        for i in range(len(copied_graphemes)):
            for j in range(len(VOWELS_LIST)):
                #print(copied_graphemes[i],VOWELS_LIST[j])    
                if copied_graphemes[i] == VOWELS_LIST[j]:
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



def has_stem_ablaut(copy, copied, root):
    '''
    Check is the first vowel in the root is different from the first vowel in the lexeme. 
    Returns false if either are schwas, because they fall under weakening and strengthening
    Returns true if the vowels are both strong but different in place or length
    >>>has_ablaut('qp’apq’upthut', 'q’pu')
    True
    >>>has_stem_ablaut('huy', 'hay')
    False
    >>>has_stem_ablaut('q’ux', 'q’ux')
    False
    >>>has_stem_ablaut('kwu','kweel')
    False
    has_stem_ablaut('kwi','kweel')
    True
    has_stem_ablaut('qp’a', 'q’pu')
    False
    '''
    vowels = get_vowels_copy_copied_root(copy, copied, root)
    try:
        if vowels[1] != vowels[2]:
            return True
    except:
        print('vowels aren\'nt in all of the copy, copied, and root. check get_vowels_copy_copied_root(copy, copied, root) function') 
    return False


def has_copy_ablaut(copy, copied, root):
    vowels = get_vowels_copy_copied_root(copy, copied, root)
    #print(vowels[0]+" " + vowels[2])
    try:
        if vowels[0] != vowels[2]:
            return True
    except:
        print('vowels aren\'nt in all of the copy, copied, and root. check get_vowels_copy_copied_root(copy, copied, root) function') 
    return False


def has_copied_ablaut(copy, copied, root):
    vowels = get_vowels_copy_copied_root(copy, copied, root)
    print(vowels[1]+" " + vowels[2])
    try:
        if vowels[1] != vowels[2]:
            return True
    except:
        print('vowels aren\'nt in all of the copy, copied, and root. check get_vowels_copy_copied_root(copy, copied, root) function') 
    return False


def has_copy_strengthening(copy, copied, root):
    vowels = get_vowels_copy_copied_root(copy, copied, root)
    #print(vowels[0]+" " + vowels[2])
    try:
        if re.search(VOWELS,vowels[0]) and re.search(SCHWA, vowels[2]):
            return True
    except:
        print('vowels aren\'nt in all of the copy, copied, and root. check get_vowels_copy_copied_root(copy, copied, root) function') 
    return False

def has_copy_reduction(copy, copied, root):
    vowels = get_vowels_copy_copied_root(copy, copied, root)
    #print(vowels[0]+" " + vowels[2])
    try:
        if re.search(SCHWA,vowels[0]) and re.search(VOWELS, vowels[2]):
            return True
    except:
        print('vowels aren\'nt in all of the copy, copied, and root. check get_vowels_copy_copied_root(copy, copied, root) function') 
    return False

def has_copied_strengthening(copy, copied, root):
    vowels = get_vowels_copy_copied_root(copy, copied, root)
    #print(vowels[1]+" " + vowels[2])
    try:
        if re.search(VOWELS,vowels[1]) and re.search(SCHWA, vowels[2]):
            return True
    except:
        print('vowels aren\'nt in all of the copy, copied, and root. check get_vowels_copy_copied_root(copy, copied, root) function') 
    return False

def has_copied_reduction(copy, copied, root):
    vowels = get_vowels_copy_copied_root(copy, copied, root)
    #print(vowels[1]+" " + vowels[2])
    try:
        if re.search(SCHWA,vowels[1]) and re.search(VOWELS, vowels[2]):
            return True
    except:
        print('vowels aren\'nt in all of the copy, copied, and root. check get_vowels_copy_copied_root(copy, copied, root) function') 
    return False

#print(has_copy_reduction('qp’ap','q’pu', 'q’pu'))
def get_copy_ablaut_index_lexeme(lexeme, root):
    '''
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
     


def get_copied_ablaut_index_lexeme(lexeme, root):
    '''
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

#print(get_copied_ablaut_index_lexeme('tsul', 'tsel', 'tselush'))


def reverse_copy_ablaut(word, root):
    '''
    >>>reverse_copy_ablaut('qp’apq’upthut', 'q’pu')
    qp’upq’upthut
    >>>reverse_copy_ablaut('tseltsulush','tselush')
    False
    >>>reverse_copy_ablaut('tsultselush','tselush')
    tseltselush
    '''
    copy = get_copy(word, root)
    copied = get_copied(word, root)
    vowel_indices = where_vowels_copy_copied_root(copy, copied, root)
    print(copy + copied + root)
    if has_copy_ablaut(copy, copied ,root):
        vowel_indices = where_vowels_copy_copied_root(copy, copied, root)
        
        no_ablaut = ''
        copy_graphemes = slice_string_graphemes(get_copy(word, root))
        copied_graphemes = slice_string_graphemes(get_copied(word, root))
        word_graphemes = slice_string_graphemes(word)
        root_graphemes = slice_string_graphemes(root)
        
        vowel_indices = where_vowels_copy_copied_root(copy, copied, root)
        
        no_ablaut = join_split_graphemes(word_graphemes[0:vowel_indices[0]]) + join_split_graphemes(root_graphemes[vowel_indices[2]]) + join_split_graphemes(word_graphemes[vowel_indices[0]+1:])
        
        return no_ablaut
    else:
        return False



def reverse_copied_ablaut(word, root):
    '''
    >>>reverse_copied_ablaut('qp’apq’upthut', 'q’pu')
    qp’upq’upthut
    reverse_copied_ablaut('tsultselush','tselush')
    None
    >>>reverse_copy_ablaut('tsultselush','tselush')
    tseltselush
    >>>reverse_copy_ablaut('tseltsulush','tselush')
    False
    '''
    copy = get_copy(word, root)
    copied = get_copied(word, root)
    print(copy, copied, root)
    copy_graphemes = slice_string_graphemes(get_copy(word, root))
    copied_graphemes = slice_string_graphemes(get_copied(word, root))
    word_graphemes = slice_string_graphemes(word)
    root_graphemes = slice_string_graphemes(root)
    
    reduplicant_indices = where_copy(word, root)
    copied_indices = where_copied(word, root)
    vowel_indices = where_vowels_copy_copied_root(copy, copied, root)
    print(copied_graphemes)
    copied_new_vowel = join_split_graphemes(copied_graphemes[:vowel_indices[0]]) + join_split_graphemes(root_graphemes[vowel_indices[2]]) + join_split_graphemes(copied_graphemes[vowel_indices[1]+1:])
    print(copied_new_vowel)
    no_ablaut = join_split_graphemes(word_graphemes[:copied_indices[0]])+ copied_new_vowel + join_split_graphemes(word_graphemes[copied_indices[1]:])
    
    #print(copied_new_vowel)
    rev_ablaut = ''
    if has_copied_ablaut(copy, copied ,root):
        rev_ablaut = copied_new_vowel + join_split_graphemes(word_graphemes[reduplicant_indices[1]:])
        return rev_ablaut
    else:
        return None
    
#print(get_copy('m’umun’','m’un’'))
#print(get_copy('kwukwimluhw','kwukwimluhw','kwumluhw'))
#print(reverse_copy_ablaut('tseltsulush','tselush'))


def get_root(parse):    
    root = parse[re.search('√', parse).start()+1:]
    if re.search('=', root):
        root_end = re.search('=',root).start()
        return root[:root_end] 
    else:
        return root

def where_stripped_in_lexeme(lexeme, stripped):
    i = list(re.search(stripped, lexeme).span())
    return(i)
    
def wrap_stripped(lexeme, stripped, parse):
    wrapped =''
    prefixes = parser.get_prefixes(parse)
    suffixes = parser.get_suffixes(parse)
    
    for i in prefixes:
        wrapped +=i
    wrapped += stripped
    for i in suffixes:
        wrapped += suffixes
        
    return wrapped

def where_in_wrapped(lexeme, parse, indices):
    iStripped = indices_stripped(lexeme, parse)  
    try:
        iStart = indices[0]+iStripped[0]
        iEnd = indices[1] + iStripped[0]
        return [iStart,iEnd]
    except:
        return [0,0]

def span_prefix_graphemes(lexeme, word_parse):
    '''
    >>>span_prefix_graphemes('hwkwunkwunlhnenum', 'hw=√kwun=lhnen=m=PL')
    [0, 1]
    '''
    
    prefixes = parser.get_prefixes(word_parse)
    root = get_root(word_parse)
    try:
        iPref = lexeme.find(prefixes[len(prefixes)-1])
        stripped_graphemes = slice_string_graphemes(lexeme[:iPref+1])    
    
        return [0,len(stripped_graphemes)]
    except:
        return [0, 0]

def span_suffix_graphemes(lexeme, word_parse):
    suffixes = parser.get_suffixes(word_parse)
    root = get_root(word_parse)
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
        
    
def indices_stripped(lexeme, parse):
    '''
    >>>indices_stripped('hwkwunkwunlhnenum', 'hw=√kwun=lhnen=m=PL')
    [1, 7]
    '''
    indices_prefix = span_prefix_graphemes(lexeme, parse)
    indices_suffix = span_suffix_graphemes(lexeme, parse)
    return [indices_prefix[1],indices_suffix[0]]
    

