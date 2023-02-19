#!/bin/bash
filename='parameter.csv'
n=1
while read line; do
# reading each line
echo "Line No. $n : $line"
n=$((n+1))
done < $filename
echo "Final line :$line"
