import socket
import threading

print('[CLIENT]')
print('WARNING! Chat communication is not encrpyted!')

HOST = input('Server\'s IP address: ')
PORT = 55555

if not HOST:
	print('Using default IP: 127.0.0.1')
	HOST = '127.0.0.1'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.connect((HOST, PORT))

ENCODE = 'utf-8'
BUFFER = 4090

def send(message, client):
	client.send(message.encode(ENCODE))

def recv(client):
	return client.recv(BUFFER).decode(ENCODE)

def read():
	while True:
		message = recv(client)
		if not message:
			client.close()
			break
		print(message)

def write():
	while True:
		message = input('') #Socket blocking prints ofver input string
		if message == ':quit':
			send('[QUIT]', client)
			client.close()
			quit()

		send(message, client)

print('[CONNECTED]')

nickname = input('Nickname: ')
send(nickname, client) #Send nickname after connect
print('Write ":quit" to quit!')
start_message = recv(client)
if start_message == '[ERROR]':
	print(f'[ERROR]: {nickname} already exists!')
	client.close()
	quit()
print(start_message)

read_thread = threading.Thread(target=read)
read_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()