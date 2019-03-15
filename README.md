# flask-server-diagnostic-web-api

A Web API for launching a simplistic diagnostic tool for your servers.

Supports memory information and file system information from a server.
Uses a 32 character long string token made of numbers and case insensitive letters to authenticate any client connecting to the server that requests for the diagnostic information.

Setup
======
Requires flask for python web API services, and python 3.

```bash
sudo pip install flask
```

If you have pip. If not, you will need to install pip for python3.

Running
------
Execution is straightforward:

```bash
python3 diagnosticService.py --ip=<ip-address> --port=<port>
```

Where ip-address is the ip address that the web service should use (this allows flexibility in limiting access from outside a network or internal testing)
Where port is the port number it should listen from (Do not forget to open said airport on local linux distributions via ufw / iptables / firewall-cmd)

You could also include python's virtualenv to run it as an independent process headless, or use java framework jenkins, or any custom system of your desire.

Trying it on curl:

```bash
curl -X GET 'http://127.0.0.1:9999/diagnostics?token=123123
```

where 127.0.0.1 is the ip address the program listens on, 9999 is the port that the program listen on, and the token to authenticate is 123123

The output will be a JSON encoded hash dataset with memory and filesystem information found using the bash scripts 'free -m' and 'df -h'
