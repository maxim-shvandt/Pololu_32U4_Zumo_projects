import socket
import sys

#=================================

def serverState( sock ):
	
	print('player 1: server state')
	
	sock.bind( ( host, port ) )
	sock.listen( 5 )
	connection = None
	
	while True:
	
		if connection is None:
			# Halts
			print('[Waiting for connection...]')
			connection, addr = sock.accept()
			print('Got connection from', addr )
			
		else:
			# Halts
			print('[Waiting for response...]')
			print( connection.recv( 1024 ) )
			message = input("Enter something to this client: ")
			connection.send( message.encode() )
			
#----------------------------------------

def clientState( sock ):

	print('player 2: client state')

	sock.connect( ( host, port ) )
	print('Connected to', host )

	while True:
	
		message = input("Enter something for the server: ")
		sock.send( message.encode() )
		# Halts
		print('[Waiting for response...]')
		print( sock.recv( 1024 ) )

#========== MAIN =================

sock = socket.socket()
host = socket.gethostname()
port = 12221

state = sys.argv[ 1 ]
#state = input("Enter your state: ")

if state == "player1":
	
	serverState(sock)
	
elif state == "player2":

	clientState(sock)
		
		