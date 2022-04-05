#!/bin/bash
#
# Self-signed certificate:
#
#openssl ecparam -out ec_key.pem -name secp256r1 -genkey
#openssl req -new -key ec_key.pem -x509 -nodes -days 365 -out cert.pem 



if [[ "$#" -lt 1 ]]; then
    echo " "
    echo "Minereader shell v0.1.0 (johnny neumonic)"
    echo " "
    echo "Usage: $0 <iptobind> [optons]"
    echo " "
    echo "Options:          --port <portnum> (specify the port number to bind to, DEFAULT: 5000)"
    echo " "
    exit
fi

PORT=5000

while [ "$#" -gt 0 ]; do
        key=${1}

        case ${key} in
                --port)
                       echo "Setting user specified port...."
                        PORT=${2}
                        shift
                        shift
                        ;;
         *)
                        shift
                        ;;
        esac
done

IPADDY=$1

uwsgi  --plugin python3 --http-socket $IPADDY:$PORT --wsgi-file uWSGI.py --callable app --processes 4 --threads 4 --stats $IPADDY:9192 --uid root --pidfile /tmp/minereader.pid 