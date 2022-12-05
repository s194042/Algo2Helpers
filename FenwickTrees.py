import math

class FenwickTree:

    def __init__(self,n) -> None:
        if isinstance(n,list):
            self.ft = [0] + n
            self.construct(2)
        else:
            self.ft = [0] * (n+1)

    def construct(self,index):
        if index > len(self.ft) - 1:
            return 
        for i in range(index,len(self.ft),index):
            self.ft[i] += self.ft[i - (index // 2)]
        self.construct(index * 2)

    def sum(self,i):
        s = 0
        while(i > 0):
            s += self.ft[i]
            i -= self.__LSB(i)
        return s
    
    def update(self,i,x):
        while(i < len(self.ft)):
            self.ft[i] += x
            i += self.__LSB(i)

    def __LSB(self,i):
        return (i) & (-i)


    def __repr__(self) -> str:
        return str(self.ft[1:])