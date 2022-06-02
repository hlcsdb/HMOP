import csv
import sys

#will have to refactor if we want to compare words ... multiple inputs and holding in list
#input number you want to search
#input_lexeme = raw_input('enter word to find')

#lexeme = input_lexeme.replace('\'', '’')

#read csv, and split on "," the line


def find_row(lexeme):
    csv_file = csv.reader(open('HukariPeterParses_data_morphophonologyProgram.csv', "r"), delimiter=",")
    
    #loop through the csv list
    for row in csv_file:
        #if current rows 2nd value is equal to input, print that row
        if lexeme == row[1]:
            #row = [row[0], row[1], row[2], row[3], row[4]]
            #print(row)
            return row
    #csv_file.close()
    return False

            
                     
def find_words_with_root(root):
    csv_file = csv.reader(open('HukariPeterParses_data_morphophonologyProgram.csv', "r"), delimiter=",")
    if root[0] != '√':
        root = '√' + root
    words_with_root = []
    for row in csv_file:
        if root == row[3]:
            words_with_root.append(row)
    #csv_file.close()
    return words_with_root

def find_root_meaning(root):
    csv_file = csv.reader(open('HukariPeterParses_data_morphophonologyProgram.csv', "r"), delimiter=",")
    if root[0] != '√':
        root = '√' + root
    for row in csv_file:
        if root == row[3]:
            return row[5]
    #csv_file.close()
    return None 
                             