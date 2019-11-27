#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# was adjnoun.py
#

# program to extract data about nouns modified by colour adjectives from the BNC
# created gbt, July 2011
# modified mcg, 2012/01/23

### import

import re

# gbt's modules:
import sys
from datetime import datetime
from classes4bnc import Pair, Node, Sentence 
import pandas as pd
#from classes4bnc import *# import defined classes (same namespace!)
### from generalfuncs import *
final_list = []
filter1 = []
### functions ###
def yield_lines(list_line):
    
    final_list.append(list_line)
    return final_list

def token_type(token):
    token_begin = token[:3]
    if token == "": # empty line
        return False
    elif token_begin == "<s>":
        return "sentencebegin"
    elif token_begin == "</s":
        return "sentenceend"
    elif token_begin == "<te":
        return "textbegin"
    elif token_begin == "</t":
        return "textend"
    else:
        return "word"
pos_func = {}

def find_an(sent,text_id,s_id):
    '''Returns a list of tuples (adjective lemma, head noun lemma).'''
    olist = []
    for i in sent.nodelist:
        pos_func[i.POS] = i.func + " Parent=" + i.parent.POS

        #what is the difference between POS and parent.POS??
        if i.POS == 'VVG' or i.POS == "VV": #and i.func == 'ROOT': # TODO: begins with JJ (to account for comparatives+superlatives, with POS-tags=JJR, JJS)          
            if i.parent.lemma == 'start' or i.parent.lemma == 'hate':
                if i.parent.index < i.index:
                    write = [text_id, s_id]
                    '''Feature: length of non-finite verb lemma'''
                    length = len(i.lemma)
                    '''Feature end'''
                    '''Feature: check whether there is a noun or adj before or after the non-finite verb'''
                    '''As binay features: befaft_bef, befaft_aft, both values can be 1 or 0'''
                    befaft_bef = 0
                    befaft_aft = 0
                    for j in sent.nodelist:
                        if j.parent_index == i.index:
                            if re.match(r'J.*|N.*', j.POS):
                                if j.index < i.index:
                                    befaft_bef = 1
                                elif j.index > i.index:
                                    befaft_aft = 1
                    '''Feature end'''
                    '''Feature: Argument structure'''
                    '''As binary features: NC (No complement), NP (Noun phrase complement), PP (Preposition phrase complement)'''
                    argstr_NC = 0
                    argstr_NP = 0
                    argstr_PP = 0
                    for j in sent.nodelist:
                        if j.parent_index == i.index:
                            if re.match(r'N.*', j.POS):
                                argstr_NP = 1
                                argstr_PP = 0
                                #In case a verb takes both NP and PP, NP always overwrite PP, regardless of their position
                                #This can be rewrite later
                            elif j.POS == 'IN' and argstr_NP == 0:
                                argstr_PP = "1"
                    if argstr_NP == 0 and argstr_PP == 0:
                        argstr_NC = 1
                    '''Feature end'''
                    '''Feature: tense'''
                    tense = 'unknown'
                    if i.parent.func == "ROOT":
                        if i.parent.POS == "VVD":
                            tense = "Past"
                        else:
                            tense = "Present"
                    else:
                        for word in sent.nodelist:
                            if re.match(r'V.*|MD', word.POS) and word.func == 'ROOT':
                                if word.form == "will":
                                    tense = "Future"
                                elif word.form == "would":
                                    tense = "Conditional"
                                elif re.match(r"can|may|shall", word.form):
                                    tense = "Present"
                                elif word.POS == "MD":
                                    tense = "Past"
                                elif word.POS == "VBP" or word.POS == "VBZ":
                                    for j in sent.nodelist:
                                        if j.index == str(int(word.index) + 1) and j.form == "going":
                                            tense = "Future"
                                        else:
                                            tense = "Present"
                                elif re.match(r'..D', word.POS):
                                    tense = "Past"
                                elif re.match(r'..P|..Z', word.POS):
                                    tense = "Present"
                    '''Turn into binary features: tense_pre, tense_pst, tense_fut, tense_cond'''
                    '''In case tense cannot be detected, all the values will be 0'''
                    tense_pre = 0
                    tense_pst = 0
                    tense_fut = 0
                    tense_cond = 0
                    if tense == 'Present':
                        tense_pre = 1
                    elif tense == 'Past':
                        tense_pst = 1
                    elif tense == 'Future':
                        tense_fut = 1
                    elif tense == 'Conditional':
                        tense_cond = 1
                    '''Feature end'''
                    '''Get target form (I have combined the ifs for VVG and VV)'''
                    if i.POS == "VVG":
                        targetform = 1
                    else:
                        targetform = 0
                    '''Now we got the target form'''
                    '''Now write features into the csv file'''
    #                write = write2 + "," + i.parent.lemma + "," + i.POS + "," + i.lemma + "," + length + "," + befaft_bef + "," + befaft_aft + "," + argstr_NC + "," + argstr_NP + "," + argstr_PP + ","  + tense + "," + targetform
                    currentsent = []
                    '''A test function: print the sentence'''
                    for node in sent.nodelist:
                        currentsent.append(node.form)
                        printsent = ' '.join(currentsent)
                    write.append(i.parent.lemma)
                    write.append(i.lemma)
                    write.append(printsent)
                    write.append(length)
                    write.append(befaft_bef)
                    write.append(befaft_aft)
                    write.append(argstr_NC)
                    write.append(argstr_NP)
                    write.append(argstr_PP)
                    write.append(tense_pre)
                    write.append(tense_pst)
                    write.append(tense_fut)
                    write.append(tense_cond)
                    write.append(i.POS)
                    write.append(targetform)
                    filter1.append(write)
    #                tup = (i.lemma,featurecompposition)            
    #                olist.append(tup)
    #                print(write)
    return olist

