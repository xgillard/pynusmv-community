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
    args = Params(model, path_to = path, mine_patterns = True, mine_sequences = True)
    rng  = range(args.min_bound, 1+args.max_bound)
    process(args.path_to, args.model, args.formula, rng, args)
