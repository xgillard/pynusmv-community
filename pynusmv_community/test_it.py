'''
Don't pay any attention to this module, it is only present here for me to fiddle
with the tool while I'm developing it in my IDE
'''
from pynusmv_community.analysis import process

class Params:
    def __init__(self, model, **kwargs):
        self.model       = model
        self.path_to     = kwargs.get('path_to',     '.')
        self.formula     = kwargs.get('formula',     None)
        
        self.min_bound   = kwargs.get('min_bound',   10)
        self.max_bound   = kwargs.get('max_bound',   10)
        
        self.dimacs      = kwargs.get('dimacs',      False)
        self.structure   = kwargs.get('structure',   False)
        self.clouds      = kwargs.get('clouds',      False)
        self.communities = kwargs.get('communities', False)
        self.stats       = kwargs.get('stats',       False)
        self.verbose     = kwargs.get('verbose',     False)
        
        # TODO add to cmdline (+ default flags)
        self.mine_patterns  = kwargs.get('frequent_patterns',  False)
        self.mine_sequences = kwargs.get('frequent_sequences', False)
        
        
if __name__ == '__main__':
    model= "NMH21_2"
    path = "/Users/user/Documents/EXPERIMENTS/bmc_data/models/nameche" 
    prop = "G (v211.U_KM_07M.st = l -> (v211.U_07M_09M.st = l xor v211.U_07M_04M.st = l))"
    args = Params(model, 
                  path_to        = path,
                  formula        = prop,
                  min_bound      = 33, 
                  max_bound      = 33,
                   
                  structure      = True,
                  stats          = True,
                  mine_sequences = True,
                  verbose        = True
                  )
    
    
    #model= "philo_9"                                  
    #path = "/Users/user/Documents/EXPERIMENTS/bmc_data/models"
    #prop = "F G (p1.waiting -> F !p1.waiting)"
    #args = Params(model,                              
    #              path_to   = path,                   
    #              structure = True,                   
    #              formula   = prop,                   
    #              min_bound = 100,                     
    #              max_bound = 100)                     
    #                                                                              
    rng  = range(args.min_bound, 1+args.max_bound)
    process(args.path_to, args.model, args.formula, rng, args)
