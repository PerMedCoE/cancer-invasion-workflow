#!/usr/bin/env bash

echo "Cleaning cancer-invasion-workflow required Building Blocks... Please wait..."

CURRENT_DIR=$(pwd)
# SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cd ../../../BuildingBlocks

cd PhysiBoSS_invasion
./clean.sh
cd ..

cd invasion_analysis
./clean.sh
cd ..

cd ${CURRENT_DIR}
