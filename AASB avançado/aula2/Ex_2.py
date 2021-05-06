# -*- coding: utf-8 -*-

class SuffixTree:

    def __init__(self):
        self.nodes = {0: (-1, {})} 
        self.num = 0
        self.seq1 = ''
        self.seq2 = ''

    def unpack(self, k):
        if self.nodes[k][0] == -1:
            m = self.nodes[k][0]
            n = ''
        else:
            m, n = self.nodes[k][0]
        return m, n


    def print_tree(self):
        for k in self.nodes.keys():
            m, n = self.unpack(k)

            if m < 0:
                print(k, "->", self.nodes[k][1])
            else:
                print(k, ":", m, n)

    def add_node(self, origin, symbol, leafnum=-1):
        self.num += 1 
        self.nodes[origin][1][
            symbol] = self.num  
        self.nodes[self.num] = (leafnum, {}) 

    def add_suffix(self, p, sufnum): 
        pos = 0
        node = 0
        while pos < len(p): 
            if p[pos] not in self.nodes[node][1].keys(): 
                if pos == len(p) - 1:  
                    self.add_node(node, p[pos], sufnum)  
                else:
                    self.add_node(node, p[pos])  
            node = self.nodes[node][1][p[pos]] 
            pos += 1  

    def suffix_tree_from_seq(self, seq1, seq2):
        seq1 = seq1 + "$"
        seq2 = seq2 + "#"
        self.seq1 = seq1
        self.seq2 = seq2
        for i in range(len(seq1)): 
            self.add_suffix(seq1[i:], (0, i))
        for i in range(len(seq2)):  
            self.add_suffix(seq2[i:], (1, i))


    def find_pattern(self, pattern):
        node = 0
        for pos in range(len(pattern)):  
            if pattern[pos] in self.nodes[node][1].keys(): 
                node = self.nodes[node][1][
                    pattern[pos]]  
            else:
                return None
        return self.get_leafes_below(node)  

    def get_leafes_below(self, node):
        final1 = []
        final0 = []  
        m, n = self.unpack(node)
        if m >= 0:  
            if m == 0:
                final0.append(n)
            else:
                final1.append(n)
        else:  
            for k in self.nodes[node][1].keys(): 
                newnode = self.nodes[node][1][k]  
                l, r = self.get_leafes_below(newnode) 
                final0.extend(l)
                final1.extend(r) 
        return(final0, final1)

    def largestCommonSubstring(self):
        suf1 = []
        suf2 = []
        m = len(self.seq1)
        f = 0
        while m > 0:
            suf1.append(self.seq1[:-f])
            f = f + 1
            m = m - 1
        g = len(self.seq2)
        r = 0
        while g > 0:
            suf2.append(self.seq2[:-f])
            r = r + 1
            g = g - 1
        string1 = ''
        string2 = ''
        score = 0
        for i in suf1:
            for l in suf2:
                newscore = 0
                count = 0
                cenas = 0
                if len(i) > len(l):
                    count = len(l)
                else:
                    count = len(i)
                while cenas < count:
                    if i[cenas] == l[cenas]:
                        newscore += 1
                    cenas += 1
                if newscore > score:
                    string1 = i
                    string2 = l
                    score = newscore
        finalmatch = ''
        count2 = 0
        while count2 < len(string1) and count2 < len(string2):
            if string1[count2] == string2[count2]:
                finalmatch += string1[count2]
            count2 += 1
        print(finalmatch)




def test():
    seq1 = "TACTA"
    seq2 = "TAAGGTACTAC"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq1, seq2)
    st.print_tree()
    print(st.find_pattern("TA"))
    print(st.find_pattern("ACG"))


def test2():
    
    st = SuffixTree()
    st.suffix_tree_from_seq(seq1, seq2)
    print(st.find_pattern("TA"))
    st.largestCommonSubstring()


test()
print()
test2()




