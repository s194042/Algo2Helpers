


def SequenceAlignment(a,b, skip_penalty = 1, mismatch_penalty = 1):
    memo = {(0,0) : 0}
    cost = __align(len(a),len(b),memo,a,b,skip_penalty,mismatch_penalty)
    yres = []
    xres = []
    __get_sol(len(a),len(b),memo,yres,xres,a,b)
    xres.reverse()
    yres.reverse()
    return cost,"".join(xres),"".join(yres)

def __align(i,j,memo,x,y,skip_penalty = 1, mismatch_penalty = 1):
    if i == 0 and j == 0:
        return 0 if x[0] == y[0] else 1
    a = b = c = float('inf')
    if i > 0:
        if (i-1,j) not in memo:
            memo[(i-1,j)] = __align(i-1,j,memo,x,y)
        a = memo[(i-1,j)]
    if j > 0:
        if (i,j-1) not in memo:
            memo[(i,j-1)] = __align(i,j-1,memo,x,y)
        b = memo[(i,j-1)]
    if j > 0 and i > 0:
        if (i-1,j-1) not in memo:
            memo[(i-1,j-1)] = __align(i-1,j-1,memo,x,y)
        c = memo[(i-1,j-1)]
    
    return min(a + skip_penalty, b + skip_penalty, c + (0 if x[i-1] == y[j-1] else mismatch_penalty))
    

def __get_sol(i,j,memo,yres,xres,x,y):
    if i == 0 and j == 0:
        return
    t = float('inf')
    res = min((memo.setdefault((i-1,j),t) + 1,(i-1,j)), (memo.setdefault((i,j-1),t) + 1,(i,j-1)), (memo.setdefault((i-1,j-1),t) + (0 if x[i-1] == y[j-1] else 1),(i-1,j-1)))
    if res[1][0] == i-1:
        xres.append(x[i-1])
    else:
        xres.append("-")
    if res[1][1] == j-1:
        yres.append(y[j-1])
    else:
        yres.append("-")
    __get_sol(res[1][0],res[1][1],memo,yres,xres,x,y)