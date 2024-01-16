import socket

# Get the host name
hostname = socket.gethostname()

# Get the IP address corresponding to the host name
ip_address = socket.gethostbyname(hostname)

print(f"The IP address of {hostname} is {ip_address}")
