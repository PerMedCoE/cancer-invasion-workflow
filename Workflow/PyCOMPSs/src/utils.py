import os
import argparse

##########################################
############ INPUT PARAMETERS ############
##########################################


def create_parser():
    """
    Create argument parser
    """
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("parameters_set", type=str, help="List of parameters set")
    parser.add_argument("outdir", type=str, help="Output directory")
    parser.add_argument("reps", type=int, help="Number of repetitions")
    parser.add_argument("max_time", type=int, help="Maximum simulation time")
    return parser


def parse_input_parameters(show=True):
    """
    Parse input parameters
    """
    parser = create_parser()
    args = parser.parse_args()
    if show:
        print()
        print(">>> WELCOME TO THE CANCER INVASION WORKFLOW")
        print("> Parameters:")
        print("\t- parameters set: %s" % args.parameters_set)
        print("\t- output folder: %s" % args.outdir)
        print("\t- replicates: %s" % str(args.reps))
        print("\t- max time: %d" % args.max_time)
        print("\n")
    return args


################################################
############ CHECK INPUT PARAMETERS ############
################################################


def check_input_parameters(args):
    """
    Check input parameters
    """
    if os.path.exists(args.outdir):
        print("WARNING: the output folder already exists")
    else:
        os.makedirs(args.outdir)
