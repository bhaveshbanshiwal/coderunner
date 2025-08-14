import pickle
 
file_name = "exception_commands.bin"

VULNERABLE_KEYWORDS = {
    'python': [
        # --- Modules for OS interaction and command execution ---
        'import os',
        'import subprocess',
        'import shutil',
        'import pty',
        'import glob',

        # --- Networking modules ---
        'import socket',
        'import ftplib',
        'import http',

        # --- Keywords for dynamic execution and file access ---
        'eval(',
        'exec(',
        'open(',
        '__import__', # A way to dynamically import modules
        
        # --- Specific dangerous functions ---
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
        # --- Headers for system calls and low-level OS interaction ---
        '#include <unistd.h>',
        '#include <sys/types.h>',
        '#include <pthread.h>',

        # --- Headers for networking ---
        '#include <sys/socket.h>',
        '#include <netdb.h>',
        '#include <arpa/inet.h>',
        '#include <netinet/in.h>',

        # --- Dangerous C-style functions ---
        'system(',
        'fork(',
        'execv',
        'execl',
        'socket(',
        'gets(',      # Extremely unsafe, should always be banned
        'strcpy(',   # Unsafe, can cause buffer overflows
        'strcat(',   # Unsafe, can cause buffer overflows
        
        # --- Keywords related to pointers and memory management ---
        # While not inherently evil, their presence increases risk
        # and warrants closer inspection, especially with user input.
        'malloc(',
        'free(',
        'new ',
        'delete ',
    ]
}


f = open(file_name, '+bw')

pickle.dump(VULNERABLE_KEYWORDS, f)


f.close()