import json
import os
from SearchSystem import tools

def getIndex():
    file = open(r'SearchSystem\invertIndex.json', 'r')
    indexStr = file.read()
    index = json.JSONDecoder().decode(indexStr)
    file.close()
    return index

def getWordList():
    # if(not os.path.isfile(r'SearchSystem\wordList.json')):
    #     os.mkdir(r'SearchSystem\wordList.json')
    file = open(r'SearchSystem\wordList.json', 'r')
    wordStr = file.read()
    wordList = json.JSONDecoder().decode(wordStr)
    file.close()
    return wordList

# print(getWordList())
