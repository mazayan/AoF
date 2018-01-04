#!/usr/bin/env bash

#stop on first error
set -e

#CONFIG
readonly DATASET1_PATH="data/Accidental_Drug_Related_Deaths__2012-June_2017.csv"
readonly DATASET2_PATH="data/County_Dataset.csv"
readonly VENV_PATH="env"
#END CONFIG


main() {

    pip3 install virtualenv

    if [ -d $VENV_PATH ]; then
        echo "Skipping venv creation as it already exists."
    else
        echo "Creating venv..."
        #virtualenv create -r requirements.txt $VENV_PATH
        python -m virtualenv $VENV_PATH
        echo "Done Creating venv"
    fi

    #activate venv
    source $VENV_PATH/bin/activate
    pip install -r requirements.txt #put this in an if block
    echo "In venv"

    #if [ -f $DATASET1_PATH ]; then
    #    echo "Skipping download since opioid dataset exists"
    #else
    echo "Downloading opioid dataset..."
    curl -o $DATASET1_PATH https://data.ct.gov/api/views/rybz-nyjw/rows.csv?accessType=DOWNLOAD
    echo "Done downloading opioid dataset"
    #fi

    python Main.py

    #deactivate venv
    #source $VENV_PATH/bin/deactivate
    deactivate
    echo "Leaving venv..."

}

main