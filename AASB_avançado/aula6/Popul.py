# -*- coding: utf-8 -*-

from Indiv import Indiv, IndivInt, IndivReal
from random import random

class Popul:

    def __init__(self, popsize, indsize, indivs=[]):
        self.popsize = popsize #tamanho da população
        self.indsize = indsize #tamanho das seq geneticas dos individuos
        if indivs: #vai ver se já existe uma população
            self.indivs = indivs 
        else:
            self.initRandomPop()

    def getIndiv(self, index):
        return self.indivs[index] #dá return de um individuo da população

    def initRandomPop(self): #vai cirar as seq geneticas do individs
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = Indiv(self.indsize, [])
            self.indivs.append(indiv_i)

    def getFitnesses(self, indivs=None): #vai buscar o fitness de todos os individuos da população
        fitnesses = []
        if not indivs:
            indivs = self.indivs
        for ind in indivs:
            fitnesses.append(ind.getFitness())
        return fitnesses

    def bestSolution(self): #vai dar return da melhor solução
        return max(self.indivs)

    def bestFitness(self): #vai dar return do melhor fitness
        indv = self.bestSolution()
        return indv.getFitness()


    def selection(self, n, indivs=None):
        res = []
        fitnesses = list(self.linscaling(self.getFitnesses(indivs)))
        for _ in range(n):
            sel = self.roulette(fitnesses)
            fitnesses[sel] = 0.0
            res.append(sel)
        return res

    def roulette(self, f): #vai selecionar um valor aleatério de fitnesses consoante assuas probabilidades
        tot = sum(f) #somatório de todos os valores de fitness
        val = random()
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] / tot)
            ind += 1
        return ind-1

    def linscaling(self, fitnesses): #escalar todos os valores para ficarem compreendidos entre 0 e 1
        mx = max(fitnesses)
        mn = min(fitnesses)
        res = []
        for f in fitnesses: 
            val = (f-mn)/(mx-mn)
            res.append(val)
        return res

    def recombination(self, parents, noffspring): #recombinação de individuos da população criar nova geração
        offspring = []
        new_inds = 0
        while new_inds < noffspring:
            parent1 = self.indivs[parents[new_inds]]
            parent2 = self.indivs[parents[new_inds+1]]
            offsp1, offsp2 = parent1.crossover(parent2)
            offsp1.mutation()
            offsp2.mutation()
            offspring.append(offsp1)
            offspring.append(offsp2)
            new_inds += 2
        return offspring

    def reinsertion(self, offspring): #vai substituir os individuos com a nova descendencia com melhore resultado
        tokeep = self.selection(self.popsize-len(offspring))
        ind_offsp = 0
        for i in range(self.popsize):
            if i not in tokeep:
                self.indivs[i] = offspring[ind_offsp]
                ind_offsp += 1


class PopulInt(Popul):

    def __init__(self, popsize, indsize, ub, indivs=[]):
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)

    def initRandomPop(self):
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = IndivInt(self.indsize, [], 0, self.ub)
            self.indivs.append(indiv_i)


class PopulReal(Popul):

    def __init__(self, popsize, indsize, lb=0.0, ub=1.0, indivs=[]): #Usamos o construtor já definido para uma população qualquer e toma nota dos atributos da população inteira e do tamanho do indivíduo e convoca a geração aleatória dos indivíduos
        self.lb = lb
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)

    def initRandomPop(self):#Igual ao de cima, mas com indivíduos reais 
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = IndivInt(self.indsize, [], lb = self.lb, ub = self.ub)
            self.indivs.append(indiv_i)