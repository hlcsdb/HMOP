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
import re
from simple_colors import *

SOUNDS = "(kw’|kw|k’|k|m’|m|n’|n|qw’|qw|q’|q|ch’|ch|hw|th|sh|lh|tth’|tth|ts’|ts|tl’|xw|x|l’|l|h|s|w’|w|y’|y|p’|p|t’|t|aa|ee|oo|ou|ii|o|u|i|e|a|’)"
BOLD = '\033[1m'
END = '\033[0m'
test_word =  'tsitsumiil'
#print(test_word)
split_lexeme = []

while len(test_word) > 0:
    onset_span = re.match(SOUNDS, test_word).span()
    split_lexeme.append(test_word[:onset_span[1]])
    test_word = test_word[onset_span[1]:]


def bold(input_string):
    return ''.join(['\033[1m', input_string, '\033[0m'])

print(bold('tsitsumiil'))