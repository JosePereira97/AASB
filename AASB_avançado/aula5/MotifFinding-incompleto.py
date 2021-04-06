# -*- coding: utf-8 -*-

from MySeq import MySeq
from MyMotifs import MyMotifs

class MotifFinding:
    
    def __init__(self, size = 8, seqs = None):
        self.motifSize = size
        if (seqs != None):
            self.seqs = seqs
            self.alphabet = seqs[0].alfabeto()
        else:
            self.seqs = []
                    
    def __len__ (self):
        return len(self.seqs)
    
    def __getitem__(self, n):
        return self.seqs[n]
    
    def seqSize (self, i):
        return len(self.seqs[i])
    
    def readFile(self, fic, t):
        for s in open(fic, "r"):
            self.seqs.append(MySeq(s.strip().upper(),t))
        self.alphabet = self.seqs[0].alfabeto()
        
        
    def createMotifFromIndexes(self, indexes):
        pseqs = []
        for i,ind in enumerate(indexes):
            pseqs.append( MySeq(self.seqs[i][ind:(ind+self.motifSize)], self.seqs[i].tipo) )
        return MyMotifs(pseqs)
        
        
    # SCORES
        
    def score(self, s):
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts()
        mat = motif.counts
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score += maxcol
        return score
   
    def scoreMult(self, s):
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        motif.createPWM()
        mat = motif.pwm
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score *= maxcol
        return score     
       
    # EXHAUSTIVE SEARCH
       
    def nextSol (self, s):
        nextS = [0]*len(s)
        pos = len(s) - 1     
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if (pos < 0): 
            nextS = None
        else:
            for i in range(pos): 
                nextS[i] = s[i]
            nextS[pos] = s[pos]+1
            for i in range(pos+1, len(s)):
                nextS[i] = 0
        return nextS
        
    def exhaustiveSearch(self):
        melhorScore = -1
        res = []
        s = [0]* len(self.seqs)
        while (s!= None):
            sc = self.score(s)
            if (sc > melhorScore):
                melhorScore = sc
                res = s
            s = self.nextSol(s)
        return res #O resultado são as posições inicais que vão maximizar o score
     
    # BRANCH AND BOUND     
     
    def nextVertex (self, s):
        res =  []
        if len(s) < len(self.seqs): # internal node -> down one level
            for i in range(len(s)): 
                res.append(s[i])
            res.append(0)
        else: # bypass
            pos = len(s)-1 
            while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
                pos -= 1
            if pos < 0: res = None # last solution
            else:
                for i in range(pos): res.append(s[i])
                res.append(s[pos]+1)
        return res
    
    
    def bypass (self, s):
        res =  []
        pos = len(s) -1
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0: res = None 
        else:
            for i in range(pos): res.append(s[i])
            res.append(s[pos]+1)
        return res
        
    def branchAndBound (self):
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0]*size
        while s != None:
            if len(s) < size:
                optimScore = self.score(s) + (size-len(s)) * self.motifSize
                if optimScore < melhorScore: s = self.bypass(s)
                else: s = self.nextVertex(s)
            else:
                sc = self.score(s)
                if sc > melhorScore:
                    melhorScore = sc
                    melhorMotif  = s
                s = self.nextVertex(s)
        return melhorMotif

    # Consensus (heuristic)
  
    def heuristicConsensus(self):
        """ Procura as posições para o motif nas duas primeiras sequências """ 
        mf = MotifFinding(self.motifSize, self.seqs[:2]) #Procura exaustiva das duas primeiras sequências
        s = mf.exhaustiveSearch() #Exemplo: (1, 3) -> 1 corresponde à primeira posição do motif na sequência e o 3 a segunda posição
        for a in range(2, len(self.seqs)): #Avalia a melhor posição para cada uma das sequências, guardando-a (maximiza o score)
            s.append(0)
            melhorScore = -1 
            melhorPosition = 0
            for b in range(self.seqSize(a) - self.motifSize + 1):
                s[a] = b 
                scoreatual = self.score(s)
                if scoreatual > melhorScore:
                    melhorScore = scoreatual
                    melhorPosition = b
                s[a] = melhorPosition
        return s

    # Consensus (heuristic)

    def heuristicStochastic (self):
        from random import randint
        s = [0] * len(self.seqs) #Gerar um vetor aleatória com o mesmo tamnho do número de sequências
        #Passo 1: inicia todas as posições com valores aleatórios 
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize) #Randint (A, B) retorna um valor x que é: A <= x <= B
        #Passo 2
        melhorscore = self.score(s)
        improve = True
        while improve:
            motif = self.createMotifFromIndexes(s) #Constrói o perfil com base nas posições iniciais s
            motif.createPWM()
            #Passo 3
            for i in range(len(self.seqs)): #Avalia a melhor posição inicial para cada sequência com base no perfil
                s[i] = motif.mostProbableSeq(self.seqs[i])
            #Passo 4
            #Verifica se houve alguma melhoria
            scr = self.score(s)
            if scr > melhorscore:
                melhorscore = scr
            else: 
                improve = False
        return s

    # Gibbs sampling 

    def gibbs (self):
        from random import randint
        s = [0] * len(self.seqs)
        #Passo 1
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize)
        melhorscore = self.score(s)
        improve = True
        while improve:
            #Passo 2: selecionar uma das sequência aleatoriamente
            seq_idx = self.seqs[randint(0, len(self.seqs) - 1)]
            #Passo 3: criar um perfil que não contenha a sequência aleatória
            seq = self.seqs().pop(seq_idx) #Removemos a sequência da lista
            spartial = s.copy().remove(seq_idx) #Removemos a referência do vetor de posições iniciais
            motif = self.createMotifFromIndexes(spartial) #Criar o perfil sem a sequência removida
            motif.createPWM()
            s[seq_idx] = motif.mostProbableSeq(seq) #Melhor posição inicial da sequência considerando o perfil
            self.seqs.insert(seq_idx, seq)
            #Passo 4
            scr = self.score(s)
            if scr > melhorscore: 
                melhorscore = scr
            else: 
                improve = False
        return s

    def roulette(self, f):
        from random import random
        tot = 0.0
        for x in f: tot += (0.01+x)
        val = random()* tot
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        return ind-1

