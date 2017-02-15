import socket
import datetime

TCP_IP = '192.168.131.129'
TCP_PORT = 5005

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((TCP_IP, TCP_PORT))
serverSocket.listen(1)
print('Server Address: ', TCP_IP)
print('Server ready to receive')
while 1:
	# Receive connection
	conn, addr = serverSocket.accept()
	print('Client Address: ', addr)
	print('Connection to Client is Established')
	# Process Client Request here
	byte_sentence = conn.recv(1024)
	# User message is decoded
	sentence = byte_sentence.decode()
	reply_string = sentence
	if sentence == 'What is the current date and time?':
		now = datetime.datetime.now()
		#“Current Date and Time – MM/DD/YYYY hh:mm:ss”
		reply_string = now.strftime("Current Date and Time: %m/%d/%Y %I:%M:%S")
		print('Successfully sent time to client')
	else:
		reply_string = "Invalid request: I have chortles!"
		print('The client requested nothing but chortles')
	# ensure that response is encoded in ascii format when sent
	reply_byte = reply_string.encode('ascii')
	conn.send(reply_byte)
	conn.close()
