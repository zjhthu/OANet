#!/usr/bin/bash
DATA_NAME=oanet_data
FILE_NAME=$1
OUTPUT_NAME=$2

if [ ! -d download_data_$DATA_NAME ]; then
    mkdir -p download_data_$DATA_NAME
fi

let CHUNK_START=$3
let CHUNK_END=$4


for ((i=CHUNK_START;i<=CHUNK_END;i++)); do
    IDX=$(printf "%03d" $i)
    URL=research.altizure.com/data/$DATA_NAME/$FILE_NAME.tar.$IDX
    wget -c $URL -P download_data_$DATA_NAME
    echo $URL
done


cat download_data_oanet_data/*.tar.* > $OUTPUT_NAME
rm -r download_data_oanet_data
