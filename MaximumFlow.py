from collections import defaultdict, deque
import graphviz
import math

def __create_G(l):
    G = defaultdict(dict)
    for n,e in l:
        g1 = G[n]
        for edge,cap in e:
            g2 = G[edge]
            g1[edge] = (n,edge,cap,True)
            g2[n] = (n,edge,0,False)
    return G


def __format_list(l):
    formatted_list = []
    for n,lst in l:
        lst = [(lst[i * 2],lst[i * 2 + 1]) for i in range(len(lst)//2)]
        formatted_list.append((n,lst))

    return formatted_list


def dfs(s,t,G,min = 0):
    stack = [s]
    visited = set()
    f = dict()
    while stack:
        current = stack.pop()
        while current in visited:
            current = stack.pop()
        visited.add(current)
        for (n,e,cap,b) in G[current].values():
            if e == t and cap > min:
                return __create_path(s,t,f,current)
            if e not in visited and cap > min:
                f[e] = current
                stack.append(e)
    return []


def bfs(s,t,G,min = 0):
    queue = deque([s])
    visited = set()
    f = dict()
    while queue:
        current = queue.popleft()
        for (n,e,cap,b) in G[current].values():
            if e == t and cap > min:
                return __create_path(s,t,f,current)
            if e not in visited and cap > min:
                visited.add(e)
                f[e] = current
                queue.append(e)
    return []            


def __create_path(s,t,f,current):
    path = [t,current]
    while current != s:
        current = f[current]
        path.append(current)
    return list(reversed(path))


def __augment(path,G):
    edge_path = [G[path[i-1]][path[i]] for i in range(1,len(path))]
    amount = min(map(lambda x: x[2],edge_path))

    for edge in edge_path:
        f,t,cap,b = edge
        G[f][t] = (f,t,cap - amount,b)
        inv_cap = G[t][f][2]
        G[t][f] = (t,f,inv_cap + amount,not b)


    return edge_path,amount,path


def FordFulkerson(s,t,inp,p = False):
    G = __create_G(__format_list(inp))
    
    while path := dfs(s,t,G):
        edge_path,a,path = __augment(path,G)
        if p:
            print(path,a)
    if p:
        __to_graph(G)
    
    return sum([G[e[1]][e[0]][2] for e in G[s].values()])

def EdmundKarp(s,t,inp,p = False):
    G = __create_G(__format_list(inp))
    
    while path := bfs(s,t,G):
        edge_path,a,path = __augment(path,G)
        if p:
            print(path,a)
            
    if p:
        __to_graph(G)
    
    return sum([G[e[1]][e[0]][2] for e in G[s].values()])


def EdmundKarpScaling(s,t,inp,p = False):
    G = __create_G(__format_list(inp))
    tmp = max([edge[2] for edge in sum([list(edges.values()) for edges in G.values()],start=[])])
    print(tmp)
    scale = int(2 ** math.floor(math.log(tmp,2)))
    while scale > 0:
        while path := bfs(s,t,G,scale-1):
            edge_path,a,path = __augment(path,G)
            if p:
                print(path,a)
        scale //=2 
            
    if p:
        __to_graph(G)
    
    return sum([G[e[1]][e[0]][2] for e in G[s].values()])



def FordFolkersonScaling(s,t,inp,p = False):
    G = __create_G(__format_list(inp))
    tmp = max([edge[2] for edge in sum([list(edges.values()) for edges in G.values()],start=[])])
    print(tmp)
    scale = int(2 ** math.floor(math.log(tmp,2)))
    while scale > 0:
        while path := dfs(s,t,G,scale-1):
            edge_path,a,path = __augment(path,G)
            if p:
                print(path,a)
        scale //=2 
            
    if p:
        __to_graph(G)
    
    return sum([G[e[1]][e[0]][2] for e in G[s].values()])


def MinimumCut(s,t,inp):
    G = __create_G(__format_list(inp))
    
    while path := bfs(s,t,G):
        edge_path,a,path = __augment(path,G)        
    value = sum([G[e[1]][e[0]][2] for e in G[s].values()])

    queue = deque([s])
    visited = set()
    while queue:
        current = queue.popleft()
        for edge in G[current].values():
            f,t,cap,b = edge
            if t not in visited and cap > 0:
                visited.add(t)
                queue.append(t)
    
    return visited, set(G.keys()).difference(visited)
    

def __to_graph(G):
    dot = graphviz.Digraph("FlowGraph",format="png",engine="neato")
    dot.edge_attr["len"] = "2.0"
    for e in G.keys():
        dot.node(str(e),str(e))
    
    for e in G.keys():
        for edge in G[e].values():
            f,t,cap,b = edge
            if not b: continue
            cap1 = G[t][f][2]
            dot.edge(str(f),str(t),label=str(cap1) + "/" + str(cap1 + cap))

    dot.render(directory="output",view=True)


