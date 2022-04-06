# minereader
DeroHE Miner With Constant Logging to MySQL Server

## Requirements
* MySQL 8.0+
* uswgi
* Python 3.6+
* Flask, Flask-MySQL

### Optional
* Metabase or other MySQL Visual Software

## Install
Clone:

`git clone https://github.com/MathNodes/minereader`


### Server

Edit the following lines with your MySQL set-up in the *minereader.py* file

```python
# EDIT THESE
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'derohe'
app.config['MYSQL_DATABASE_PASSWORD'] = 'PASSWORD'
app.config['MYSQL_DATABASE_DB'] = 'derohe'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
```


On a server set-up minereader server

```
./app_run.sh IP --port port
```


### Client

Use `dero-miner-android-mathnodes` or `dero-miner-linux-mathnodes` on your device or CPU.

**NOTE**: The only thing changed in MathNodes DeroHE miner from the DEROPROJECT is the following:

Line 288:
```go
logger.V(0).Info("", "height", strconv.FormatInt(int64(our_height),10), "blocks", strconv.FormatInt(int64(block_counter),12), "mini_blocks", strconv.FormatInt(int64(mini_block_counter),12), "hash_rate", hash_rate_string, "worker_hashrate", mining_string)
```

Line 293:
```go
time.Sleep(60 * time.Second) //changed to log every minute instead of every second (MathNodes)
```

Edit `mining.sh` or `mining-android.sh` with your Wallet Address and a DAEMON if you have one. Feel free to use our daemon if you didn't set one up: `dero.mathnodes.com:10100`

Run
```shell
./mining.sh
```

In a new terminal on the same device run the *minereader* script

```shell
./minereader-android Moniker IP:PORT
```

Where **IP:PORT** is the IP address and Port number of your minereader server.

All done. Use your MySQL set-up to check your status.


## MySQL Config

### Create DEROHE Table, User, and Permissions

Open mysql

```shell
mysql -u root -p
```

Create Table and User. Edit PASSWORD with yours
```sql
CREATE TABLE miners (id INT UNSIGNED NOT NULL AUTO_INCREMENT, moniker VARCHAR(50), blocks SMALLINT UNSIGNED, mini_blocks SMALLINT UNSIGNED, network_hash_rate VARCHAR(20), worker_hash_rate VARCHAR(20), height MEDIUMINT UNSIGNED, last_report TIMESTAMP, PRIMARY KEY(id)); 


CREATE USER 'derohe'@'localhost' IDENTIFIED WITH mysql_native_password BY 'PASSWORD';
GRANT ALTER, REFERENCES, SELECT, INSERT, UPDATE, CREATE, DELETE, LOCK TABLES,SHOW VIEW, EVENT, TRIGGER ON derohe.* TO 'derohe'@'localhost';

FLUSH PRIVILEGES;
```

## SQL Query for Status

```sql
SELECT moniker, blocks, mini_blocks, network_hash_rate, worker_hash_rate,height,last_report
FROM 
(WITH ranked_messages AS (
  SELECT m.*, ROW_NUMBER() OVER (PARTITION BY moniker ORDER BY id DESC) AS rn
  FROM miners AS m 
)
SELECT moniker, blocks, mini_blocks, network_hash_rate, worker_hash_rate,height,last_report FROM ranked_messages WHERE rn = 1) `miners`

WHERE moniker <> '' 
```

## Metabase with 60 second refresh

![img/derohe_metabase.png](img/derohe_metabase.png)

