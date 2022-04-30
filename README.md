# Via-Kramer-Whiteboard Project
A project intended for the Coventry University Talent Showcase event where we hack into IoT (Internet of Things) e.g. the whiteboard. We managed to get full RCE without admintstrator priveladge for the kramer Go (debain) and the same for the windows version but pre-exisitng user needed with password.

## Guidelines
 Official guidelines to follow - "Clearly identify and describe any potentially harmful content in a disclaimer in the project’s README.md file or source code comments.
Provide a preferred contact method for any 3rd party abuse inquiries through a SECURITY.md file in the repository (e.g., "Please create an issue on this repository for any questions or concerns"). Such a contact method allows 3rd parties to reach out to project maintainers directly and potentially resolve concerns without the need to file abuse reports"

### `---Disclaimer---`
This repository contains a IOT VIA Kramer Go exploit created for educational purposes. It shall be deployed in a controlled environment for testing and results posted as shown.

## Team Members 

|   Name              |    Username     |
|---------------------|-----------------|
| Owen Ball           |   Ballo-02      |
|                     |   sharkmoos     |

## Official Documentation on exploit-db
Windows Script - https://www.exploit-db.com/exploits/50848
Linux Script - https://www.exploit-db.com/exploits/50856

## What's in this repository?

### `Linux-Go/Whiteboard.py`
The main script for the Linux version of VIA Kramer with comments explianing the code and two added fields "t" for theme (change the code name, room name and colour) and "b" for the background (change the background photo of the whiteboard) with the main feature of a command line with root

### `Linux-Go/Original.py`
The original script for the Linux version of VIA Kramer without comments just the command line with root

### `Windows-Go/Whiteboard.py`
The main script for the Linux version of VIA Kramer with comments explianing the code and two added fields "t" for theme (change the code name, room name and colour) and "b" for the background (change the background photo of the whiteboard) with the main feature of a command line cmdlet

### `Windows-Go/Original.py`
The original script for the Windows version of VIA Kramer without comments just the command line for cmdlet

### `Hacking Poster`
A .pdf that was used in the Coventry university Talent Showcase event to show this project

### `IOT Presentation`
A .pptx presentation file that explains the project in full from start to finish what was also showcased at the Coventry university Talent Showcase event

## How to use?

### `Linux-Go/Whiteboard.py` and `Windows-Go/Whiteboard.py`
python3 Whiteboard.py target

[Optional] python3 Original.py target tb

t - Theme text

b - Background photo


Example
 - python3 Linux-Go/Whiteboard.py 10.10.11.145
 - python3 Windows-Go/Whiteboard.py 10.10.11.145 tc
 - python3 Linux-Go/Whiteboard.py 10.10.11.145 t

### `Linux-Go/Original.py` and `Windows-Go/Original.py`
python3 Original.py target
 
Example
 - python3 Windows-Go/Original.py 10.10.11.145
