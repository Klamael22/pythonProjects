vmDetector.py is my attempt at writing a simple yet extendable script to try and detect if it is running in a VM or not.

I will also be using this script as an opportunity to practice using regular expressions.

The script works by performing various commands to query the system, then match the info returned to patterns that may indicate the host is a VM.

So far I have only implemented support for Windows, but will be adding Linux support. 

The methods used by the script currently:
Registry checker
CPU checker
NIC checker
Network info checker