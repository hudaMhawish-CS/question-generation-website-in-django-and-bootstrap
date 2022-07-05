import nltk
import re
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from nltk import FreqDist
# from __future__ import division
from nltk import tokenize
from pattern.en import  conjugate


import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

def nerTagger(nlp, tokenize):
    doc = nlp(tokenize)

    finalList = []
    array = [[]]
    for word in doc:
        array[0] = 0
        for ner in doc.ents:
            if (ner.text == word.text):
                finalList.append((word.text, ner.label_))
                array[0] = 1
        if (array[0] == 0):
            finalList.append((word.text, 'O'))

    return finalList

def get_chunk(chunked):
    str1 = ""
    for j in range(len(chunked)):
        str1 += (chunked[j][0] + " ")
    return str1

def get_possible_chunk(segment, chunked):
    m = len(chunked)
    list1 = []
    for j in range(m):
        if (len(chunked[j]) > 2 or len(chunked[j]) == 1):
            list1.append(j)
        if (len(chunked[j]) == 2):
            str1 = chunked[j][0][0] + " " + chunked[j][1][0]
            if (str1 in segment) == True:
                list1.append(j)
    return list1


def chunk_complement(list1, j, chunked):
    m = list1[j]

    tag11 = []
    tag13 = []
    str1 = ""
    str3 = ""
    for k in range(m):
        if k in list1:
            str3 += get_chunk(chunked[k])
        else:
            str3 += (chunked[k][0] + " ")

    for k in range(m + 1, len(chunked)):
        if k in list1:
            str1 += get_chunk(chunked[k])

        else:
            str1 += (chunked[k][0] + " ")

    str2 = get_chunk(chunked[m])

    tok3 = nltk.word_tokenize(str3)
    tag3 = nltk.pos_tag(tok3)

    tok2 = nltk.word_tokenize(str2)
    tag2 = nltk.pos_tag(tok2)

    tok1 = nltk.word_tokenize(str1)
    tag1 = nltk.pos_tag(tok1)


    return tag1, tag2, tag3, str1, str2, str3

def process_pr(string):
    tok = nltk.word_tokenize(string)
    tag = nltk.pos_tag(tok)

    str1 = tok[0].capitalize()
    str1 += " "
    if len(tok) != 0:
        for i in range(1, len(tok)):
            if tag[i][1] == "NNP":
                str1 += tok[i].capitalize()
                str1 += " "
            else:
                str1 += tok[i].lower()
                str1 += " "
        tok = nltk.word_tokenize(str1)
        str1 = ""
        for i in range(len(tok)):
            if tok[i] == "i" or tok[i] == "we":
                str1 += "you"
                str1 += " "
            elif tok[i] == "my" or tok[i] == "our":
                str1 += "your"
                str1 += " "
            elif tok[i] == "your":
                str1 += "my"
                str1 += " "
            elif tok[i] == "you":
                if i - 1 >= 0:
                    to = nltk.word_tokenize(tok[i - 1])
                    ta = nltk.pos_tag(to)
                    if ta[0][1] == 'IN':
                        str1 += "me"
                        str1 += " "
                    else:
                        str1 += "i"
                        str1 += " "
                else:
                    str1 += "i "

            elif tok[i] == "am":
                str1 += "are"
                str1 += " "
            else:
                str1 += tok[i]
                str1 += " "

    return str1


