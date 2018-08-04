#! /bin/bash

for i in `seq 1 122`
do
	url="http://www.sto.cc/book-88721-${i}.html"
	output="priest-zhenhun-${i}.html"
	echo $url $output
	curl -o $output $url
done