#!/bin/bash

#########################################################
#	baidu tieba spirt				#
#	version 0.1.1 yellow cat			#
#							#
#	code by						#
#	== Fang Yunlin ==				#
#							#
#	mail: cst05001@gmail.com			#
#	Google Talk: cst05001@gmail.com			#
#	MSN: cst05001@hotmail.com			#
#							#
#	Jul 7, 2009					#
#########################################################

BASENAME=`basename $0`
DIR2=`dirname $0`
DIR1=$PWD/$DIR2/

#load the config
USERNAME=`cat ${DIR1}config.txt | grep 'username' | awk -F '=' '{print $2}'`
PASSWORD=`cat ${DIR1}config.txt | grep 'password' | awk -F '=' '{print $2}'`
TIEBANAME=`cat ${DIR1}config.txt | grep 'tiebaname' | awk -F '=' '{print $2}'`

#Get the page source and put it into file tmp.html
echo Login ...
curl -D ${DIR1}cookie.txt "http://passport.baidu.com/?login&username=$USERNAME&password=$PASSWORD" >> /dev/null

while [ 1 -eq 1 ]; do

echo Get information of $TIEBANAME
curl -o ${DIR1}tmp.html -b ${DIR1}cookie.txt "http://tieba.baidu.com/$TIEBANAME"

#Get the kz from file tmp.html and put it into file kz.txt
cat ${DIR1}tmp.html | grep 'class=t' | awk -F 'kz=' '{print $2}' | awk -F '\"' '{print $1}' > ${DIR1}kz.txt
#Get the title from file tmp.html and put it into file title.txt
cat ${DIR1}tmp.html | grep 'class=t' | awk -F '_blank >' '{print $2}' | awk -F '<' '{print $1}' > ${DIR1}title.txt

#Read the kz from  file kz.txt and put it into the array 
#Read the title from  file title.txt and put it into the array 
#One page has 50 titles
title_list=()
for index in {1..50}; do
	title_list[$((($index-1)*3))]=`cat ${DIR1}title.txt | sed -n "${index}p"`
	title_list[$((($index-1)*3+1))]=`cat ${DIR1}kz.txt | sed -n "${index}p"`
done

row=`wc -l ${DIR1}black_title.txt | awk '{print $1}'`
if [ $row -eq 0 ]; then
	echo 'Nothing in the black_title .'
fi

for black_title in `cat ${DIR1}black_title.txt`; do
	for index in {1..50}; do
		echo ${title_list[$((($index-1)*3))]} | grep $black_title >> /dev/null
		if [ $? -eq 0 ]; then
			echo Black_list ${title_list[$((($index-1)*3))]} found .
			kz=${title_list[$((($index-1)*3+1))]}
			curl -o ${DIR1}sub_html_source.html -b ${DIR1}cookie.txt "http://tieba.baidu.com/f?kz=$kz"
			del_url="http://tieba.baidu.com"`cat ${DIR1}sub_html_source.html | grep 'onClick="d(' | awk -F "'" '{print $2}' | awk -F "'" '{print $1}'`
			echo do $del_url
			curl -b ${DIR1}cookie.txt $del_url >> /dev/null
			echo "Delete ${title_list[$((($index-1)*3))]} ."
		fi
	done
done
sleep 30
done
