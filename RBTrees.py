import graphviz

class RNNode:
    def __init__(self,val) -> None:
        self.p = self.left = self.right = None
        self.color = True
        self.val = val
    
    def __str__(self) -> str:
        return str(self.val)

class RBTree:
    root = None
    dot = None

    def left_rotate(self,z):
        y = z.right
        if y.left is not None:
            y.left.p = z
        y.p = z.p
        if z.p == None:
            self.root = y
        elif z.p.left == z:
            z.p.left = y
        else:
            z.p.right = y
        z.right = y.left
        y.left = z
        z.p = y

    def right_rotate(self,z):
        y = z.left
        if y.right is not None:
            y.right.p = z
        y.p = z.p
        if z.p == None:
            self.root = y
        elif z.p.right == z:
            z.p.right = y
        else:
            z.p.left = y
        z.left = y.right
        y.right = z
        z.p = y


    def insert(self,z):
        z = RNNode(z)
        y = None
        x = self.root
        while x is not None:
            y = x
            if z.val > x.val:
                x = x.right
            else:
                x = x.left
        z.p = y
        if y is None:
            self.root = z
        elif z.val < y.val:
            y.left = z
        else:
            y.right = z
        z.color = True
        z.left = None
        z.right = None
        self.__insert_fix(z)


    def __insert_fix(self,z):
        while z.p is not None and z.p.color:
            if z.p.p is not None and z.p.p.left == z.p:
                y = z.p.p.right
                if y is not None and y.color:
                    z.p.p.color = True
                    z.p.color = False
                    y.color = False
                    z = z.p.p
                else:
                    if z.p.right == z:
                        z = z.p
                        self.left_rotate(z)
                    z.p.color = False
                    z.p.p.color = True
                    self.right_rotate(z.p.p)
                    z = z.p.right         
            elif z.p.p is not None and z.p.p.right == z.p:
                y = z.p.p.left
                if y is not None and y.color:
                    z.p.p.color = True
                    z.p.color = False
                    y.color = False
                    z = z.p.p
                else:
                    if z.p.left == z:
                        z = z.p
                        self.right_rotate(z)
                    z.p.color = False
                    z.p.p.color = True
                    self.left_rotate(z.p.p)
                    z = z.p.left
                    
        self.root.color = False   

    def search(self,val):
        return self.__search(val,self.root)

    def __search(self, val, x):
        if x is None: raise Exception
        if x.val == val: return x
        if x.val < val : return self.__search(val,x.right)
        return self.__search(val,x.left)

    def __is_leaf(self,x):
        return x.left is None and x.right is None
    
    def __succesor(self,x):
        if x is None or x.right is None: raise Exception
        x = x.right
        while not self.__is_leaf(x):
            x = x.left
        return x


    

    def delete(self,x):
        z = self.search(x)
        if z.left is None:
            oc = z.color
            x = z.right
            self.__trans(z,x)
            del z
            if not oc:
                self.__delete_fix(x)
        elif z.right is None:
            oc = z.color
            x = z.left
            self.__trans(z,x)
            del z
            if not oc:
                self.__delete_fix(x)
    

    def __delete_fix(self,x):
        pass
        
        

    def __trans(self,u,v):
        if u.p == self.root:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p                      

    def prop_holds(self):
        _,r = self.__prop_pd(self.root)
        return (self.__prop_red(self.root),r)

    def __prop_red(self,x):
        if x is None or not x.color:
            return True
        return (x.left is None or (not x.left.color)) and (x.right is None or (not x.right.color))

    def __prop_pd(self,x):
        if x is None:
            return (-1,True)
        ld,lb = self.__prop_pd(x.left)
        rd,rb = self.__prop_pd(x.right)
        return ((0 if x.color else 1) + ld, ld == rd and lb and rb)

    def to_str(self,x):
        if x == None:
            return ""
        return  str(x) + " " + self.to_str(x.left)  + self.to_str(x.right)
    
    def to_graph(self,red_edges = False):
        self.dot = graphviz.Digraph("RBTree",format='png')
        self.__to_graph_h(self.root,red_edges)
        self.dot.render(directory="output",view=True)


    def __to_graph_h(self,x,red_edges = False):
        if x is None:
            return
        self.dot.node(str(x),str(x),color="red" if x.color and not red_edges else "black")
        if x.left is not None:
            self.__to_graph_h(x.left,red_edges)
            self.dot.edge(str(x),str(x.left),color = "red" if x.left.color and red_edges else "black")
        if x.right is not None:
            self.__to_graph_h(x.right,red_edges)
            self.dot.edge(str(x),str(x.right),color = "red" if x.right.color and red_edges else "black")

        
    
    def __str__(self) -> str:
        return self.to_str(self.root)
        