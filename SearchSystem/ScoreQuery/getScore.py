import cmath

def get_tfidf(index, fileNum , docID, word) :
    docID = str(docID)
    if docID not in index[word]:
        return "0"
    tf = len(index[word][docID])
    df = len(index[word])
    idf = cmath.log10(fileNum / df).real
    return tf * idf

def get_wfidf(index, fileNum, docID, word):
    docID = str(docID)
    if docID not in index[word]:
        return "0"
    tf = len(index[word][docID])
    df = len(index[word])
    wf = 1 + cmath.log10(tf).real
    idf = cmath.log10(fileNum / df).real
    return wf * idf

def get_wfidf_Score(index,fileNum,docID,wordList):
    score = 0
    docID = str(docID)
    for word in wordList:
        if word not in index or docID not in index[word]:
            continue
        tf = len(index[word][docID])
        df = len(index[word])
        wf = 1 + cmath.log10(tf).real
        idf = cmath.log10(fileNum / df).real
        score += wf * idf
    return score

def get_tfidf_Score(index,fileNum,docID,wordList):
    score = 0
    docID = str(docID)

    for word in wordList:

        if word not in index or docID not in index[word]:
            continue
        tf = len(index[word][docID])
        df = len(index[word])
        idf = cmath.log10(fileNum / df).real
        # print("filenum / df",fileNum / df, "df: ",df, " idf: ", idf )
        score += tf * idf
    return score


def get_tfidf_improve_Score(index, fileNum, docID, wordList):
    score = 0
    docID = str(docID)

    for word in wordList:

        if word not in index or docID not in index[word]:
            continue
        #该文档的词出现频度
        pmk1 = len(index[word][docID])
        pmk2 = 0
        for otherDocID in index[word]:
            pmk2 += len(index[word][otherDocID])
        #其他文档的出现频度
        pmk2 - pmk1
        # df = len(index[word])
        idf = cmath.log10(1+pmk1/pmk2).real
        # print("filenum / df",fileNum / df, "df: ",df, " idf: ", idf )
        score += pmk1 * idf
    return score
