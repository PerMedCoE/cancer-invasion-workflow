#!/usr/bin/python3

import os
import csv

# To set building block debug mode
from permedcoe import set_debug
# Import building block tasks
from PhysiBoSS_Invasion_BB import physiboss_invasion
from invasion_analysis_BB import invasion_analysis
# Import utils
from utils import parse_input_parameters

# PyCOMPSs imports
from pycompss.api.api import compss_wait_on_directory
from pycompss.api.api import compss_wait_on_file
from pycompss.api.api import compss_wait_on


def main():
    """
    MAIN CODE
    """
    set_debug(False)

    print("----------------------------")
    print("| Cancer Invasion Workflow |")
    print("----------------------------")

    # GET INPUT PARAMETERS
    args = parse_input_parameters()

    parameters_sets = []
    with open(args.parameters_set, 'r') as psets:
        for line in psets.readlines():
            print(line)
            raw_pset = line.split(",")
            print(raw_pset)
            for value in raw_pset[1:]:
                parameters_sets.append((raw_pset[0].strip(), float(value.strip())))
                
    print(parameters_sets)

    for i_pset, parameter_set in enumerate(parameters_sets):
            
        pset_id = "parameter_%d" % i_pset 
        os.makedirs(os.path.join(args.outdir, pset_id))
        
        pset_filepath = os.path.join(args.outdir, pset_id, "parameter_set.csv")
        with open(pset_filepath, "w") as pset_file:
            pset_file.write("%s,%g" % (parameter_set[0], (parameter_set[1])))
        
        physiboss_results = []
        physiboss_subfolder = "physiboss_results"  # do not modify (hardcoded in meta-analysis)
        for r in range(1, args.reps + 1):
            print(">>> Repetition: " + str(r))
            name = "run_" + str(r)
            out_file = os.path.join(args.outdir, pset_id, physiboss_subfolder, name + ".out")
            err_file = os.path.join(args.outdir, pset_id, physiboss_subfolder, name + ".err")
            print("\t- " + out_file)
            print("\t- " + err_file)
            results_dir = os.path.join(args.outdir, pset_id, physiboss_subfolder, name)
            os.makedirs(results_dir)
            
            physiboss_results.append(results_dir)
            # PHYSIBOSS
            physiboss_invasion(parameter_set=pset_filepath,
                            repetition=r,
                            out_file=out_file,
                            err_file=err_file,
                            results_dir=results_dir,
                            max_time=args.max_time)

        for physiboss_result in physiboss_results:
            compss_wait_on_directory(physiboss_result)

        analysis_data_path = "invasion_analysis"
        os.makedirs(os.path.join(args.outdir, pset_id, analysis_data_path))
        invasion_analysis(os.path.join(args.outdir, pset_id, physiboss_subfolder), os.path.join(args.outdir, pset_id, analysis_data_path, "data.csv"))
        

if __name__ == "__main__":
    main()
