#!/bin/bash

if [[ -z "$1" ]] || [[ -z "$2" ]]; then
	echo " "
	echo "Please enter a Moniker for your worker and a minereader server IP address and port"
	echo " "
	echo "e.g. $0 'MyWorkerName' x.x.x.x:YYYY"
	echo " "
	exit
fi

moniker=$1
minereader_server=$2

tail -f dero-miner-android-mathnodes.log | while read -r line; do
        json=`echo "$line" | sed 's/\}/,\"moniker\"\:\"'"${moniker}"'\"\}/g'`
        curl -X POST http://$minereader_server/miner \
           -H 'Content-Type: application/json' \
           -d "${json}"
done