#this function check if the node is in the list of tuples or not
#def isNodeInList(n):
#    for p in listTup:
#        if p.getTup() == n:
#            return listTup.index(p)
#    return -1

#check the current list of lemmas
# if lemma is in the list, adds 1 to the number of occurrences
#otherwise it adds the lemma in the list (with #occurences == 1)
#def checkList(act):
#    num = isNodeInList(act)
#    if num > -1:
#        listTup[num].add1()
#        #print(listTup[num].tup[0]+ "-" +  listTup[num].tup[1] + " has been found " + str(listTup[num].getNum()) + " times")
#    else:
#        listTup.append(Pair(act))
        #print(listTup[num].tup[0]+ "-" +  listTup[num].tup[1] + " has been found for the first time")

def process_bnc_mod():
    text_id = 0
    i = 0
    s_id = 0
    within_sent = False
    limit = 1000000#124529467 number of tokens in bnc.xml plus two
    #limit = 1000000
    bnc = open(home + 'bnc.xml', 'r', encoding = 'UTF-8', errors = 'ignore')
    while i < limit:
#        if(i%25000 == 0) and (i != 0):
#            print("Processed " + str(i) + " lines")
#        if(i%1245294 == 0):
#            print("Processed " + str(i) + " from " + str(limit) + " lines, (" + str((i/limit)*100) + "%)")
        i = i + 1
        iamin = "token: " + str(i)+ "\n\t"
        line = bnc.readline()
        if token_type(line) == "textend": # text starts
            text_id += 1
            print(text_id)
        if token_type(line) == "sentencebegin": # count sentences
            if within_sent == True: # errors in the corpus coding...
                pass
            else:
                within_sent = True
                s_id=s_id+1
                newsent = Sentence(s_id) # sentence id
        elif token_type(line) == "sentenceend": # process sentence and flush
            within_sent = False # finish sentence
            try:
                newsent.assign_parents()
            except:
                msg = iamin + str(newsent) + "\n"
                sys.stderr.write(msg)
            anlist = find_an(newsent,text_id,s_id) # returns list with a and n
            
#            for tupla in anlist:
#                checkList(tupla)
#            del(newsent)
        elif token_type(line) == "word":
            itemlist = line.split()
            yield_lines(itemlist)
            #burada liste olarak itemler geliyor
            try:
                node = Node(atts=itemlist)
            except:
                msg = iamin + str(newsent) + "\n"
                sys.stderr.write(msg)
            newsent.append_node(node)
        elif token_type(line) == False:
            sys.stderr.write("* Reached EOF *\n")
            break
    bnc.close()
    msg = "Done! Number of sentences processed: " + str(s_id) + ", and tokens: " + str(i) + "\n"
    sys.stderr.write(msg)
    return anlist
    
### main ###

### global variables
home = 'F:/学习（语言学）/计算语义学/Project/'
#dropbox = home + 'Dropbox/distsem/'
#nounlistfile = dropbox + 'data/head_nouns/nounswithcolouradjs.txt'
#csvfile = home + 'output.csv'

# *** TO DO: separate freq_of from selected_nouns ***
#minfreq = 0 # make it a user-controlable parameter for the script?
#listTup = []

a = datetime.now()
print("[Begin]")

print("Let's start...")
anlist = process_bnc_mod()

#of = open(csvfile, 'w')
#of.flush()
#text = "Adj;Noun;Occurrences\n"
#of.write(text)
#for i,line in enumerate(lines):
   # if i < 2: continue
    #foo(line)
#for el in listTup:
#    if(el.getNum() >= minfreq):
       #tam sayıyı aldırma => str(el)[-2:]
        #print(str(el) + " appears " + str(el).split(";")[1] + " times(min frequency=", minfreq,")it's added to the output list")
#        info = str(el)
#        of.write(info +"\n")

#csv1_data = home + 'sample_data.csv'
csv2_data = home + 'filtered.csv'
#1-------------------------------------
#pof.flush()
#for lines in final_list:
#    pof = open(csv_data, 'w')
#    text = str(lines)
#    pof.write(text)
#    pof.write("\n")
#    pof.close()

#2-------------------------------------
#df = pd.DataFrame(final_list)
#df.to_csv(csv1_data, sep=',',index=False)

df2 = pd.DataFrame(filter1)
df2.to_csv(csv2_data, sep=',',index=False)

#df2 = pd.DataFrame(anlist)
#df2.to_csv(csv2_data, sep=',',index=False)


b = datetime.now()

#of.close()
print("Process finished!")
c = b - a
print("Time spent (sec):" + str(c.seconds))
print(csv2_data + " created!")
print("[End]")

