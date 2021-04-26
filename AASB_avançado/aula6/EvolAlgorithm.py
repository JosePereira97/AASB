from Popul import Popul


class EvolAlgorithm:

    def __init__(self, popsize, numits, noffspring, indsize):
        self.popsize = popsize #tamanho da população
        self.numits = numits
        self.noffspring = noffspring
        self.indsize = indsize #tamanho genetico de cada individuo

    def initPopul(self, indsize):
        self.popul = Popul(self.popsize, indsize) #criar uma população

    def evaluate(self, indivs): #vai avaliar o fitnees de cada individuo
        for i in range(len(indivs)):
            ind = indivs[i]
            fit = 0.0
            for x in ind.getGenes():
                if x == 1:
                    fit += 1.0
            ind.setFitness(fit)
        return None

    def iteration(self):
        parents = self.popul.selection(self.noffspring) #selecionar 50 individuos da população
        offspring = self.popul.recombination(parents, self.noffspring) #vai fazer a recombinação desses individuos
        self.evaluate(offspring) #vai avaliar o fitness deses individuos
        self.popul.reinsertion(offspring) #e vai ver se o integra na população

    def run(self):
        self.initPopul(self.indsize) #iniciar uma população
        self.evaluate(self.popul.indivs) #avaliar o fitnees dos individups
        self.bestsol = self.popul.bestSolution() #avaliar a melhor solução
        for i in range(self.numits+1): #vamos correr esta descendencia numits vezes e ver qual é a melhor solução
            self.iteration()
            bs = self.popul.bestSolution() 
            if bs > self.bestsol:
                self.bestsol = bs
            print("Iteration:", i, " ", "Best: ", self.bestsol)

    def printBestSolution(self):
        print("Best solution: ", self.bestsol.getGenes())
        print("Best fitness:", self.bestsol.getFitness())


def test():
    ea = EvolAlgorithm(100, 20, 50, 100)
    ea.run()


if __name__ == "__main__":
    test()
