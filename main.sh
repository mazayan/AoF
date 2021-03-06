#!/usr/bin/env bash

#stop on first error
set -e

#CONFIG
readonly DATASET1_PATH="./data/Accidental_Drug_Related_Deaths__2012-June_2017.csv"
readonly VENV_PATH="./env"
#END CONFIG


main() {
    echo "Installing requirements"
    sudo /usr/local/bin/pip3 install -r requirements.txt
    echo "Done installing requirements"

    if [ -s $DATASET1_PATH ]; then
        echo "Skipping download since opioid dataset exists"
    else
        echo "Downloading opioid dataset..."
        curl -o $DATASET1_PATH https://data.ct.gov/api/views/rybz-nyjw/rows.csv?accessType=DOWNLOAD
        echo "Done downloading opioid dataset"
    fi

    python3 Main.py

}

main