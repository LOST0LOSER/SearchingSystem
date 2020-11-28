import sys
import os
sys.path.append(os.getcwd())
from SearchSystem import tools
sys.path.append(tools.projectpath)
import InformationExtraction as IE
import json
import re
import nltk
import random

files = os.listdir(tools.reuterspath)

selected_file = files[random.randint(0,len(files))]
selected_file_path = os.path.join(tools.reuterspath,selected_file)
select_document_text = None

if os.path.isfile(selected_file_path):
    file = open(selected_file_path, "r")
    article = json.load(file)
    title = article["title"]
    content = article["content"]
    file.close()
    select_document_text = content


def parse_document(document):
   document = re.sub('\n', ' ', document)
   if isinstance(document, str):
       document = document
   else:
       raise ValueError('Document is not string!')
   document = document.strip()
   sentences = nltk.sent_tokenize(document)
   sentences = [sentence.strip() for sentence in sentences]
   return sentences

"""
进行分块,完成命名实体建立
"""
# trees = IE.regularExtractRelation(select_document_text)
# named_entities, ne_chunked_sents = IE.nltkNameEntityRecognition(
#     select_document_text)

#整篇直接分块
named_entities, ne_chunked_sents = IE.nltkNameEntityRecognition_allArticle(
    select_document_text)
"""
根据命名实体，识别实体间对应的关系
"""
# for ne_chunked_sent in ne_chunked_sents:
#     pack_relation_dicts = IE.relationExtraction(ne_chunked_sent)
#整篇的方式
pack_relation_dicts = IE.relationExtraction(ne_chunked_sents)







# # store named entities in a data frame
# entity_frame = pd.DataFrame(named_entities, columns=[
#                             'Entity Name', 'Entity Type'])
# # display results
# print(entity_frame)
print(None)
    
