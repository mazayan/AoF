#!/usr/bin/env bash

#stop on first error
set -e

#CONFIG
#readonly DATASET1_PATH="/usr/bin/env/AoF_Project/data/"
#readonly DATASET2_PATH="/usr/bin/env/AoF_Project/data/County_Dataset.csv"
#readonly VENV_PATH="/usr/bin/env"

readonly DATASET1_PATH="~/env/data/"
readonly DATASET2_PATH="~/env/data/County_Dataset.csv"
readonly VENV_PATH="~/env"

python3 -m venv /Users/Mazayan/Desktop
#END CONFIG


main() {

    git clone....

    if [ -d $VENV_PATH ]; then
        echo "Skipping venv creation as it already exists."
    else
        echo "Creating venv..."
        #virtualenv create -r requirements.txt $VENV_PATH
        python3 -m virtualenv $VENV_PATH
        pip3 install -r requirements.txt
        echo "Done Creating venv"
    fi

    #activate venv
    source $VENV_PATH/activate
    echo "In venv"

    if [ -f $DATASET1_PATH ]; then
        echo "Skipping download since opioid dataset exists"
    else
        echo "Downloading opioid dataset..."
        curl -o $DATASET1_PATH https://data.ct.gov/api/views/rybz-nyjw/rows.csv?accessType=DOWNLOAD
        echo "Done downloading opioid dataset"
    fi

    python Main.py

    #deactivate venv
    source $VENV_PATH/deactivate
    echo "Leaving venv..."

}

main