#!/usr/bin/env bash

echo "Installing cancer-invasion-workflow required Building Blocks... Please wait..."

python3 -m pip install 'git+https://github.com/PerMedCoE/BuildingBlocks.git@main#subdirectory=PhysiBoSS_Invasion'
python3 -m pip install 'git+https://github.com/PerMedCoE/BuildingBlocks.git@main#subdirectory=invasion_analysis'

echo "cancer-invasion-workflow required Building Blocks installed"
