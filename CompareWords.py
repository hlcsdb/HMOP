'''
CompareWords.py
Compares various features of words
'''
from Words import Words

def compare_words(words:list):
    print("Commonalities: ")
    compare_categories(words)
    compare_prefixes(words)
    compare_suffixes(words)
    compare_linf(words)
    compare_copy(words)
    

def compare_categories(words:list):
    a = words[0].get_grammatical_categories()
    b = words[1].get_grammatical_categories()
    intersect = set(a).intersection(b)
    
    for i in range(2,len(words)):
        a = words[i].get_grammatical_categories()
        intersect = set(a).intersection(intersect)
    if len(intersect) > 0:
        print('the common grammatical category(s) are: ' + str(intersect))
            
def compare_prefixes(words:list):
    a = words[0].get_prefix_list()
    b = words[1].get_prefix_list()
    intersect = set(a).intersection(b)
    
    for i in range(2,len(words)):
        a = words[i].get_prefix_list()
        intersect = set(a).intersection(intersect)
    if len(intersect) > 0:
        print('the common prefix(es) are: ' + str(intersect))    
            
def compare_suffixes(words:list):
    a = words[0].get_suffix_list()
    b = words[1].get_suffix_list()
    intersect = set(a).intersection(b)
    
    for i in range(2,len(words)):
        a = words[i].get_suffix_list()
        
        intersect = set(a).intersection(intersect)
    if len(intersect) > 0:
        print('the common suffix(es) are: ' + str(intersect))    
            
def compare_linf(words:list):
    for i in range(len(words)-1):
        next_word = i+1
        if words[i].get_has_linf() != words[next_word].get_has_linf():
            return False
    
    if words[0].get_has_linf():
        print('Both/all have l-infixation')
    elif not words[0].get_has_linf():
        print('Neither/none have l-infixation')        
    
    return True

def compare_copy(words:list):
    for i in range(len(words)-1):
        next_word = i+1
        if words[i].get_has_copy() != words[next_word].get_has_copy():
            return False
    
    if words[0].get_has_copy():
        print('Both/all have reduplication')
    elif not words[0].get_has_copy():
        print('Neither/none have reduplication')
    
    return True



                   