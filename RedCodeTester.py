'''
TESTFILE
Chloe Farr
April 15, 2022
For LING590 / HLCS
'''
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import ManageParse as parser
import LexemeInfo as lexemeInfo
import CheckForRegex as regCheck
import MorphologicalProcesses as morphoProcess
import re

def Main_Tester():
    #test_index_vowel_word()
    #test_index_vowel_root()
    #test_starts_with_l()
    #test_has_hRes_copying()
    #test_agree_hresonant_copy()
    #test_contains_l_mid()    
    #test_remove_l_infixation()
    #test_starts_with_resonant()
    #test_has_weakening()
    #test_has_strengthening()
    #test_has_metathesis()
    #test_reverse_metathesis()
    #test_has_ablaut()
    #test_reverse_ablaut()
         # this function doesn't work yet
    #test_reverse_stem_ablaut() 
    #test_get_to_underlying()
    #try_slice_string_graphemes()
    #test_get_root()
    #test_find_reduplicant() #need to redo in regex
    print()
    
def test_index_vowel_word():
    i1 = regCheck.index_vowel_word('kwi’kwetst','kwtsu')
    r1 = (2, 3)
    i2 = regCheck.index_vowel_word('huy', 'hay')
    r2 = (1, 2)
    i3 = regCheck.index_vowel_word('hee’wi’wuqus', 'wiq')
    r3 = None
    i4 = regCheck.index_vowel_word('qp’apq’upthut', 'q’pu')
    r4 = (3, 4)
    
    print(i1 == r1)
    print(i2 == r2)
    print(i3 != r3)
    print(i4 == r4)
    
def test_index_vowel_root():
    i1 = regCheck.index_vowel_root('kwi’kwetst','kwtsu')
    r1 = [3, 4]
    i2 = regCheck.index_vowel_root('huy', 'hay')
    r2 = [1, 2]
    i3 = regCheck.index_vowel_root('hee’wi’wuqus', 'wiq')
    r3 = [1, 3]
    i4 = regCheck.index_vowel_root('qp’apq’upthut', 'q’pu')
    r4 = [3, 4]
    
    print(i1 == r1)
    print(i2 == r2)
    print(i3 == r3)
    print(i4 == r4)

def test_starts_with_l():
    i1 = regCheck.starts_with_l('l’ots')
    r1 = True
    i2 = regCheck.starts_with_l('lots')
    r2 = True
    i3 = regCheck.starts_with_l('tleni')
    r3 = False
    i4 = regCheck.starts_with_l('keni')
    r4 = False
    i5 = regCheck.starts_with_l('lheni')
    r5 = False    
    
    print(i1 == r1)
    print(i2 == r2)
    print(i3 == r3)
    print(i4 == r4)
    print(i5 == r5)
    
def test_has_hRes_copying():
    i1 = regCheck.has_hRes_copying('hum’een’','meen’')
    r1 = True
    i2 = regCheck.has_hRes_copying('hwsmul’mul’q','mel’q')
    r2 = True
    i3 = regCheck.has_hRes_copying('heeyum’','hey’')
    r3 = False
    i4 = has_hRes_copying('hi’hul’ush','le’')
    r4 = True
    i5 = regCheck.agree_hresonant_copy('hunuw’nutst', 'nuw’')
    r5 = 'nunuw’nutst'
    
    print(i1 == r1)
    print(i2 == r2)
    print(i3 == r3)
    print(i4 == r4)
    print(i5 == r5)
    
def test_agree_hresonant_copy():
    i1 = regCheck.agree_hresonant_copy('hum’een’','meen’')
    r1 = 'mum’een’'
    i2 = regCheck.agree_hresonant_copy('hwsmul’mul’q','mel’q')
    r2 = 'mwsmul’mul’q'
    i3 = regCheck.agree_hresonant_copy('heeyum’','hey’')
    r3 = 'heeyum’'

    print(i1 == r1)
    print(i2 == r2)
    print(i3 == r3)
    
def test_contains_l_mid():
    i1 = regCheck.contains_l_mid('me’luxulh')
    r1 = True
    i2 = regCheck.contains_l_mid('nelu’')
    r2 = True
    i3 = regCheck.contains_l_mid('mulhistimuhw')
    r3 = False
    i4 = regCheck.contains_l_mid('l’ots')
    r4 = False
    i5 = regCheck.contains_l_mid('nilh')
    r5 = False    
    
    print(i1 == r1)
    print(i2 == r2)
    print(i3 == r3)
    print(i4 == r4)
    print(i5 == r5)    
    

#check l infixation

def test_remove_l_infixation():
    i1 = regCheck.remove_l_infixation('kwul’a’kwti’','kwaty')
    r1 = 'kwa’kwti’'
    i2 = regCheck.remove_l_infixation('huli’huy’u','huye’')
    r2 = 'huhuy’u'

    print(i1 == r1)
    print(i2 == r2)
    
    
def test_starts_with_resonant():
    i1 = regCheck.starts_with_resonant('l’ots')
    r1 = True
    i2 = regCheck.starts_with_resonant('nilh')
    r2 = True
    i3 = regCheck.starts_with_resonant('ya’thut')
    r3 = True
    i4 = regCheck.starts_with_resonant('pekw’')
    r4 = False
    
    print(i1 == r1)
    print(i2 == r2)
    print(i3 == r3)
    print(i4 == r4)    
    
def test_has_weakening():
    i1 = regCheck.has_weakening('huy', 'hay')
    r1 = True
    i2 = regCheck.has_weakening('qp’apq’upthut', 'q’pu')
    r2 = False
    i3 = regCheck.has_weakening('q’uxq’ux', 'q’ux')
    r3 = False  
    
    print(i1 == r1)
    print(i2 == r2)
    print(i3 == r3)

