from random import randint, random, shuffle, uniform


class Indiv:

    def __init__(self, size, genes=[], lb=0, ub=1):
        self.lb = lb
        self.ub = ub
        self.genes = genes #lista de genes
        self.fitness = None
        self.multfitness = None
        if not self.genes: #se n tiver uma lista de genes, vai criar uma lista com tamanho de size
            self.initRandom(size)

    # comparadores.
    # Permitem usar sorted, max, min

    def __eq__(self, solution):
        if isinstance(solution, self.__class__): #a ver se a solução pertence à classe
            return self.genes.sort() == solution.genes.sort() #vai dar return da self.genes, sendo esta igual a solution.genes
        return False #return False pois a solution n pertence a classe Indiv

    def __gt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness > solution.fitness #vai dar return do self.fitness maior do que a solution.fitness
        return False

    def __ge__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness >= solution.fitness #vai dar return do self.fitness maior ou igual a solution.fitness
        return False

    def __lt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness < solution.fitness #vai dar return de self.fitness sendo menor que solution.fitness
        return False

    def __le__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness <= solution.fitness #vai dar return de self.fitness sendo este menor ou igual a solution.fitness
        return False

    def __str__(self):
        return f"{str(self.genes)} {self.getFitness()}" #vai devolver em string o self.genes e o fitness a frente

    def __repr__(self): #vai dar return da string
        return self.__str__()

    def setFitness(self, fit): #vai dar a self.fitness o valor de fit
        self.fitness = fit
    
    def setmultFitness(self, fit):
        self.multfitness = fit

    def getFitness(self): #vai dar return do valor de self.fitness
        return self.fitness

    def getGenes(self): #vai dar return dos genes
        return self.genes

    def initRandom(self, size): #criar as seq de genes com 1 e 0 ou outros valores sendo lb ou ub*
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(self.lb, self.ub))

    def mutation(self): #São dependentes das representações #vai causar uma mutação aleatoria na selg.genes
        s = len(self.genes)
        pos = randint(0, s-1)
        if self.genes[pos] == 0:
            self.genes[pos] = 1
        else:
            self.genes[pos] = 0

    def crossover(self, indiv2):
        return self.one_pt_crossover(indiv2) #vai dar return de um objeto que vai ser o crossover entre o primeiro e o segundo individuo

    def one_pt_crossover(self, indiv2): 
        offsp1 = []
        offsp2 = []
        s = len(self.genes)
        pos = randint(0, s-1)
        for i in range(pos): #vai misturar os genes entre o individuo 1 e o 2 sendo o pos a posição onde troca os valores de ambos
            offsp1.append(self.genes[i])
            offsp2.append(indiv2.genes[i])
        for i in range(pos, s):
            offsp2.append(self.genes[i])
            offsp1.append(indiv2.genes[i])
        res1 = self.__class__(s, offsp1, self.lb, self.ub) #
        res2 = self.__class__(s, offsp2, self.lb, self.ub) #
        return res1, res2


class IndivInt (Indiv): #tudo igual mas com individuos inteiros

    def __init__(self, size, genes=[], lb=0, ub=1):
        self.lb = lb
        self.ub = ub
        print(self.ub)
        self.genes = genes
        self.fitness = None
        if not self.genes:
            self.initRandom(size)

    def initRandom(self, size): #criar seq random com um numero entre 0 ub, n entendo porque n é lb aqui
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(0, self.ub))

    def mutation(self): #pode criar uma mutação ou não...
        s = len(self.genes)
        pos = randint(0, s-1)
        self.genes[pos] = randint(0, self.ub)


class IndivReal(Indiv): #individuos reais
 
    def initRandom(self, size):
        self.genes = []
        for _ in range(size):
            self.genes.append(uniform(self.lb, self.ub)) 
    
    def mutation(self): #vai ocorrer uma unica mutação
        s = len(self.genes)
        pos = randint(0, s-1)
        self.genes[pos] = uniform(self.lb, self.ub)
