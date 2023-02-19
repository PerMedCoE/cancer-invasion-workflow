#!/usr/bin/env bash

echo "Uninstalling cancer-invasion-workflow required Building Blocks... Please wait..."

python3 -m pip uninstall -y PhysiBoSS_Invasion_BB
python3 -m pip uninstall -y invasion_analysis_BB

echo "Uninstall finished"
