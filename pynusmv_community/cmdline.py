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
    args.add_argument("-k", "--bound",
                      type=int,
                      default=10,
                      help="The problem bound (max number of steps in a trace)")
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
    args.add_argument("-S", "--stats",
                      #type   = bool,
                      default= False,
                      action = 'store_true',
                      help   = 'Generate statistics')
    return args.parse_args()

def do_nothing_flags():
    flags = namedtuple('Flags', 'dimacs structure clouds stats')
    return flags(False, False, False, False)
    

