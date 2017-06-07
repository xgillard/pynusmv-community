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
    
    counter = 0
    for s in s_cluster:
        counter += 1
        
        # curated info
        text = " ".join(sorted(filter(lambda x: x!="???", s)))
        cloud= WordCloud(stopwords={},regexp=r'\w[\.\[\]\{\}\w]+').generate(text)
        cloud.to_file("{}/clouds/{:03d}/{:03d}.png".format(model, bound, counter))
  
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