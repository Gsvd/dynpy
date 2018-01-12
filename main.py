from requests import get
from socket import gethostbyname


def get_public_ip():
    tmp = get(r'http://ipv4.jsonip.com')
    return tmp.json()['ip']

def update_ip(username, password, dns, ip):
    url = "https://www.ovh.com/nic/update?system=dyndns&hostname={dns}&myip={ip}".format(dns=dns, ip=ip)
    tmp = get(url, auth=(username, password))
    if tmp.status_code == 200:
        return True
    else:
        return False

if __name__ == "__main__":
    public_ip = get_public_ip()
    entries = [ 
                {"dns": "domain.com", "username": "YOUR_USERNAME", "password": "YOUR_PASSWORD"},
                {"dns": "www.domain.com", "username": "YOUR_USERNAME", "password": "YOUR_PASSWORD"},
                {"dns": "dev.domain.com", "username": "YOUR_USERNAME", "password": "YOUR_PASSWORD"}
            ]
    for entry in entries:
        if gethostbyname(entry.get("dns")) != public_ip:
            if update_ip(entry.get("username"), entry.get("password"), entry.get("dns"), public_ip):
                print("Successfull: {dns} set to {ip}".format(dns=entry.get("dns"), ip=public_ip))
            else:
                print("Error: {dns} set to {ip}".format(dns=entry.get("dns"), ip=public_ip))
        else:
            print("{dns} already points to {ip}".format(dns=entry.get("dns"), ip=public_ip))
