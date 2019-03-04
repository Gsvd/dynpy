from requests import get
from socket import gethostbyname
from json import loads


def get_public_ip():
    tmp = get(r'http://ipv4.jsonip.com')
    return tmp.json()['ip']

def update_ip(username, password, dns, ip, provider):
    url = provider.format(dns=dns, ip=ip)
    tmp = get(url, auth=(username, password))
    return True if tmp.status_code == 200 else False

if __name__ == "__main__":
    public_ip = get_public_ip()
    with open("config.json", "r") as content_file:
        content = content_file.read()
        entries = loads(content)["entries"]
        for entry in entries:
            if update_ip(entry["username"], entry["password"], entry["dns"], public_ip, entry["provider"]):
                print("Successful: {dns} set to {ip}".format(dns=entry["dns"], ip=public_ip))
            else:
                print("Error: {dns} set to {ip}".format(dns=entry["dns"], ip=public_ip))
