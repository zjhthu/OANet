#!/usr/bin/bash
DATA_NAME=oanet_data
FILE_NAME=data_dump

if [ ! -d download_data_$DATA_NAME ]; then
    mkdir -p download_data_$DATA_NAME
fi

CHUNK_START=0
CHUNK_END=47

for ((i=CHUNK_START;i<=CHUNK_END;i++)); do
    IDX=$(printf "%03d" $i)
    URL=research.altizure.com/data/$DATA_NAME/$FILE_NAME.tar.$IDX
    wget -c $URL -P download_data_$DATA_NAME
    echo $URL
done

URL=research.altizure.com/data/$DATA_NAME/sha1sum.txt
wget -c $URL -P download_data_$DATA_NAME

cat download_data_oanet_data/*.tar.* > data_dump.tar.gz

