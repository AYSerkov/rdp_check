# rdp_check
**RDP Connection Checker**

This script allows you to check the availability of Remote Desktop Protocol (RDP) connections to a list of hosts, subnets, or individual IP addresses using xfreerdp. It automates the process of validating user authentication and detecting whether RDP access is allowed or denied for each target.

**Features**
- Single Target Check: You can check the RDP connection status for a single host (IP address, DNS name).
- Batch Check: The script supports checking multiple targets (IP addresses, DNS names, or subnets) by loading them from a file.

Ensure you have xfreerdp installed on your system. You can install it:

```bash
apt-get install freerdp2-x11
pip install termcolor
```

**Usage**
- Checking a Single Target
You can check a single host (IP address or DNS name) using the --target option:

```bash
python rdp_checker.py -t <host> -u <username> -p <password> -d <domain>
```

- Batch Checking from a File
To check multiple hosts, subnets, or DNS names, you can create a file with a list of targets and pass it with the --targets option:
```
ts.domain.local
172.16.123.2
10.2.3.0/24
```

```bash
python rdp_checker.py -T targets.txt -u <username> -p <password> -d <domain>
```

![1](https://github.com/user-attachments/assets/8fc0cfe7-f2ba-47da-98e9-976de81df9da)
