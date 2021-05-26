# Ex1:
#a, b)
import csv 
csv_file = {}
with open('nome do fichheiro') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    csv_reader.__next__()
    for row in csv_reader:
        components = []
        for element in range(1, len(row)):
            components.append(row[element])
        csv_file[row[0]] = components

resultado_media = {}
for i in csv_file:
    if 'HIST' in  i and i != 'gene':
        total = 0
        n = 0
        for j in i:
            total = total + int(j)
            n = n  + 1
        resultado_media[i] = total/n


#c)
diferenca_ordenada = {}

for i in csv_file:
    if i !='gene':
        difA = csv_file[i][0] - csv_file[i][1]
        difB = csv_file[i][2] - csv_file[i][3]
        if difA > difB:
            diferenca_ordenada[csv_file[i]] = [difA, difB]
        else:
            diferenca_ordenada[csv_file[i]] = [difB, difA]

#d)
for i in csv_file:
    if 'HIST' in i:
        values = csv_file[i]
        del csv_file[i]
        i.replace('HIST', 'hist')
        csv_file[i] = values

        #(10^9 * reads) / (readstotais*o tamanho da seq))
#EX2 a) (10^9 * 100)/(10000*1000) = 100000
        #(10^9 *100)/(15000*3000) = 66666.(6)
        #Pelo resultado podemos concluir que o que tem maior expressão é o A
    
    # b) (10^9 *100)/(10000*1000) = 100000
        #(10^9 *260)/(10000*3000) = 
        #  pelo resultado podemos concluir que o gene g00017 tem mais expressão

        #c) para o gene g0017 a condição A é a maior
        #(10^9 *200)/(15000*3000) = 
        #para o gene g0018 a condição A é o que tem a expressão mais alta

#EX3  a) temos substituições como na primeira linha, deleção presenta na primeira linha, inserção na 4 linha. (Inversão alterar a ordem)
    #b)# DP = 5; QUAL = 70.5
        # DP = 8; QUAL = 52

        # DP = 10; QUAL = 28.5

        # DP = 28; QUAL = 7.35

        # DP = 25; QUAL = 4.42

        # DP = 22; QUAL = 66

        # DP = 9; QUAL = 33.5

        # DP = 5; QUAL = 7.35

    #c)
#import vcf
vcf = False
vcffile = {}
vcf_reader = vcf.Reader('filename')
for i in vcf_reader:
    components = []
    for elem in range(1,len(i)):
        components.append(elem)
    vcffile[i] = components

insercoes = []
for i in vcffile:
    if i != '#CHROM' and len(vcffile[i][3])>len(vcffile[i][2]):
        insercoes.append(vcffile[i][3]-vcffile[i][2])
insercoes.sort()

        #d)
substituicao = 0
insercao = 0
delecao = 0
inversao = 0
for i in vcffile:
    if i != '#CHROM':
        if len(vcffile[i][3]) == len(vcffile[i][2]) and vcffile[i][3] != vcffile[i][2]:
            substituicao = substituicao + int(vcffile[i][6].split('=')[1])
        elif len(vcffile[i][3])>len(vcffile[i][2]):
            insercao = insercao + int(vcffile[i][6].split('=')[1])
        elif len(vcffile[i][3])<len(vcffile[i][2]):
            delecao = delecao + int(vcffile[i][6].split('=')[1])
        else:
            inversao = inversao + int(vcffile[i][6].split('=')[1])

#4
#a) 

# "Scale-free" : as distribuições dos graus aproxima a power law; isto implica que existem poucos nós com muitas ligações e muitos nós com poucas ligações.

# "Small-world" : o valor de L (comprimento médio dos caminhos mais curtos) é pequeno, o que significa que os nós estarão mais pertos do que o que seria expectável.

# Hierárquica : composta por módulos com a maioria de nós de baixo grau altamente ligados entre si por nós de grau mais elevado (esperado no caso, por exemplo, de uma rede metabólica).

#b)
#'scale-free' : mean_degree, se os vértices tiverem um média de ligações baixa implica que é um scale-free

# 'small-world' : mean_distances, se a média de distâncias entre cada vértice for baixa é um amll-worls

# hierásquica : clustering_coef, que vai calcular a probabilidade de um nó ser agrupado

