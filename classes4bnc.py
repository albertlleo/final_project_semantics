# created gbt, July 2011
# modified mcg, 2012/01/29
import sys

### classes ###

class Sentence:
    "Class for storing dependency-parsed sentences (lists of nodes) and doing various operations with them"
    def __init__(self, idx=None):
        n = Node(['','','','0','-1','']) # ROOT node; index = 0, parent_index = -1
        self.nodelist = [n] # element 0 in nodelist: the ROOT node
        self.idx = idx

    def __str__(self):
        # ***mirar pprint
        sent = 'sent ' + str(self.idx) + ":"
        for i in self.nodelist:
            sent = sent + i.form + " "
        return sent

    def append_node(self,node):
        self.nodelist.append(node)

    def assign_parents(self):
        for i in self.nodelist:
            idx = int(i.parent_index)
            try:
                i.set_parent(self.nodelist[idx])
            except IndexError:
                msg = str(idx) +': '+ str(self.nodelist)+ str(self)
                sys.stderr.write(msg)

# ['The', 'the', 'DT', '1', '3', 'NMOD']
# ['major', 'major', 'JJ', '2', '3', 'NMOD']
# ['impact', 'impact', 'NN', '3', '4', 'SBJ']
# ['is', 'be', 'VBZ', '4', '0', 'ROOT']
# ['yet', 'yet', 'RB', '5', '7', 'ADV']
# ['to', 'to', 'TO', '6', '7', 'VMOD']
# ['come', 'come', 'VV', '7', '4', 'PRD']
# ['.', '.', 'SENT', '8', '4', 'P']
class Node:
    "Node class for storing nodes in MALT parser parsed sentences."

    def __init__(self, atts=None):
        if atts == None:
            sys.stderr.write("Error: no attributes for this node \n")
            return False
        elif atts == []: # for empty nodes (self.parent)
            self.form = "#empty" # for __str__ method in class Sentence
            self.parent_index = -1 # every node should have at least form and parent_index
        elif len(atts) == 2:
            self.lemma = atts[0]
            self.POS = atts[1]
        elif len(atts) != 6:
            msg = "Error: expecting 6 attributes\n\tAttributes: " + str(atts)
            sys.stderr.write(msg)
            return False
        else:
            self.form = atts[0]
            self.lemma = atts[1]
            self.POS = atts[2]
            self.index = atts[3]
            self.parent_index = atts[4]
            self.func = atts[5]
            self.parent = Node([])

    def __str__(self):
        return str(self.form + " " + self.lemma + " " + self.POS + " " + self.index + " " + self.parent_index + " " + self.func)

    def set_parent(self, parent_node):
        self.parent = parent_node
    
    def getLemma(self):
        return self.lemma
    
    def getPOS(self):
        return self.POS
    
    def getLemmaPOS(self):
        return str(self.getLemma() + " " + self.getPOS())
        
# classe PairAdj-Noun, ocurrencies
class Pair:
    "Pair class for storing Adj-Noun and #occurrences of these nodes in our corpus"
    
    def __init__(self, tup):
        if tup == None:
            sys.stderr.write("Error: no node for this node \n")
            return False
        else:
            self.tup = tup
            self.num = 1
    
    def __str__(self):
        return str(self.tup[0] + ";" + self.tup[1] + ";" + str(self.num))
    
    def getTup(self):
        return self.tup
    
    def add1(self):
        self.num = self.num + 1
        
    def getNum(self):
        return self.num
