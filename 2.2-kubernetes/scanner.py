import os
import sys
os.system('nmap -sT {} |grep -vE "Starting|Host|Nmap done|Not|All|MAC"'.format(sys.argv[1]))
