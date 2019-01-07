#!/bin/bash



declare -a zones
zones=`ns1 -k zone list | grep -v ZONE`

changed_files=/tmp/${i}.changes.txt


DIR=/tmp/zones_new/

touch /tmp/diff.txt


	if [ -e /tmp/all_changes.txt ] ; then
           	rm /tmp/all_changes.txt


	fi

	if [ -d "$DIR" ] ; then


       	   	echo "new and orig zones dirs exists"


	else

           	`mkdir /tmp/zones_orig/ /tmp/zones_new/ /tmp/zones_changed/ /tmp/no_zones/ /tmp/zones_sync/`

	fi

       #Sync zone files from S3 to /tmp/zones_orig
        	aws s3 cp s3://adi-aws-inf-prod-dnswatch-zonefiles/000-all-zones/ /tmp/zones_sync/ --recursive >/dev/null 2>&1


for z in `ls /tmp/zones_sync/`

do

		grep -rv '^;' /tmp/zones_sync/$z > /tmp/zones_orig/$z

done



for i in $zones


do
	dig -t AXFR $i @xfr01.nsone.net | grep -v '^;' > /tmp/zones_new/${i}.zone.txt

	grep SOA /tmp/zones_new/${i}.zone.txt

	if [ $? -ne 0 ]; then
		mv /tmp/zones_new/${i}.zone.txt /tmp/no_zones/
                rm -rf /tmp/zones_orig/${i}.zone.txt
	fi


	diff /tmp/zones_orig/${i}.zone.txt /tmp/zones_new/${i}.zone.txt > /tmp/diff.txt > /dev/null 2>&1

	if [ $? -ne 0 ]; then

       		#if there are different zone files copy to zones_changed dir

		cp /tmp/zones_new/${i}.zone.txt /tmp/zones_changed/ > /dev/null 2>&1


        	#a=${i}

#		cat /tmp/diff.txt > /tmp/all_changes.txt
	fi

#done

		rm -rf /tmp/zones_orig/addvance.net.zone.txt

		diff /tmp/zones_orig/${i}.zone.txt /tmp/zones_new/${i}.zone.txt  > /tmp/diffs/${i}.changes.txt


	if [ $? -ne 0 ]; then



#		aws s3 sync /tmp/zones_changed/ s3://adi-aws-inf-prod-dnswatch-zonefiles/000-all-zones/

		#copy zone files that changed back to S3

		aws sns publish  --topic-arn arn:aws:sns:us-east-1:xxxxxxxxxxx:DnsWatch2 \
                       --region=us-east-1 \
                       --subject "DnsWatch2 zone change ${i}" \
                       --message="..."$'\n'"$(cat /tmp/diffs/${i}.changes.txt)"


	fi

done


        aws s3 sync /tmp/zones_changed/ s3://adi-aws-inf-prod-dnswatch-zonefiles/000-all-zones/

        rm -rf /tmp/zones_new/* & rm -rf /tmp/zones_orig/* & rm -rf /tmp/zones_changed/* & rm -rf /tmp/diffs/* \
		rm -rf /tmp/zones_sync/*

		 #>> /tmp/diff.txt



### EOF
