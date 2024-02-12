# DSC180A-Activity-Centers

This repo generates 'Activity Centers', which are boundaries of high density of Activity in the San Diego County Region.

## To generate the export

### Activate your Conda environment.

This file will download the required data, and generate the exports to the output/ folder. Anaconda needs to be installed and configured before running this script.

To create a conda environment compatable with our code, run `conda env create --file=environment.yml -n activity_centers` in the root directory of this project.

Then, to activate it, run `conda activate activity_centers`

### Download necessary data

Most of the data sources for this project automatically download through our run.sh script, however one business sites dataset needs to be downloaded from a publicly available source, SanGIS. This requires a free public account before downloading, which our bash script could not perform. The data can be downloaded from here:
https://rdw.sandag.org/Account/GetFSFile.aspx?dir=Business&Name=BUSINESS_SITES.zip

This file needs to be extracted in the SANGIS folder in '/data', which may not be generated until the run.sh file is run. The final path should be '/data/SANGIS/BUSINESS_SITES/BUSINESS_SITES.shp'

### Run the run.sh file

Then, simply run `sh run.sh` on Mac, or `bash run.sh` on windows.

This may take awhile to run, as it will download all required dependencies, data, and execute python code.