#5
#Class - MyGraph
def isClique(self,listNodes):
    for node in listNodes:
        lista = self.get_adjacents(node)
        for i in listNodes:
            if i != node:
                if i not in lista:
                    return False
    return True

#6
#a)
def eIsolado (self, idNo):
    adj = self.get_adjacents(idNO)
    if adj:
        return False
    else:
        return True

#b)
def nosIsolados(self):
    badjoras = []
    for i in self.graph.keys():
        Isisolated = eIsolado(i)
        if Isisolated == True:
            badjoras.append(i)
    return badjoras

#7)
#a)
def centralidade_de_proximidade_vertice(self, v): #A centralidade de proximidade d eum vértice é dado pelo reciproco da soma das suas distâncias aos demain nós
    total_ligacoes = 0
    total_ligacoes_com_vertice = 0
    for i in self.graph.keys(): 
        for j in self.graph.keys(): 
            if i != j and i != v and j != v:
                caminho_mais_curto = self.shortest_path(i, j)
                if caminho_mais_curto is not None:
                    total_ligacoes = total_ligacoes + 1
                    if v in caminho_mais_curto: 
                        total_ligacoes_com_vertice = total_ligacoes_com_vertice + 1
    proximidade = total_ligacoes_com_vertice / total_ligacoes
    return proximidade

#b)
def centralidade_dos_vertices(self):
    lista = []
    for i in self.graph.keys():
        badjoras = self.centralidade_de_proximidade_vertice(i)
        lista.append(i, badjoras)
    lista.sort(key = lambda x:x[1], reverse=True)
    return lista

#c) São importantes pois os metabolitos com um maior numero de centralidade indicam que são essencias para essa rede metabólica, o que indica que se estes não exestirem a rede metabólica pode n funcionar

#8)
#d)
def centralidade_closeness_vertice(self,v): #a centralidade de um vertice a outros vertices é calculado por o numero de nós que passam am v -1 a dividir pelas distâncias totais 
    distancia_nos = self.reachable_with_dist(v)
    total = 0
    N = 0
    for i, d in distancia_nos:
        total = total + d
        N+=1
    closeness_vertice = float((N-1)/total)
    return(closeness_vertice)

#e)
def centralidade_closeness_vertice(self,v):
    lista = []
    for i in self.graph.keys():
        badjoras = self.centraçidade_closeness_vertice(v)
        lista.append(i, badjoras)
    lista.sort(key = lambda x:x[1], reverse=True)
    return lista

#9)

#a)Ás vezes com erros de sequenciação ou falhas na sequenciação ou coisas muito repetitivas existe o problema que esses fregamentos podem ser demasiado grande. Ao partir em fragementos conseguimos ter uma maior representação dessas zonas no entanto isto trás um problema com a complexidade porque temos um maior numero de fragmentos a processar.

#b) class deBruijn
def composition(k, seq):
    res = []
    for i in range(len(seq)-k+1): #vamos dar append de todos os fragmentos da seq de tamanho k
        res.append(seq[i:i+k])
    res.sort() #vamos organizar a lista e devolver a lista
    return res

#c)
def ex9c (self,k, seq):
    lista = []
    for i in seq:
        lista.extend(composition(k,i))
    npm = self.create_deBruijn_graph(lista)
    path = npm.eulerian_path()
    return path

#10)
#a) Ao ocorrer erros, vamos perdes as ligações verdadeiras o que pode causar problemas na recontrução dos path e a trabalhar com o grafo

#b)
def fragmentosErro(self, listaFragmentos):
    lista_de_erros = []
    contagens = {}
    for i in listaFragmentos:
        if i in contagens:
            contagens[i] =+1
        else:
            contagens[i] = 1
    for i in contagens.keys():
        for j in contagens.keys():
            if contagens[i] == 1 and i!=j:
                dif = 0
                for char in range(len(i)):
                    if i[char] != j[char]:
                        dif = dif + 1
                if dif == 1 and contagens[j] > 1:
                    lista_de_erros.append(i)
    return i

#11)
#a) class BWT
def test():
    seq ='tactactac$'
    bw = BWT(seq)
    print(bw.bwt)
test()

