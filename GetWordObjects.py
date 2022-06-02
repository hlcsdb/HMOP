'''
ExportObjects
Chloe Farr
April 20, 2022
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

def bold(input_string):
    return ''.join(['\033[1m', input_string, '\033[0m'])

def get_word_object(lex_parse):
    lexeme = lex_parse[0]
    parse = lex_parse[1]
    root = regCheck.get_root(parse)
    #print(root)
    stripped_lexeme = lexemeInfo.strip_lexeme_affixes(lexeme, parse)
    grammatical_categories = parser.get_clean_grammatical_categories(parse)
    
    #temporary strings----
    without_l = stripped_lexeme
    without_h = stripped_lexeme
    rev_copy_ablaut = stripped_lexeme
    rev_copied_ablaut = stripped_lexeme
    copy_and_copied_red_ablaut = stripped_lexeme
    rev_ablaut_with_h = stripped_lexeme
    
    #print outs----
    print('\n\nThe lexeme is: \'' + bold(lexeme)+ '\' and its root is: \''+ bold(root) + '\'')
    print('The lemexe holds grammatical meaning of: ' + bold(str(grammatical_categories))+ '.')
    if len(stripped_lexeme) != len(lexeme):
        print('Without affixes, the lexeme would appear to be: \''+bold(stripped_lexeme) + '\'. The following information will exclude affixes.')
    
    print('\nL-INFIXATION----')
    if regCheck.has_l_infixation(regCheck.agree_hresonant_copy(stripped_lexeme, root),root):
        without_l = regCheck.remove_l_infixation(regCheck.agree_hresonant_copy(stripped_lexeme, root),root)
        print(without_l)
        without_h = without_l
        rev_copy_ablaut = without_l
        rev_copied_ablaut = without_l
        print('There is l-infixation in this lexeme. The l-infix exists at indices: ' + bold(str(regCheck.where_l_infixation(stripped_lexeme, root))))
        print('Without the infix, the word appears to be: \'' + bold(without_l) + '\'')
    else: 
        print('There appears to be no l-infixation in this lexeme.')

    print('\nREDUPLICATION----')
    if regCheck.has_hRes_copying(without_h, root):
        without_h = regCheck.agree_hresonant_copy(without_l, root)   
        
    if not regCheck.has_copy(without_h, root):
        print('There appears to be no reduplication in this lexeme.')
    else:
        print('The lexeme has reduplication. Here is the information about the reduplication:')
        rev_copy_ablaut = without_h
        rev_copied_ablaut = without_h
        if regCheck.has_hRes_copying(stripped_lexeme, root):
            print('\tThere is reduplication with resonant apiration in this lexeme. The copy with resonant aspiration appears to be: \'' + bold(regCheck.get_hresonant_copy(lexeme, regCheck.get_copy(without_h, root))) + '\'.')
            print('\tWith the resonant aspiration, the copied lexeme would appear to be : \'' + bold(regCheck.get_hresonant_copy(stripped_lexeme,regCheck.get_copy(without_h, root)) + without_h) + '\n\tWithout the resonant aspiration, the underlying lexeme would appear to be : \'' + bold(without_h) + '\'.') 
            print('\n\tBecause this lexeme has reduplication with resonant apiration, we\'ll temporarily replace that with the resonant from the lexeme to look further into the reduplication.')
        if regCheck.has_l_infixation(without_h, root):
            print('\tBecause this lexeme has l-infixation, we\'ll temporarily remove that from the lexeme to look at reduplication. \n\t\tWithout the l-infix, the surface form would appear to be: \'' + bold(without_l) + '\'.')
        
        copy = regCheck.get_copy(without_h, root)
        copied = regCheck.get_copied(without_h, root)
        print('\tThe underlying reduplicant segment of \'' + lexeme + '\' is: \'' + bold(copy) + '\'. It exists at indices: ' + bold(str(regCheck.where_copy(without_h, root))))
        print('\tThe reduplicated segment of \'' + lexeme + '\' is: \'' + bold(copied) + '\'. It exists at indices: ' + bold(str(regCheck.where_copied(without_h, root))))
        
        if regCheck.has_copy_ablaut(copy, copied, root) or regCheck.has_copied_ablaut(copy, copied, root):
            print('\n\tABLAUT----')
        if regCheck.has_copy_ablaut(copy, copied, root):
            copy_ablaut_index = str(regCheck.get_copy_ablaut_index_lexeme(without_h, root)[2])
            if regCheck.has_copy_reduction(copy, copied, root):
                print('\tThe reduplicant segment of ' + lexeme + ' has vowel reduction. The reduced vowel exists at indices: ' + bold(copy_ablaut_index))
            elif regCheck.has_copy_strengthening(copy, copied, root):
                print('\tThe reduplicant segment of ' + lexeme + ' has vowel reduction. The reduced vowel exists at indices: ' + bold(copy_ablaut_index))
            elif regCheck.has_copy_ablaut(copy, copied, root):
                print('\tThe reduplicant segment of ' + lexeme + ' has vowel reduction. The reduced vowel exists at indices: ' + bold(copy_ablaut_index))           
            rev_copy_ablaut = regCheck.reverse_copy_ablaut(without_h, root)
            print('\tThe lexeme underlying the copy segment ablaut appears to be: \'' + bold(rev_copy_ablaut) + '\'')
            if regCheck.has_hRes_copying(stripped_lexeme, root):
                rev_ablaut_with_h = regCheck.get_hresonant_copy(stripped_lexeme, rev_copy_ablaut)        
                print('\tThe lexeme underlying the reduplicant with h-aspiration in place appears to be: \'' + bold(rev_ablaut_with_h)  + '\'')
            
        if regCheck.has_copied_ablaut(copy, copied, root):
            copied_ablaut_index = str(regCheck.get_copied_ablaut_index_lexeme(rev_copy_ablaut, root)[2])
            if regCheck.has_copied_reduction(copy, copied, root):
                print('\tThe reduplicated segment of ' + lexeme + ' has vowel reduction. The reduced vowel exists at indices: ' + bold(copied_ablaut_index))
            elif regCheck.has_copied_strengthening(copy, copied, root):
                print('\tThe reduplicated segment of ' + lexeme + ' has vowel reduction. The reduced vowel exists at indices: ' + bold(copied_ablaut_index))
            elif regCheck.has_copied_ablaut(copy, copied, root):
                print('\tThe reduplicated segment of ' + lexeme + ' has vowel reduction. The reduced vowel exists at indices: ' + bold(copied_ablaut_index))  
            #print(rev_copy_ablaut + ' ' + root)
            rev_copied_ablaut = regCheck.reverse_copied_ablaut(without_h, root)
            print('\tThe lexeme underlying the base\'s reduplicated segment ablaut appears to be: \'' + bold(rev_copied_ablaut) + '\'')  
            if regCheck.has_hRes_copying(stripped_lexeme, root):
                rev_ablaut_with_h = regCheck.get_hresonant_copy(stripped_lexeme,rev_copied_ablaut)
                print('\tThe lexeme underlying the base\'s reduplicated segment with h-aspiration in place appears to be: \'' + bold(rev_ablaut_with_h)  + '\'')
        
        if regCheck.has_copy_ablaut(copy, copied, root) and regCheck.has_copied_ablaut(copy, copied, root):
            copy_and_copied_red_ablaut = regCheck.reverse_copied_ablaut(rev_copy_ablaut, root)
            print('\tThe lexeme underlying both ablaut appears to be: \'' + bold(copy_and_copied_red_ablaut) + '\'')
            if regCheck.has_hRes_copying(stripped_lexeme, root):
                rev_ablaut_with_h = regCheck.get_hresonant_copy(stripped_lexeme,copy_and_copied_red_ablaut)
                print('\tThe lexeme underlying both ablaut with h-aspiration in place appears to be: \'' + bold(rev_ablaut_with_h)  + '\'')  
        
        print('The underlying form of the lexeme \'' + lexeme + '\' is: \'' + bold(regCheck.wrap_stripped(lexeme, rev_copied_ablaut, parse)) + '\'')
        

def get_underlying(lex_parse):
    lexeme = lex_parse[0]
    parse = lex_parse[1]
    root = regCheck.get_root(parse)
    #print(root)
    stripped_lexeme = lexemeInfo.strip_lexeme_affixes(lexeme, parse)
    grammatical_categories = parser.get_clean_grammatical_categories(parse)
    
    #temporary strings----
    without_l = stripped_lexeme
    without_h = stripped_lexeme
    rev_copy_ablaut = stripped_lexeme
    rev_copied_ablaut = stripped_lexeme
    copy_and_copied_red_ablaut = stripped_lexeme
    rev_ablaut_with_h = stripped_lexeme
        
    if regCheck.has_l_infixation(regCheck.agree_hresonant_copy(stripped_lexeme, root),root):
        without_l = regCheck.remove_l_infixation(regCheck.agree_hresonant_copy(stripped_lexeme, root),root)

        without_h = without_l
        rev_copy_ablaut = without_l
        rev_copied_ablaut = without_l


    if regCheck.has_hRes_copying(without_h, root):
        without_h = regCheck.agree_hresonant_copy(without_l, root)   
        
    if regCheck.has_copy(without_h, root):
        rev_copy_ablaut = without_h
        rev_copied_ablaut = without_h
         
        copy = regCheck.get_copy(without_h, root)
        copied = regCheck.get_copied(without_h, root)
        

        if regCheck.has_copy_ablaut(copy, copied, root):
            copy_ablaut_index = str(regCheck.get_copy_ablaut_index_lexeme(without_h, root)[2])
        
            rev_copy_ablaut = regCheck.reverse_copy_ablaut(without_h, root)

            if regCheck.has_hRes_copying(stripped_lexeme, root):
                rev_ablaut_with_h = regCheck.get_hresonant_copy(stripped_lexeme, rev_copy_ablaut)        
                
            
        if regCheck.has_copied_ablaut(copy, copied, root):
            copied_ablaut_index = str(regCheck.get_copied_ablaut_index_lexeme(rev_copy_ablaut, root)[2])
            
            rev_copied_ablaut = regCheck.reverse_copied_ablaut(without_h, root)

            if regCheck.has_hRes_copying(stripped_lexeme, root):
                rev_ablaut_with_h = regCheck.get_hresonant_copy(stripped_lexeme,rev_copied_ablaut)
                
        
        if regCheck.has_copy_ablaut(copy, copied, root) and regCheck.has_copied_ablaut(copy, copied, root):
            copy_and_copied_red_ablaut = regCheck.reverse_copied_ablaut(rev_copy_ablaut, root)

            if regCheck.has_hRes_copying(stripped_lexeme, root):
                rev_ablaut_with_h = regCheck.get_hresonant_copy(stripped_lexeme,copy_and_copied_red_ablaut)
                
    underlying = regCheck.wrap_stripped(lexeme, rev_copied_ablaut, parse)
    return underlying
        
#print(get_underlying(['tsul’tsa’luqw','√tsa’luqw=PL']))
    
#get_word_object(['tsul’tsa’luqw','√tsa’luqw=PL'])  
#get_word_object(['hwkwunkwunlhnenum','hw=√kwun=lhnen=m=PL'])
#get_word_object(['hulelum’', '√lem’=RDP=PL'])

#get_word_object(['tsuli’tsetl’um’','√tstl’um=DIM=PL=PROG']) # can't use this because there's an inserted vowel in the base... messes everything up basically, and for some reson the l-infix isn't working




#def get_word_objects(word_parse):
    #print('<Word>')
    #lexeme = word_parse[0]
    #parse = word_parse[1]
    #print('<lexeme>' + lexeme + '</lexeme>')
    #print('<lexemeGramphemeList>' +  str(regCheck.slice_string_graphemes(lexeme)) + '</lexemeGramphemeList>')
    #print('<parse>' + parse + '</parse>')
    
    #root = regCheck.get_root(parse)
    #print('<root>' + root + '</root>')
    #print('<rootGramphemeList>' +  str(regCheck.slice_string_graphemes(root)) + '</rootGramphemeList>')
    
    #stripped_lexeme = lexemeInfo.strip_lexeme_affixes(lexeme, parse)
    #temp_stripped = stripped_lexeme
    #print('<strippedLexeme>' + stripped_lexeme + '</strippedLexeme>')
    #print('<strippedGraphemeList>' + str(regCheck.slice_string_graphemes(stripped_lexeme)) + '</strippedGraphemeList>')
    #print('<iStripped>' + str(regCheck.indices_stripped(lexeme,parse)) + '</iStripped>')
    #grammatical_categories = parser.get_clean_grammatical_categories(parse)
    #print('<grammaticalCategories>' + str(grammatical_categories) + '</grammaticalCategories>')
    #temp_stripped_lexeme = stripped_lexeme
    ###----------
    
    #if regCheck.has_hRes_copying(stripped_lexeme, root) and regCheck.has_copy(lexeme, root):
        #temp_stripped_lexeme = regCheck.agree_hresonant_copy(stripped_lexeme, root)
        #h_surface_reduplicant = regCheck.get_copy(temp_stripped_lexeme, root)
        #h_surface_reduplicant = stripped_lexeme[0] + h_surface_reduplicant[1:]
    #try:
        #print('<noHCopying>' + temp_stripped_lexeme + '</noHCopying>')
        #print('<reduplicantH>' + h_surface_reduplicant + '</reduplicantH>')   
    #except:
        #print('<noHCopying></noHCopying>')
        #print('<reduplicantNoH></reduplicantNoH>')          
        
    #if regCheck.has_l_infixation(temp_stripped_lexeme, root):
        #temp_word = regCheck.remove_l_infixation(temp_stripped_lexeme,root)
        #temp_stripped_lexeme = temp_word
        #reduplicant_with_l = regCheck.find_red_with_l(temp_stripped_lexeme, root)
        #i_l_infix = regCheck.where_l_infixation(temp_stripped_lexeme, root)
    #try:
        #print('<noLInfix>' + regCheck.wrap_stripped(lexeme, stripped_lexeme) + '</noLInfix>')
        #print('<reduplicantNoL>' + reduplicant_no_l + '</reduplicantNoL>')
        #print('<reduplicantL>' + reduplicant_with_l + '</reduplicantL>')  
        #print('<iLInfix>' + i_l_infix + '</iLInfix>')
        
        
    #except:
        #print('<noLInfix></noLInfix>')
        #print('<reduplicantNoL></reduplicantNoL>')
        #print('<reduplicantL></reduplicantL>')  
        #print('<iLInfix></iLInfix>')        
    
    #try:
        #if has_copy(temp_stripped_lexeme, root):
            #underlying_reduplicant = regCheck.get_copy(stripped_No_H, root)
            #iURed = regCheck.where_copy(stripped_No_H,root)
            #iRed_wrapped = regCheck.where_in_wrapped(lexeme, parse, iURed)
             
            #print('<underlyingReduplicant>' + underlying_reduplicant + '</underlyingReduplicant>')
            #print('<iReduplicant>' + str(iURed) + '</iReduplicant>' )
            #print('<iRedWrapped>' + str(iRed_wrapped) + '</iRedWrapped>')   

            #copied = regCheck.get_copied(stripped_No_H, root)
            #print('<copied>' + copied + '</copied>')
            #iCopied = regCheck.where_copied(stripped_No_H, root)
            #print('<iCopied>' + str(iCopied) + '</iCopied>')
            #iCopied_wrapped = regCheck.where_in_wrapped(lexeme, parse, iCopied)
            #print('<iCopiedWrapped>' + str(iCopied_wrapped) + '</iCopiedWrapped>')
        
    #except:
        #underlying_reduplicant = regCheck.get_copy(stripped_lexeme, root)
        #iURed = regCheck.where_copy(stripped_lexeme,root)
        #iRed_wrapped = regCheck.where_in_wrapped(lexeme, parse, iURed)
         
        #print('<underlyingReduplicant>' + underlying_reduplicant + '</underlyingReduplicant>')
        #print('<iReduplicant>' + str(iURed) + '</iReduplicant>')
        #print('<iRedWrapped>' + str(iRed_wrapped) + '</iRedWrapped>')   
        
        #copied = regCheck.get_copied(stripped_lexeme, root)
        #print('<copied>' + copied + '</copied>')
        #iCopied = regCheck.where_copied(stripped_lexeme, root)
        #print('<iCopied>' + str(iCopied) + '</iCopied>')
        #iCopied_wrapped = regCheck.where_in_wrapped(lexeme, parse, iCopied)
        #print('<iCopiedWrapped>' + str(iCopied_wrapped) + '</iCopiedWrapped>')
        
    #if has_copy(stripped_lexeme, root)
        
    #print('</Word>')
    

#word_parse = [['tsul’tsa’luqw','√tsa’luqw=PL'],['tsultselush','√tselush=PL'],['kwukwimluhw','√kwumluhw=PL'],['ts’uy’ts’eey’u','√ts’eey’u=PL'],['hwkwunkwunlhnenum','hw=√kwun=lhnen=m=PL'],['huliqwu','√luqwa=PL'],['slhunlheni’','s=√lheni’=PL'],['hulixwtun','√luxw=ten=PL'],['slhunlheni’','s=√lheni’=PL'],['lhul’lhul’q','√lhul’q=PL']]


#for i in word_parse:
    #get_word_objects(i)