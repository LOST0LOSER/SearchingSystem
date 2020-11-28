import nltk
#词形还原
from nltk.stem import WordNetLemmatizer
#语料库
from nltk.corpus import wordnet
#词令牌化与贴类型标签
from nltk import word_tokenize, pos_tag

#获取词所属类别
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

#去除符号
deleteSignal = [',','.',';','&',':','>',"'",'`','(',')','+','!','*','"','?']
deleteSignalForInput = [',','.',';','&',':','>',"'",'`','+','!','*','"','?']

#还原句子中单词原型
#完成词分块
def lemmatize_sentence(sentence,forinput):
    res = []
    result = []
    #词形还原
    #将词令牌化
    lemmatizer = WordNetLemmatizer()
    for word, pos in pos_tag(word_tokenize(sentence)):
        wordnet_pos = get_wordnet_pos(pos) or wordnet.NOUN
        res.append(lemmatizer.lemmatize(word, pos=wordnet_pos)) #根据分得类别进行还原词形

    for word in res:
        #如果是 's什么的，直接排除
        if word[0] is '\'':
            continue
        
        #去除标点符号
        if not forinput:
            for c in deleteSignal:
                word = word.replace(c,'')
        else:
            for c in deleteSignalForInput:
                word = word.replace(c,'')

        #排除空的字符串
        if len(word) is 0 or word[0] is '-':
            continue

        #如果分解的单词中有/,则将其中的每个单词添加到结果中
        if word.find('/') > 0:
            rs = word.split('/')
            for w in rs:
                w = getWord(w)
                result.append(w)
        else:
            word = getWord(word)
            result.append(word)

    return result

#还原词型
def getWord(word):
    if word.istitle():
        word = word.lower()
        word = WordNetLemmatizer().lemmatize(word, pos='n')
    else:
        word = WordNetLemmatizer().lemmatize(word, pos='n')
    return word

# while 1:
#     str = input()
#     result = lemmatize_sentence(str)
#     for word in result:
#         print(word)

#print(WordNetLemmatizer().lemmatize('probable', pos='v'))