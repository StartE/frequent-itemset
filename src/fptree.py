input_array1 = [
    ['l1','l2','l5'],
    ['l2','l4'],
    ['l2','l3'],
    ['l1','l2','l4'],
    ['l1','l3'],
    ['l2','l3'],
    ['l1','l3'],
    ['l1','l2','l3','l5'],
    ['l1','l2','l3'],
    ['l1','l2','l5','l6']
]
input_array = [
    ['A','B','D','E'],
    ['B','C','E'],
    ['A','B','D','E'],
    ['A','B','C','E'],
    ['A','B','C','D','E'],
    ['B','C','D']
]
"""
https://en.wikibooks.org/wiki/Data_Mining_Algorithms_In_R/Frequent_Pattern_Mining/The_FP-Growth_Algorithm#An_example
https://blog.csdn.net/hsc_1/article/details/80452211
"""
def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = retDict.get(frozenset(trans),0)+1
    return retDict

input_array = createInitSet(input_array)

class TreeNode(object):
    def __init__(self,nameValue,numOccur,parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
    def inc(self,num):
        self.count += num
    def display(self,ind = 1):#DFS print the tree
        print("___"*ind,self.name,':',self.count)
        for child in self.children.values():
            child.display(ind + 1)

def createTree(dataset, minSupport = 3,verbose = False):
    #create header table
    headerTable = {}
    for trans in dataset:
        for item in trans:
            headerTable[item] = headerTable.get(item,0) + dataset[trans]
    print(headerTable)
    """
    headerTable
    B : 6
    E : 5
    A : 4
    C : 4
    D : 4
    """

    #remove unsupport item from the table
    keysToDel = []
    for k in headerTable.keys():
        if headerTable[k] < minSupport:
            keysToDel.append(k)
    for k in keysToDel:
        headerTable.pop(k,None)
    """
    headerTable
    B : 6
    E : 5
    A : 4
    C : 4
    D : 4
    """

    frequentSet = set(headerTable.keys())
    if len(frequentSet) == 0:
        return None,None
    """
    frequentSet = {B,E,A,C,D}
    """

    # init link field to headtable
    for k in headerTable.keys():
        headerTable[k] = [headerTable[k], None]
    """
    headerTable
    B : [6,None]
    E : [5,None]
    A : [4,None]
    C : [4,None]
    D : [4,None]
    """

    # init tree
    retTree = TreeNode('Null',1,None)

    # create tree
    for trans,count in dataset:
        loadD = {} # trans = [A,B,D,E]
        for item in trans:
            if item in frequentSet:#frequentSet = {B,E,A,C,D}
                loadD[item] = headerTable[item][0]
        if(len(loadD) > 0): #loadD = {A:3,B:6,D:4,E:5}
            #sort by frquent -hightest come first
            st = sorted(loadD.items(),key = lambda v:v[1], reverse = True) #st = {B:6,E:5,D:4,A:3}
            orderedItem = [v[0] for v in st] #[B,E,D,A]
            updateTree(orderedItem, retTree, headerTable,count)
            if verbose == True:
                retTree.display()
                print("                        ")
    return retTree, headerTable
"""
 Tree-----------------------------------
                            null:
                            B:6
                    E:5                  C:1
          A:4             C:1                D:1
  D:2          C:2
            D:1
 HeaderTable-------------------------------
    B : [6,TreeNode(B,6)]
    E : [5,TreeNode(E,5)]
    A : [4,TreeNode(A,4)]
    C : [4,TreeNode(C,2)->TreeNode(C,1)->TreeNode(C,1)]
    D : [4,TreeNode(D,2)->TreeNode(D,1)->TreeNode(D,1)]
"""

def updateTree(orderedItem, inTree, headerTable,count):
    headTree = inTree
    for item in orderedItem:
        if item in inTree.children:
            inTree.children[item].inc(count) #if child exists, child.count++
        else:
            inTree.children[item] = TreeNode(item,count,inTree) #else, create TreeNode,set count=1,set parent

            # Append the linked list in headerTable
            if headerTable[item][1] == None:
                headerTable[item][1] = inTree.children[item]
            else:
                updateHeader(headerTable[item][1],inTree.children[item])
        inTree = inTree.children[item]
    inTree = headTree #return the head of the tree

def updateHeader(nodeToTest, targetNode):
    while(nodeToTest.nodeLink != None): 
        # go to the end of the linked-list
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

#---------we will create a tree and notetable-----------------
retTree, headerTable = createTree(input_array)

def ascendTree(leafNode,prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent,prefixPath) #prefixPath add parent

def findPrefixPath(treeNode):
    """
                A
            B
        C       D:1
    D:2
    """
    conditionParrent = {}
    while treeNode is not None:
        prefixPath = []
        ascendTree(treeNode,prefixPath)
        if len(prefixPath) > 1:
            conditionParrent[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink #next node
    return conditionParrent #{ {A,B,E}:2, {A,B,C,E}:1, {B,C}:1 }
"""
 Tree-----------------------------------
                            null:
                            B:6
                    E:5                  C:1
          A:4             C:1                D:1
  D:2          C:2
            D:1
 HeaderTable-------------------------------
    B : [6,TreeNode(B,6)]
    E : [5,TreeNode(E,5)]
    A : [4,TreeNode(A,4)]
    C : [4,TreeNode(C,2)->TreeNode(C,1)->TreeNode(C,1)]
    D : [4,TreeNode(D,2)->TreeNode(D,1)->TreeNode(D,1)]
"""
#-------------get frequentItem Lists-----------------------------
print(headerTable)
freqItemList = []
preFix = set([])

def mineTree(headerTable,minSupport,preFix,freqItemList, level= 0):
    # start from lowest frequent item
    st = sorted(headerTable.items(),key = lambda p:p[1][0]) #p[0]=key,p[1]=value,p[1][0] = item_count
    bigL = [v[0] for v in st]

    for base in bigL:# D
        newFreqSet = preFix.copy()
        newFreqSet.add(base) #{D}
        freqItemList.append((newFreqSet,headerTable[base][0])) #[{D}:4]

        conditionParrent = findPrefixPath(headerTable[base][1]) #{ {A,B,E}:2, {A,B,C,E}:1, {B,C}:1 }
        _, myHeadTable = createTree(conditionParrent,minSupport) 
        """level = 0
        tree:
                   B:4
                E:3    C:1
             A:3
           C:1
        myHeadTable:
            B: [4,tree(B,4)]
            E: [3,tree(E,3)]
            A: [3,tree(A,3)]
            C: [2,tree(C,1)->tree(C,1)]
        """

        if myHeadTable is not None:
            mineTree(myHeadTable,minSupport,newFreqSet,freqItemList,level + 1)
            """level = 1
            A,B,E from lowest of headTable
            A:
            newFreqSet = {DA}
            freqItemList = [{D}:4,{DA}:3]
            conditionParrent = {{B,E}:3}
                tree:
                        B:3
                    E:3
                myHeadTable :
                    B:[3,tree(B)]
                    E:[3,tree(E)]
                level = 2
                    B:
                    newFreqSet = {DAB}
                    freqItemList = [{D,A,B}:3]
            """
