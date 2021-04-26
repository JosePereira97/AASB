class MySeq:

    def __init__(self, seq, tipo="dna"): #função inicial da classe, guarda o tipo de seq e a seq em upper.
        self.seq = seq.upper()
        self.tipo = tipo

    def __len__(self): #return ao comprimento da seq
        return len(self.seq)

    def __getitem__(self, n): #devolve o aminiácido na posição n da seq
        return self.seq[n]

    def __getslice__(self, i, j): #devolve a seq entre a posição i e j
        return self.seq[i:j]

    def __str__(self): #devolve o tipo de seq e a seq a frente
        return self.tipo + ":" + self.seq

    def printseq(self): #dá print da seq
        print(self.seq)

    def alfabeto(self): #vai definiir o alfabeto consoante o tipo
        if (self.tipo == "dna"): #alfabeto de DNA
            return "ACGT"
        elif (self.tipo == "rna"): #alfabeto de RNA
            return "ACGU"
        elif (self.tipo == "protein"): #alfabeto de preoteinas
            return "ACDEFGHIKLMNPQRSTVWY"
        else:
            return None

    def valida(self): #vai validar se a seq, para ver se esta corresponde ao tipo inserido na classe
        alf = self.alfabeto()
        res = True
        i = 0
        while i < len(self.seq) and res:
            if self.seq[i] not in alf:
                res = False
            else:
                i += 1
        return res

    def validaER(self): #vai validar mas com expressões regulares
        import re
        if (self.tipo == "dna"):
            if re.search("[^ACTGactg]", self.seq) != None:
                return False
            else:
                return True
        elif (self.tipo == "rna"):
            if re.search("[^ACUGacug]", self.seq) != None:
                return False
            else:
                return True
        elif (self.tipo == "protein"):
            if re.search("[^ACDEFGHIKLMNPQRSTVWY_acdefghiklmnpqrstvwy]", self.seq) != None:
                return False
            else:
                return True
        else:
            return False

    def transcricao(self): #vai ocorrer a transcrição passar de uma seq de DNA para RNA
        if (self.tipo == "dna"):
            return MySeq(self.seq.upper().replace("T", "U"), "rna")
        else:
            return None

    def compInverso(self): #vai dar o complemento inverso da seq de DNA
        if (self.tipo != "dna"):
            return None
        comp = ""
        for c in self.seq.upper():
            if (c == 'A'):
                comp = "T" + comp
            elif (c == "T"):
                comp = "A" + comp
            elif (c == "G"):
                comp = "C" + comp
            elif (c == "C"):
                comp = "G" + comp
        return MySeq(comp)

    def traduzSeq(self, iniPos=0): #vai ocorrer a trdução da seq de DNA para proteina começando a tradução na posição iniPos
        if (self.tipo != "dna"):
            return None
        seqM = self.seq.upper()
        seqAA = ""
        for pos in range(iniPos, len(seqM)-2, 3):
            cod = seqM[pos:pos+3]
            seqAA += self.traduzCodao(cod)
        return MySeq(seqAA, "protein")

    def orfs(self): #vai fazer a tradução de todas as orfs possiveis numa seq de DNA e devolve uma lista com estas traduções
        if (self.tipo != "dna"):
            return None
        res = []
        res.append(self.traduzSeq(0))
        res.append(self.traduzSeq(1))
        res.append(self.traduzSeq(2))
        compinv = self.compInverso()
        res.append(compinv.traduzSeq(0))
        res.append(compinv.traduzSeq(1))
        res.append(compinv.traduzSeq(2))
        return res

    def traduzCodao(self, cod): #função responsável por pegar num codão e traduzilo para um aminoácido
        tc = {"GCT": "A", "GCC": "A", "GCA": "A", "TGT": "C", "TGC": "C",
              "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E", "TTT": "F", "TTC": "F",
              "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G", "CAT": "H", "CAC": "H",
              "ATA": "I", "ATT": "I", "ATC": "I",
              "AAA": "K", "AAG": "K",
              "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
              "ATG": "M", "AAT": "N", "AAC": "N",
              "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
              "CAA": "Q", "CAG": "Q",
              "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
              "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
              "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
              "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
              "TGG": "W",
              "TAT": "Y", "TAC": "Y",
              "TAA": "_", "TAG": "_", "TGA": "_"}
        if cod in tc:
            aa = tc[cod]
        else:
            aa = "X"  # errors marked with X
        return aa

    def traduzCodaoER(self, cod): #transforma codão em aminoácido mas com expressões regulares
        import re
        if re.search("GC.", cod):
            aa = "A"
        elif re.search("TG[TC]", cod):
            aa = "C"
        elif re.search("GA[TC]", cod):
            aa = "D"
        elif re.search("GA[AG]", cod):
            aa = "E"
        elif re.search("TT[TC]", cod):
            aa = "F"
        elif re.search("GG.", cod):
            aa = "G"
        elif re.search("CA[TC]", cod):
            aa = "H"
        elif re.search("AT[TCA]", cod):
            aa = "I"
        elif re.search("AA[AG]", cod):
            aa = "K"
        elif re.search("TT[AG]|CT.", cod):
            aa = "L"
        elif re.search("ATG", cod):
            aa = "M"
        elif re.search("AA[TC]", cod):
            aa = "N"
        elif re.search("CC.", cod):
            aa = "P"
        elif re.search("CA[AG]", cod):
            aa = "Q"
        elif re.search("CG.|AG[AG]", cod):
            aa = "R"
        elif re.search("TC.|AG[TC]", cod):
            aa = "S"
        elif re.search("AC.", cod):
            aa = "T"
        elif re.search("GT.", cod):
            aa = "V"
        elif re.search("TGG", cod):
            aa = "W"
        elif re.search("TA[TC]", cod):
            aa = "Y"
        elif re.search("TA[AG]|TGA", cod):
            aa = "_"
        else:
            aa = None
        return aa

    def maiorProteina(self): #vai procurar a maior proteina presente numa seq proteica, sendo que uma proteina começa em M e acaba em _
        if (self.tipo != "protein"):
            return None
        seqAA = self.seq.upper()
        protAtual = ""
        maiorprot = ""
        for aa in seqAA:
            if aa == "_":
                if len(protAtual) > len(maiorprot):
                    maiorprot = protAtual
                protAtual = ""
            else:
                if len(protAtual) > 0 or aa == "M":
                    protAtual += aa
        return MySeq(maiorprot, "protein")

    def maiorProteinaER(self): #vai procurar a maior proteina mas em expressões regulares
        import re
        if (self.tipo != "protein"):
            return None
        mos = re.finditer("M[^_]*_", self.seq)
        sizem = 0
        lprot = ""
        for x in mos:
            ini = x.span()[0]
            fin = x.span()[1]
            s = fin - ini + 1
            if s > sizem:
                lprot = x.group()
                sizem = s
        return MySeq(lprot, "protein")

    def todasProteinas(self): #vai realizar a construção de todas as proteinas
        if (self.tipo != "protein"):
            return None
        seqAA = self.seq.upper()
        protsAtuais = []
        proteinas = []
        for aa in seqAA:
            if aa == "_":
                if protsAtuais:
                    for p in protsAtuais:
                        proteinas.append(MySeq(p, "protein"))
                    protsAtuais = []
            else:
                if aa == "M": #por cada M que encontrar vai inicializar uma nova proteina
                    protsAtuais.append("")
                for i in range(len(protsAtuais)): #adicionar os aminoacidos as proteinas correspondentes
                    protsAtuais[i] += aa

        return proteinas

    def maiorProteinaORFs(self): #vai encontrar a maior proteina em todas as orfs
        if (self.tipo != "dna"):
            return None
        larg = MySeq("", "protein")
        for orf in self.orfs():
            prot = orf.maiorProteinaER()
            if len(prot.seq) > len(larg.seq):
                larg = prot
        return larg


# teste
def teste():
    seq_dna = input("Sequencia:")
    s1 = MySeq(seq_dna)
    s1.printseq()

    if s1.validaER():
        print("Sequencia valida")
        print("Transcricao: ")
        s1.transcricao().printseq()
        print("Complemento inverso:")
        s1.compInverso().printseq()
        print("Traducao: ")
        s1.traduzSeq().printseq()
        print("ORFs:")
        for orf in s1.orfs():
            orf.printseq()
        print("Maior proteina nas ORFs:")
        s1.maiorProteinaORFs().printseq()
    else:
        print("Sequencia invalida")


if __name__ == "__main__":
    teste()
