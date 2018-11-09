import pandas as pd 

#data = pd.read_csv('test.txt',header=None,dtype=object)
#data_matrix = data.values

data_matrix = [
    ['1','3','4'],
    ['2','3','5'],
    ['1','2','3','5'],
    ['2','5']
]

ct = lambda x : pd.Series(1,index = x)
arrary = list(map(ct,data_matrix))
input_arrary = pd.DataFrame(arrary).fillna(0)


input_arrary = (input_arrary == 1)
support = 0.06 
confidence = 0.35 
ms = '--' #连接符，用来区分不同元素，如A--B。需要保证原始表格中不含有该字符

def connect_string(x, ms):
    fun = lambda i:sorted(i.split(ms)) # [B--C,B--D,B--E]
    x = list(map(fun, x)) # [[B,C],[B,D],[B,E]]
    l = len(x[0]) # 2 in example
    r = []
    for i in range(len(x)):
        for j in range(i,len(x)):
            #[B,C] and [B,D] => [B,C,D]
            if x[i][:l-1] == x[j][:l-1] and x[i][l-1] != x[j][l-1]:
                r.append(x[i][:l-1]+sorted([x[j][l-1],x[i][l-1]]))
    return r

def find_rule(d,support, confidence):
    result = pd.DataFrame(index = ['support','confidence'])
    support_series = d.sum() /len(d)
    print('C1{}'.format(support_series))
    column = list(support_series[support_series > support].index)
    print('L1{}'.format(column))
    k = 1
    while len(column) > 1:
        k += 1
        print('Search Candiadate and Limit of {}'.format(k))
        column = connect_string(column,ms) 
        print("Candidate of {} is {}".format(k,column))
        s_fun = lambda i: d[i].prod(axis = 1,numeric_only = True)
        column_link = [ms.join(i) for i in column]
        d_2 = pd.DataFrame(list(map(s_fun,column)),index = column_link).T
        print('d2 \n',d_2)
        support_series2 = d_2[column_link].sum()/len(d)
        column = list(support_series2[support_series2 >support].index)
        print("Limit of {} is {}".format(k,column))
        print('support_series\n',support_series2)
        support_series = support_series.append(support_series2)
        print("support_series\n",support_series)
        print("Rule of {} is \n:".format(k))
        column2 = []
        for item in column:
            item = item.split(ms)
            for j in range(len(item)):
                column2.append(item[:j]+item[j+1:]+item[j:j+1])
        confidence_series = pd.Series(index = [ms.join(i) for i in column2])
        for item in column2:
            print(len(item))
            confidence_series[ms.join(item)] = support_series[ms.join(sorted(item))]/support_series[ms.join(item[:len(item)-1])]

        for item in confidence_series[confidence_series > confidence].index:
            result[item] = 0.0
            result[item]['confidence'] = confidence_series[item]
            result[item]['support'] = support_series[ms.join(sorted(item.split(ms)))]
    result = result.T.sort_values(['confidence','support'],ascending = False)
    return result

result = find_rule(input_arrary,support,confidence)
print(result)