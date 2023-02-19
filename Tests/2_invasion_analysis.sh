#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

export PERMEDCOE_IMAGES=${SCRIPT_DIR}/../../BuildingBlocks/Resources/images/
export COMPUTING_UNITS=10

# Self contained assets in package
INVASION_ANALYSIS_ASSETS=$(python3 -c "import invasion_analysis_BB; import os; print(os.path.dirname(invasion_analysis_BB.__file__))")

source ${SCRIPT_DIR}/aux.sh
disable_pycompss

mkdir $(pwd)/result/

invasion_analysis_BB -d \
    --mount_points ${PHYSIBOSS_ASSETS}/assets/:${PHYSIBOSS_ASSETS}/assets/ \
    --physiboss_results_path $(pwd)/result/physiboss_results/ \
    --output_data $(pwd)/result/invasion_analysis/data.csv

enable_pycompss
