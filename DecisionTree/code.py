"""
@author:Bharat Simha Reddy R S
"""
import csv
import copy
import random
import math
import collections 
import sys

class node:
    def __init__(self):
        self.label = -1
        self.isLeaf = -1
        self.right=None
        self.left=None
        self.attribute =None
        self.D_set=None  

class DecisionTree:
    def __init__(self, data, F_list):
        self.data = data
        self.F_list = F_list
    
    def split(self, D_set, val):
        i = self.F_list.index(val)
        N_set=[]
        P_set=[]
        for row in D_set:
            if row[i] == 0:
                N_set.append(row)
            else:
                P_set.append(row)
        return (N_set, P_set)
    
    def entropy(self, D_set):
        C_list = [row[-1] for row in D_set]
        res = collections.Counter(C_list)
        entropy = 0.0
        for i in res:
            prob = float(res[i])/len(C_list)
            entropy -= prob * math.log(prob,2)
        return entropy    

    def VI(self, D_set):
        C_list = [row[-1] for row in D_set]
        res = collections.Counter(C_list)
        if len(res) <= 1:
            return 0
        else:
            vi = 1.0
            for i in res:
                prob = (float(res[i])/len(C_list))
                vi *= prob
            return vi
        
    def InfoGain(self, D_set, D_C_list):
        B_G = 0.0
        B_F = ''
        base = self.entropy(D_set)
        new = 0.0
        for val in D_C_list:
            (N_set, P_set) = self.split(D_set, val)
            prob = float(len(P_set))/len(D_set)
            new = prob * self.entropy(P_set) + (1 - prob)*self.entropy(N_set)
            gain = base - new
            if gain > B_G:
                B_G = gain
                B_F = val
        return B_G, B_F
    
    def VarImp(self, D_set, D_list):
        B_G = 0.0
        final=''
        base = self.VI(D_set)
        new = 0.0
        for val in D_list:
            (N_set, P_set) = self.split(D_set, val)
            prob = (float(len(P_set)))/len(D_set)
            new = prob * self.VI(P_set) + (1 - prob)*self.VI(N_set)
            gain = base - new
            if gain > B_G:
                B_G = gain
                final = val
        return B_G, final

    def IGclass(self,C_list,root,D_set, D_C_list):
        if C_list.count(C_list[0]) == len(C_list):
            root.label = C_list[0]
            root.isLeaf = 1
            root.left = None
            root.right = None
            return root        
        root.label = self.maximum(D_set)
        entropy = self.entropy(D_set)
        if len(D_C_list) == 0 or entropy == 0:
            root.isLeaf = 1
            root.left = None
            root.right = None
            return root
        return root
    
    def VIclass(self,C_list,root,D_set, D_C_list):
        
        if C_list.count(C_list[0]) == len(C_list):
            root.label = C_list[0]
            root.leaf = 1
            root.left = None
            root.right = None
            return root

        root.label = self.maximum(D_set)

        if len(D_C_list) == 0:
            root.leaf = 1
            root.left = None
            root.right = None
            return root
        return root
    
    def classification(self, row, root):
        if root.right == None and root.left == None:
            return root.label
        i = self.F_list.index(root.attribute)
        if row[i] == 0:
            return self.classification(row, root.left)
        else:
            return self.classification(row, root.right)
        
    def accuracy(self, data, root):
        if root == None or len(data) == 0:
            return 0
        C = 0
        att = [row[-1] for row in data]
        i = 0
        for row in data:
            if int(self.classification(row, root)) == int(att[i]):
                C= C+1
            i=i+1
        acc = float(C)/len(att)
        return acc
    
    def C_list(self,D_set):
        
        C_list = [row[-1] for row in D_set]
        
        return C_list
    
    def Tree(self, D_set, D_C_list):
        if(len(D_set) == 0):
            return None

        root= node()
        C_list = self.C_list(D_set)
        root=self.IGclass(C_list,root,D_set, D_C_list)
        B_G, B_F = self.InfoGain(D_set, D_C_list)

        if B_G > 0:
            
            root.attribute = B_F
            D_C_list.remove(B_F)
            C1 = copy.deepcopy(D_C_list)
            C2 = copy.deepcopy(D_C_list)
            D_set_0, D_set_1 = self.split(D_set, B_F)
            root.left = self.Tree(D_set_0, C1)
            root.right = self.Tree(D_set_1, C2)
        return root
     
    def Tree2(self, D_set, D_C_list):
        if(len(D_set) == 0):
            return None

        root=node()
        C_list = self.C_list(D_set)
        root=self.VIclass(C_list,root,D_set, D_C_list)
        B_G, B_F = self.VarImp(D_set, D_C_list)

        if B_G > 0:
            root.attribute = B_F
            D_C_list.remove(B_F)
            C1 = copy.deepcopy(D_C_list)
            C2 = copy.deepcopy(D_C_list)
            D_set_0, D_set_1 = self.split(D_set, B_F)
            root.left = self.Tree2(D_set_0, C1)
            root.right = self.Tree2(D_set_1, C2)
        return root
    
    def maximum(self, D_set):
        C_list = [row[-1] for row in D_set]
        C_count = {}
        for tag in C_list:
            if tag not in C_count.keys():C_count[tag] = 0
            C_count[tag] += 1
        count = -1
        val = -1
        for key in C_count.keys():
            if C_count[key] > count:
                count = C_count[key]
                val = key
        return val
    
    def order(self,root):
        order = []
        if root == None or root.isLeaf == 1:
            return root
        queue = collections.deque([root])
        while len(queue) > 0:
            C_root = queue.popleft()
            order.append(C_root)
            if C_root.left!= None and C_root.left.isLeaf == -1:
                queue.append(C_root.left)
            if C_root.right!= None and C_root.right.isLeaf == -1:
                queue.append(C_root.right)
        return order
    
    def pruning(self, data, root, l, k):
        
        B_root = copy.deepcopy(root)
        for i in range(1, l):
            C_root = copy.deepcopy(root)
            m = random.randint(1, k)
            for j in range(1, m):            
                ordered_node = self.order(C_root)
                n = len(ordered_node) - 1
                if n <= 0:
                    return B_root
                p = random.randint(1, n)
                newnode = ordered_node[p]
                newnode.isLeaf = 1
                newnode.left = None
                newnode.right = None
            old = self.accuracy(data, B_root)
            new = self.accuracy(data, C_root)
            B_root= self.compare(old,new,B_root,C_root)
        return B_root
    
    def compare(self,old,new,B_root,C_root):
        if(new > old):
                B_root = C_root
        return B_root
    
    def display(self, root,l):
        s = ''
        if root == None:
            return ''
        if root.left == None and root.right == None:
            s += str(root.label) + '\n'
            return s  
        bar = ''
        for i in range(0, l):
            bar += '|'
        s += bar
        if root.left!= None and root.left.left == None and root.left.right == None:
            s +=  str(root.attribute) + " = 0 : "
        else:
            s +=  str(root.attribute) + " = 0 :\n"
        s += self.display(root.left, l + 1)
        s += bar
        if root.left != None and root.right.left == None and root.right.right == None:
            s += str(root.attribute) + " = 1 :"
        else:
            s += str(root.attribute) + " = 1 :\n"
        s += self.display(root.right, l + 1)
        return s

       
    
