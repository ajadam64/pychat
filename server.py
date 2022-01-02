#Todo: non-blocking sockets (asyncronous), SSL socket encryption or RSA, chat commands

import socket
import threading

print('[SERVER]')
print('WARNING! Chat communication is not encrpyted!')

HOST = input('Server\'s IP address: ')
PORT = 55555

if not HOST:
	print('Using default IP: 127.0.0.1')
	HOST = '127.0.0.1'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Prevents: OSError: [Errno 98] Address already in use
server.bind((HOST, PORT))
server.listen()

ENCODE = 'utf-8'
BUFFER = 4090

clients = {} #{socket: [name, isRoot]}

def send(message, client):
	client.send(message.encode(ENCODE))

def recv(client):
	return client.recv(BUFFER).decode(ENCODE)

def broadcast(message, curr_client):
	#Don't broadcast to self
	for client in clients.keys():
		if not(client == curr_client):
			send(message, client)

def handle(client, address, nickname):
	while True:
		message = recv(client)
		if not message or message == '[QUIT]':
			clients.pop(client)
			broadcast(f'{nickname} has quit!', None)
			client.close()
			print(f'[CLOSED] {address}')
			break

		#client_nickname = clients[client][0] #Get client nickname from dictionary
		message = f'{nickname}: {message}'
		broadcast(message, client)
		print(message)

def start():
	while True:
		client, address = server.accept()
		print(f'[CONNECTED] {address}')
		
		nickname = recv(client)
		#Check clients is not empty
		if clients:
			#Check if ninckname is in clients
			if nickname in list(clients.values())[0]:
				send('[ERROR]', client)
				client.close()
				continue #Close client and accept new client
		
		clients.update({client: [nickname]}) #clients.update({client: [nickname, isRoot]})
		broadcast(f'{nickname} joined!', None) #Treated as send
		print(f'{nickname} joined!')

		thread = threading.Thread(target=handle, args=(client,address,nickname))
		thread.start()

print('[LISTENING]')
start()