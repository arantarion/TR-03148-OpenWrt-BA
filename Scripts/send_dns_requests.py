import socket

websites = []
with open('top-1000-websites.txt') as file:
	websites = file.readlines()

websites = [line.rstrip('\n') for line in websites]

IPs = []
for website in websites:
	try:
		IPs.append(socket.gethostbyname(website))
	except:
		pass

print(len(IPs))