if __name__ == "__main__":
    
    L = int (sys.argv[1])
    K = int (sys.argv[2])
    # print (L,K)
	
    training_file_path = sys.argv[3]
    validation_file_path = sys.argv[4]
    test_file_path = sys.argv[5]
    
    Print = sys.argv[6]
    # L=22
    # k=11
    with open(training_file_path,'r') as f1:
        reader = csv.reader(f1)
        data = list(reader)
    C_List = data[0][:-1]
    data = data[1:]
    set2 = []
    set1 =[]
    for row in data:
        set2.append([int(i) for i in row])
        set1.append([int(i) for i in row])
    DT = DecisionTree(set, C_List)
    D_list = copy.deepcopy(C_List)
    D_list2 = copy.deepcopy(C_List)
    VarImp_tree= DT.Tree2(set1,D_list2)
    Ent_tree= DT.Tree(set2, D_list)

    with open(test_file_path,'r') as f2:
        test_data = list(csv.reader(f2))
    test_data = test_data[1:]
    test_D_set = []
    for row in test_data:
        test_D_set.append([int(i) for i in row])
        
    with open(validation_file_path,'r') as f3:
        data= list(csv.reader(f3)) 
    C_List = data[0][:-1]
    data = data[1:]
    D_set = []
    for row in data:
        D_set.append([int(i) for i in row])

    print 'Pre-Pruning accuracy(entropy):',DT.accuracy(test_D_set, Ent_tree)
    print 'Pre-Pruning accuracy(Var_Imp):',DT.accuracy(test_D_set, VarImp_tree)
    Ent_B_Tree = DT.pruning(D_set, Ent_tree, L, K)
    Var_B_Tree = DT.pruning(D_set,VarImp_tree, L, K)
    print 'Post-Pruning accuracy(entropy):',DT.accuracy(test_D_set,Ent_B_Tree)
    print 'Post-Pruning accuracy(Var_Imp):',DT.accuracy(test_D_set,Var_B_Tree)
    if Print =='yes':
        print('Pre_pruning Tree(entropy):',DT.display(Ent_tree, 0))
        print('Pre_pruning Tree(Var_Imp):',DT.display(VarImp_tree, 0))   
        print('Post_pruning Tree(entropy):',DT.display(Ent_B_Tree, 0))  
        print('Post_pruning Tree(Var_Imp):',DT.display(Var_B_Tree, 0))
     
  