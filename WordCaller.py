'''
WordCaller.py
Person is prompted to enter a word or root. word objects are created for the word inputted, or all words with the given root
'''
import LocateDictWord as parse_dict
from Words import Words
import CompareWords as word_compare
import string

def input_root():
    input_root = input('Enter root: ')
    input_root = input_root.replace('\'', '’').lstrip().rstrip()
    words = parse_dict.find_words_with_root(input_root)
    #print(words)
    
    print('Root definition: ' + parse_dict.find_root_meaning(input_root))
    
    word_objects = []
    for word in words:
        word_objects.append(Words(word[1]))
    
    i = 1   
    for word_object in word_objects:
        print(str(i) + '. ' + word_object.word)
        i+=1

    compare_input_inquiry = input('Word you like to compare words? Y/N\n')
    if compare_input_inquiry == ('Y' or 'y'):
        compare(word_objects)
        
def input_word():
    input_lexeme = input('enter word to find: ')
    word = Words(input_lexeme)
    word.get_basics()
    
    repeat_input = input('\n\nWould you like to search again? Y/N: \n')
    if input == 'Y':
        choose_input()
    
def compare(word_objects):
    input_list = input('input the numbers of each word you\'d like to compare, separated by commas (e.g. 1, 3):\n')
    input_list = input_list.replace(' ', '').split(',')
    #print(input_list)
    compare_list = []
    for i in range(len(input_list)):
        word_index = int(input_list[i])-1
        compare_list.append(word_objects[word_index])
    
    
    #print(compare_list)
    word_compare.compare_words(compare_list)
    
    compare_input_inquiry = input('Word you like to compare other words in this set? Y/N\n')
    if compare_input_inquiry == 'Y':
        compare(word_objects)   

def choose_input():
    input_option = input('Type \'A\', then \'Enter\' to search an individual lexeme.\nType \'B\' , then \'Enter\' to search for lexemes associated with a root.\n')
    if input_option == ('A' or 'a'):
        input_word()
    elif input_option == ('B' or 'b'):
        input_root()
    else:
        try_again_input = input('Invalid option. Type \'Enter\' to try again.')
        if try_again_input == "":
            choose_input()
        else:
            print('Please exit the program and try again')
        



choose_input()
#compare_words()