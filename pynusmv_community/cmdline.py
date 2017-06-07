'''
This module contains nothing but the logic to parse the command line arguments
'''
import argparse

from collections import namedtuple 

def arguments():
    args = argparse.ArgumentParser(description="""
        A tool to analyze the community structure of SAT BMC problem instances
    """)
    
    args.add_argument("model",
                      help="The model to load")
    args.add_argument("-p", "--path-to",
                      type = str,
                      default = ".",
                      help = "The path to the folder containing the 'main' module")
    
    # The time steps to consider
    args.add_argument("-k", "--min-bound",
                      type=int,
                      default=0,
                      help="The minimal problem size")
    args.add_argument("-K", "--max-bound",
                      type=int,
                      default=10,
                      help="The maximal problem size")
    
    args.add_argument("-f", "--formula",
                      help = "A formula to generate the model checking problem")
    # Customization flags
    args.add_argument("-d", "--dimacs",
                      #type   = bool,
                      default= False,
                      action = 'store_true',
                      help   = 'Generate a DIMACS .cnf file for each instance')
    args.add_argument("-s", "--structure",
                      #type   = bool,
                      default= False,
                      action = 'store_true',
                      help   = 'Generate a variable graph for each instance')
    args.add_argument("-c", "--clouds",
                      #type   = bool,
                      default= False,
                      action = 'store_true',
                      help   = 'Generate a word cloud for each community of each instance')
    args.add_argument("-C", "--communities",
                      #type   = bool,
                      default= False,
                      action = 'store_true',
                      help   = 'Generate 2 files with the communities analyzed (raw and curated)')
    args.add_argument("-S", "--stats",
                      #type   = bool,
                      default= False,
                      action = 'store_true',
                      help   = 'Generate statistics')
    args.add_argument("-v", "--verbose",
                      #type   = bool,
                      default= False,
                      action = 'store_true',
                      help   = 'Verbose information during the run')
    return args.parse_args()

def do_nothing_flags():
    flags = namedtuple('Flags', 'dimacs structure clouds stats')
    return flags(False, False, False, False)
    
def log_verbose(func):
    '''
    Decorator that logs the call to a function if it is called with a keyword
    flags which has an attribute 'verbose' set to true.
    '''
    def logger(*args, **kwargs):
        print("{} | {} {}".format(func.__name__, *args, **kwargs))
        func(*args, **kwargs)
    return logger
