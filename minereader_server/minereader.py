#!/bin/env python3
import json
from time import sleep
from flask import Flask, request
from flaskext.mysql import MySQL




# initialization
app = Flask(__name__)
mysql = MySQL()

app.config["DEBUG"] = True
app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False

# EDIT THESE
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'derohe'
app.config['MYSQL_DATABASE_PASSWORD'] = 'PASSWORD'
app.config['MYSQL_DATABASE_DB'] = 'derohe'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


mysql.init_app(app)

def UpdateMinerTable(query):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


@app.route('/miner',methods=['POST','GET'])
def miner_info():
    miner_content = request.json
    status = {'status' : False}
    print(miner_content)
    print("Updating Database...", end='')
    
    if 'worker_hashrate' in miner_content.keys():
        if '+' in miner_content['T']:
            dtime = miner_content['T'].split('+')[0]
        elif 'Z' in miner_content['T']:
            dtime = miner_content['T'].replace('T', ' ')
            dtime = dtime.replace('Z', ' ')
        else:
            dtime = ''
            blah = miner_content['T'].split('-')[0:-1]
            for e in blah:
                dtime = dtime + e + '-'
            dtime = rreplace(dtime,'-', '',1)
        dtime = dtime.replace('T', ' ')
        dtime = dtime.replace('Z', ' ')    
        whr   = miner_content['worker_hashrate'].replace('MINING @ ', '')
        miner_content['T'] = dtime
        miner_content['worker_hashrate'] = whr
        insquery = '''
                    INSERT IGNORE INTO miners (moniker, blocks, mini_blocks, network_hash_rate, worker_hash_rate, height, last_report)
                    VALUES ("%s", %d, %d, "%s", "%s", %d ,"%s");
                    ''' % (miner_content['moniker'],int(miner_content['blocks']),int(miner_content['mini_blocks']),miner_content['hash_rate'],
                           miner_content['worker_hashrate'],int(miner_content['height']), miner_content['T'])
        UpdateMinerTable(insquery)
        status['status'] = True
        return json.dumps(status)
    else:
        status['status'] = False
        return json.dumps(status)


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

