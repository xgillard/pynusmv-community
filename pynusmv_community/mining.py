'''
This module contains all the mining-related functionalities. These 
functions compute nothing per themselves (except trivial stuffs) and rely on 
core to do the heavy lifting.
'''

import os
from pynusmv_community import core

def mine_frequent_patterns(model, bound, clusters, graph):
    '''
    Mines the most frequent patterns in each of the `clusters` of the `graph`
    (based on their semantic value in the problem defined by `model` unrolled
    `bound` times) and dump them to a CSV file.
    
    .. note::
        Mining the patterns is somewhat weaker than mining the sequences. You
        might want to call that instead.
    '''
    import re
    import pymining.itemmining as _mine
    
    os.makedirs("{}/mining/{:03d}".format(model, bound), exist_ok=True)
    
    # represent a vertex
    reprs= lambda v: core.vertex_repr(graph, v)
    #  curate the communities
    curat= lambda c: [ reprs(v) for v in c if reprs(v) != '???' ]
    # represent a community as a set of transactions
    trans= lambda c: [ re.split('[\.\*]+', v) for v in curat(c) ]
    
    # mine the patterns of a community
    def _do_mine(community):
        # returns a dictionary {frozenset} -> {count}
        relim_in = _mine.get_relim_input(trans(community))
        patterns = _mine.relim(relim_in)
        return patterns
    
    def _mine_by_frequence(x):
        return sorted(_do_mine(x).items(), reverse=True, key=lambda t: t[1])
    
    with open("{}/mining/{:03d}/patterns.csv".format(model, bound), 'w') as f:
        # print the headline
        print('Community     ; Count ; Pattern', file = f)
        counter = 0
        for community in clusters :
            counter += 1
            for items,cnt in _mine_by_frequence(community):
                text = ' '.join(items)
                print("{:3d} ; {:5d} ; {}".format(counter, cnt, text), file = f)

def mine_frequent_sequences(model, bound, clusters, graph):
    '''
    Mines the most frequent sequences in each of the `clusters` of the `graph`
    (based on their semantic value in the problem defined by `model` unrolled
    `bound` times) and dump them to a CSV file.
    '''
    import re
    import pymining.seqmining as _mine
    
    os.makedirs("{}/mining/{:03d}".format(model, bound), exist_ok=True)
    
    # represent a vertex
    reprs= lambda v: core.vertex_repr(graph, v)
    #  curate the communities
    curat= lambda c: [ reprs(v) for v in c if reprs(v) != '???' ]
    # represent a community as a set of transactions
    trans= lambda c: [ re.split('[\.\*]+', v) for v in curat(c) ]
    
    # symbol table -> one integer represent one symbol
    def symbolic(transactions_list):
        sym_2_id = dict()
        id_2_sym = dict()
        counter  = 0
        
        # memoize tokens and ids
        for transaction in transactions_list:
            for token in transaction:
                if token not in sym_2_id:
                    counter         += 1
                    sym_2_id[token]  = counter
                    id_2_sym[counter]= token
        
        # convert tokens to id
        converted = [[sym_2_id[tok] for tok in transaction] for transaction in transactions_list ]
        
        return (converted, id_2_sym)
    
    # define what can be mined
    minable = lambda c: symbolic(trans(c))
    
    with open("{}/mining/{:03d}/sequences.csv".format(model, bound), 'w') as f:
        # print the headline
        print('Community     ; Count ; Sequence', file = f)
        counter = 0
        for community in clusters:
            counter    += 1
            seqs, conv = minable(community)
            freq_seqs  = _mine.freq_seq_enum(seqs, 2)
            freq_seqs  = sorted(freq_seqs, reverse=True, key=lambda x: (x[1], len(x[0])))
            
            # Now dump the mined information to file
            for seq,cnt in freq_seqs:
                items= [conv[i] for i in seq]
                text = '.'.join(items)
                print("Community {:3d} ; {:5d} ; {}".format(counter, cnt, text), file = f)
    
