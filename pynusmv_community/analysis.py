'''
This is the main module that is used to kickstart the problem generation and
analysis.
'''
import pandas

from pynusmv.init      import init_nusmv
from pynusmv.glob      import load
from pynusmv.bmc.glob  import BmcSupport

from pynusmv_community import misc
from pynusmv_community import output


def analyze_one(
        model, bound, formula=None, 
        dimacs= False, # do I want to keep the .cnf file ?
        draw  = False, # do I want to draw a graph ?
        clouds= False, # do I want to generate one wordcloud per community 
        ):
    '''
    Analyzes the `model` for one given depth and one given `formula`. This step
    generates one dataframe of statistics corresponding to a shallow analysis
    of the problem. However, the analysis can be enriched with the following
    flags to produce additional artifacts (side effects) to help make a deeper
    analysis.
    
        + 'dimacs = True' will produce a *.cnf file containing the dimacs
           representation of the problem
        + 'draw   = True' will produce a *.png file visually representing the 
           variable graph.
        + 'clouds = True' will produce a wordcloud (*.png file) per analyzed
           community to show the semantic information that occurs the most often
           in that community.
           
    .. note::
        It is assumed that pynusmv is initialized, the model is loaded and 
        the bmc sub system is ready to operate too.
        
    :param model: the name of the model being treated. This serves no point 
        besides 'self documentation' (generating the folder structures with 
        the appropriate names)
    :param bound: the number of time steps to generate on the problem path
    :param formula: an LTL formula to be checked via model checking (may be None)
    
    :return: a dictionary collecting the informations about the instance, its 
        bound and the number of communities and the graph modularity. This can
        be later collected into a dataframe to build evolution statistics
    '''
    cnf      = misc.mk_cnf(bound, formula)
    graph    = misc.mk_graph(cnf)
    clusters = graph.community_multilevel()
    
    # generate the dimacs instance if needed
    if dimacs:
        output.dimacs(model, bound, cnf)
    
    # generate the variable graph if needed
    if draw:
        output.structure(model, bound, clusters, graph)
    
    # generate word clouds if needed
    if clouds:
        output.clouds(model, bound, clusters, graph)
                
    return  {
            'instance'     : [model], 
            'bound'        : [bound],
            '#communities' : [misc.community_count(clusters)],
            'modularity'   : [clusters.modularity]
            }
    

def analyze_all(
        model, 
        formula  = None, 
        depths   = range(10),
        dimacs   = False,
        draw     = False,
        clouds   = False,
        stats    = False):
    '''
    Repeatedly performs the analysis of `model` for all `depth`. By default,
    this analysis generates no output. However the following flags can be 
    customized to generate derived artifacts.
    
        + 'dimacs = True' will produce a *.cnf file containing the dimacs
           representation of the problem
        + 'draw   = True' will produce a *.png file visually representing the 
           variable graph.
        + 'clouds = True' will produce a wordcloud (*.png file) per analyzed
           community to show the semantic information that occurs the most often
           in that community.
        + 'stats  = True' will produce a csv file containing all the raw 
           statistical data alongside with two charts plotting the evolution of
           the #communities and modulatity over time
    
    .. note::
        It is assumed that pynusmv is initialized, the model is loaded and 
        the bmc sub system is ready to operate too.
    
    :param model: the name of the model being treated. This serves no point 
        besides 'self documentation' (generating the folder structures with 
        the appropriate names)
    :param formula: an LTL formula to be checked via model checking (may be None)
    :param depths: a range of path lengths for which to generate and analyze
        SAT problems.
    '''
    frames = []
    for bound in depths:
        record = analyze_one(model, bound, formula, dimacs, draw, clouds)
        frames.append( pandas.DataFrame.from_dict(record) )
        
    # gather statistic data
    if stats:
        output.statistics(model, frames)
        

def process(
        path_to,
        model, 
        formula  = None, 
        depths   = range(10),
        dimacs   = False,
        draw     = False,
        clouds   = False,
        stats    = False):
    '''
    Initializes PyNuSMV and loads the model, then proceeds to the bulk of the
    analysis. See `analyze_one` and `analyze_all` for further details about 
    what is done.
    
    By default, this analysis generates no output. However the following flags 
    can be customized to generate derived artifacts.
    
        + 'dimacs = True' will produce a *.cnf file containing the dimacs
           representation of the problem
        + 'draw   = True' will produce a *.png file visually representing the 
           variable graph.
        + 'clouds = True' will produce a wordcloud (*.png file) per analyzed
           community to show the semantic information that occurs the most often
           in that community.
        + 'stats  = True' will produce a csv file containing all the raw 
           statistical data alongside with two charts plotting the evolution of
           the #communities and modulatity over time
    '''
    
    with init_nusmv():
        load(misc.merge_model_text(path_to, model+".smv"))
        
        with BmcSupport():
            analyze_all(model, formula, depths, dimacs, draw, clouds, stats)
            
def main():
    # TODO parse command line arguments
    process("/Users/user//Documents/EXPERIMENTS/bmc_data/models/nameche", 
            "NMH21_2", 
            depths = range(3), 
            draw   = True)
    
if __name__ == "__main__":
    main()