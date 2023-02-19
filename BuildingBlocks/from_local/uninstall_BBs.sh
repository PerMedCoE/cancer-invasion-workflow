#!/usr/bin/env bash

echo "Uninstalling cancer-invasion-workflow required Building Blocks... Please wait..."

CURRENT_DIR=$(pwd)
# SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cd ../../../BuildingBlocks

cd PhysiBoSS_Invasion
./uninstall.sh
cd ..

cd invasion_analysis
./uninstall.sh
cd ..

cd ${CURRENT_DIR}
