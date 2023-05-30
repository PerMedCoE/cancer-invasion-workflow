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
from pycompss.api.api import compss_wait_on_file
from pycompss.api.api import compss_barrier
from pycompss.api.api import compss_wait_on


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
    simulations_path = "simulations"
    for i_pset, parameter_set in enumerate(parameters_sets):
        pset_id = "parameter_%d" % i_pset
        os.makedirs(os.path.join(args.outdir, simulations_path, pset_id))
        pset_filepath = os.path.join(
            args.outdir, simulations_path, pset_id, "parameter_set.csv"
        )
        with open(pset_filepath, "w") as pset_file:
            pset_file.write("%s,%g" % (parameter_set[0], (parameter_set[1])))
        physiboss_results = []
        physiboss_subfolder = (
            "physiboss_results"  # do not modify (hardcoded in meta-analysis)
        )
        for r in range(1, args.reps + 1):
            print(">>> Repetition: " + str(r))
            name = "run_" + str(r)
            out_file = os.path.join(
                args.outdir,
                simulations_path,
                pset_id,
                physiboss_subfolder,
                name + ".out",
            )
            err_file = os.path.join(
                args.outdir,
                simulations_path,
                pset_id,
                physiboss_subfolder,
                name + ".err",
            )
            print("\t- " + out_file)
            print("\t- " + err_file)
            results_dir = os.path.join(
                args.outdir, simulations_path, pset_id, physiboss_subfolder, name
            )
            os.makedirs(results_dir)

            physiboss_results.append(results_dir)
            # PHYSIBOSS
            physiboss_invasion(
                parameter_set=pset_filepath,
                repetition=r,
                out_file=out_file,
                err_file=err_file,
                results_dir=results_dir,
                parallel=os.environ["COMPUTING_UNITS"],
                max_time=args.max_time,
                tmpdir=TMPDIR,
            )

        for physiboss_result in physiboss_results:
            compss_wait_on_directory(physiboss_result)

        analysis_subfolder = "invasion_analysis"
        analysis_path = os.path.join(
            args.outdir, simulations_path, pset_id, analysis_subfolder
        )
        physiboss_result_path = os.path.join(
            args.outdir, simulations_path, pset_id, physiboss_subfolder
        )

        os.makedirs(analysis_path)
        analysis_paths.append(os.path.join(analysis_path, "data.csv"))

        invasion_analysis(
            tmpdir=TMPDIR,
            physiboss_result_path=physiboss_result_path,
            output_data=os.path.join(analysis_path, "data.csv"),
        )

    for analysis_path in analysis_paths:
        compss_wait_on_file(analysis_path)

    invasion_plots_directory = os.path.join(args.outdir, "plots")
    os.makedirs(invasion_plots_directory)
    invasion_generate_plots(
        tmpdir=TMPDIR,
        simulations_path=os.path.join(args.outdir, simulations_path),
        parameter_sets=args.parameters_set,
        plot_directory=invasion_plots_directory,
    )

    compss_wait_on_directory(invasion_plots_directory)


if __name__ == "__main__":
    main()
