#!/bin/bash

# requests info on a HTTP/S curl call

curl -so /dev/null \
  -w "Response Code: \t\t%{http_code} \
      \nName Resolution: \t%{time_namelookup} sec\
      \nConnect Time: \t\t%{time_connect} sec\
      \nPre Transfer: \t\t%{time_pretransfer} sec\
      \nStart TTFB: \t%{time_starttransfer} sec\
      \nTotal: \t\t\t%{time_total} sec\
      \nSpeed Download: \t%{speed_download} bytes/sec \
      \nSize: \t\t\t%{size_download} bytes \
      \n\n" \
  $1
