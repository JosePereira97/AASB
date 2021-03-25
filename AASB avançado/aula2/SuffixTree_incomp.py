# -*- coding: utf-8 -*-

class SuffixTree:
    
    def __init__(self):
        self.nodes = { 0:(-1,{}) } # root node
        self.num = 0
        self.seq = ''
    
    def print_tree(self):
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0:
                print (k, "->", self.nodes[k][1]) 
            else:
                print (k, ":", self.nodes[k][0])
                
    def add_node(self, origin, symbol, leafnum = -1):
        self.num += 1
        self.nodes[origin][1][symbol] = self.num
        self.nodes[self.num] = (leafnum,{})
        
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
    
    def suffix_tree_from_seq(self, text):
        self.seq = text
        t = text+"$"
        for i in range(len(t)):
            self.add_suffix(t[i:], i)
            
    def find_pattern(self, pattern):
        pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():
                node = self.nodes[node][1][pattern[pos]]
                pos += 1
            else:
                return None
        return self.get_leafes_below(node)
        

    def get_leafes_below(self, node):
        res = []
        if self.nodes[node][0] >=0: 
            res.append(self.nodes[node][0])            
        else:
            for k in self.nodes[node][1].keys():
                newnode = self.nodes[node][1][k]
                leafes = self.get_leafes_below(newnode)
                res.extend(leafes)
        return res
    
    def nodes_below(self, node): #Ex1a)
        if node >= len(self.nodes):
            return None
        else:
            id_nodes = list(self.nodes[node][1].values())
            for i in id_nodes:
                id_nodes.extend(list(self.nodes[i][1].values()))
            return id_nodes

    def matches_prefix(self, prefix):
        print(self.seq)

        def function(i):
            lista = []
            if i > 0: #a function ele vai correr de volta a Root e reconstruir as strings a partir das leafs
                for n, f in self.nodes.items():
                    for m in list(f[1].values()):
                        if i == m:
                            for key, value in f[1].items():
                                if i == value:
                                    lista.extend(key)
                                    x = function(n)
                                    lista.extend(x)
            else:
                for n, f in self.nodes.items():
                    for m in list(f[1].values()):
                        if i == m:
                            for key, value in f[1].items():
                                if i == value:
                                    lista.append(key)
            
            return lista

        ns = SuffixTree.find_pattern(self, prefix)

        if ns == None or ns == []: #vai vere se existem leaf belows com o prefix
            return None
        else:
            matches = []
            matches.append(prefix) #vai adicionar o prefix pois é match
            for i in ns:
                for key, value in self.nodes.items(): #vamos a todos os items do dicionário
                    if i == value[0]: #para encontrar o value que obtivemos das leafs
                        x = function(key) #vamos correr a fuction
                        x.reverse() #vamos reverter a list
                        del(x[-1]) #retira-se o dólar
                        string = ''.join(x) #transforma em string
                        matches.append(string) # e adicionas a string a lista
            matches = sorted(matches, key =len, reverse = True) # vamos fazer sorted da lista
            matchesfinal = matches.copy() #vamos fazer uma copy do valore da lista para n alterar mos a matches
            for i in range(len(matches)): #vamos correr todos os valores da lista match
                m = len(matches[i])
                f = 1
                while m > len(prefix) + 1: # e com este ciclo while vamos cortar letra a letra das seq do match
                    matchesfinal.append(matches[i][:-f])
                    m = m -1
                    f = f + 1
            return(list(dict.fromkeys(matchesfinal))) #remove-mos os duplicados

            





def test():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    print (st.find_pattern("TA"))
    print (st.find_pattern("ACG"))
    print(st.nodes_below(2))

def test2():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    print (st.find_pattern("TA"))
    print(st.matches_prefix('TA'))

test()
print()
test2()
        
            
    
    
