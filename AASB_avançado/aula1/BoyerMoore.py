# -*- coding: utf-8 -*-

class BoyerMoore:
    
    def __init__(self, alphabet, pattern):
        self.alphabet = alphabet
        self.pattern = pattern
        self.preprocess()

    def preprocess(self):
        self.process_bcr()
        self.process_gsr()
        
    def process_bcr(self):
        self.occ = {}
        for c in self.alphabet: #todos os valores do alfabeto ficam com -1 no dicionário
            self.occ[c] = -1
        for i in range(len(self.pattern)): #muda a posição do dicionário para das letras do pattern para a ultima
            k = self.pattern[i]
            self.occ[k] = i
        print(self.occ)

            
    def process_gsr(self):
        self.f = [0] * (len(self.pattern) + 1) #uma lista de 0 igual ao comprimento do padrão
        self.s = [0] * (len(self.pattern) + 1)
        i = len(self.pattern)
        j = len(self.pattern) + 1
        self.f[i] = j
        while i > 0:
            while j <= len(self.pattern) and self.pattern[i - 1] != self.pattern[j - 1]: #vai cirar a lista e de quantas casas pode avançar errando em certas posições do padrão
                if self.s[j] == 0:
                    self.s[j] = j - i
                j = self.f[j]
            i = i - 1
            j = j - 1
            self.f[i] = j
        j = self.f[0]

        for i in range(len(self.pattern)):
            if self.s[i] == 0:
                self.s[i] = j
            if i == j:
                j = self.f[j]
        
        
    def search_pattern(self, text):
        res = []
        i = 0  # posição na sequencia
        while i <= len(text) - len(self.pattern):
            j = len(self.pattern) - 1
            while j >= 0 and self.pattern[j] == text[j + i]:
                j = j - 1
            if j < 0:
                res.append(i)
                i = i + self.s[0]
            else:
                c = text[j + i]
                i += max(self.s[j + 1], j - self.occ[c]) #avançar no texto dependendo onde a reconstrução do padrão parou



        return res

def test():
    bm = BoyerMoore("ACTG", "ACCA")
    print (bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC"))

test()

# result: [5, 13, 23, 37]
            
