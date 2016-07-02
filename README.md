# server_stats
Utility scripts to collect stats on a regular basis and POST the data in JSON form to a remote server.

# INSTALL
```
cd /root/
git clone git@github.com:evgenypim/server_stats.git
cd ./server_stats/etc
cp ./stats.yaml.example ./stats.yaml
vi ./stats.yaml
ln -sf /root/server_stats/etc/stats.yaml /etc/
```

You need to execute the scripts via a crontab.  The script will then POST the data to a server you nominate.  Presumably you could set up a php script to post data to a PostgreSQL, Mongo or CouchDB database.  Then write a query interface for it.

I am writing a service to POST the data to now.  I run a [software development company](http://www.oneit-software.com.au/) and I'm writing this tool to support hundreds of VMs.  It's in early stages at the moment, but I'd love to get feedback from others to make it better, so contact me and I'll set you up an account.

# Dependencies
apt-get install python-yaml python-psutil python-requests

# Usage
The system is composed of 1 utility that can collect data depending on the command line arguments you pass:
```
stats.py stats.py [-h] [--verbosity] 
                  [--diskUsed] [--diskIO] [--dirUsed] [--cpu] [--memory] [--network] [--apacheLog]
```

--verbosity can be 0 - 2 (defaults to 1).

See below for which arguments trigger what data to be sent.  The system will try to send as much data as it can, however an error will result in a non-0 result


# Data Posted
The system's goal is to POST data to the api_url, with a record like the following:
{"records": [{ record1 }, { record2 } ... ], "apiKey": "abc123"}

The individual records are documented below:
## Server stats from stats.py
```
# --diskUsed Disk used at the mountpoint (d2) in MB
{"date": "2016-06-30 21:20:28", "V": 320032.71484375, "d2": "/", "t": "DISK-USAGE", "d1": "my-server-name"}

# --cpu CPU time in iowait in ms (since bootup)
{"date": "2016-06-30 21:20:28", "V": 512340, "t": "CPU-IOWAIT", "d1": "my-server-name"}

# --cpu Total CPU time (user + system) in iowait in ms (since bootup).
{"date": "2016-06-30 21:20:28", "V": 22430720, "t": "CPU-TOTAL", "d1": "my-server-name"}

# --memory Memory used (used - buffers) in MB
{"date": "2016-06-30 21:20:28", "V": 7351.94140625, "t": "MEM-USED", "d1": "my-server-name"}

# --memory Swap used in MB
{"date": "2016-06-30 21:20:28", "V": 1633.88671875, "t": "MEM-SWAP", "d1": "my-server-name"}

# --network Network traffic received in MB on the interface d2
{"date": "2016-06-30 21:20:28", "V": 619.4905185699463, "d2": "eth0", "t": "NET-RCV", "d1": "my-server-name"}

# --network Network traffic sent in MB on the interface d2
{"date": "2016-06-30 21:20:28", "V": 557.3779401779175, "d2": "eth0", "t": "NET-SENT", "d1": "my-server-name"}

# --diskIO Disk reads since bootup on the device d2
{"date": "2016-06-30 21:20:28", "V": 1245400, "d2": "dm-0", "t": "DISK-READS", "d1": "my-server-name"}

# --diskIO Disk writes since bootup on the device d2
{"date": "2016-06-30 21:20:28", "V": 389955, "d2": "dm-0", "t": "DISK-WRITES", "d1": "my-server-name"}

# --dirUsed Send the size of the directory in MB
{"date": "2016-06-30 21:04:06", "V": 92672.92578125, "d2": "/root/backups/zbackup.encrypted/", "t": "DSIZE", "d1": "my-server-name"}

# --apacheLog Send the number of requests since the last invocation
{"date": "2016-06-30 21:08:54", "V": 5, "d2": "vm1_tc8", "t": "LOG_REQUESTS-COUNT", "d1": "my-server-name"}

# --apacheLog Send the average duration of requests since the last invocation in ms
{"date": "2016-06-30 21:08:54", "V": 35.8, "d2": "vm1_tc8", "t": "LOG_REQUESTS-DURATION", "d1": "my-server-name"}
```

## Apache Log Caveats
We scan the matching log files.  The log files are a standard Apache tomcat log file with the response duration after the response code, which should have a format like:
```
203.161.1.2 - - [01/Jul/2016:06:52:08 +0800] "GET /test/file.htm HTTP/1.1" 200 1ms 53938 "http://www.madeup.com.au/test/index.htm" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36" www.madeup.com.au
```
I set that up in Tomcat using the following code in server.xml:
```
<Valve className="org.apache.catalina.valves.AccessLogValve" directory="/usr/local/tomcat/vm1/logs/" prefix="tc" suffix=".log" pattern="%h %l %u %t &quot;%r&quot; %s %Dms %b &quot;%{Referer}i&quot; &quot;%{User-agent}i&quot; %v" resolveHosts="false"/>
```


# Config description
Config file path: /etc/stats.yaml - regular yaml file.
```
#API key and URL
api_key: abc123
api_url: https://api.url.com

# For disks subsystem stats
disks:
        # Mount points for free/used stats per mountpoint
        mount_points:
                - /home
                - /

        # Block devs fo o|i stats
        block_devs:
                - sda1
                - dm-0

        # full paths to dirs for dir size stats
        dirs_size:
                - /mnt/media/
                - /tmp/

# For network subsystem
networking:
        interfaces:
                - enp3s0
                - br0

apache_logs:
        # List of keys. The key is the value used in dim2
        - website1:
                # The glob of the files to scan for
                file: /var/log/apache2/log_website1*.log
                # The optional regex of the URI to process. This only processes php files.
                # It is regular Python regular expr.
                # see https://docs.python.org/2/library/re.html#regular-expression-syntax
                url_filter: .php
        - website2:
                file: /var/log/apache2/log_website2*.log
```

# TODO
The project is finished.  Hahaha ... just kidding.  Some more items I can think of are:

#### Apache Log to General Logging
There is no reason why the apache log couldn't match other types of logs e.g. application logs.  We just need an extractor to pull out the pattern to check and the value to store.  For some logs, we might not need a value it is simply enough to record the number of lines e.g. matching ERROR.

#### Line Matching Power
Something like the rsync where you can specify includes and exclude regexes and it processes them in sequence.  For example
- exclude: do_not_track.jsp
- include: .jsp
- include: .htm

#### More stats collectors
This could go on forever, which is why the following is good.

#### Make the code structure OO
Each stats extractor screams to be a class.  Then add plugins to support new types of stats.

This could be done like Nagios where we call an executable and it just returns json rather than a tightly coupled python module.

