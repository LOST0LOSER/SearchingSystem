import json
import os

projectpath = os.getcwd()
projectpath = os.path.join(projectpath, "SearchSystem")
reuterspath = projectpath.replace("SearchSystem","Reuters")
VSMpath = projectpath.replace("SearchSystem","VSM")

def writeToFile(item,filename):
    # 将数据写入到文件中
    file = open(filename,'w')
    str = json.JSONEncoder().encode(item)
    file.write(str)
    file.close()

#获取文档名中的文档的id,文件都是数字编号的html超文本
def getDocID(filename):
    end = filename.find('.')
    docId = -1
    if(end!=-1):
        docId = filename[0:end]
        docId = int(docId) 
    return docId

def getWholeDocList():
    files = os.listdir(reuterspath)
    fileList = []
    for file in files:
        fileList.append(getDocID(file))
    return sorted(fileList)

print("getting file list...")
wholeDocList = getWholeDocList()
