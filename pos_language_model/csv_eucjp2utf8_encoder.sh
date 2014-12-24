#!/bin/bash

for f in ../data/mecab-ipadic-2.7.0-20070801/*.csv
do
	echo $f
	nkf -Ew $f > ${f}.utf8
done