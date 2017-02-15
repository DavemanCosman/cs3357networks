import socket
# Connection to establish with the Client
TCP_IP = '192.168.131.129'
TCP_PORT = 5005

# Establish connection
print("Attempting to contact server at ",TCP_IP,":",TCP_PORT)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((TCP_IP, TCP_PORT))
print ("Connection to Server Established")
# Valid request: What is the current date and time?
sentence = input('Type request to server: ')

# Encode sentence in bytes to send to server
byte_sentence = sentence.encode('ascii')
clientSocket.send(byte_sentence)
# once the result arrives, decode it to ascii
byte_result = clientSocket.recv(1024)
result = byte_result.decode('ascii')
print ('From Server: ', result)

clientSocket.close()
