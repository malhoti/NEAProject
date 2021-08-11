print('hello mal')
import random

import socket

hostname = socket.gethostname()

# getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)

print(hostname)
print(ip_address)

