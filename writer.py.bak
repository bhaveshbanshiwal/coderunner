import pickle

file_name = "exception_commands.bin"

VULNERABLE_KEYWORDS = {
    'python': [
        'import os',
        'import subprocess',
        'import shutil',
        'import pty',
        'import glob',
        'import socket',
        'import ftplib',
        'import http',
        'eval(',
        'exec(',
        'open(',
        '__import__',
        'os.system',
        'os.remove',
        'os.rmdir',
        'os.removedirs',
        'os.rename',
        'os.environ',
        'shutil.rmtree',
        'subprocess.run',
        'subprocess.call',
        'subprocess.check_call',
    ],
    'cpp': [
        '#include <unistd.h>',
        '#include <sys/types.h>',
        '#include <pthread.h>',
        '#include <sys/socket.h>',
        '#include <netdb.h>',
        '#include <arpa/inet.h>',
        '#include <netinet/in.h>',
        'system(',
        'fork(',
        'execv',
        'execl',
        'socket(',
        'gets(',
        'strcpy(',
        'strcat(',
        'malloc(',
        'free(',
        'new ',
        'delete ',
    ]
}

with open(file_name, 'wb') as f:
    pickle.dump(VULNERABLE_KEYWORDS, f)