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


b = [] #with 1,2,3,
c = [] #only 1,2
for item in a:
    new_item = []

    choice = np.random.choice([True,False],size = 1,replace = False,p=[0.1,0.9])
    if choice[0] == False:
        for v in item:
            new_item.append(v+'3')
        b.append(new_item)
    else:
        length = len(item)
        ch = np.random.choice( [x for x in range(length)] ,size = 1,replace = False)
        for i,v in enumerate(item):
            if i == ch[0]:
                new_item.append(v+'1')
            new_item.append(v+'2')
        b.append(new_item)
        c.append(new_item)


all_df = pd.DataFrame(b)
all_df.to_csv("data.csv",header = None, index=False)
sub_df = pd.DataFrame(c)
sub_df.to_csv("data_contention.csv",header = None, index=False)

pd_df = pd.DataFrame({"trans":b})
pd_df.to_csv("data_pd.csv", index=False)
pd_df_c = pd.DataFrame({"trans":c})
pd_df_c.to_csv("data_pd_c.csv", index=False)

with open('data.txt','w') as out:
    for trans in b:
        for index,item in enumerate(trans):
            if index != len(trans)-1:
                out.write(str(item)+'\t')
            else:
                out.write(str(item))
        out.write('\n')
with open('data_c.txt','w') as out:
    for trans in c:
        for index,item in enumerate(trans):
            if index != len(trans)-1:
                out.write(str(item)+'\t')
            else:
                out.write(str(item))
        out.write('\n')