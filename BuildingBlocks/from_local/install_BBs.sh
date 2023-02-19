#!/usr/bin/env bash

echo "Installing cancer-invasion-workflow required Building Blocks... Please wait..."

CURRENT_DIR=$(pwd)
# SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cd ../../../BuildingBlocks

cd PhysiBoSS_Invasion
./install.sh
cd ..

cd invasion_analysis
./install.sh
cd ..


cd ${CURRENT_DIR}
