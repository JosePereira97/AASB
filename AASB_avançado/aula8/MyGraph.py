# -*- coding: utf-8 -*-

## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:
    
    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g #recebe um dicionário

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v]) #vai dar print dos nós e dos seus valores

    ## get basic info

    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys()) #vai retornar uma lista com todos os nós
        
    def get_edges(self): 
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys(): #vai dar append do nódulo e aos valores do nodulo :o
            for d in self.graph[v]:
                edges.append((v,d))
        return edges
      
    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())
      
    ## add nodes and edges    
    
    def add_vertex(self, v):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v  not in self.graph.keys():
            self.graph[v] = []
        
    def add_edge(self, o, d):
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph ''' 
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        if d not in self.graph[o]:
            self.graph[o].append(d)


    ## successors, predecessors, adjacent nodes
        
    def get_successors(self, v):
        return list(self.graph[v]) 
             
    def get_predecessors(self, v): #vai buscar todos os nodulos anteriores
        res = []
        for k in self.graph.keys():
            if v in self.graph[k]:
                res.append(k)
        return res
    
    def get_adjacents(self, v): #vai juntar todos as duas listas, sem haver repetições
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        res = pred
        for p in suc:
            if p not in res: res.append(p)
        return res
        
    ## degrees    
    
    def out_degree(self, v):
        return len(self.get_successors(v)) #calcula o numero de saidas do nodulo
    
    def in_degree(self, v):
        return len(self.get_predecessors(v)) #calcula o numero de entradas
        
    def degree(self, v):
        return len(self.get_adjacents(v)) #calcula o numero de entradas e saidas sem repetições
        
    
    ## BFS and DFS searches    
    
    def reachable_bfs(self, v):
        l = [v] #criar uma lista
        res = [] #lista de nodulos visitados
        while len(l) > 0: #enquanto a lista de nodulos por visitar for maior que 0 vai continuar
            node = l.pop(0) #vamos dar pop do primeiro valor
            if node != v: res.append(node) # e se este for diferente do nodulo original adicionamos a res 
            for elem in self.graph[node]: #depois vamos correr os nodulos que estão 
                if elem not in res and elem not in l and elem != node: #se eles n se encontrarem em res nem em l vamos adiciona los a l
                    l.append(elem)
        return res
        
    def reachable_dfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            s = 0
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem) #igual ao de cima mas a unica diferença é que vai inserir na lista nas posições iniciais
                    s += 1
        return res
    
    def distance(self, s, d): #Vai ver a distância entre um nó e outro
        if s == d: return 0
        l = [(s,0)]
        visited = [s]
        while len(l) > 0:
            node, dist = l.pop(0)
            for elem in self.graph[node]:
                if elem == d: return dist + 1
                elif elem not in visited:
                    l.append((elem,dist+1))
                    visited.append(elem)

        return None
        
    def shortest_path(self, s, d): #vai encontrar o caminho mais curto entre dois nós
        if s == d: return []
        l = [(s,[])]
        visited = [s]
        while len(l) > 0:
            node, preds = l.pop(0)
            for elem in self.graph[node]:
                if elem == d: return preds+[node,elem]
                elif elem not in visited:
                    l.append((elem,preds+[node]))
                    visited.append(elem)
        return None
        
    def reachable_with_dist(self, s): #retorna uma lista com todos os nós e as distâncias correspondentes ao nó s*
        res = []
        l = [(s,0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: res.append((node,dist))
            for elem in self.graph[node]:
                if not is_in_tuple_list(l,elem) and not is_in_tuple_list(res,elem): 
                    l.append((elem,dist+1))
        return res

## cycles
    def node_has_cycle (self, v):
        l = [v] #visitar todos os nósulos e ver se estes voltam ao nodulo v
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v: return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return res

    def has_cycle(self): #vai ver se o grafos tem ciclos ou n
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): return True
        return res


def is_in_tuple_list (tl, val):
    res = False
    for (x,y) in tl:
        if val == x: return True
    return res


def test1():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()
    print (gr.get_nodes())
    print (gr.get_edges())
    

def test2():
    gr2 = MyGraph()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)
    
    gr2.add_edge(1,2)
    gr2.add_edge(2,3)
    gr2.add_edge(3,2)
    gr2.add_edge(3,4)
    gr2.add_edge(4,2)
    
    gr2.print_graph()
  
def test3():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()

    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))

def test4():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    
    print (gr.distance(1,4))
    print (gr.distance(4,3))

    print (gr.shortest_path(1,4))
    print (gr.shortest_path(4,3))

    print (gr.reachable_with_dist(1))
    print (gr.reachable_with_dist(3))

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    
    print (gr2.distance(2,1))
    print (gr2.distance(1,5))
    
    print (gr2.shortest_path(1,5))
    print (gr2.shortest_path(2,1))

    print (gr2.reachable_with_dist(1))
    print (gr2.reachable_with_dist(5))

def test5():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    print (gr.node_has_cycle(2))
    print (gr. node_has_cycle(1))
    print (gr.has_cycle())

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    print (gr2. node_has_cycle(1))
    print (gr2.has_cycle())


if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
    test5()
