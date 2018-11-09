"""
1-workload type:
A,B,C,D,E, by  3:3:2:1:1
2-contention: 
contender1,victim2,independ3 by 1:1:8

rules: 
one contender,one victim, other may be victim or independent
All independent

example:



"""
import numpy as np
import pandas as pd
a = []
for i in range(1000):# as large as you can
    for length in range(1,6): # len of cluster 1,2,3,4,5,6
        #1,2,3,4,5 rate 1:2:4:4:1
        if length == 2:
            for k in range(2):
                r = np.random.choice(['A','B','C','D'],size = length,replace= False)
                a.append(r)
        if length == 3 or length == 4:
            for k in range(4):
                r = np.random.choice(['A','B','C','D','E'],size = length,replace= False)
                a.append(r)
        if length == 1:
            for k in range(1):
                r = np.random.choice(['A','B','D'],size = length,replace= False)
                a.append(r)
        if length == 5:
            for k in range(1):
                r = np.random.choice(['A','B','C','D','E','F'],size = length,replace= False)
                a.append(r)


np.random.shuffle(a)
print('Shuffle')


b = []
for item in a:
    new_item = []
    choice = np.random.choice([True,False],size = 1,replace = False,p=[0.1,0.9])
    if choice[0] == False:
        for v in item:
            new_item.append(v+'3')
    else:
        length = len(item)
        ch = np.random.choice( [x for x in range(length)] ,size = 1,replace = False)
        #print('ch',ch)
        for i,v in enumerate(item):
            if i == ch[0]:
                new_item.append(v+'1')
            new_item.append(v+'2')
    b.append(new_item)


"""
test = pd.read_csv("test.csv")
print(test['trans'][0])
"""
sub_df = pd.DataFrame({"trans":b})
sub_df.to_csv("test.csv", index=False)
