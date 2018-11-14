import os
import csv
import json
from collections import namedtuple
from itertools import combinations

class TransactionManager(object):

    def __init__(self,transactions):
        self._num_transactions = 0
        self._items = []
        self._item_index_map = {}
        for transaction in transactions:
            self.add_transaction(transaction)

    def add_transaction(self,transaction):
        for item in transaction:
            if item not in self._item_index_map:
                self._items.append(item)
                self._item_index_map[item] = set()
            self._item_index_map[item].add(self._num_transactions)
        self._num_transactions +=1 

    def init_candidates(self):
        """
        [item] is necessary, if item = 'ab', frozenset(item)= {'a','b'},
        if item = ['ab'],frozenset(item) = {'ab'}
        """
        return  [frozenset([item]) for item in self._items]

    def calculate_support(self,candidate):
        if not candidate:
            return 1.0

        if not self._num_transactions:
            return 0.0

        total_indexs = None
        for item in candidate:
            if item == 'E':
                print('get')
            indexs = self._item_index_map[item]
            if indexs is None:
                return 0.0
            if total_indexs is None:
                total_indexs = indexs
            else:
                total_indexs = total_indexs.intersection(indexs)
        return len(total_indexs)/self._num_transactions
    
    @property
    def items(self):
        return sorted(self._items)

    @property
    def num_transactions(self):
        return self.num_transactions
    

    @staticmethod
    def create(transactions):
        if isinstance(transactions,TransactionManager):
            return transactions
        return TransactionManager(transactions)

def load_trans(input_file):
    with open(input_file,'r') as csvfile:
        for transcation in csv.reader(csvfile, delimiter = '\t'):
            yield transcation

def apriori(transactions,max_length,min_support,min_confidence,min_lift):

    transaction_manager = TransactionManager.create(transactions)
    support_records = get_support(transaction_manager,min_support,max_length)
    for record in support_records:
        detail_reocords = get_confidence_lift(transaction_manager,record,min_confidence,min_lift)
        detail_reocords = list(detail_reocords) #convert generator to list
        if not detail_reocords:
            continue
        yield RelationRecord(record.items,record.support,detail_reocords)

def get_next_candidates(prev_candidates,length):
    items = set()
    for prev_candidate in prev_candidates:
        for item in prev_candidate:
            items.add(item)
    items = sorted(items)
    tmp_candidates = [frozenset(x) for x in combinations(items,length)]

    if length <3:
        return tmp_candidates
    candidates = [
        candidate for candidate in tmp_candidates
        if all(
            True if frozenset(item) in prev_candidates else False
            for item in combinations(candidate,length - 1)
        )
    ]
    return candidates

SupportRecord = namedtuple('SupportRecord', ('items', 'support'))
RelationRecord = namedtuple('RelationRecord',SupportRecord._fields + ('detail_records',))
DetailRecord = namedtuple('DetailRecord',('item_base','item_add','confidence','lift'))

def get_support(transaction_manager,min_support,max_length):
    candidates = transaction_manager.init_candidates()
    length = 1
    while candidates:
        with_min_support_candidates = []
        for candidate in candidates:
            support = transaction_manager.calculate_support(candidate)
            if support < min_support:
                continue
            yield SupportRecord(candidate,support)
            with_min_support_candidates.append(candidate)
        length = length + 1
        if length and length > max_length:
            break
        candidates = get_next_candidates(with_min_support_candidates,length)

def get_confidence_lift(transaction_manager, support_record,min_confidence,min_lift):
    items = support_record.items
    for combination_set in combinations(sorted(items),len(items)-1):
        item_base = frozenset(combination_set)
        item_add = frozenset(items.difference(item_base))
        confidence = support_record.support/transaction_manager.calculate_support(item_base)
        lift = confidence/transaction_manager.calculate_support(item_add)
        if confidence < min_confidence:
            continue
        if lift < min_lift:
            continue
        yield DetailRecord(item_base,item_add,confidence,lift)

def save_to_json(relation_records,output_file):
    def default_func(value):
        if isinstance(value, frozenset):
            return sorted(value)
        raise TypeError(repr(value)+' is not JSON serializable')
    with open(output_file,'w') as out_file:
        for record in relation_records:
            converted_record = record._replace(
                detail_records= [x._asdict() for x in record.detail_records]
            )
            json.dump(
                converted_record._asdict(), out_file, default=default_func, ensure_ascii=False
            )
            out_file.write(os.linesep)
def main():
    min_support = 0.1
    max_length = 5
    min_confidence = 0.3
    min_lift = 0
    input_file = 'src/data_c.txt'
    output_file = 'src/test_out.json'
    transactions = load_trans(input_file)
    relation_records = apriori(transactions,max_length,min_support,min_confidence,min_lift)
    save_to_json(relation_records,output_file)

if __name__ == '__main__':
    main()