# tests

def test1():  
    sm = MotifFinding()
    sm.readFile('C:/Users/josep/OneDrive/Documentos/GitHub/AASB/AASB_avançado/aula5/exemploMotifs.txt', 'dna')
    sol = [25,20,2,55,59]
    sa = sm.score(sol)
    print(sa)
    scm = sm.scoreMult(sol)
    print(scm)

def test2():
    print ("Test exhaustive:")
    seq1 = MySeq("ATAGAGCTGA","dna")
    seq2 = MySeq("ACGTAGATGA","dna")
    seq3 = MySeq("AAGATAGGGG","dna")
    mf = MotifFinding(3, [seq1,seq2,seq3])
    sol = mf.exhaustiveSearch()
    print ("Solution", sol)
    print ("Score: ", mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

    print ("Branch and Bound:")
    sol2 = mf.branchAndBound()
    print ("Solution: " , sol2)
    print ("Score:" , mf.score(sol2))
    print("Consensus:", mf.createMotifFromIndexes(sol2).consensus())
    
    print ("Heuristic consensus: ")
    sol1 = mf.heuristicConsensus()
    print ("Solution: " , sol1)
    print ("Score:" , mf.score(sol1))

def test3():
    mf = MotifFinding()
    mf.readFile("C:/Users/josep/OneDrive/Documentos/GitHub/AASB/AASB_avançado/aula5/exemploMotifs.txt","dna")
    print ("Branch and Bound:")
    sol = mf.branchAndBound()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

def test4():
    mf = MotifFinding()
    mf.readFile("C:/Users/josep/OneDrive/Documentos/GitHub/AASB/AASB_avançado/aula5/exemploMotifs.txt","dna")
    print("Heuristic stochastic")
    sol = mf.heuristicStochastic()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print ("Score mult:" , mf.scoreMult(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())
    sol2 = mf.gibbs()
    print ("Score:" , mf.score(sol2))
    print ("Score mult:" , mf.scoreMult(sol2))
test1()
print('-------------------')
test2()
print('-------------------')
test3()
print('-------------------')
test4()
