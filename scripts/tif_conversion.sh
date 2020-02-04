#!/bin/bash

working_directory=../../data
cd $working_directory

mkdir -p optimized

for filename in *.tif
do
    gdal_translate -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 \
        -co BIGTIFF=YES -co COMPRESS=LZW $filename optimized/$filename
done
cd optimized
for filename in *.tif
do
    gdalbuildvrt ${filename%.*}.vrt $filename
done
