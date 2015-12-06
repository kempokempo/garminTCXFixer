# garminTCXFixer
Fixes inconsistent datetime stamp in garmin generated TCX files

## About
My Garmin 520 occassionally records random time stamps in the middle of a ride - most often some random date in 2019. This script parses the TCX file, looking for time deltas greater than 1 second and fixes the time stamp, writing it out to a new file.

## Usage
tcxFixer.py -i <inputfile> -o <outputfile>