def verb_auxiliary_reverse(clause):
    tok = nltk.word_tokenize(clause)
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)
    #     chunked.draw()
    str1 = ""
    str2 = ""
    str3 = ""
    list1 = get_possible_chunk(clause, chunked)
    if len(list1) != 0:
        m = list1[len(list1) - 1]
        for j in range(len(chunked[m])):
            str1 += chunked[m][j][0]
            str1 += " "
    tok1 = nltk.word_tokenize(str1)
    tag1 = nltk.pos_tag(tok1)
    gram1 = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*}"""
    chunkparser1 = nltk.RegexpParser(gram1)
    chunked1 = chunkparser1.parse(tag1)
    #     chunked1.draw()
    list2 = get_possible_chunk(str1, chunked1)
    if len(list2) != 0:

        m = list2[0]
        for j in range(len(chunked1[m])):
            str2 += (chunked1[m][j][0] + " ")
    tok1 = nltk.word_tokenize(str1)
    tag1 = nltk.pos_tag(tok1)
    gram1 = r"""chunk:{<VB.?|MD|RP>+}"""
    chunkparser1 = nltk.RegexpParser(gram1)
    chunked2 = chunkparser1.parse(tag1)
    #     chunked2.draw()
    list3 = get_possible_chunk(str1, chunked2)
    if len(list3) != 0:

        m = list3[0]
        for j in range(len(chunked2[m])):
            str3 += (chunked2[m][j][0] + " ")
    X = ""
    str4 = ""
    st = nltk.word_tokenize(str3)
    if len(st) > 1:
        X = st[0]
        s = ""
        for k in range(1, len(st)):
            s += st[k]
            s += " "
        str3 = s
        str4 = X + " " + str2 + str3

    if len(st) == 1:
        tag1 = nltk.pos_tag(st)
        if tag1[0][0] != 'are' and tag1[0][0] != 'were' and tag1[0][0] != 'is' and tag1[0][0] != 'am':
            if tag1[0][1] == 'VB' or tag1[0][1] == 'VBP':
                X = 'do'
            if tag1[0][1] == 'VBD' or tag1[0][1] == 'VBN':
                verb = str(tag1[0][0])
                verb = conjugate(verb, tense="INFINITIVE", person=3, number="singular", mood="indicative")
                X = 'did'
                str3 = verb
            if tag1[0][1] == 'VBZ':
                X = 'does'
            str4 = X + " " + str2 + str3 + " "
        if (tag1[0][0] == 'are' or tag1[0][0] == 'were' or tag1[0][0] == 'is' or tag1[0][0] == 'am'):
            str4 = tag1[0][0] + " " + str2

    return str4


auxlist = ['am', 'is', 'are', 'were', 'was']


def verb_Reverse(PR, Node):
    st1=""
    st2=""
    if len(PR) > 1:
        st1 = 'they'

    else:
        st1 = PR[0][0]

        if PR[0][0] == "I":
            st1 = "You"
    if len(Node) == 1:  # Base Verb
        tense = str(Node[0][1])
        verb = Node[0][0]

        if Node[0][0] in auxlist:
            vx = Node[0][0]
            if vx == "am":
                vx = "are"
            res = vx + " " + st1
            return "", vx, st1
        else:
            if tense.endswith('P'):
                if len(PR) > 1:
                    st2 = 'do'
                else:
                    st2 = 'does'
            elif tense.endswith('D'):
                verb = str(Node[0][0])
                verb = conjugate(verb, tense="INFINITIVE", person=3, number="singular", mood="indicative")
                st2 = 'did'
        return verb, st2, st1

    else:
        tense = str(Node[1][1])
        return str(Node[1][0]), str(Node[0][0]), st1


def get_pr(chunked):
    proun = []
    for r in chunked:
        if len(r) >= 2:
            proun.append(r)

    return proun


def who(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)
    m = len(chunked)

    list1 = get_possible_chunk(segment_set[num], chunked)
    # chunked.draw()
    if len(list1) != 0:
        for j in range(len(list1)):

            tag1, tag2, tag3, str1, str2, str3 = chunk_complement(list1, j, chunked)
            s11 = 'who '

            gram2 = r"""chunk:{(<RB.?>*)<VB.?|MD|RP>+}"""

            chunkparser = nltk.RegexpParser(gram2)
            chunked2 = chunkparser.parse(tag2)
            mm = len(chunked2)
            PR = get_pr(chunked2)


            list2 = get_possible_chunk(str2, chunked2)

            if len(list2) != 0:
                str2 = chunked2[list2[0]]
                vb, vx, PR = verb_Reverse(PR, str2)
                # str2 = get_chunk(chunked2[list2[0]])
                str2 = s11 + " " + vx + " " + vb
                for k in range(list2[0] + 1, len(chunked2)):
                    if k in list2:
                        str2 += get_chunk(chunked2[k])
                    else:
                        str2 += (chunked2[k][0] + " ")

                str2 += (" " + str1)
                tok_1 = nltk.word_tokenize(str2)
                str2 = ""
                for h in range(len(tok_1)):
                    str2 += (tok_1[h] + " ")

                str2 += '?'

                return str2, segment_set[num]
    else:
        return ("", "")


def howmany(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<DT>?<CD>+<RB>?<JJ|JJR|JJS>?<NN|NNS|NNP|NNPS|VBG>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)
    #     chunked.draw()
    list1 = get_possible_chunk(segment_set[num], chunked)
    s = ""

    if len(list1) != 0:
        for j in range(len(chunked)):
            str1 = ""
            str3 = ""
            str2 = " how many "
            if j in list1:
                for k in range(j):
                    if k in list1:
                        str1 += get_chunk(chunked[k])
                    else:
                        str1 += (chunked[k][0] + " ")
                str1 = verb_auxiliary_reverse(str1)
                for k in range(j + 1, len(chunked)):
                    if k in list1:
                        str3 += get_chunk(chunked[k])
                    else:
                        str3 += (chunked[k][0] + " ")

                st = get_chunk(chunked[j])
                tok = nltk.word_tokenize(st)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<RB>?<JJ|JJR|JJS>?<NN|NNS|NNP|NNPS|VBG>+}"""
                chunkparser = nltk.RegexpParser(gram)
                chunked1 = chunkparser.parse(tag)
                #                 chunked1.draw()
                list2 = get_possible_chunk(st, chunked1)
                z = ""

                for k in range(len(chunked1)):
                    if k in list2:
                        z += get_chunk(chunked1[k])

                str4 = str2 + z + str1 + str3
                for k in range(len(segment_set)):
                    if k != num:
                        str4 += ("," + segment_set[k])
                str4 += '?'
                str4 = process_pr(str4)
                # str4 = 'Q.' + str4
                s = str4
    return s, segment_set[num]