#b)
def inverse_bwt(self):
    firstcol = self.get_first_col()
    res = ""
    c = "$" 
    occ = 1
    for i in range(len(self.bwt)):
        pos = find_ith_occ(self.bwt, c, occ)
        c = firstcol[pos]
        occ = 1
        k = pos-1
        while firstcol[k] == c and k >= 0:
            occ += 1
            k -= 1
        res += c
    return res

#12)
#a) class MetabolicNetwork
def final_metabolites(self):
    final = []
    for i in self.graph.keys():
        if i in self.node_types['metabolite'] and self.graph[i] == []:
            final.append(i)
    return final

#b)
def shortest_path_product(self, initial_metabolites, target_product):
    if target_product in initial_metabolites: 
        return []
    metabs = {}
    for m in initial_metabolites: 
        metabs[m] = []
    reacs = self.active_reactions(initial_metabolites)
    cont = True
    while cont:
        cont = False
        for r in reacs:
            sucs = self.get_successors(r)
            preds = self.get_predecessors(r)
            for s in sucs:
                if s not in metabs: 
                    previous = []
                    for p in preds:
                        for rr in metabs[p]:
                            if rr not in previous: previous.append(rr)
                    metabs[s] = previous + [r]
                    if s == target_product: 
                        return metabs[s]
                    cont = True
        if cont: 
            reacs = self.active_reactions(metabs.keys())
    return None

def active_reactions(self, active_metabolites):
    if self.net_type != "metabolite-reaction" or not self.split_rev:
        return None
    res = []
    for v in self.node_types['reaction']:
        preds = set(self.get_predecessors(v)) #set uma lista sem duplicados
        if len(preds)>0 and preds.issubset(set(active_metabolites)):
            res.append(v)
    return res
def produced_metabolites(self, active_reactions):
    res = []
    for r in active_reactions:
        sucs = self.get_successors(r)
        for s in sucs:
            if s not in res: res.append(s)
    return res

#13)
#a)

def graph_components(self):
    if not self.is_connected() or not self.check_balanced_graph(): 
        return None
    edges_visit = list(self.get_edges())#lista com os arcos do grafo
    res = []#abrir lista para ciclo
    while edges_visit:#enquanto o edges_visit tiver elementos(??)
        pair = edges_visit[0]#primeiro arco
        i = 1#contagem
        if res != []:#se o res nao estiver vazio
            while pair[0] not in res[len(res)-1]:#se o primeiro arco nao estiver em res (ou seja, nao estiver 'coberto')
                pair = edges_visit[i]#vai buscar o arco i
                i = i + 1#somar 1 ao i
        edges_visit.remove(pair)#remover o arco
        start, nxt = pair
        cycle = [start, nxt]
        while nxt != start:#constroi os varios ciclos
            for suc in self.graph[nxt]:
                if (nxt, suc) in edges_visit:
                    pair = (nxt,suc)
                    nxt = suc
                    cycle.append(nxt)
                    edges_visit.remove(pair)
        res.append(cycle)
    return res

#b)
def graph_components_cenas(self):
    components = self.graph_components()
    organizes_components = sorted(components, key = len, reverse=True)
    for i in organizes_components:
        m = tries_DeBruijn(i)
        if m == None:
            pass
        else:
            return m

def tries_DeBruijn(frags):
    # try with original size
    dbgr = DeBruijnGraph(frags)
    nb = dbgr.check_nearly_balanced_graph()
    if (nb[0] is not None and nb[1] is not None):
        p = dbgr.eulerian_path()
        return dbgr.seq_from_path(p)
    k = len(frags[0])  # assuming all of the same size (not tested)
    while (k >= 2):
        nfrags = []
        for f in frags:
            nf = composition(k, f)
            nfrags.extend(nf)
        dbgr = DeBruijnGraph(nfrags)
        nb = dbgr.check_nearly_balanced_graph()
        if (nb[0] is not None and nb[1] is not None):
            p = dbgr.eulerian_path()
            return dbgr.seq_from_path(p)
        else: k -= 1
    return None

