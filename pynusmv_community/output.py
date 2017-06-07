'''
This module serves the solve purpose of gathering the functions producing output
files for the main analysis process.
'''

import os
import igraph
import pandas

from wordcloud         import WordCloud
from pynusmv_community import misc


def dimacs(model, bound, cnf):
    '''
    Saves the DIMACS output for the given `cnf` formula derived from `model`
    unrolled `bound` times
    '''
    os.makedirs("{}/instances/".format(model), exist_ok=True)
    with open("{}/instances/{:03d}.cnf".format(model, bound), 'w') as f:
        f.write(misc.to_dimacs(cnf))
        
def structure(model, bound, clusters, graph):
    '''
    Saves an image representing the structure of the sat problem derived from
    `model` unrolled `bound` times and classified in `clusters`
    '''
    os.makedirs("{}/structure/".format(model), exist_ok=True)
    igraph.plot(clusters, 
                layout  = graph.layout("large_graph"),
                bbox    = (0, 0, 2400, 2400),
                target  = "{}/structure/{:03d}.png".format(model, bound))
  
def communities(model, bound, clusters, graph):
    '''
    Saves text file dumps for the communities stored in the `clusters` of the 
    `graph` derived from `bound` unrolling of the time for `model`
    '''
    os.makedirs("{}/communities/{:03d}".format(model, bound), exist_ok=True)
    s_cluster = [ [misc.vertex_repr(graph, v) for v in c ] for c in clusters ]
    
    # DUMP the complete information (containing ???)
    with open("{}/communities/{:03d}/raw.txt".format(model, bound), 'w') as f:
        # But also CURATE the data to make it easier to read
        with open("{}/communities/{:03d}/curated.txt".format(model, bound), 'w') as c:
            counter = 0
            for s in s_cluster:
                counter += 1
                # raw information
                text = " ".join(sorted(s))
                print( "{:03d} -> {}\n".format(counter, text) , file=f )
                
                # curated info
                text = " ".join(sorted(filter(lambda x: x!="???", s)))
                print( "{:03d} -> {}\n".format(counter, text) , file=c )


def clouds(model, bound, clusters, graph):
    '''
    Saves the wordclouds for the communities stored in the `clusters` of the 
    `graph` derived from `bound` unrolling of the time for `model`
    '''
    os.makedirs("{}/clouds/{:03d}".format(model, bound), exist_ok=True)
    s_cluster = [ [misc.vertex_repr(graph, v) for v in c ] for c in clusters ]
    
    counter = 0
    for s in s_cluster:
        counter += 1
        
        # curated info
        text = " ".join(sorted(filter(lambda x: x!="???", s)))
        cloud= WordCloud(stopwords={},regexp=r'\w[\.\[\]\{\}\w]+').generate(text)
        cloud.to_file("{}/clouds/{:03d}/{:03d}.png".format(model, bound, counter))


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
    reprs= lambda v: misc.vertex_repr(graph, v)
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
    reprs= lambda v: misc.vertex_repr(graph, v)
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
    

def statistics(model, frames):
    '''
    Aggregates and produces machine processable statistics from the `frames` 
    obtained from `model`.
    '''
    os.makedirs("{}/stats/".format(model), exist_ok=True)
        
    # compute the results
    results = pandas.concat( frames )
    chart   = lambda z: results[['bound', z]].plot(x='bound', y=z, kind="scatter")
    commu   = chart('#communities').get_figure()
    modul   = chart("modularity").get_figure()
    
    # save 'em to file
    results.to_csv("{}/stats/data.csv".format(model))
    commu.savefig('{}/stats/comunities.png'.format(model))
    modul.savefig('{}/stats/modularity.png'.format(model))