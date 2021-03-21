# -*- coding: utf-8 -*-

class SuffixTree:

    def __init__(self):
        self.nodes = {0: (-1, {})} 
        self.num = 0
        self.seq1 = ''
        self.seq2 = ''

    def unpack(self, k): #função que vai dar o unpack do tupulo que se encontra nas leafs
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
        self.seq1 = seq1 #vamos adicionar as seqs ao init
        self.seq2 = seq2
        for i in range(len(seq1)): 
            self.add_suffix(seq1[i:], (0, i)) #vamos adicionar as leafs o 0, ou 1 correspondente a seq e o i que é o numero da letra onde começou
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

    def get_leafes_below(self, node): #alterar mos a get leafes para 2 seq, vai fazer o mesmo mas para 2 listas diferentes onde vai fazer consoante as suas seq
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

    def largestCommonSubstring(self): #vai correr as duas seq e vai ver quais os aonde é que existe um match maior onde as duas seq e dá isso como output
        finalmatch = ''
        finalcount = 0
        for i in range(len(self.seq1)):
            count = 0
            match = ''
            for l in self.seq2:
                if self.seq1[i] == l:
                    match+=self.seq1[i]
                    count+=1
                    i+=1
                else:
                    if count > finalcount:
                        finalmatch = match
                        finalcount = count
                    match = ''
                    count = 0
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
    seq1 = "GADGGFGGGGGGGGGHLDHOFOIGJKCTA"
    seq2 = "TAAGADGGFGGGGGGGGGHLDHOFOIGJKCTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq1, seq2)
    print(st.find_pattern("TA"))
    st.largestCommonSubstring()


test()
print()
test2()




