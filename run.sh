#!/bin/bash

# Download the required data if it does not exist

if ! test -d ./data; then
  echo "No data folder. Generating folder."
  mkdir ./data;
fi

if ! test -d ./data/SANGIS; then
  echo "No SANGIS folder. Generating folder."
  mkdir ./data/SANGIS;
fi

download () {
    if ! test -f ./data/$1; then
    echo "No $1 file. Downloading file."
    curl  -o ./data/$1 "$2";
    fi
}
download_sangis () {
    if ! test -f ./data/SANGIS/$1; then
    echo "No $1 file. Downloading file."
    curl  -o ./data/$1 "$2";
    fi
}


download "tracts.csv" "https://opendata.sandag.org/api/views/g3xq-yubj/rows.csv?date=20231211&accessType=DOWNLOAD"
download "ca_od_main_JT00_2021.csv.gz" "https://lehd.ces.census.gov/data/lodes/LODES8/ca/od/ca_od_main_JT00_2021.csv.gz"
download "Census_Blocks_20231127.csv" "https://opendata.sandag.org/api/views/bevn-aqff/rows.csv?date=20231211&accessType=DOWNLOAD"
download "ca_wac_S000_JT00_2021.csv.gz" "https://lehd.ces.census.gov/data/lodes/LODES8/ca/wac/ca_wac_S000_JT00_2021.csv.gz"
# download_sangis "Business_Enterprise_Zones_SD.ZIP" "https://rdw.sandag.org/Account/GetFSFile.aspx?dir=Business&Name=Business_Enterprise_Zones_SD.ZIP"
# download_sangis "BUSINESS_SITES.zip" "https://rdw.sandag.org/Account/GetFSFile.aspx?dir=Business&Name=BUSINESS_SITES.zip"

# Check if output folder exists
if ! test -d ./output; then
  echo "No output folder. Generating folder."
  mkdir ./output;
fi


# Change to the directory containing the Python scripts
cd ./python;

# Run the Python scripts

echo "Running cluster-generation.py";
python cluster-generation.py;


echo "Complete! Check /output for clusters.csv";