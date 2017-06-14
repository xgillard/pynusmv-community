'''
Don't pay any attention to this module, it is only present here for me to fiddle
with the tool while I'm developing it in my IDE
'''
import pynusmv_community.cmdline as cmdline
import pynusmv_community.main    as main
 
        
if __name__ == '__main__':
    model= "NMH21_2"
    path = "/Users/user/Documents/EXPERIMENTS/bmc_data/models/nameche" 
    prop = "G (v211.U_KM_07M.st = l -> (v211.U_07M_09M.st = l xor v211.U_07M_04M.st = l))"
    
    
    #model= "philo_9"                                  
    #path = "/Users/user/Documents/EXPERIMENTS/bmc_data/models"
    #prop = "F G (p1.waiting -> F !p1.waiting)"
    
    args     = cmdline.arguments().parse_args([
        '--path', path, '--formula', prop, '-k', '20', '-K', '20',
        '--dump-cnf', '--dump-stats',
        '--show-cluster-graph', 
        model
        ])
    
                                                                                  
    rng  = range(args.min_bound, 1+args.max_bound)
    main.process(args.path, args.model, args.formula, rng, args)
