from requests import get
from socket import gethostbyname


OVH = "https://www.ovh.com/nic/update?system=dyndns&hostname={dns}&myip={ip}"
GOOGLE = "https://domains.google.com/nic/update?hostname={dns}&myip={ip}"

def get_public_ip():
    tmp = get(r'http://ipv4.jsonip.com')
    return tmp.json()['ip']

def update_ip(username, password, dns, ip, bridge):
    url = bridge.format(dns=dns, ip=ip)
    tmp = get(url, auth=(username, password))
    return True if tmp.status_code == 200 else False

if __name__ == "__main__":
    public_ip = get_public_ip()
    # BRIDGE IS AN EXAMPLE, REPLACE BY YOUR PROVIDER'S URL
    entries = [ 
                {"dns": "domain.com", "username": "YOUR_USERNAME", "password": "YOUR_PASSWORD", "bridge": GOOGLE},
                {"dns": "sample.com", "username": "YOUR_USERNAME", "password": "YOUR_PASSWORD", "bridge": OVH},
                {"dns": "dev.domain.com", "username": "YOUR_USERNAME", "password": "YOUR_PASSWORD", "bridge": GOOGLE}
            ]
    for entry in entries:
        if update_ip(entry.get("username"), entry.get("password"), entry.get("dns"), public_ip, entry.get("bridge")):
            print("Successfull: {dns} set to {ip}".format(dns=entry.get("dns"), ip=public_ip))
        else:
            print("Error: {dns} set to {ip}".format(dns=entry.get("dns"), ip=public_ip))
