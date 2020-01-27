#!/bin/bash

working_directory=../../data

mkdir -p $working_directory/optimized
mkdir -p $working_directory/vrt

for filename in $working_directory/*.tif
do
    gdal_translate -co TILED=YES -co BLOCKXSIZE=512 -co BLOCKYSIZE=512 \
        -co BIGTIFF=YES -co COMPRESS=LZW \
        $filename $working_directory/optimized/$(basename $filename)
    gdalbuildvrt \
        $working_directory/vrt/$(basename ${filename%.*}.vrt) \
        $working_directory/optimized/$(basename $filename)
done
