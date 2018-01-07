#!/usr/bin/env bash

#stop on first error
set -e

#CONFIG
readonly DATASET1_PATH="./data/Accidental_Drug_Related_Deaths__2012-June_2017.csv"
readonly DATASET2_PATH="./data/County_Dataset.csv"
readonly VENV_PATH="./env"
#END CONFIG


main() {

    echo "Installing virtualenv"
    python3 -m pip install virtualenv

    if [ -d $VENV_PATH ]; then
        echo "Skipping venv creation as it already exists."
    else
        echo "Creating virtualenv..."
        #virtualenv --python=/usr/bin/python3.6 $VENV_PATH
        python3 virtualenv $VENV_PATH
        echo "Done Creating virtualenv"
    fi

    #activate venv
    source $VENV_PATH/bin/activate

    echo "In venv"

    python3 -m pip install -U pip setuptools

    echo "Installing requirements"
    python3 -m pip install -r requirements.txt
    echo "Done installing requirements"

    if [ -s $DATASET1_PATH ]; then
        echo "Skipping download since opioid dataset exists"
    else
        echo "Downloading opioid dataset..."
        curl -o $DATASET1_PATH https://data.ct.gov/api/views/rybz-nyjw/rows.csv?accessType=DOWNLOAD
        echo "Done downloading opioid dataset"
    fi

    python3 Main.py

    deactivate
    echo "Leaving venv..."

}

main