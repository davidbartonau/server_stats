# server_stats
script to collect some stats
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

# For network subsystem
networking:
	interfaces:
	- enp3s0
	- br0
```