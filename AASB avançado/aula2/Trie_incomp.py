# -*- coding: utf-8 -*-

class Trie:
    
    def __init__(self):
        self.nodes = { 0:{} } # dictionary
        self.num = 0
    
    def print_trie(self):
        for k in self.nodes.keys():
            print (k, "->" , self.nodes[k]) 
    
    def add_node(self, origin, symbol):
        self.num += 1
        self.nodes[origin][symbol] = self.num
        self.nodes[self.num] = {}
    
    def add_pattern(self, p):
        pos = 0
        node = 0
        while pos < len(p):
            if p[pos] not in self.nodes[node].keys():
                self.add_node(node, p[pos])
            node = self.nodes[node][p[pos]]
            pos+=1
            
    def trie_from_patterns(self, pats):
        for i in pats:
            self.add_pattern(i)
            
    def prefix_trie_match(self, text):
        match = ""
        node = 0
        for i in range(len(text)):
            if text[i] in self.nodes[node].keys():
                node = self.nodes[node][text[i]]
                match += text[i]
                if self.nodes[node] == {}:
                    return match
            else:
                return None
        return None
        
    def trie_matches(self, text):
        res = []
        for i in range(len(text)):
            m = self.prefix_trie_match(text[i:])
            if m != None:
                res.append((i,m))
        return res
        
          
def test():
    patterns = ["GAT", "CCT", "GAG"]
    t = Trie()
    t.trie_from_patterns(patterns)
    t.print_trie()

   
def test2():
    patterns = ["AGAGAT", "AGC", "AGTCC", "CAGAT", "CCTA", "GAGAT", "GAT", "TC"]
    t = Trie()
    t.trie_from_patterns(patterns)
    print (t.prefix_trie_match("GAGATCCTA"))
    print (t.trie_matches("GAGATCCTA"))
    
test()
print()
test2()