def whom(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram = r"""chunk:{<VB.?|MD|RP>+<DT>?<RB.?>*<JJ.?>*<NN.?|PRP|PRP\$|POS|VBG|DT|CD|VBN>+}"""
    chunkparser = nltk.RegexpParser(gram)
    chunked = chunkparser.parse(tag)
#     chunked.draw()
    list1 = get_possible_chunk(segment_set[num], chunked)
    list3 =""

    if len(list1) != 0:
        for j in range(len(chunked)):
            str1 = ""
            str2 = ""
            str3 = ""
            if j in list1:
                for k in range(j):
                    if k in list1:
                        str1 += get_chunk(chunked[k])
                    else:
                        str1 += (chunked[k][0] + " ")

                for k in range(j + 1, len(chunked)):
                    if k in list1:
                        str3 += get_chunk(chunked[k])
                    else:
                        str3 += (chunked[k][0] + " ")

                if chunked[j][1][1] == 'PRP':
                    str2 = " whom "
                else:
                    for x in range(len(chunked[j])):
                        if (chunked[j][x][1] == "NNP" or chunked[j][x][1] == "NNPS" or chunked[j][x][1] == "NNS" or
                                chunked[j][x][1] == "NN"):
                            break

                    for x1 in range(len(ner)):
                        if ner[x1][0] == chunked[j][x][0]:
                            if ner[x1][1] == "PERSON":
                                str2 = " whom "
                            elif ner[x1][1] == "LOC" or ner[x1][1] == "ORG" or ner[x1][1] == "GPE":
                                str2 = " what "
                            elif ner[x1][1] == "TIME" or ner[x1][1] == "DATE":
                                str2 = " what time "
                            else:
                                str2 = " what "

                strx =get_chunk(chunked[j])
                tok = nltk.word_tokenize(strx)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<VB.?|MD>+}"""
                chunkparser = nltk.RegexpParser(gram)
                chunked1 = chunkparser.parse(tag)
#                 chunked1.draw()

                strx = get_chunk(chunked1[0])

                str1 += strx

                tok = nltk.word_tokenize(str1)
                tag = nltk.pos_tag(tok)
                gram = r"""chunk:{<EX>?<DT>?<JJ.?>*<NN.?|PRP|PRP\$|POS|IN|DT|CC|VBG|VBN>+<RB.?>*<VB.?|MD|RP>+}"""
                chunkparser = nltk.RegexpParser(gram)
                chunked1 = chunkparser.parse(tag)
#                 chunked1.draw()
                list2 = get_possible_chunk(str1, chunked1)

                if len(list2) != 0:
                    m = list2[len(list2) - 1]

                    str4 = get_chunk(chunked1[m])
                    str4 =verb_auxiliary_reverse(str4)
                    str5 = ""
                    str6 = ""

                    for k in range(m):
                        if k in list2:
                            str5 += get_chunk(chunked1[k])
                        else:
                            str5 += (chunked1[k][0] + " ")

                    for k in range(m + 1, len(chunked1)):
                        if k in list2:
                            str6 += get_chunk(chunked1[k])
                        else:
                            str6 += (chunked1[k][0] + " ")
                    if str2==" what time " or str2==" what ":
                        st = str5 + str2 + str4 + str6
                    else:
                        st = str5 + str2 + str4 + str6+ str3
                    for l in range(num + 1, len(segment_set)):
                        st += ("," + segment_set[l])
                    st += '?'
                    st = process_pr(st)
                    # st = 'Q.' + st
                    list3=st

    return list3,segment_set[num]


def where(segment_set, num, ner):
    tok = nltk.word_tokenize(segment_set[num])
    tag = nltk.pos_tag(tok)
    gram_where = r"""chunk:{(<TO>)<DT>?<RB.?>*<NN.>+}"""
    chunkparser = nltk.RegexpParser(gram_where)
    chunked = chunkparser.parse(tag)

    # chunked.draw()
    m = len(chunked)
    #  if len(chunked.any()) > 0:
    #      print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    #  if m>2 or m<2:
    #      return ("","")
    if m == 0:
        return ("", "")
    list1 = get_possible_chunk(segment_set[num], chunked)
    ques = ''
    if len(list1) != 0:
        for j in range(len(list1)):

            tag1, tag2, tag3, str1, str2, str3 = chunk_complement(list1, j, chunked)

            s11 = 'Where '

            gram1 = r"""chunk:{(<RB.?>*)<VB.?|MD|RP>+}"""
            gram2 = r"""chunk:{<NN.*>)}"""
            jj = list1[j]
            for x in range(len(chunked[jj])):
                if (chunked[jj][x][1] == "NNP" or chunked[jj][x][1] == "NNPS" or chunked[jj][x][1] == "NNS" or
                        chunked[jj][x][1] == "NN"):
                    break

            for x1 in range(len(ner)):
                if ner[x1][0] == chunked[jj][x][0]:
                    if ner[x1][1] == "LOC" or ner[x1][1] == "ORG" or ner[x1][1] == "GPE":
                        ques = 'Where'
            if ques != 'Where':
                return ("", "")

            # chunkparser = nltk.RegexpParser(gram2)
            chunked1 = chunked[list1[j]]
            # chunked1.draw()

            chunkparser = nltk.RegexpParser(gram1)
            chunked2 = chunkparser.parse(tag3)
            # chunked2.draw()

            list11 = get_possible_chunk(str2, chunked1)
            str11 = 'str11'
            if len(list11) != 0:
                str11 = chunked1[list11[0]]
            str11 = get_chunk(str11)

            ################FRSH#########

            str2Com = str2
            mm = len(chunked2)


            PR = get_pr(chunked2)


            list2 = get_possible_chunk(segment_set[num], chunked2)
            if len(list2) != 0:
                str2 = chunked2[list2[0]]


                vb, vx, PR = verb_Reverse(PR, str2)
                str2 = s11 + " " + vx + " " + PR + " " + vb
                for k in range(list2[0] + 1, len(chunked2)):

                    if k in list2:
                        str2 += get_chunk(chunked2[k])
                    else:
                        str2 += (chunked2[k][0] + " ")

                str2 += (" " + str1)
                tok_1 = nltk.word_tokenize(str2)
                str2 = ""
                for h in range(len(tok_1)):
                    str2 += (tok_1[h] + " ")

                str2 += '?'

                QA_Pair = (str2, str2Com)
                return QA_Pair
    else:
        return (("", ""))

def QA(sentence):
    singleSentences = sentence.split(".")
    List = []
    if len(singleSentences) != 0:
        for i in range(len(singleSentences)):
            segmentSets = singleSentences[i].split(",")
            ner = nerTagger(nlp, singleSentences[i])
            if (len(segmentSets)) != 0:
                for j in range(len(segmentSets)):
                    Q,A=howmany(segmentSets, j, ner)
                    if Q != "":
                        List.append((Q,A))

                    Q,A=who(segmentSets, j, ner)
                    if Q != "":
                        List.append((Q,A))

                    Q,A=whom(segmentSets, j, ner)
                    if Q != "":
                        List.append((Q,A))
                    Q,A=where(segmentSets, j, ner)
                    if Q != "":
                        List.append((Q,A))
    return List


class QG():
    def sum(self, sentence):

        list = QA(sentence)
        question=[]
        for i in list:
            question.append(i[0])
        question = '\n'.join(question)
        return f"{question}"


