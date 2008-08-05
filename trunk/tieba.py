#/usr/bin/env python

# -*- coding = utf_8 -*-

import urllib2
import urllib
import cookielib
import sys
import os
import re
import codecs
import time

PATH_MAIN = sys.argv[0]
i = len( PATH_MAIN ) - 1
while i > 0:
	if PATH_MAIN[i] != os.sep:
		i -= 1
	else:
		break
PATH = PATH_MAIN[0:i]

MAIN_CONF = PATH + 'main.conf'
TIEBA_LIST = PATH  + 'tieba_list.conf'
DIRTY_WORDS_CONF = PATH + 'dirty_words.conf'

fin = open( MAIN_CONF, 'r' )
lines = fin.readlines()
fin.close()

username = ''
password = ''
for attr in lines:
	if re.match( 'USERNAME', attr ):
		username = re.findall( 'USERNAME=(.*)', attr )
	if re.match( 'PASSWORD', attr ):
		password = re.findall( 'PASSWORD=(.*)', attr )

username = username[0]
password = password[0]

cookie = cookielib.CookieJar()
opener = urllib2.build_opener( urllib2.HTTPCookieProcessor( cookie ) )
urllib2.install_opener( opener )

print 'Login in by ' + unicode( username, 'gb2312' )  + '...'
http = urllib2.urlopen( 'http://passport.baidu.com/?login&&username=' + username + '&&password=' + password )

while 1:
	fin = open( TIEBA_LIST, 'r' )
	tieba_list = fin.readlines()
	fin.close()

	fin = open( DIRTY_WORDS_CONF, 'r' )
	dirty_words = fin.readlines()
	fin.close()
	for index in range( 0, len( dirty_words ) ):
		if dirty_words[index] == '\n':
			dirty_words.remove( dirty_words[index] )
			continue
		dirty_words[index] = unicode( re.sub( '\n', '', dirty_words[index] ), 'gb2312' )


	for attr in tieba_list:
		if attr == '\n':
			continue

		print 'Checking ' + unicode( attr, 'gb2312' )
		tieba = re.sub( '\n', '', attr )

		http = urllib2.urlopen( 'http://tieba.baidu.com/' + tieba )
		html = http.read()
		http.close()
		kz_title = re.findall( '<td class="s"><a class=t.*kz=(\d*)" target=_blank >(.*)</a></td>', html )

		for attr in kz_title:
			title = unicode( attr[1], 'gb2312' )
			for word in dirty_words:
				if re.match( '.*' + word + '.*', title ):
					print 'Delete ' + title
					http = urllib2.urlopen( 'http://tieba.baidu.com/f?kz=' + attr[0] )
					html = http.read()
					http.close()
					del_str = re.findall( 'onClick="d\(\'(.*)\'', html )
					url_del = 'http://tieba.baidu.com' + del_str[0]
					http = urllib2.urlopen( url_del )
					http.close()

	print 'Sleeping ...'
	time.sleep( 10 )
