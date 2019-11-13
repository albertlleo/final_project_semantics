import xmltodict
from textwrap import wrap
import numpy as np

with open('bnc_small.xml') as fd:
    doc = xmltodict.parse(fd.read())
    dict_sentences={}
    dict_final={}
    a=[]
    array=[]
    array2=[]

    for i in range(1,len(doc['text']['s'])):
        a.append(doc['text']['s'][i].split('\s'))
        dict_sentences[i] = (doc['text']['s'][i].split('\s'))
        # for ele in dict_sentences[i]:
        #       array[i]=ele.split("\t")
        # for ab in array:
        #     array2.append(ab.split("\n"))

        # aa = [i.split('\t', 1)[0] for i in dict_sentences[i]]
        # dict_final[str(aa)]=(dict_sentences[i])

print("")
value = []

array= [ele.split("\t") for ele in dict_sentences[i]]
for ele in dict_sentences[1]:
    array=ele.split("\t")
    for i in array:
        if "\n"  in i:
            value.append(i)

# this is a test for comit and push

print(array)
print(value)
# print(dict_final)







