#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# was adjnoun.py
#

# program to extract data about nouns modified by colour adjectives from the BNC
# created gbt, July 2011
# modified mcg, 2012/01/23

### import

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
vvg_hold = []
vv_hold = []
mention_distance = {}
def find_an(sent,text_id,s_id):
    '''Returns a list of tuples (adjective lemma, head noun lemma).'''
    olist = []
    for i in sent.nodelist:
        pos_func[i.POS] = i.func + " Parent=" + i.parent.POS
        length = len(i.lemma)
        write2 = (text_id, s_id)
        
        
        #what is the difference between POS and parent.POS??
        if i.POS == 'VVG': #and i.func == 'ROOT': # TODO: begins with JJ (to account for comparatives+superlatives, with POS-tags=JJR, JJS)            
            if i.parent.lemma == 'start' or i.parent.lemma == 'hate':
                word = (i.lemma, write2)
                vvg_hold.append(word)
                write = (write2, i.parent.lemma + "," + i.POS + "," + i.lemma + "," + "|1", length)
                filter1.append(write)
#                print(write)
        elif i.POS == 'VV':
            
            
            if i.parent.lemma == 'start' or i.parent.lemma == 'hate':  
#                for j in range(0,len(sent.nodelist) - 1):
#                        if i.lemma == (i - j).lemma:
#                            print("XXX")
                write2 = (text_id, s_id)
                write = (write2, i.parent.lemma + "," + i.POS + "," + i.lemma + "," + "|0", length)
                filter1.append(write)
                #print(str(sent))
                #print "\t*** " + i.form + '-' + i.parent.form
                tup = (i.lemma, i.parent.lemma)
                olist.append(tup)
        else:
            word = (i.lemma, write2)
            vv_hold.append(word)
            
        # for multiple occurrences of AN
# example: 'financial' in the following structure: ###TODO: check other examples of 'coord' to see if they receive the same structure
#practical       practical       JJ      7       10      NMOD
#and     and     CC      8       7       CC
#financial       financial       JJ      9       7       COORD
#support support NN      10      13      NMOD
    return olist, vvg_hold, vv_hold

def find_mention(vvg_hold, vv_hold):
    for j in range(0,len(vvg_hold)):
        for k in range(0, len(vv_hold)):
            if vvg_hold[j][0] == vv_hold[k][0]:
                if vvg_hold[j][1][1] >= vv_hold[k][1][1]:
                    if vvg_hold[j][1][0] == vv_hold[k][1][0]:
                        value = abs(vvg_hold[j][1][1] - vv_hold[k][1][1])
                        lemma = vvg_hold[j][0]
                        mention_distance[lemma] = value
                        will_print = (mention_distance, lemma)
#                    print(vvg_hold[j][0], "=", min(mention_distance))
    return [will_print]
    
    
#    for j in range(1,len(vvg_hold)):
#        for k in range(0, len(vvg_hold) - j):
#            if vvg_hold[j-1][0] == vv_hold[j-1+k][0]: #or vvg_hold[j-1][0] == vv_hold[j-1+k][0]:
#                if vvg_hold[j-1][1][0] == vv_hold[j-1-k][1][0]:
#                    print(abs(vvg_hold[j-1][1][1] - vv_hold[j-1-k][1][1]))
                
#this function check if the node is in the list of tuples or not
def isNodeInList(n):
    for p in listTup:
        if p.getTup() == n:
            return listTup.index(p)
    return -1

#check the current list of lemmas
# if lemma is in the list, adds 1 to the number of occurrences
#otherwise it adds the lemma in the list (with #occurences == 1)
def checkList(act):
    num = isNodeInList(act)
    if num > -1:
        listTup[num].add1()
        #print(listTup[num].tup[0]+ "-" +  listTup[num].tup[1] + " has been found " + str(listTup[num].getNum()) + " times")
    else:
        listTup.append(Pair(act))
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
            anlist, vvg_hold, vv_hold = find_an(newsent,text_id,s_id) # returns list with a and n
            for tupla in anlist:
                checkList(tupla)
            del(newsent)
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
    #return freq_of
    
### main ###

### global variables
home = 'C:/Users/u175213/Desktop/'
#dropbox = home + 'Dropbox/distsem/'
#nounlistfile = dropbox + 'data/head_nouns/nounswithcolouradjs.txt'
csvfile = home + 'output.csv'

# *** TO DO: separate freq_of from selected_nouns ***
minfreq = 0 # make it a user-controlable parameter for the script?
listTup = []

a = datetime.now()
print("[Begin]")

print("Let's start...")
process_bnc_mod()

of = open(csvfile, 'w')
of.flush()
text = "Adj;Noun;Occurrences\n"
of.write(text)
#for i,line in enumerate(lines):
   # if i < 2: continue
    #foo(line)
for el in listTup:
    if(el.getNum() >= minfreq):
       #tam sayıyı aldırma => str(el)[-2:]
        #print(str(el) + " appears " + str(el).split(";")[1] + " times(min frequency=", minfreq,")it's added to the output list")
        info = str(el)
        of.write(info +"\n")

csv1_data = home + 'sample_data.csv'
csv2_data = home + 'filtered.csv'
csv3_data = home + 'distance.csv'
#1-------------------------------------
#pof.flush()
#for lines in final_list:
#    pof = open(csv_data, 'w')
#    text = str(lines)
#    pof.write(text)
#    pof.write("\n")
#    pof.close()

#2-------------------------------------
df = pd.DataFrame(final_list)
df.to_csv(csv1_data, sep=',',index=False)

df2 = pd.DataFrame(filter1)
df2.to_csv(csv2_data, sep=',',index=False)

will_print = find_mention(vvg_hold, vv_hold)

df3 = pd.DataFrame(will_print)
df3.to_csv(csv3_data, sep=',',index=False)

b = datetime.now()

of.close()
print("Process finished!")
c = b - a
print("Time spent (sec):" + str(c.seconds))
print(csvfile + " created!")
print("[End]")

