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
    
def clouds(model, bound, clusters, graph):
    '''
    Saves the wordclouds for the communities stored in the `clusters` of the 
    `graph` derived from `bound` unrolling of the time for `model`
    '''
    os.makedirs("{}/clouds/{:03d}".format(model, bound), exist_ok=True)
    s_cluster = [ [misc.vertex_repr(graph, v) for v in c ] for c in clusters ]
    with open("{}/clouds/{:03d}/raw.txt".format(model, bound), 'w') as f:
        counter = 0
        for s in s_cluster:
            counter += 1
            text = " ".join(s)
            cloud= WordCloud().generate(text)
            
            cloud.to_file("{}/clouds/{:03d}/{:03d}.png".format(model, bound, counter))
            print( "{:03d} -> {}".format(counter, text) , file=f )
            
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