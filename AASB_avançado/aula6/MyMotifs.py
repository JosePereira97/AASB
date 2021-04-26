def createMatZeros(nl, nc): #criar uma matriz de zeros
    res = []
    for _ in range(0, nl):
        res.append([0]*nc)
    return res


def printMat(mat): #print a cada linha da matriz
    for i in range(0, len(mat)):
        print(mat[i])


class MyMotifs:

    def __init__(self, seqs=[], pwm=[], alphabet=None):
        if seqs:
            self.size = len(seqs[0]) #comprimento dos motifs
            self.seqs = seqs  # objetos classe MySeq
            self.alphabet = seqs[0].alfabeto() #alfabeto das seqs
            self.doCounts() #criar matriz de contagens
            self.createPWM() #criar matriz de probabilidades
        else:
            self.pwm = pwm
            self.size = len(pwm[0])
            self.alphabet = alphabet

    def __len__(self):
        return self.size #return do comprimento dos motifs

    def doCounts(self): #vai criar a matriz de contagens
        self.counts = createMatZeros(len(self.alphabet), self.size)
        for s in self.seqs:
            for i in range(self.size):
                lin = self.alphabet.index(s[i])
                self.counts[lin][i] += 1

    def createPWM(self): #vai criar a matriz de probabilidades
        if self.counts == None:
            self.doCounts()
        self.pwm = createMatZeros(len(self.alphabet), self.size)
        for i in range(len(self.alphabet)):
            for j in range(self.size):
                self.pwm[i][j] = float(self.counts[i][j]) / len(self.seqs)

    def consensus(self): #rai arranjar o consensus a partir da count
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet)):
                if self.counts[i][j] > maxcol:
                    maxcol = self.counts[i][j]
                    maxcoli = i
            res += self.alphabet[maxcoli]
        return res

    def maskedConsensus(self): #vai encontrar o masked concensus que implica ter mais de 50%
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet)):
                if self.counts[i][j] > maxcol:
                    maxcol = self.counts[i][j]
                    maxcoli = i
            if maxcol > len(self.seqs) / 2:
                res += self.alphabet[maxcoli]
            else:
                res += "-"
        return res

    def probabSeq(self, seq): #vai calcular a probabilidade de um seq consoante uma PWM
        res = 1.0
        for i in range(self.size):
            lin = self.alphabet.index(seq[i])
            res *= self.pwm[lin][i]
        return res

    def probAllPositions(self, seq): #
        res = []
        for _ in range(len(seq)-self.size+1): #vai ver todas as probabilidades de todos os motifs possiveis de uma seq
            res.append(self.probabSeq(seq[_:_ + self.size])) #//corrigido//
        return res

    def mostProbableSeq(self, seq): #vai procurar numa seq só o motif com mais probabilidade de acontecer
        maximo = -1.0
        maxind = -1
        for k in range(len(seq)-self.size):
            p = self.probabSeq(seq[k:k + self.size])
            if(p > maximo):
                maximo = p
                maxind = k
        return maxind


def test():
    # test
    from MySeq import MySeq
    seq1 = MySeq("AAAGTT")
    seq2 = MySeq("CACGTG")
    seq3 = MySeq("TTGGGT")
    seq4 = MySeq("GACCGT")
    seq5 = MySeq("AACCAT")
    seq6 = MySeq("AACCCT")
    seq7 = MySeq("AAACCT")
    seq8 = MySeq("GAACCT")
    lseqs = [seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8]
    motifs = MyMotifs(lseqs)
    printMat(motifs.counts)
    printMat(motifs.pwm)
    print(motifs.alphabet)

    print(motifs.probabSeq("AAACCT"))
    print(motifs.probabSeq("ATACAG"))
    print(motifs.mostProbableSeq("CTATAAACCTTACATC"))

    print(motifs.consensus())
    print(motifs.maskedConsensus())


if __name__ == '__main__':
    test()
