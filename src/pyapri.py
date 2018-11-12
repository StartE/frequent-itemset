"""
a simple implementation of Apriori algroithm by Python
"""

import sys
import csv
import argparse
import json
import os
from collections import namedtuple
from itertools import combinations
from itertools import chain

# Meta information
__version__ = "1.1.2"
__author__ = "YL"

class TranscationManager(object):
    """
    Transaction managers.
    """
    def __init__(self,transactions):
        """
        use transactions like that [['A','B],['C','D]]
        """
        self.__num_transaction = 0
        self.__items = []
        self.__transaction_index_map = {}
        for transaction in transactions:
            self.add_transcation(transaction)
    
    def add_transcation(self,transaction):
        """
        Arguments:
            transaction -- A transaction as an iterable object(eg.['A','B'])
        """
        for item in transaction:
            if item not in self.__transaction_index_map:
                self.__items.append(item)
                self.__transaction_index_map[item] = set()
            self.__transaction_index_map[item].add(self.__num_transaction)
        self.__num_transaction +=1

    def calc_support(self,items):
        """
        Returns a support for items.

        Arguments:
            items -- Items as an iterable object(eg. ['A','B']).
        """
        if not items:
            return 1.0
        
        if not self.__num_transaction:
            return 0.0
        
        # Create the transcation index intersection
        sum_indexs = None
        for item in items:
            indexs = self.__transaction_index_map[item]
            if indexs is None:
                # No support for any set that contains a not existing item
                return 0.0
            if sum_indexs is None:
                # Assign the indexes on the first time.
                sum_indexs = indexs
            else:
                sum_indexs = sum_indexs.intersection(indexs)
        
        # Calculate and return the support
        return len(sum_indexs)/self.__num_transaction
    
    def initial_candidates(self):
        """
        Returns the initial candidates
        """
        return [frozenset([item]) for item in self.items]
    
    @property
    def num_transaction(self):
        """
        get and set or property num_transaction
        """
        return self.__num_transaction
    
    @property
    def items(self):
        """
        get and set of property items
        """
        return sorted(self.__items)
    
    @staticmethod
    def create(transactions):
        """
        Create the Transaction Manager with a transaction instance.
        If the given instance is a TransactionManger, this returns itself
        """
        if isinstance(transactions,TranscationManager):
            return transactions
        return TranscationManager(transactions)

SupportRecord = namedtuple('SupportRecord',('itsms','support'))
RelationRecord = namedtuple('RelationRecoed',SupportRecord._fields + ('ordered_statics',))
OrderedStatistic = namedtuple('OrderedStatistic',('item_base','item_add','confidence','lift',))

def create_next_candidates(prev_candidates,length):
    """
    Arguments:
        length, the lengths of next candidates.
    """
    item_set = set()
    for candidate in prev_candidates:
        for item in candidate:
            item_set.add(item)
    items = sorted(item_set)

    tmp_next_candidates = (frozenset(x) for x in combinations(items,length))

    # Return all the candidates if the length of the next candidates is 2
    # since their subsets are the same items
    if length <3:
        return list(tmp_next_candidates)
    
    # Filter candidates that all of their subsets are in previous candidates
    next_candidates = [
        candidate for candidate in tmp_next_candidates
        if all(
            True if frozenset(x) in prev_candidates else False
            for x in combinations(candidate,length -1)
        )
    ]
    return next_candidates

def get_support_records(transaction_manager,min_support,**kwargs):
    """
    Return a generator of support records with given transactions.

    Arguments:
        transaction_manager -- Transactions as a TransactionManager instance.
        min_support -- A minimum support (float).
    Keyword arguments:
        max_length -- The maximum length of relations (integer).
    """
    # Parse arguments.
    max_length = kwargs.get('max_length')

    # For testing.
    _create_next_candidates = kwargs.get('_create_next_candidates',create_next_candidates)

    # Process.
    candidates = transaction_manager.initial_candidates()
    length = 1
    while candidates:
        relations = set()
        for relation_candidate in candidates:
            support = transaction_manager.calc_support(relation_candidate)
            if support < min_support:
                continue
            candidate_set = frozenset(relation_candidate)
            relations.add(candidate_set)
            yield SupportRecord(candidate_set,support)
        length += 1
        if max_length and length >max_length:
            break
        candidates = _create_next_candidates(relations,length)

def gen_ordered_statistics(transaction_manager,record):
    """
    Returns a generator of ordered statistics as OrderedStatistic instances.
    Arguments:
        transaction_manager -- Transactions as a TransactionManager instance.
        record -- A support record as a SupportRecord instance.
    """
    items = record.items
    for combination_set in combinations(sorted(items),len(items)-1):
        items_base = frozenset(combination_set)
        items_add = frozenset(items.difference(items_base))
        confidence = (
            record.support / transaction_manager.calc_support(items_base)
        )
        lift = confidence / transaction_manager.calc_support(items_add)
        yield OrderedStatistic(
            frozenset(items_base),
            frozenset(items_add),
            confidence,
            lift
        )

def filter_ordered_statistics(ordered_statistics, **kwargs):
    """
    Filter OrderedStatistic objects.
    Arguments:
        ordered_statistics -- A OrderedStatistic iterable object.
    Keyword arguments:
        min_confidence -- The minimum confidence of relations (float).
        min_lift -- The minimum lift of relations (float).
    """
    min_confidence = kwargs.get('min_confidence',0.0)
    min_lift = kwargs.get('min_lift',0.0)

    for ordered_statistic in ordered_statistics:
        if ordered_statistic.confidence < min_confidence:
            continue
        if ordered_statistic.lift < min_lift:
            continue
        yield ordered_statistic

def apriori(transactions,**kwargs):
    """
    Executes Apriori algorithm and returns a RelationRecord generator.
    Arguments:
        transactions -- A transaction iterable object
                        (eg. [['A', 'B'], ['B', 'C']]).
    Keyword arguments:
        min_support -- The minimum support of relations (float).
        min_confidence -- The minimum confidence of relations (float).
        min_lift -- The minimum lift of relations (float).
        max_length -- The maximum length of the relation (integer).
    """
    # Parse the arguments.
    min_support = kwargs.get('min_support', 0.1)
    min_confidence = kwargs.get('min_confidence', 0.0)
    min_lift = kwargs.get('min_lift', 0.0)
    max_length = kwargs.get('max_length', None)
    
    #Check argumensts.
    if min_support <= 0:
        raise ValueError('minimum support must be > 0')

    # For testing.
    _gen_support_records = kwargs.get(
        '_gen_support_records', gen_support_records)
    _gen_ordered_statistics = kwargs.get(
        '_gen_ordered_statistics', gen_ordered_statistics)
    _filter_ordered_statistics = kwargs.get(
        '_filter_ordered_statistics', filter_ordered_statistics)

    # Calculate supports.
    transaction_manager = TranscationManager.create(transactions)
    support_records = _gen_support_records(
        transaction_manager,min_support,max_length = max_length)

    #Calculate ordered stats.
    for support_record in support_records:
        ordered_statics = list(
            _filter_ordered_statistics(
                _gen_ordered_statistics(transaction_manager,support_record),
                min_confidence = min_confidence,
                min_lift = min_lift,
            )
        )
        if not ordered_statics:
            continue
        yield RelationRecord(support_record.itsms,support_record.support,ordered_statics)
    