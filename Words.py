import LocateDictWord as parse_dict
import ManageParse as parse_manager
import CheckForRegex as mopho_checks
import LexemeInfo as stripLex
import GetWordObjects as processed
import sys

class Words:
    #import LocateDictWord as parse_dict
    
    def __init__(self, w):
        self.word = w.replace('\'', '’').lstrip().rstrip()
        self.set_basics()
    
    def set_dict_row(self):
        temp_word = ' ' + self.word
        self.dict_row = parse_dict.find_row(temp_word)
    
    def get_word(self):
        return self.word
    
    def set_id(self):
        self.id = self.dict_row[0]
        
    def get_id(self):
        return self.id
    
    def set_parse(self):
        #get parse from csv
        self.parse = self.dict_row[4]
        
    def get_parse(self):
        return self.parse
    
    def set_root(self):
        temp_root = self.dict_row[3][1:]
        self.root = temp_root
        
    def get_root(self):
        return self.root
    
    def set_lex_graphemes(self):
        self.lex_graphemes = mopho_checks.slice_string_graphemes(self.word)
    
    def get_lex_graphemes(self):
        return self.lex_graphemes 
    
    def set_root_graphemes(self):
        self.root_graphemes = mopho_checks.slice_string_graphemes(self.root)
    
    def get_root_graphemes(self):
        return self.root_graphemes 
        
    def set_def(self):
        self.definition = self.dict_row[5]
    
    def get_def(self):
        return self.definition
    
    def set_underlying(self):
        self.underlying = processed.get_underlying([self.word, self.parse])
        
    def get_underlying(self):
        return self.underlying
    
    def set_grammatical_categories(self):
        self.grammatical_categories = parse_manager.get_clean_grammatical_categories(self.parse)
        self.parse_no_categories = parse_manager.strip_grammatical_categories_from_parse(self.parse)
    
    def get_grammatical_categories(self):
        return self.grammatical_categories 
    
    #def set_parse_no_categories(self):
        #self.parse_no_categories = parse_manager.strip_grammatical_categories_from_parse(self.parse)

    def get_parse_no_categories(self):
        return self.parse_no_categories
    
    def set_affixes(self):
        self.prefix_list = parse_manager.get_prefixes(self.parse_no_categories)
        self.suffix_list = parse_manager.get_suffixes(self.parse_no_categories)
        
    #def set_prefix_list(self):
        #self.prefix_list = parse_manager.get_prefixes(self.parse_no_categories)
        
    def get_prefix_list(self):
        return self.prefix_list
    
    #def set_suffix_list(self):
        #self.suffix_list = parse_manager.get_suffixes(self.parse_no_categories)
    
    def get_suffix_list(self):
        return self.suffix_list
    
    def set_stripped_lexeme(self):
        self.stripped = stripLex.strip_lexeme_affixes(self.word, self.parse)
    
    def get_stripped_lexeme(self):
        return self.stripped
    
    def set_stripped_lexeme_graphemes(self):
        self.stripped_lexeme_graphemes = mopho_checks.slice_string_graphemes(self.stripped)
    
    def get_stripped_lexeme_graphemes(self):
        return self.stripped_lexeme_graphemes 
    
    def set_wrapper(self):
        a = self.word[0:self.word.find(self.root)]
        b = self.word[len(a)+len(self.stripped):]
        self.wrapper = [a,b]
    
    def wrap(self, to_insert):
        return self.wrapper[0] + to_insert + self.wrapper[1]
    
    def set_underlying_affixes(self):
        self.underlying_affixes = self.wrap(mopho_checks.join_split_graphemes(parse_manager.reverse_affix_vowel_change(self)))
    
    def get_underlying_affixes(self):
        return self.underlying_affixes
    
    def set_linf(self):
        if mopho_checks.has_l_infixation(self.stripped, self.root):
            self.linfixing = mopho_checks.has_l_infixation(self.stripped, self.root)
            self.i_linfix = mopho_checks.where_l_infixation(self.stripped, self.root)
            self.no_linf = mopho_checks.remove_l_infixation(self.stripped, self.root)
        else: 
            self.linfixing = None
            self.i_linfix = []
            self.no_linf = None
            
    def get_has_linf(self):
        return self.linfixing
    
    def get_i_linf(self):
        return self.i_linfix      
                        
    def set_copy(self):
        temp_stripped = self.stripped
        
        if True == (self.copying and self.linfixing):
            self.i_l_red = mopho_checks.where_red_with_l(self.stripped, self.root)
            temp_stripped = self.no_linf
            
            if mopho_checks.has_copy(temp_stripped, self.root):
                self.copying = True
                self.copy = mopho_checks.get_copy(temp_stripped, self.root)
                self.hcopy = None
                self.i_copy = mopho_checks.where_copy(temp_stripped, self.root)
                
            elif mopho_checks.has_hRes_copying(temp_stripped, self.root):
                self.copying = True
                agree_h_copying = mopho_checks.agree_hresonant_copy(temp_stripped, self.root)
                self.copy = mopho_checks.get_copy(agree_h_copying, self.root)
                self.hcopy = mopho_checks.get_hresonant_copy(temp_stripped, self.root)
                self.i_copy = mopho_checks.where_copy(agree_h_copying, self.root)
        
            else:
                self.copying = False
                self.copy = None
                self.hcopy = None
                self.i_copy = []
        else:
            self.i_l_red = []
    
            
    def set_copied(self):
        if self.linfixing:
            temp_stripped = self.no_linf        
            if mopho_checks.has_copy(temp_stripped, self.root) or mopho_checks.has_hRes_copying(temp_stripped, self.root):
                temp_stripped = self.word
                if mopho_checks.has_hRes_copying(temp_stripped, self.root):
                    temp_stripped = mopho_checks.agree_hresonant_copy(temp_stripped, self.root)
                    
                self.copied = mopho_checks.get_copied(temp_stripped, self.root)
                self.i_copied = mopho_checks.where_copied(temp_stripped, self.root)
            
        else:
            self.copied = None
            self.i_copied = []            
            
    def set_reduplication(self):
        if mopho_checks.has_copy(self.stripped, self.root) or mopho_checks.has_hRes_copying(self.stripped, self.root):
            self.copying = True
            self.set_copy()
            self.set_copied()
        else:
            self.copying = False
            self.copy = None
            self.hcopy = None
            self.i_copy = []
            self.copied = None
            self.i_copied = []   
            self.i_l_red = []
            
            
    def get_copied(self):
        return self.copied
    
    def get_has_copy(self):
        return self.copying
    
    def get_copy(self):
        return self.copy
    
    def get_has_hcopying(self):
        return self.has_hcopy    
    
    def get_hcopy(self):
        return self.hcopy
    
    def get_i_copy(self):
        return self.i_copy    
    
    #def set_copy_indices(self):
        #self.i_copy = mopho_checks.where_copy(self.stripped, self.root)
        
    #def get_copy_indices(self):
        #return self.i_copy
    
    #def set_copied_indices(self):
        #self.i_copied = mopho_checks.where_copied(self.stripped, self.root)
    
    def get_copied_indices(self):
        return self.i_copied
    
    def set_basics(self):
        self.set_dict_row()
        self.set_id()
        self.set_parse()
        self.set_root()
        self.set_lex_graphemes()
        self.set_root_graphemes()
        self.set_def()
        self.set_underlying()
        self.set_stripped_lexeme()
        self.set_wrapper()
        self.set_stripped_lexeme_graphemes()
        
        self.set_grammatical_categories()
        #self.set_parse_no_categories()
        self.set_affixes()
        self.set_underlying_affixes()
        self.set_linf()
        self.set_reduplication()
        
        #self.set_has_hcopying()
        
    def list_for_csv(self):
        as_graphemes = mopho_checks.slice_string_graphemes(self.word)
        where_in_wrapped = mopho_checks.indices_stripped(self.word, self.parse)
        
        #fields = ['lexeme','stripped_lexeme','root','parse','underlying','definition','word_graphemes','where_in_wrapped','grammatical_categories','suffixes','prefixes','copy','copy_indices','copied','copied_indices','h_copy', 'linfixation_indices', 'without_linfixation', 'l_copy_indices']
        
        return [self.word, self.stripped, self.root, self.parse, self.underlying, self.definition, as_graphemes, where_in_wrapped, self.grammatical_categories, self.suffix_list, self.prefix_list, self.copy, self.i_copy, self.copied, self.i_copied, self.hcopy, self.i_linfix, self.no_linf, self.i_l_red]
        
        
    def get_basics(self):
        #print(self.dict_row)
        #print(self.id)
        print('Word: ' + self.word)
        print('Root: ' + self.root)
        print('Parse: ' + self.parse)
        print('Definition: ' + self.definition)
        print('Grammatical categories: ' + str(self.grammatical_categories))
        print('Prefixes: ' + str(self.prefix_list))
        print('Suffixes: ' + str(self.suffix_list))
        print('Underlying affixes: ' + self.underlying_affixes)
        print('Has copying: ' + str(self.copy))
        print('Has l-infixation: ' + str(self.linfixing))
        print('nol inf: ' + str(self.no_linf))
        print('copied_l: ' + str(self.i_l_red))
        
#w1 = Words('slheq’lhuq’stuhw')
#print(w1.word)
#print(w1.underlying_affixes)
