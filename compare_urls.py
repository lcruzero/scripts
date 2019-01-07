#!/usr/bin/python2.7

#compare content length and response code 

import sys
import zipimport
import os

#cl_count = 0
#resp_count = 0

def file_cmp():
    cl_count = 0
    resp_count = 0
    #check content length size and Resp Code returned by tests_resp_01 Vs tests_resp_02 s
    with open('pre_check.txt', 'r') as b_resp, open('post_check.txt', 'r') as a_resp:
        for x,y in zip(b_resp,a_resp):
            b_resp = x.split()
            a_resp = y.split()
            try:
               if b_resp[2] == 'None' or b_resp[2] == '0':
                   b_resp[2] = '157'
               if a_resp[2] == 'None' or a_resp[2] == '0':
                   a_resp[2] = '157'
               #comparison of content-length, if there is a diff > 50% increment count and print
              # num = abs((int(b_resp[2]) - int(a_resp[2])) / (int(a_resp[2]))) * 100
              # print(num)
               if abs((float(b_resp[2]) - float(a_resp[2])) / (float(a_resp[2]))) * 100 > 50:
                  print '  ERROR:', a_resp[0], 'Content-Length before', b_resp[2], 'Content-Length after', a_resp[2]
                  cl_count +=1
                  b_resp = x.split()
                  a_resp = y.split()
               #comparison of resp code, if not equal and if post check is greater than 399 increment and print 
               if int(b_resp[1]) != int(a_resp[1]) and int(a_resp[1]) > 399:
                   print '  ERROR:', a_resp[0], 'Resp code before', b_resp[1], 'Resp code after', a_resp[1]
                   resp_count += 1
            except ValueError as ex:
                print("  Found value error")
                print(ex.message)
                continue
    if cl_count > 0 or resp_count > 0:
        if os.path.isfile('urls.txt.ignore'):
            print "Failures detected but exiting 0 due to presence of urls.txt.ignore"
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        sys.exit(0)


file_cmp()
