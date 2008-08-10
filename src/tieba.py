#!/usr/bin/env python

import urllib
import urllib2
import cookielib
import sys
import os
import re
import time

class tieba:
    config_file_coding = 'gb2312'
    cookie = ''
    opener = ''
    html = ''
    http = ''
    
    DIR_NAME = ''   
    PATH_MAIN = ''
    PATH_MAIN_CONFIG = ''
    PATH_DIRTY_WORDS = ''
    PATH_TIEBA_LIST = ''
    
    username = ''
    password = ''
    sleep_time = ''
    
    tieba_list = []
    dirty_words = []
    
    url_main = 'http://www.baidu.com'
    url_login = 'http://passport.baidu.com'
    url_tieba = 'http://tieba.baidu.com'
    
    kz_title_author_time = []
    
    def __init__(self):
        self.init_path()
        self.init_conf()
        self.init_network()
        self.login()
        self.read_dirty_words()
    
    def init_path(self):
        self.PATH_MAIN = sys.argv[0]
        self.DIR_NAME = os.path.dirname( self.PATH_MAIN )
        self.PATH_MAIN_CONFIG = os.path.join( self.DIR_NAME, 'main.conf')
        self.PATH_DIRTY_WORDS = os.path.join( self.DIR_NAME, 'dirty_words.conf')
        self.PATH_TIEBA_LIST = os.path.join( self.DIR_NAME, 'tieba_list.conf' )
        
    def init_conf(self):
        print 'Reading ' + self.PATH_MAIN_CONFIG
        try:
            fin = open(self.PATH_MAIN_CONFIG, 'r')
            for line  in fin.read().splitlines():
                if len(line):
                    attr, value = line.strip().split('=')
                    if attr == 'USERNAME':
                        self.username = value
                    elif attr == 'PASSWORD':
                        self.password = value
                    elif attr == 'SLEEP':
                        self.sleep_time = value
                        print 'Sleep time = ' + self.sleep_time
                    elif attr == 'CODING':
                        self.config_file_coding = value
                        print 'Coding = ' + self.config_file_coding
                    
                    
            fin.close()
        except IOError:
            print 'Can not open ' + self.PATH_MAIN_CONFIG
            sys.exit(1)
            
        print 'Reading ' + self.PATH_TIEBA_LIST
        try:
            fin = open(self.PATH_TIEBA_LIST, 'r')
            self.tieba_list = fin.read().splitlines()
            fin.close()
            self.tieba_list.remove('')
        except IOError:
            print 'Can not open ' + self.PATH_TIEBA_LIST
            sys.exit(2)
            
    def init_network(self):
        print 'Init the network'
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(self.opener)
        
            
    def read_dirty_words(self):
        try:
            fin = open(self.PATH_DIRTY_WORDS, 'r')
            self.dirty_words = fin.read().splitlines()
            fin.close()
        except IOError:
            print 'Can not open ' + self.PATH_DIRTY_WORDS
            sys.exit(2)
            
    def login(self):
        try:
            print 'Login in by ID : ' + self.username
            url = self.url_login + '/?login&username=' + self.username + '&password=' + self.password
            self.http = urllib2.urlopen(url)
            self.http.close()
        except urllib2.URLError:
            print 'Can not connect to the internet.\nPlease check your network .'
        
    def get_title_list(self, tieba):
        try:
            url = self.url_tieba + '/' + tieba
            self.http = urllib2.urlopen(url)
            self.html = self.http.read()
            self.kz_title_author_time_reply = re.findall( '<td class="s"><a class=t.*kz=(\d*)" target=_blank >(.*)</a></td>\r\n<td class="u">.*<font color=\'#000000\'>(.*)</font>.*</td>\r\n<td class="u">(.*)&nbsp;.*<font color=\'#000000\'>(.*)</font>.*</td>', self.html, re.M)
        except urllib2.URLError:
            print 'Can not connect to the internet.\nPlease check your network .'
            
    def del_article(self, kz):
        try:
            url = self.url_tieba + '/f?kz=' + kz
            self.http = urllib2.urlopen(url)
            self.html = self.http.read()
            del_str = re.findall('onClick="d\(\'(.*)\'', self.html)
            if not del_str:
                print 'ID ' + self.username + ' have no right to del the article'
                print 'Quit'
                sys.exit(3)
            url_del = self.url_tieba + del_str[0]
            self.http = urllib2.urlopen(url_del)
            self.http.close()
        except urllib2.URLError:
            print 'Can not connect to the internet.\nPlease check your network .'

     
    def run(self):
        while True:
            for tieba in self.tieba_list:
                print 'Checking ' + unicode(tieba, self.config_file_coding)
                self.get_title_list(unicode(tieba, self.config_file_coding).encode('utf_8'))
                
                for attr in self.kz_title_author_time_reply:
                    for word in self.dirty_words:
                        rule = '.*' + word + '.*'
                        if re.match(unicode(rule, self.config_file_coding), unicode(attr[1], self.config_file_coding)):
                            print unicode(attr[1], self.config_file_coding) + 'will be delete'
                            self.del_article(attr[0])
                            break
                        
            print 'Sleeping ...'
            time.sleep(int(self.sleep_time))

if __name__ == '__main__':
    t = tieba()
    t.run()