#!/usr/bin/env bash

echo "Downloading cancer-invasion-workflow required containers... Please wait..."

CURRENT_DIR=$(pwd)
CONTAINER_FOLDER=$(pwd)/cancer-invasion-workflow-containers
mkdir -p ${CONTAINER_FOLDER}
cd ${CONTAINER_FOLDER}

apptainer pull physicell_invasion.sif docker://ghcr.io/permedcoe/physicell_invasion:latest
apptainer pull invasion_analysis.sif docker://ghcr.io/permedcoe/invasion_analysis:latest

cd ${CURRENT_DIR}

echo "cancer-invasion-workflow required containers downloaded"
echo ""
echo "Containers stored in: ${CONTAINER_FOLDER}"
echo ""
echo "Please, don't forget to run:"
echo "    export PERMEDCOE_IMAGES=${CONTAINER_FOLDER}"
echo "Before running the workflow."
echo ""