#14)
#a)
def suffix_tree_from_seq(self, seq1, seq2):
    seq1 = seq1 + "$"
    seq2 = seq2 + "#"
    for i in range(len(seq1)): 
        self.add_suffix(seq1[i:], (0, i)) #vamos adicionar as leafs o 0, ou 1 correspondente a seq e o i que é o numero da letra onde começou
    for i in range(len(seq2)):  
        self.add_suffix(seq2[i:], (1, i))



#b)
def largestCommonSubstring(self):
    res = []
    for i in self.nodes[0][1].values():
        inspect = [0,0]
        m1, m2 = [], []
        start = self.get_leafes_below2(i)
        for j in start:
            m, n, coord = j
            if n == 1:
                inspect[1] = 1
                m1.append(coord)
            elif n == 0:
                inspect[0] = 1
                m2.append(coord)
        if inspect != [1,1]: pass
        else:
            for i in m2:
                for j in m1:
                    l1,coord1 = self.find_node(j)
                    l2, coord2 = self.find_node(i)
                    while coord2 != coord1 and coord2 > 0 and coord1 > 0:
                        l1, coord1 = self.find_node(coord1)
                        l2, coord2 = self.find_node(coord2)
                    if coord2 == coord1:
                        res.append(self.get_sequence(coord2))
    res = sorted(res,key = len)
    return res[len(res)-1]



def find_node(self,coord):  # encontrar o nodulo anterior
    x = len(self.nodes) - 1
    p = 1
    while p != 0 and x >= 0:  #ciclo do while para correr os nodes e procurar qual o node e a letra associada aoa seguimento para o proximo node
        for i in self.nodes[x][1].keys():
            if self.nodes[x][1][i] == coord:
                p = 0
                k = i,x
        x -=1
    return k  #devolve a letra associada e o node

def get_leafes_below2(self, node):
    res = []
    m,n = self.descompact(node) #desconcatenar os tuplos
    if m >= 0:  # maior ou igual 0 é para verificar uma leaf
        res.append((m, n, node))  # adicionar o valor da leaf
    else:
        for k in self.nodes[node][1].keys():  # correr todas as keys no nodulo
            newnode = self.nodes[node][1][k]  # mudar para o node
            leafes = self.get_leafes_below2(newnode)  # recursividade para seguir os ramos ate leaf
            res.extend(leafes)  # concatenar a lista da recursiva
    return res

#15)
#a) fazer tudo por 1 e dividilas pelo total das colunas, depois pegasse na probabilidade maisor de cada coluna e multiplicasse.

#b) 
def mostProbableSeqEX(self, seq, pwm): #vai ver qual a posição inicial da subseq de uma seq de comprimento indefenido encaixa melhor no quandro de motifs das seqs
    maximo = -1.0
    maxind = -1
    for k in range(len(seq)-self.motifSize):
        p = self.probabSeqEX(seq[k:k+ self.motifSize], pwm)
        if(p > maximo):
            maximo = p
            maxind = k
    return maxind

#c)
def heuristicStochastic (self):
    from random import randint
    s = [0] * len(self.seqs) #Gerar um vetor aleatória com o mesmo tamnho do número de sequências
    #Passo 1: inicia todas as posições com valores aleatórios 
    for i in range(len(self.seqs)):
        s[i] = randint(0, self.seqSize(i) - self.motifSize) #vai escolher um valor random para ser o valor inicial de cada seq
    #Passo 2
    melhorscore = self.score(s)
    improve = True
    while improve:
        motif = self.createMotifFromIndexes(s) #Constrói o perfil com base nas posições iniciais s
        motif.createPWM() #vai criar a matriz PWM  
        #Passo 3
        for i in range(len(self.seqs)): #Avalia a melhor posição inicial para cada sequência com base no perfil
            s[i] = motif.mostProbableSeq(self.seqs[i]) #vai ver em cada seq de self.seqs, qual é a subseq nelas que é mais provável de acontecer no quandro PWM
        #Passo 4
        #Verifica se houve alguma melhoria
        scr = self.score(s) #vai calcular o score
        if scr > melhorscore: #se o score melhorou volta a repetir o processo se não acaba e devolve as melhores posições das subseqs
            melhorscore = scr
        else: 
            improve = False
    return s

#d) Não é o exato pois não vai sempre encontrar o o ótimo global, pode sempre encontrar o ótimo local.




    




    







                











    




        

        



    




        



