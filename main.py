import os
from requests import get
from socket import gethostbyname
from json import loads
from datetime import datetime


def get_public_ipv4():
    tmp = get(r'http://ipv4.jsonip.com')
    return tmp.json()['ip']

def get_public_ipv6():
    tmp = get(r'http://jsonip.com')
    return tmp.json()['ip']

def update_ip(username, password, dns, ip, provider, dt_string):
    url = provider.format(dns=dns, ip=ip)
    tmp = get(url, auth=(username, password))
    if tmp.status_code == 200:
        print("[{date}] Successful: {dns} set to {ip}".format(date=dt_string, dns=dns, ip=ip))
    else:
        print("[{date}] Error: {dns} set to {ip}".format(date=dt_string, dns=dns, ip=ip))
    return True if tmp.status_code == 200 else False

if __name__ == "__main__":
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    public_ipv4 = get_public_ipv4()
    public_ipv6 = get_public_ipv6()
    with open("{}/config.json".format(os.path.dirname(__file__)), "r") as content_file:
        content = content_file.read()
        entries = loads(content)["entries"]
        for entry in entries:
            update_ip(entry["username"], entry["password"], entry["dns"], public_ipv4, entry["provider"], dt_string)
            if public_ipv4 != public_ipv6:
                update_ip(entry["username"], entry["password"], entry["dns"], public_ipv6, entry["provider"], dt_string)
