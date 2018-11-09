input_array1 = [
    ['A1','B2','C2','D3'],
    ['A1','B2','D2','C3'],
    ['A2','B1','C1'],
    ['B1','C2','D2'],
    ['A1','C1','D2'],
    ['A2','C2','D1'],
    ['B2','C1','D2'],
    ['B1','C1','D2','E1'],
    ['B3', 'C2','D2','E1'],
    ['A1','C1','E2'],
    ['A2','C2','D1'],
    ['C1','E2'],
    ['A2','B2','E1']
]
input_array2 = [
    [1,3,4],
    [2,3,5],
    [1,2,3,5],
    [2,5]
]
input_array = [
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
support = 3
def get_limit1(input_array,support = 2):
    cand1 = {}
    for trans in input_array:
        for e in trans:
            e_set = frozenset([e])
            if cand1.get(e_set) == None:
                cand1[e_set] = 1
            else:
                cand1[e_set] += 1
    limit1 = {}
    for item,value  in cand1.items():
        if value >= support:
            limit1[item] = value
    return cand1,limit1

cand1,L1 = get_limit1(input_array,support)

def display(freq):
    print('  item     value     ')
    for item,value in freq.items():
        print(' {}  {} '.format(list(item),value))
def print_c(candidates):
    print('  candidate       ')
    for item in candidates:
        print('  {}  '.format(list(item)))
print("----------------------Candidate 1---------------------")
display(cand1)
print("----------------------Limit 1---------------------")
display(L1)

def getCk(limitk_1, k):
    """
    l2 = { {1,2}:2,{1,5}:1,{2,5}:3,{2,3}:4,{1,3}:2 }, k=3, return [ {1,2,5},{1,2,3},{2,3,5},{1,3,5} ]
    """
    candidates = []
    limit_keys = list(limitk_1.keys())
    length = len(limit_keys)
    for i in range(length):
        for j in range(i+1, length):
            a1 = list(limit_keys[i])
            a2 = list(limit_keys[j])
            a1.sort()
            a2.sort()
            L1 = a1[:k-2]
            L2 = a2[:k-2]
            if L1 == L2:
                candidates.append( frozenset(limit_keys[i]) | frozenset(limit_keys[j]))
    return candidates

def getLk(Ck,input_array,support = 2):
    lk = {}
    for c_item in Ck:
        lk[c_item] = 0
    for c_item in Ck:
        for trans in input_array:
            if c_item.issubset(set(trans)):
                lk[c_item] += 1
    lk_support = {}
    for item,value in lk.items():
        if value >= support:
            lk_support[item] = value
    return lk_support

C2 = getCk(L1,2)
print("----------------------Candidate 2---------------------")
print_c(C2)
L2 = getLk(C2,input_array,support)
print("----------------------Limit 2---------------------")
display(L2)
C3 = getCk(L2,3)
print("----------------------Candidate 3---------------------")
print_c(C3)
L3 = getLk(C3,input_array,support)
print("----------------------Limit 3---------------------")
display(L3)

# find the rules use confidence; confidence(A=>B) = support(A & B )/ support(A)
# confidece(A => B,C) = support({A,B,C}) /support({A})

def get_rules(L1,L2,L3):
    print("----------------------Current Frequent---------------------")
    print(L1.keys())
    print(L2.keys())
    print(L3.keys())
    print("----------------------Find Rules---------------------")
    for item,value in L3.items():
        for i, v in L1.items():
            if i.issubset(item):
                print('{} => {} is {} '.format( list(i),list(item - i),value/v ))
        for i, v in L2.items():
            if i.issubset(item):
                print('{} => {} is {} '.format( list(i),list(item - i),value/v ))
get_rules(L1,L2,L3)