import os
import nltk
from nltk import data
from SearchSystem.InvertedIndex import establishIndex
from SearchSystem.InvertedIndex import establishVSM
from SearchSystem.InvertedIndex import getIndex
from SearchSystem.LanguageAnalysis import stemming
from SearchSystem.Serching import searchWord
from SearchSystem.SpellingCorrect import spell
from SearchSystem.ScoreQuery import sortDoc
from SearchSystem.BoolSearch import BoolSearchDel
from SearchSystem import tools
from InformationExtraction import NamedEntityRecognition as NER
import json

#nltk库路径
data.path.append(r"nltk_data")

DIRECTNAME = 'Reuters'

# print("establishing the INDEX...")
# establishIndex.createIndex(DIRECTNAME)

print("getting word list...")
WORDLIST = getIndex.getWordList()
print("getting index...")
INDEX = getIndex.getIndex()
print("loading the wordnet...")
stemming.lemmatize_sentence("a", False)

PATH = tools.projectpath + DIRECTNAME
FILES = os.listdir(tools.reuterspath)
FILENUM = len(FILES)


def runservice(choice, INPUTSTATEMENT):
    # 结果列表初始化
    resultlist = []
    print("stemming...")
    INPUTWORDS = stemming.lemmatize_sentence(INPUTSTATEMENT, True)
    print(INPUTWORDS)
    print("spelling correcting...")
    INPUTWORDS = spell.correctSentence(INPUTWORDS)
    print(INPUTWORDS)

    IOBTree = NER.createIOBTree(INPUTWORDS)
    

    WORDSET = set(INPUTWORDS)

    DOCLIST = searchWord.searchWords(INDEX, WORDSET)
    # 普通排序查询
    if choice == 1:
        SORTEDDOCLIST = sortDoc.sortScoreDocList(
            INDEX, FILENUM, WORDSET, DOCLIST)
        for doc in SORTEDDOCLIST:
            print("doc ID: ", doc[1], " score: ", "%.4f" % doc[0])

        resultlist = SORTEDDOCLIST

    # TOP K排序 查询
    elif choice == 2:
        SORTEDDOCLIST = sortDoc.TopKScore(
            20, INDEX, FILENUM, WORDSET, DOCLIST)
        for doc in SORTEDDOCLIST:
            print("doc ID: ", doc[1], " score: ", "%.3f" % doc[0])

        resultlist = SORTEDDOCLIST

    # Bool 查询
    elif choice == 3:
        print(len(DOCLIST), "DOCs :")
        print(DOCLIST)
        resultlist = DOCLIST
    # 短语查询
    elif choice == 4:
        PHRASEDOCLIST = searchWord.searchPhrase(INDEX, WORDSET, INPUTWORDS)
        if 0 == len(PHRASEDOCLIST):
            print("Doesn't find \"", INPUTWORDS, '"')
        else:
            for key in PHRASEDOCLIST:
                print('docID: ', key, "   num: ", len(PHRASEDOCLIST[key]))
                print('    location: ', PHRASEDOCLIST[key])
        for key in PHRASEDOCLIST:
            resultlist.append(key)
    # 模糊查询
    elif choice == 5:
        list = searchWord.wildcardSearch(INPUTSTATEMENT, INDEX, WORDLIST)
        for searchPhrase in list:
            for articleKey in list[searchPhrase]:
                resultlist.append(articleKey)

    elif choice == 6:
        resultDict = searchWord.searchSynonymsWord(INDEX, INPUTWORDS[0])
        for synonymsWord in resultDict:
            for articleID in resultDict[synonymsWord]:
                resultlist.append(articleID)

    else:
        print("Invalid choice! Please observe these choices carefully!")
        return None

    finalpagelist = []

    # 信息归一化
    if choice == 1 or choice == 2:
        for article in resultlist:
            articleID = article[1]  # 1为文章ID
            articleTitle, articleContent = getArticle(int(articleID))
            articleScore = "%.4f" % article[0]  # 0为相关度分值
            finalpagelist.append(
                {"articleID": articleID, "articleTitle": articleTitle, "articleContent": articleContent, "articleScore": articleScore})
    elif choice == 3:
        for articleID in resultlist:
            articleTitle, articleContent = getArticle(int(articleID))
            finalpagelist.append(
                {"articleID": articleID, "articleTitle": articleTitle, "articleContent": articleContent})
    elif choice == 4 or choice == 5 or choice == 6:
        for articleID in resultlist:
            articleTitle, articleContent = getArticle(int(articleID))
            finalpagelist.append(
                {"articleID": articleID, "articleTitle": articleTitle, "articleContent": articleContent})

    return finalpagelist


def getArticle(pageID: int):
    pagepath = None
    title = None
    content = None
    if os.path.isdir(tools.reuterspath):
        pagepath = os.path.join(tools.reuterspath, "{0}.json".format(pageID))
        if os.path.isfile(pagepath):
            file = open(pagepath, "r")
            article = json.load(file)
            title = article["title"]
            content = article["content"]
            file.close()
    return title, content
