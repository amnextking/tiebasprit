#!/usr/bin/env python

import tieba

print '''
    Program is running .
    If you want to quit ,
    please press Ctrl-C if you are using Linux/Unix/BSD/Mac OSX
    if you are using Windows , please Ctrl-Z
    '''

try:
    main = tieba.tieba()
    main.run()
except KeyboardInterrupt:
    print '\n'*24 + 'Bye'