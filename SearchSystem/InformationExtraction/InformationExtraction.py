import nltk
from nltk import data
from nltk import pos_tag , word_tokenize
import nltk.chunk as chunk
from nltk.tag import StanfordNERTagger
from nltk.corpus import ieer
from nltk.corpus import conll2000
from nltk.corpus import conll2002
import re
from nltk.sem import relextract

data.path.append(r"nltk_data")

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


def classifyClass(split_annotations:list):
    for n, i in enumerate(split_annotations):
        if i == "I-PER":
            split_annotations[n] = "PERSON"
        if i == "I-ORG":
            split_annotations[n] = "ORGANIZATION"
        if i == "I-LOC":
            split_annotations[n] = "LOCATION"
    return split_annotations

def group(_list,n):
    for i in range(0,len(_list),n):
        val = _list[i:i+n]
        if len(val) == n:
            yield tuple(val)



def createIOBTree(splited_words):
    pos_tag_word_list = pos_tag(word_tokenize(splited_words))

    # tree = nltk.ne_chunk(pos_tag_word_list)

    # reference_annotations = list(group(pos_tag_word_list, 2))

    # pure_tokens = pos_tag_word_list[::2]
    # tagged_word = nltk.pos_tag(pure_tokens)
    nltk_unformatted_prediction = nltk.ne_chunk(pos_tag_word_list)  # 分块,返回树结构
    multiline_string = nltk.chunk.tree2conllstr(nltk_unformatted_prediction)
    listed_posTag_and_nameEntity = multiline_string.split()

    # 删除标签留下命名实体
    del listed_posTag_and_nameEntity[1::3]
    listed_nameEntity = listed_posTag_and_nameEntity

    # 修改类标注保持一致
    for name,tag in enumerate(listed_nameEntity):
        if tag == "B-PERSON":
            listed_nameEntity[name] = "PERSON"
        if tag == "I-PERSON":
            listed_nameEntity[name] = "PERSON"
        if tag == "B-ORGANIZATION":
            listed_nameEntity[name] = "ORGANIZATION"
        if tag == "I-ORGANIZATION":
            listed_nameEntity[name] = "ORGANIZATION"
        if tag == "B-LOCATION":
            listed_nameEntity[name] = "LOCATION"
        if tag == "I-LOCATION":
            listed_nameEntity[name] = "LOCATION"
        if tag == "B-GPE":
            listed_nameEntity[name] = "GPE"
        if tag == "I-GPE":
            listed_nameEntity[name] = "GPE"
    # 将组预测放入元组中
    nltk_formatted_prediction = list(group(listed_nameEntity,2))

    return nltk_formatted_prediction


def regularExtractRelation(select_document_text):
    # 词性语法规则
    # 定义分块语法
    # 这个规则是说一个NP块由一个可选的限定词后面跟着任何数目的形容词然后是一个名词组成
    # NP(名词短语块) DT(限定词) JJ(形容词) NN(名词) NNP(专有名词 单数形式 NNPS复数)
    # PP 所属短语 VP动词短语 CLAUSE主谓关系
    grammar = '\n'.join([
        'NP: {<DT|PRP\$>?<JJ>*<NN|NNP|NNPS>}',  # 前面有限定词或人称代词,一个或多个形容词后紧跟一个名词
        'NP: {<DT>*<NNP|NNPS>}',  # 一个或多个限定词后紧跟一个专有名词
        # 'NP: {<NNP|NNPS>+}',  # 一个或多个专有名词组成
        #递归处理
        'PP: { < IN > <NP > }',
        'VP: { < VB.* > <NP|PP|CLAUSE > +$}',
        'CLAUSE: { < NP > <VP > }'
    ])

    #分句
    document_sentences = parse_document(select_document_text)
    #分词标注过的句子形成的词列表
    tokenized_sentences = [nltk.word_tokenize(
        sentence) for sentence in document_sentences]
    #使用nltk命名实体来创建实体树，实现分块
    tagged_sentences = [nltk.pos_tag(sentence)
                        for sentence in tokenized_sentences]

    # 进行分块
    cp = nltk.RegexpParser(grammar)
    trees = []
    for tagged_sentence in tagged_sentences:
        tree = cp.parse(tagged_sentence)
        trees.append(tree)
    return trees

"""
返回tuple,tree对象
"""
def nltkNameEntityRecognition(select_document_text):
    document_sentences = parse_document(select_document_text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in document_sentences]
    #使用nltk命名实体来创建实体树，实现分块
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    ne_chunked_sents = [nltk.ne_chunk(tagged_sentence)
                        for tagged_sentence in tagged_sentences]

    #抽取所有命名实体
    named_entities = list(set())
    for ne_tagged_sentence in ne_chunked_sents:
        for tagged_tree in ne_tagged_sentence:
            # 抽取含有命名实体标签的词信息，并抽取其
            if hasattr(tagged_tree, 'label'):
                entity_name = tagged_tree.leaves()  # 获取词
                entity_type = tagged_tree.label()  # 获取命名实体
                #去重
                if (entity_name, entity_type) not in named_entities:
                    named_entities.append((entity_name, entity_type))
    return named_entities , ne_chunked_sents # 1 为 命名实体的元组列表组合，2 为分块得到的句子树结构


