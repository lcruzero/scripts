#!/usr/bin/python2.7

#generate content length and requests reponse status code 

import sys
import argparse
import requests
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout

def request_urls(filename):
    if args.pretest == True:
        file = open('pre_check.txt', 'a')    
    elif args.post == True:
        file = open('post_check.txt', 'a')
    
    #filename with urls to request
    urls = (filename)
    with open(filename) as f:
        # Don't forget about passing -H 'X-ADI-Pass: 1'     
        headers = {'X-ADI-Pass': '1'}


        #iterate over urls and strip them on lines and spaces 
        for url in map(str.strip, f):
            if args.prepend == True:
                url = url.replace('//','//fastly-staging-')
            try:
                #make a get request to list of urls with headers X-ADI-Pass
                req = requests.get(url,headers=headers,timeout=4)
                #get status codes 
                r_status = req.raise_for_status.im_self.status_code
                r_url = req.url
                #get content lenght 
                r_content_length = req.headers.get('Content-Length')
                print "  %s %s %s" % (url, r_status, r_content_length)
                file.write("%s %s %s\n" % (url, r_status, r_content_length))
            except HTTPError:
                r_content_length = '50'
                r_status = '666'
               # print "%s 2 2" % url
                print "  %s %s %s" % (url, r_status, r_content_length), 'Error'
                file.write("%s %s %s\n" % (url, r_status, r_content_length))

            except ConnectionError:
                r_content_length = '50'
                r_status = '666'
                print "  %s %s %s" % (url, r_status, r_content_length), 'Error'
                file.write("%s %s %s\n" % (url, r_status, r_content_length))
            except Timeout:
                r_content_length = '50'
                r_status = '666'
                print "  %s %s %s" % (url, r_status, r_content_length), 'Error'
                file.write("%s %s %s\n" % (url, r_status, r_content_length ))


#pretest against staging run as ./url_smoketest.py -f ../edge-config/tier/property/urls.txt -p -s
#post against staging run as ./url_smoketest.py -f ../edge-config/tier/property/urls.txt -o -s
#omit -s to run pre/post tests against FQDNs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='pass filename containing urls, check response code of urls in file')
    parser.add_argument('-f','--filename-with-urls',dest='filename', help='urls to check response code', required=True)
    parser.add_argument('-p','--pre-test', dest='pretest',help='pre change test', action='store_true', required=False)
    parser.add_argument('-o','--post-test',dest='post', help='post change test', action='store_true',required=False)
    parser.add_argument('-s','--prepend',dest='prepend', help='prepend fastly url', action='store_true',required=False)

    args = parser.parse_args()

    request_urls(args.filename)

