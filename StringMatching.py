import graphviz


def create_fail(p):
    # add useless character in front, to correct index
    p = "e" + p + "#"
    m = len(p)
    fail = [0] * m
    j = 0
    for i in range(1,m):
        fail[i] = j
        while j > 0 and p[i] != p[j]:
            j = fail[j]
        j += 1
    return fail[1:]



def create_optim_fail(P):
    fail = [0 for _ in range(len(P))]
    j = 0
    for i in range(1,len(P)):
        if P[i] == P[j]:
            fail[i] = fail[j]
        else:
            fail[i] = j
        while j > 0 and P[i] != P[j]:
            j = fail[j]
        j = j+1
    return fail

def KMP(P,T):

    START = "epsilon"
    END = "end"

    T = T.rstrip()
    P = P.rstrip()

    T = list(T)
    P = [START] + list(P) + [END]
    m = len(P) - 2
    res = []
    fail = create_optim_fail(P)
    j = 1
    i = 0
    for i in range(len(T)):
        while j > 0 and T[i] != P[j]:
            j = fail[j]
        i += 1
        if j == m:
            res.append(i - m)
            j = fail[-1]-1
        j += 1
    return res


def automata(P):
    f = create_fail(P)
    graph = graphviz.Digraph("Automata","png",engine="dot")
    with graph.subgraph() as dot:
        dot.attr(rank="same")
        dot.edge_attr["len"] = "2.0"
        dot.graph_attr["rankdir"] = "LR"
        dot.node("epsilon","epsilon")
        dot.node("#","#")
        for i,c in enumerate(P):
            dot.node(str(i),c)
        dot.edge("epsilon","0")
        dot.edge(str(len(P)-1),"#")
        dot.edge("#",str(f[-1]-1))
        for i in range(1,len(P)):
            dot.edge(str(i-1),str(i))
        for i,fail in enumerate(f[:-1]):
            if fail == 0:
                dot.edge(str(i),"epsilon")
            else:
                dot.edge(str(i),str(fail-1))
    graph.render(directory="output",view=True)
            


