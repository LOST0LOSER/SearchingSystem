import os
from SearchSystem import tools
from SearchSystem.LanguageAnalysis import PreprocessFile


def createIndex(directname):
    invertedIndex = {}
    # reuturPath = os.path.join(tools.projectpath,directname)
    if(os.path.isdir(tools.reuterspath)):
        files = os.listdir(tools.reuterspath)
        for file in files:
            print("analyzing file: ", file)
            #每个文档的词项 list
            title, content = PreprocessFile.preProcess(file)
            docId = getDocID(file)

            num = 0 #word在文档中的位置
            for word in content:
                # if word.isdigit():
                #     num += 1
                #     continue

                if word not in invertedIndex:
                    docList = {}
                    docList[docId] = [num]
                    invertedIndex[word] = docList
                else:
                    if docId not in invertedIndex[word]:
                        invertedIndex[word][docId] = [num]
                    else:
                        invertedIndex[word][docId].append(num)

                num += 1

    #给倒排索引中的词项排序
    invertedIndex = sortTheDict(invertedIndex)
    #获取词项列表
    wordList = getWordList(invertedIndex)
    #将数据写入文件中
    #将建立的倒序索引存储成json
    #将建立的词语索引存储到wordlist
    invertedIndexPath = os.path.join(tools.projectpath,'invertIndex.json')
    wordListPath = os.path.join(tools.projectpath, 'wordList.json')
    tools.writeToFile(invertedIndex, invertedIndexPath)
    tools.writeToFile(wordList, wordListPath)


#获取文档名中的文档的id
def getDocID(filename):
    end = filename.find('.')
    docId = filename[0:end]
    return int(docId)

def sortTheDict(dict):
    sdict =  { k:dict[k] for k in sorted(dict.keys())}
    for stem in sdict:
        sdict[stem] = { k:sdict[stem][k] for k in sorted(sdict[stem].keys())}
    return sdict

def printIndex(index):
    for stem in index:
        print(stem)
        for doc in index[stem]:
            print("    " , doc , " : " , index[stem][doc])

def getWordList(invertedIndex):
    wordList = []
    for word in invertedIndex.keys():
        wordList.append(word)
    return wordList

# print("establishing the INDEX...")
# establishIndex.createIndex('Reuters')



# createIndex('test')
