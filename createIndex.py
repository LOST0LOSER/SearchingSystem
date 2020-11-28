import os
from SearchSystem import tools
import nltk
from nltk import data
from SearchSystem.InvertedIndex import establishIndex
from SearchSystem.InvertedIndex import establishVSM
from SearchSystem.InvertedIndex import getIndex
# from InvertedIndex import getIndex
# from LanguageAnalysis import stemming
# from Serching import searchWord
# from SpellingCorrect import spell
# from scoreQuery import sortDoc
# from BoolSearch import BoolSearchDel


data.path.append(r"nltk_data")

# DIRECTNAME = 'Reuters'
# print("establishing the INDEX...")
# establishIndex.createIndex(tools.reuterspath)

print("getting word list...")
WORDLIST = getIndex.getWordList()
print("getting index...")
INDEX = getIndex.getIndex()

establishVSM.createVSM(INDEX,WORDLIST,'VSM')

# print("loading the wordnet...")
# stemming.lemmatize_sentence("a", False)

# PATH = tools.projectpath + DIRECTNAME
# FILES = os.listdir(tools.reuterspath)
# FILENUM = len(FILES)

