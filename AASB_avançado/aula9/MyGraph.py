# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 01:33:42 2017

@author: miguelrocha
"""

## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:
    
    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g    

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v])

    ## get basic info

    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())
        
    def get_edges(self): 
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v,d))
        return edges
      
    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())
      
    ## add nodes and edges    
    
    def add_vertex(self, v):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():
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
        return list(self.graph[v])     # needed to avoid list being overwritten of result of the function is used           
             
    def get_predecessors(self, v):
        res = []
        for k in self.graph.keys(): 
            if v in self.graph[k]: 
                res.append(k)
        return res
    
    def get_adjacents(self, v):
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        res = pred
        for p in suc: 
            if p not in res: res.append(p)
        return res
        
    ## degrees    
    
    def out_degree(self, v):
        return len(self.graph[v])
    
    def in_degree(self, v):
        return len(self.get_predecessors(v))
        
    def degree(self, v):
        return len(self.get_adjacents(v))
        
    def all_degrees(self, deg_type = "inout"):
        ''' Computes the degree (of a given type) for all nodes.
        deg_type can be "in", "out", or "inout" '''
        degs = {}
        for v in self.graph.keys():
            if deg_type == "out" or deg_type == "inout":
                degs[v] = len(self.graph[v])
            else: degs[v] = 0
        if deg_type == "in" or deg_type == "inout":
            for v in self.graph.keys():
                for d in self.graph[v]:
                    if deg_type == "in" or v not in self.graph[d]:
                        degs[d] = degs[d] + 1
        return degs
    
    def highest_degrees(self, all_deg= None, deg_type = "inout", top= 10):
        if all_deg is None: 
            all_deg = self.all_degrees(deg_type)
        ord_deg = sorted(list(all_deg.items()), key=lambda x : x[1], reverse = True)
        return list(map(lambda x:x[0], ord_deg[:top]))
        
    
    ## topological metrics over degrees

    def mean_degree(self, deg_type = "inout"):
        degs = self.all_degrees(deg_type)
        return sum(degs.values()) / float(len(degs))
        
    def prob_degree(self, deg_type = "inout"):
        degs = self.all_degrees(deg_type)
        res = {}
        for k in degs.keys():
            if degs[k] in res.keys():
                res[degs[k]] += 1
            else:
                res[degs[k]] = 1
        for k in res.keys():
            res[k] /= float(len(degs))
        return res    
    
    
    ## BFS and DFS searches    
    
    def reachable_bfs(self, v):
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            for elem in self.graph[node]:
                if elem not in res and elem not in l and elem != node:
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
                    l.insert(s, elem)
                    s += 1
        return res    
    
    def distance(self, s, d):
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
        
    def shortest_path(self, s, d):
        if s == d: return 0
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
        
    def reachable_with_dist(self, s):
        res = []
        l = [(s,0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: res.append((node,dist))
            for elem in self.graph[node]:
                if not is_in_tuple_list(l,elem) and not is_in_tuple_list(res,elem): 
                    l.append((elem,dist+1))
        return res
 
    ## mean distances ignoring unreachable nodes
    def mean_distances(self):
        tot = 0
        num_reachable = 0
        for k in self.graph.keys(): 
            distsk = self.reachable_with_dist(k)
            for _, dist in distsk:
                tot += dist
            num_reachable += len(distsk)
        meandist = float(tot) / num_reachable
        n = len(self.get_nodes())
        return meandist, float(num_reachable)/((n-1)*n)  #numero de liga????es observadas /pelo numero de liga????es esperadas
    
    def closeness_centrality(self, node):
        dist = self.reachable_with_dist(node)
        if len(dist)==0: return 0.0
        s = 0.0
        for d in dist: s += d[1] 
        return len(dist) / s 
        
    
    def highest_closeness(self, top = 10): 
        cc = {}
        for k in self.graph.keys():
            cc[k] = self.closeness_centrality(k)
        print(cc)
        ord_cl = sorted(list(cc.items()), key=lambda x : x[1], reverse = True)
        return list(map(lambda x:x[0], ord_cl[:top]))
            
    
    def betweenness_centrality(self, node):
        total_sp = 0
        sps_with_node = 0
        for s in self.graph.keys(): 
            for t in self.graph.keys(): 
                if s != t and s != node and t != node:
                    sp = self.shortest_path(s, t)
                    if sp is not None:
                        total_sp += 1
                        if node in sp: sps_with_node += 1 
        return sps_with_node / total_sp
                    
    
    ## cycles    
    def node_has_cycle (self, v):
        l = [v]
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
    
    def has_cycle(self):
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): return True
        return res

    ## clustering
        
    def clustering_coef(self, v):
        adjs = self.get_adjacents(v)
        if len(adjs) <=1: return 0.0
        ligs = 0
        print(adjs)
        for i in adjs:
            for j in adjs:
                if i != j:
                    if j in self.graph[i] or i in self.graph[j]: 
                        ligs = ligs + 1
        return float(ligs)/(len(adjs)*(len(adjs)-1))
        
    def all_clustering_coefs(self):
        ccs = {}
        for k in self.graph.keys():
            ccs[k] = self.clustering_coef(k)
        return ccs
        
    def mean_clustering_coef(self):
        ccs = self.all_clustering_coefs()
        return sum(ccs.values()) / float(len(ccs))
            
    def mean_clustering_perdegree(self, deg_type = "inout"):
        degs = self.all_degrees(deg_type)
        ccs = self.all_clustering_coefs()
        degs_k = {}
        for k in degs.keys():
            if degs[k] in degs_k.keys(): degs_k[degs[k]].append(k)
            else: degs_k[degs[k]] = [k]
        ck = {}
        for k in degs_k.keys():
            tot = 0
            for v in degs_k[k]: tot += ccs[v]
            ck[k] = float(tot) / len(degs_k[k])
        return ck


    def all_degrees(self, deg_type = "inout"): #vai calcular os graus de entrada e os graus de saida para todos os nodulos
        degs = {}
        for v in self.graph.keys():
            if deg_type == "out" or deg_type == "inout":
                degs[v] = len(self.graph[v])
            else: degs[v] = 0
        if deg_type == "in" or deg_type == "inout":
            for v in self.graph.keys():
                for d in self.graph[v]:
                    if deg_type == "in" or v not in self.graph[d]:
                        degs[d] = degs[d] + 1
        return degs

    def mean_degree (self, deg_type = "inout"): #vai devolver a m??dia dos graus na ??rvore
        degs = self.all_degrees(deg_type)
        return sum(degs.values()) / float(len(degs))
    
    def prob_degree (self, deg_type = "inout"): #vai devolver a probabilidade de todos os graus na ??rvore ou ambos o grau ?? o numero de entrada  de saida
        degs = self.all_degrees(deg_type)
        res = {}
        for k in degs.keys():
            if degs[k] in res.keys():
                res[degs[k]] += 1
            else:
                res[degs[k]] = 1
        for k in res.keys():
            res[k] /= float(len(degs))
        return res

    def mean_distances(self): #Vai devolver a m??dia de dist??ncias entre todos os n??dulos e a propor????o de n??s atingiveis a partir de um n??.
        tot = 0
        num_reachable = 0
        for k in self.graph.keys():
            distsk = self.reachable_with_dist(k)
            for _, dist in distsk:
                tot += dist
            num_reachable += len(distsk)
        meandist = float(tot) / num_reachable
        n = len(self.get_nodes())
        return meandist, float(num_reachable)/((n-1)*n)

    
    def centralidade_de_Grau_Vertice(self, v): #A centralidade de grau de um v??rtice ?? dada pelo seu grau
        allDegree = self.all_degrees()
        return(allDegree[v])

    def centralidade_de_Grau_Grafo(self, s): #s ?? o numero de n??s mais elevados pretendidos com os seus devidos graus*
        allDegree = self.all_degrees()
        Centralidade = {}
        for i in allDegree.keys():
            if len(list(Centralidade.keys())) < s:
                Centralidade[i] = allDegree[i]
            else:
                valuebaixo = sorted(list(Centralidade.values()), key = len)
                if valuebaixo[0] < allDegree[i]:
                    for key in Centralidade.keys():
                        if Centralidade[key] == valuebaixo[0]:
                            Centralidade.pop(key)
                            break
                    Centralidade[i] = allDegree[i]
        return(Centralidade)

    def centralidade_de_proximidade_vertice(self, v): #A centralidade de proximidade d eum v??rtice ?? dado pelo reciproco da soma das suas dist??ncias aos demain n??s
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
    
    def centralidade_de_proximidade_vertice(self,s): #s o numero de nos mais elevados pretendidos
        proximidade = {}
        for i in self.graph.keys():
            score = self.centralidade_de_proximidade_vertice(i)
            if len(list(proximidade.keys())) < s:
                proximidade[i] = score
            else:
                valuebaixo = sorted(list(proximidade.values()), key = len)
                if valuebaixo[0] < score:
                    for key in proximidade.keys():
                        if proximidade[key] == valuebaixo[0]:
                            proximidade.pop(key)
                            break
                    proximidade[i] = score
        return proximidade

    def centralidade_closeness_vertice(self,v): #a centralidade de um vertice a outros vertices ?? calculado por o numero de n??s que passam am v -1 a dividir pelas dist??ncias totais 
        distancia_nos = self.reachable_with_dist(v)
        total = 0
        N = 0
        for i, d in distancia_nos:
            total = total + d
            N+=1
        closeness_vertice = float((N-1)/total)
        return(closeness_vertice)

    def centralidade_closeness_grafo(self, s): #sendo s o numero de n??s
        closennes_grafo = {}
        for i in self.graph.keys():
            score = self.centralidade_closeness_vertice(i)
            if len(list(closennes_grafo.keys())) < s:
                closennes_grafo[i] = score
            else:
                valuebaixo = sorted(list(closennes_grafo.values()), key = len)
                if valuebaixo[0] < score:
                    for key in closennes_grafo.keys():
                        if closennes_grafo[key] == valuebaixo[0]:
                            closennes_grafo.pop(key)
                            break
                    closennes_grafo[i] = score
        return closennes_grafo


            




def is_in_tuple_list(tl, val):
    res = False
    for (x,y) in tl:
        if val == x: return True
    return res

    
if __name__ == "__main__":
    gr = MyGraph()
    gr.add_vertex(1)
    gr.add_vertex(2)
    gr.add_vertex(3)
    gr.add_vertex(4)
    gr.add_edge(1,2)
    gr.add_edge(2,3)
    gr.add_edge(3,2)
    gr.add_edge(3,4)
    gr.add_edge(4,2)
    gr.print_graph()
    print(gr.size())
    
    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))
    
    print(gr.all_degrees("inout"))
    print(gr.all_degrees("in"))
    print(gr.all_degrees("out"))
    
    gr2 = MyGraph({1:[2,3,4], 2:[5,6],3:[6,8],4:[8],5:[7],6:[],7:[],8:[]})
    print(gr2.reachable_bfs(1))
    print(gr2.reachable_dfs(1))
    
    print(gr2.distance(1,7))
    print(gr2.shortest_path(1,7))
    print(gr2.distance(1,8))
    print(gr2.shortest_path(1,8))
    print(gr2.distance(6,1))
    print(gr2.shortest_path(6,1))

    print(gr2.reachable_with_dist(1))
    
    print(gr.has_cycle())
    print(gr2.has_cycle())
    
    print(gr.mean_degree())
    print(gr.prob_degree())
    print(gr.mean_distances())
    print (gr.clustering_coef(1))
    print (gr.clustering_coef(2))
    print()
    print()
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    print (gr.clustering_coef(1))
    print (gr.clustering_coef(2))
    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    print (gr2.clustering_coef(1))
    gr3 = MyGraph( {1:[2,3], 2:[1,3], 3:[1,2]} )
    print (gr3.clustering_coef(1))