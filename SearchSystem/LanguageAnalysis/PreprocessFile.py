import os
from SearchSystem import tools
from SearchSystem.LanguageAnalysis import stemming
import json

def preProcess(filename):
    filedir = os.path.join(tools.reuterspath,filename)
    if os.path.isfile(filedir):
        file = open(filedir, 'r')
        # content = file.read()
        article = json.load(file)
        content = article["content"]
        title = article["title"]
        words = stemming.lemmatize_sentence(content,False)
        file.close()
        return title, words
    return None

# def processDirectory(directname):
#     path = tools.projectpath
#     path = os.path.join(path,directname)
#     files = os.listdir(path)
#     result = []
#     for file in files:
#         filepath = os.path.join(path, file)
#         if os.path.isfile(filepath):
#             content = preProcess(filepath)
#             result.append(content)
#             # print(content)
#     return result

#processDirectory('test')