def nltkNameEntityRecognition_allArticle(select_document_text):
    # document_sentences = parse_document(select_document_text)
    tokenized_sentences = nltk.word_tokenize(select_document_text)
    #使用nltk命名实体来创建实体树，实现分块
    tagged_sentences = nltk.pos_tag(tokenized_sentences)
    ne_chunked_sents = nltk.ne_chunk(tagged_sentences)

    #抽取所有命名实体
    named_entities = list(set())
    for ne_tagged_sentence in ne_chunked_sents:
        # 抽取含有命名实体标签的词信息，并抽取其
        if hasattr(ne_tagged_sentence, 'label'):
            entity_name = ne_tagged_sentence.leaves()  # 获取词
            entity_type = ne_tagged_sentence.label()  # 获取命名实体
            #去重
            if (entity_name, entity_type) not in named_entities:
                named_entities.append((entity_name, entity_type))
    return named_entities, ne_chunked_sents  # 1 为 命名实体的元组列表组合，2 为分块得到的句子树结构

"""
一元分块器，
该分块器可以从训练句子集中找出每个词性标注最有可能的分块标记，
然后使用这些信息进行分块
"""
class UnigramChunker(nltk.ChunkParserI):

    """
    构造函数 :param train_sents: Tree对象列表
    """
    def __init__(self, train_sents):
        train_data = []
        # 当解析的目标是多棵语法树时
        # for sent in train_sents:
        #     # 将Tree对象转换为IOB标记列表[(word, tag, IOB-tag), ...]
        #     conlltags = nltk.chunk.tree2conlltags(sent)

        #     # 找出每个词性标注对应的IOB标记
        #     ti_list = [(t, i) for w, t, i in conlltags]
        #     train_data.append(ti_list)

        # 将Tree对象转换为IOB标记列表[(word, tag, IOB-tag), ...]
        conlltags = nltk.chunk.tree2conlltags(train_sents)
        # 找出每个词性标注对应的IOB标记
        ti_list = [(t, i) for w, t, i in conlltags]
        train_data.append(ti_list)
        # 使用一元标注器进行训练
        self.__tagger = nltk.UnigramTagger(train_data)

    """
    对句子进行分块 :param tokens: 标注词性的单词列表 :return: Tree对象
    """
    def parse(self, tokens):
        # 取出词性标注
        tags = [tag for (word, tag) in tokens]
        # 对词性标注进行分块标记
        ti_list = self.__tagger.tag(tags)
        # 取出IOB标记
        iob_tags = [iob_tag for (tag, iob_tag) in ti_list]
        # 组合成conll标记
        conlltags = [(word, pos, iob_tag)
                     for ((word, pos), iob_tag) in zip(tokens, iob_tags)]

        return nltk.chunk.conlltags2tree(conlltags)

"""
param: train_sents_trees : list<tree>
"""
def relationExtraction(chunk_tree):
    IN = re.compile(r'.*\b in \b.*')
    # chunk_tree.headline = ['S'] #文法开头什么都没有，因为文章被分成句子，每个句子单独成树了
    # chunk_tree.text = chunk_tree  #api变动，识别text作为其读入内容
    relations = []
    # conllStr = chunk.tree2conlltags(chunk_tree)
    # chunk_tree = chunk.conlltags2tree(conllStr)

    #得到不同的两对，一个是没有命名实体的词组，另一个则有
    pairs = relextract.tree2semi_rel(chunk_tree)
    fix_pairs = []

    for word_list , tree in pairs:
        fix_pairs.append(tree)
    reldicts = relextract.semi_rel2reldict(pairs)

    #打印出关系表
    for reldict in reldicts:
        print('\n')
        for k, v in sorted(reldict.items()):
            print(k, '=>', v)  # doctest: +ELLIPSIS

    # org_place_relations = relextract.extract_rels(
    #     'ORG', 'GPE', chunk_tree, corpus='conll2002', pattern=IN)

    # per_place_relations = relextract.extract_rels(
    #     'PER', 'GPE', chunk_tree, corpus='conll2002', pattern=IN)

    
    # condition = False
    # if fix_pairs.__contains__('PERSON') and fix_pairs.__contains__('ORGANIZATION'):
    #     condition = True

    # has_per = False
    # has_org = False
    # for tree in fix_pairs:
    #     if getattr(tree,'label') is 'PERSON':
    #         has_per = True
    #     if getattr(tree, 'label') is 'ORGANIZATION':
    #         has_org = False

    # for relation in nltk.sem.extract_rels('PERSON', 'ORGANIZATION', chunk_tree, corpus='ace', pattern=PR):
    #     print(relation)
    #     relations.append(nltk.sem.rtuple(relation))

    return reldicts

