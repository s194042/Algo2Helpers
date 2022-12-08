import math

# ---------- works with current notes with insert(i,x) inserting left of i ----------

class RotateArray:
    def __init__(self,n) -> None:
        self.arrays = []
        left = n
        nsqrt = math.ceil(math.sqrt(n))
        self.nsqrt = nsqrt
        while left > nsqrt:
            self.arrays.append([None for _ in range(nsqrt)])
            left -= nsqrt
        self.arrays.append([None for _ in range(nsqrt)])
        self.offsets = [0 for _ in range(len(self.arrays))]

    def get(self,i):
        r = i // self.nsqrt
        k = ((i % self.nsqrt) + self.offsets[r]) % self.nsqrt
        return self.arrays[r][k]

    def insert(self,i,x):
        r = i // self.nsqrt
        k = (i % self.nsqrt)
        self.__prop_over(r+1,self.arrays[r][self.offsets[r]-1])
        self.__rebuild_ins(r,k,x)

    def delete(self,i,):
        r = i // self.nsqrt
        k = (i % self.nsqrt)
        self.__rebuild__del(r,k)
        self.__prop_under(r+1)
    
    def __rebuild_ins(self,r,k,x):
        new = [None] * (self.nsqrt + 1)
        for i in range(self.nsqrt):
            oldindex = ((i % self.nsqrt) + self.offsets[r]) % self.nsqrt
            if i < k:
                new[i] = self.arrays[r][oldindex]
            elif i == k:
                new[k] = x
                new[i+1] = self.arrays[r][oldindex]
            else:
                new[i+1] = self.arrays[r][oldindex]
        self.arrays[r] = new[0:self.nsqrt]
        self.offsets[r] = 0
    
    def __rebuild__del(self,r,k):
        new = [None] * self.nsqrt
        for i in range(self.nsqrt):
            oldindex = ((i % self.nsqrt) + self.offsets[r]) % self.nsqrt
            if i < k:
                new[i] = self.arrays[r][oldindex]
            elif i > k:
                new[i-1] = self.arrays[r][oldindex]
        self.arrays[r] = new
        self.offsets[r] = 0
    
    def __prop_over(self,r,x):
        if x is None or r >= len(self.arrays): return
        tmp = self.arrays[r][self.offsets[r]]
        if tmp is not None:
            self.offsets[r] = (self.offsets[r] - 1) % self.nsqrt
        self.__prop_over(r+1,self.arrays[r][self.offsets[r]])
        self.arrays[r][self.offsets[r]] = x

    def __prop_under(self,r):
        if r >= len(self.arrays): return
        x = self.arrays[r][self.offsets[r]]
        if x is None: return
        self.arrays[r-1][self.offsets[r-1] - 1] = x
        self.arrays[r][self.offsets[r]] = None
        self.offsets[r] = (self.offsets[r] + 1) % self.nsqrt
        self.__prop_under(r+1)


    def __str__(self) -> str:

        return str(sum([[r[(i + o) % len(r)] for i in range(0,len(r)) if r[(i + o) % len(r)] is not None] for o,r in zip(self.offsets,self.arrays)],start=[]))

    def __repr__(self) -> str:
        return self.__str__()


    