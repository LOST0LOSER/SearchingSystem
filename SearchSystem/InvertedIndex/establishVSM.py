import os
import cmath
from SearchSystem import tools

def createVSM(index, wordList, directname):
    # path = tools.projectpath + directname
    # path = os.path.join(tools.VSMpath,directname)
    if os.path.isdir(tools.reuterspath):
        files = os.listdir(tools.reuterspath)
        fileNum = len(files)
        VSM = {}
        for file in files:
            fileID = str(getDocID(file))
            tf_idf_list = {}
            for word in wordList:
                tf_idf_list[word] = []
                if fileID not in index[word]:
                    tf_idf_list[word].append(0)
                    continue

                #文章该词出现的频度，词频
                tf = len(index[word][str(fileID)])
                #出现该词的文章总数
                df = len(index[word])
                #保留三位小数，df/fileNum倒数
                # idf =  float("%.3f" % cmath.log(10 , fileNum / df).real)
                #逆向文本频率
                idf = cmath.log10(fileNum / df).real
                #描述文章之间的相似性
                tf_idf = "%.2f" % float(tf * idf)

                tf_idf_list[word].append(tf_idf)

            VSM[fileID] = tf_idf_list
            # print(tf_idf_list)
            
    VSMpath = os.path.join(tools.VSMpath, "VSM.json")
    tools.writeToFile(VSM, VSMpath)
    #return VSM


    
# 获取文档名中的文档的id
def getDocID(filename):
    end = filename.find('.')
    docId = filename[0:end]
    return int(docId)
