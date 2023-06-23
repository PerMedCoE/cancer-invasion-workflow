#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
if [[ -z "${PERMEDCOE_IMAGES}" ]]; then
  default_images=$(realpath ${SCRIPT_DIR}/../../../BuildingBlocks/Resources/images/)/
  export PERMEDCOE_IMAGES=${default_images}
  echo "WARNING: PERMEDCOE_IMAGES environment variable not set. Using default: ${default_images}"
else
  echo "INFO: Using PERMEDCOE_IMAGES from: ${PERMEDCOE_IMAGES}"
fi

dataset=$(pwd)/../../Resources/data

# Set the tool internal parallelism and constraint
export COMPUTING_UNITS=1

runcompss \
    --log_level=off \
    --graph \
    --python_interpreter=python3 \
    $(pwd)/src/cancer_invasion.py \
      ${dataset}/parameters_small.csv \
      $(pwd)/results/ \
      5 \
      20 #4500


######################################################
# APPLICATION EXECUTION EXAMPLE
# Call:
#       ./run.sh
#
# Example:
#       ./run.sh
######################################################
