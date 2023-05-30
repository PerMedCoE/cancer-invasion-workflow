#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
if [[ -z "${PERMEDCOE_IMAGES}" ]]; then
  default_images=$(realpath ${SCRIPT_DIR}/../../BuildingBlocks/Resources/images/)/
  export PERMEDCOE_IMAGES=${default_images}
  echo "WARNING: PERMEDCOE_IMAGES environment variable not set. Using default: ${default_images}"
else
  echo "INFO: Using PERMEDCOE_IMAGES from: ${PERMEDCOE_IMAGES}"
fi
export COMPUTING_UNITS=1

mkdir $(pwd)/result/

TEMP_DIRECTORY=$(pwd)/results_wd
mkdir -p ${TEMP_DIRECTORY}

PhysiBoSS_invasion_BB \
    --debug \
    --parameter_set $(pwd)/../Resources/data/parameters_small.csv \
    --repetition 1 \
    --parallel ${COMPUTING_UNITS} \
    --max_time 100 \
    --out_file $(pwd)/result/physiboss_results.out \
    --err_file $(pwd)/result/physiboss_results.err \
    --results_dir $(pwd)/result/physiboss_results/ \
    --tmpdir ${TEMP_DIRECTORY}
