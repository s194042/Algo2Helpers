
count = [0]

def SequenceAlignment(a,b, skip_penalty = 1, mismatch_penalty = 1):
    memo = {(0,0) : 0}
    cost = __align(len(a),len(b),memo,a,b,skip_penalty,mismatch_penalty)
    yres = []
    xres = []
    __get_sol(len(a),len(b),memo,yres,xres,a,b,skip_penalty,mismatch_penalty)
    xres.reverse()
    yres.reverse()
    return cost,"".join(xres),"".join(yres)


def __align(i,j,memo,x,y,skip_penalty = 1, mismatch_penalty = 1):
    if i == 0 and j == 0:
        memo[i,j] = 0
        return 0
    a = b = c = float('inf')
    if i > 0:
        if (i-1,j) not in memo:
            __align(i-1,j,memo,x,y,skip_penalty,mismatch_penalty)
        a = memo[(i-1,j)]
    if j > 0:
        if (i,j-1) not in memo:
            __align(i,j-1,memo,x,y,skip_penalty,mismatch_penalty)
        b = memo[(i,j-1)]
    if j > 0 and i > 0:
        if (i-1,j-1) not in memo:
            __align(i-1,j-1,memo,x,y,skip_penalty,mismatch_penalty)
        c = memo[(i-1,j-1)]
    memo[i,j] = min(a + skip_penalty, b + skip_penalty, c + (0 if x[i-1] == y[j-1] else mismatch_penalty))
    return min(a + skip_penalty, b + skip_penalty, c + (0 if x[i-1] == y[j-1] else mismatch_penalty))
    

def __get_sol(i,j,memo,yres,xres,x,y,skip_penalty = 1, mismatch_penalty = 1):
    count[0] += 1
    if i == 0 and j == 0:
        return
    t = float('inf')
    res = ((memo.setdefault((i-1,j),t),(i-1,j)), (memo.setdefault((i,j-1),t),(i,j-1)), (memo.setdefault((i-1,j-1),t),(i-1,j-1)))
    cur = memo.setdefault((i,j),t)
    a,b,c = res
    tmp = [i for i,p in [(a,skip_penalty),(b,skip_penalty),(c,0 if x[i-1] == y[j-1] else mismatch_penalty)] if cur - i[0] == p]
    res = min(tmp)    

    if res[1][0] == i-1:
        xres.append(x[i-1])
    else:
        xres.append("-")
    if res[1][1] == j-1:
        yres.append(y[j-1])
    else:
        yres.append("-")
    __get_sol(res[1][0],res[1][1],memo,yres,xres,x,y,skip_penalty,mismatch_penalty)



