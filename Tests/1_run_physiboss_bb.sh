#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

export PERMEDCOE_IMAGES=${SCRIPT_DIR}/../../BuildingBlocks/Resources/images/
export COMPUTING_UNITS=10

# Self contained assets in package
PHYSIBOSS_INVASION_ASSETS=$(python3 -c "import PhysiBoSS_Invasion_BB; import os; print(os.path.dirname(PhysiBoSS_Invasion_BB.__file__))")

source ${SCRIPT_DIR}/aux.sh
disable_pycompss

mkdir $(pwd)/result/

PhysiBoSS_Invasion_BB -d \
    --mount_points ${PHYSIBOSS_ASSETS}/assets/:${PHYSIBOSS_ASSETS}/assets/ \
    --repetition 1 \
    --parallel ${COMPUTING_UNITS} \
    --max_time 100 \
    --out_file $(pwd)/result/physiboss_results.out \
    --err_file $(pwd)/result/physiboss_results.err \
    --results_dir $(pwd)/result/physiboss_results/

enable_pycompss
