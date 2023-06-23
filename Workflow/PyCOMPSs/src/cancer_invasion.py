#!/usr/bin/python3

import os

# To set the default PyCOMPSs TMPDIR
from permedcoe import TMPDIR

# Import building block tasks
from PhysiBoSS_invasion_BB import physiboss_invasion
from invasion_analysis_BB import invasion_analysis
from invasion_analysis_BB import invasion_generate_plots

# Import utils
from utils import parse_input_parameters

# PyCOMPSs imports
from pycompss.api.api import compss_wait_on_directory


def main():
    """
    MAIN CODE
    """
    print("----------------------------")
    print("| Cancer Invasion Workflow |")
    print("----------------------------")

    # GET INPUT PARAMETERS
    args = parse_input_parameters()

    parameters_sets = []
    with open(args.parameters_set, "r") as psets:
        for line in psets.readlines():
            print(line)
            raw_pset = line.split(",")
            print(raw_pset)
            for value in raw_pset[1:]:
                parameters_sets.append((raw_pset[0].strip(), float(value.strip())))

    analysis_paths = []
    simulations_subfolder = "simulations"
    simulations_path = os.path.join(args.outdir, simulations_subfolder)

    for i_pset, parameter_set in enumerate(parameters_sets):
        pset_id = "parameter_%d" % i_pset

        main_results_path = os.path.join(simulations_path, pset_id)

        os.makedirs(main_results_path)
        pset_filepath = os.path.join(main_results_path, "parameter_set.csv")

        with open(pset_filepath, "w") as pset_file:
            pset_file.write("%s,%g" % (parameter_set[0], (parameter_set[1])))

        physiboss_results = []
        # Do not modify physiboss_subfolder (it is hardcoded in meta-analysis)
        physiboss_subfolder = "physiboss_results"
        physiboss_result_path = os.path.join(main_results_path, physiboss_subfolder)

        physiboss_final_net_results = []

        for r in range(1, args.reps + 1):
            print(">>> Repetition: " + str(r))
            name = "run_" + str(r)
            out_file = os.path.join(physiboss_result_path, name + ".out")
            err_file = os.path.join(physiboss_result_path, name + ".err")
            print("\t- " + out_file)
            print("\t- " + err_file)

            results_dir = os.path.join(physiboss_result_path, name)
            os.makedirs(results_dir)
            physiboss_results.append(results_dir)

            final_net_dir = os.path.join(physiboss_result_path, name + "_final_net")
            os.makedirs(final_net_dir)
            physiboss_final_net_results.append(final_net_dir)

            # PhysiBoSS
            physiboss_invasion(
                parameter_set=pset_filepath,
                repetition=r,
                out_file=out_file,
                err_file=err_file,
                results_dir=results_dir,
                parallel=os.environ["COMPUTING_UNITS"],
                max_time=args.max_time,
                final_net_dir=final_net_dir,
                tmpdir=TMPDIR,
            )

        analysis_subfolder = "invasion_analysis"
        analysis_path = os.path.join(main_results_path, analysis_subfolder)

        os.makedirs(analysis_path)
        output_data = os.path.join(analysis_path, "data_%s.csv" % str(i_pset))
        analysis_paths.append(output_data)

        invasion_analysis(TMPDIR, output_data, *physiboss_final_net_results)

    invasion_plots_path = os.path.join(args.outdir, "plots")
    os.makedirs(invasion_plots_path)

    invasion_generate_plots(
        TMPDIR, args.parameters_set, invasion_plots_path, *analysis_paths
    )

    compss_wait_on_directory(invasion_plots_path)


if __name__ == "__main__":
    main()
