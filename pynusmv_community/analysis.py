'''
This is the main module that is used to kickstart the problem generation and
analysis.
'''
import pandas

from pynusmv.init      import init_nusmv
from pynusmv.glob      import load
from pynusmv.bmc.glob  import BmcSupport

from pynusmv_community import cmdline
from pynusmv_community import misc
from pynusmv_community import output

IDLE = cmdline.do_nothing_flags()

@cmdline.log_verbose
def analyze_one(model, bound, formula=None, flags = IDLE):
    '''
    Analyzes the `model` for one given depth and one given `formula`. This step
    generates one dataframe of statistics corresponding to a shallow analysis
    of the problem. However, the analysis can be enriched with the following
    flags to produce additional artifacts (side effects) to help make a deeper
    analysis.
    
        + 'dimacs = True' will produce a *.cnf file containing the dimacs
           representation of the problem
        + 'structure = True' will produce a *.png file visually representing the 
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
    if flags.dimacs:
        output.dimacs(model, bound, cnf)
    
    # generate the variable graph if needed
    if flags.structure:
        output.structure(model, bound, clusters, graph)
    
    # generate word clouds if needed
    if flags.clouds:
        output.clouds(model, bound, clusters, graph)
    
    # generate the communities dump if needed
    if flags.communities:
        output.communities(model, bound, clusters, graph)
    
    return  {
            'instance'     : [model], 
            'bound'        : [bound],
            '#communities' : [misc.community_count(clusters)],
            'modularity'   : [clusters.modularity]
            }
    

def analyze_all(model, formula = None, depths = range(10), flags = IDLE):
    '''
    Repeatedly performs the analysis of `model` for all `depth`. By default,
    this analysis generates no output. However the following flags can be 
    customized to generate derived artifacts.
    
        + 'dimacs = True' will produce a *.cnf file containing the dimacs
           representation of the problem
        + 'structure = True' will produce a *.png file visually representing the 
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
        record = analyze_one(model, bound, formula, flags)
        frames.append( pandas.DataFrame.from_dict(record) )
        
    # gather statistic data
    if flags.stats:
        output.statistics(model, frames)
        

def process(path_to, model, formula = None, depths = range(10), flags = IDLE):
    '''
    Initializes PyNuSMV and loads the model, then proceeds to the bulk of the
    analysis. See `analyze_one` and `analyze_all` for further details about 
    what is done.
    
    By default, this analysis generates no output. However the following flags 
    can be customized to generate derived artifacts.
    
        + 'dimacs = True' will produce a *.cnf file containing the dimacs
           representation of the problem
        + 'structure = True' will produce a *.png file visually representing the 
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
            analyze_all(model, formula, depths, flags)
            
def main():
    '''
    The main entry point of the tool. See --help for the full details of what
    it can do.
    '''
    args = cmdline.arguments()
    rng  = range(args.min_bound, 1+args.max_bound)
    process(args.path_to, args.model, args.formula, rng, args)
    
if __name__ == "__main__":
    main()