def test_has_strengthening():
    i1 = regCheck.has_strengthening('qp’apq’upthut', 'q’pu')
    r1 = True
    i2 = regCheck.has_strengthening('huy', 'hay')
    r2 = False
    i3 = regCheck.has_strengthening('q’uxq’ux', 'q’ux')
    r3 = False
    
    print(i1 == r1)
    print(i2 == r2)
    print(i3 == r3)
    
    
def test_has_metathesis():
    i1 = regCheck.has_metathesis('qp’apq’upthut', 'q’pu')
    r1 = False
    i2 = regCheck.has_metathesis('huy', 'hay')
    r2 = False
    i3 = regCheck.has_metathesis('q’uxq’ux', 'q’ux')
    r3 = False
    i4 = regCheck.has_metathesis('qtewustun','qit')
    r4 = True
    
    print(i1 == r1)
    print(i2 == r2)
    print(i3 == r3) 
    print(i4 == r4) 
    
    
def test_reverse_metathesis():
    i1 = regCheck.reverse_metathesis('qp’apq’upthut', 'q’pu')
    r1 = 'qp’apq’upthut'
    i2 = regCheck.reverse_metathesis('huy', 'hay')
    r2 = 'huy'
    i3 = regCheck.reverse_metathesis('q’uxq’ux', 'q’ux')
    r3 = 'q’uxq’ux'
    i4 = regCheck.reverse_metathesis('qtewustun','qit')
    r4 = 'qetwustun'
    i5 = regCheck.reverse_metathesis('kwakwma’tsiin’','kwam’')
    r5 = 'kwakwma’tsiin’'   
    
    print(i1 == r1)
    print(i2 == r2)
    print(i3 == r3) 
    print(i4 == r4) 
    print(i5 == r5)
    
def test_has_ablaut():
    i1 = regCheck.has_ablaut('qp’apq’upthut', 'q’pu')
    r1 = False
    i2 = regCheck.has_ablaut('huy', 'hay')
    r2 = False
    i3 = regCheck.has_ablaut('q’uxq’ux', 'q’ux')
    r3 =  False
    i4 = regCheck.has_ablaut('kwukweel’','kweel')
    r4 = False
    i5 = regCheck.has_ablaut('kwikweel’','kweel')
    r5 = True
    
    print(i1 == r1)
    print(i2 == r2)
    print(i3 == r3) 
    print(i4 == r4) 
    print(i5 == r5)    
    
def test_reverse_ablaut():
    i1 = regCheck.reverse_ablaut('qp’apq’upthut', 'q’pu')
    r1 = 'qp’upq’upthut'
    i2 = regCheck.reverse_ablaut('huy', 'hay')
    r2 = 'hay'
    i3 = regCheck.reverse_ablaut('q’uxq’ux', 'q’ux')
    r3 = 'q’uxq’ux'
    i4 = regCheck.reverse_ablaut('qtewustun','qit')
    r4 = 'qtiwustun'   
    
    print(i1 == r1)
    print(i2 == r2)
    print(i3 == r3) 
    print(i4 == r4)    
    
# this function doesn't work yet
def test_reverse_stem_ablaut():
    i1 = regCheck.reverse_ablaut('kwi’kwetst','kwtsu')
    r1 = 'kwi’kwutst'
    i2 = regCheck.reverse_ablaut('kwul’a’kwti’','kwaty')
    r2 = 'kwul’a’kwti’' #??
    i3 = regCheck.reverse_ablaut('huli’huy’u','huye’')
    r3 = 'huli’huy’u'
    i4 = regCheck.reverse_ablaut('hiil’e’lum’', 'lem')
    r4 = 'hiil’e’lem’'
    
    print(i1 == r1)
    print(i2 == r2)
    print(i3 == r3) 
    print(i4 == r4)      
    
    
def test_get_to_underlying():
    i1 = regCheck.get_to_underlying('hi’huy’u','huye’')
    r1 = 'hu’huy’u'
    i2 = regCheck.get_to_underlying('heeyum’','hey’')
    r2 = 'heyum’'
    i4 = regCheck.get_to_underlying('kwukwa’qut','kwa’') #hw- actually a prefix so it wouldn't pass through any of these
    r4 = 'kwakwa’qut'
    i5 = regCheck.get_to_underlying('kwi’kwetst','kwtsu')
    r5 = 'kwu’i’kwetst'# !!this is wrong need to copy from the stem not the root... metathesis happend in stem not in copy
    i6 = regCheck.get_to_underlying('huli’huy’u','huye’')
    r6 = 'hi’huy’u' # not sure this is actually what the output is supposed to be
    i7 = regCheck.get_to_underlying('kwul’a’kwti’','kwaty')
    r7 = 'kwa’kwti’'   
    
    print(i1 == r1)
    print(i2 == r2)
    print(i3 == r3) 
    print(i4 == r4)   
    print(i5 == r5)
    print(i6 == r6)
    print(i7 == r7) 
    
def try_slice_string_graphemes():
    
    i1 = regCheck.slice_string_graphemes('ts’i’ts’umiil’')
    r1 = ['ts’', 'i', '’', 'ts’', 'u', 'm', 'ii', 'l’']
    i2 = regCheck.slice_string_graphemes('ts’uli’ts’umiil’')
    r2 = ['ts’', 'u', 'l', 'i', '’', 'ts’', 'u', 'm', 'ii', 'l’']
    print(i1 == r1)
    print(i2 == r2)    
      
    
def test_get_root():
    i1 = regCheck.get_root('shhw=√ne’=m=PL')
    r1 = 'ne’'
    i2 = regCheck.get_root('hw=√kwun=lhnen=t')
    r2 = 'kwun'
    print(i1 == r1)
    print(i2 == r2)    
    
Main_Tester() 