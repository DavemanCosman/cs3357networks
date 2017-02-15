#UDP_Server.py
#David Cosman
#
#A simple UDP Server implementing rdt2.2
#Coded in Python 3.5

import binascii
import socket
import struct
import sys
import hashlib

CLIENT_UDP_IP = "192.168.131.130"

def main():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    unpacker = struct.Struct('I I 8s 32s')
    
    #Create the server socket
    serverSock = CreateRcvSocket(UDP_IP, UDP_PORT);
    #expected initial seq value of 0
    seq = 0

    #listen
    while True:
        #Receive Data
        UDP_Packet = RcvData(serverSock, unpacker);
        print ("client address is: ", CLIENT_UDP_IP)
        #Create the Checksum for comparison
        chksum = CreateChksum(UDP_Packet[0],UDP_Packet[1],UDP_Packet[2]);
       	#Compare Checksums to test for corrupt data
        ack = Checksum(UDP_Packet, chksum);
        #Is the sequence order correct?
        seqCorrect = Checkseq(UDP_Packet, seq);
        print("Building ACK response to client")
        UDP_Reply = BuildPacket (ack, seq);
        SendPacket (serverSock, UDP_Reply, CLIENT_UDP_IP, UDP_PORT);
        #adjust seq if packet was not corrupt and seq was correct
        if ack == 1 and seqCorrect == True:
            if seq == 0:
                seq = 1
            else:
                seq = 0
        print('\n')

#Creates socket for Server to recieve data from client(s)
#Returns the receiver socket
def CreateRcvSocket(IP, PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, PORT))
    return sock;

#Method to recieve and unpack data from client packets
#Returns packet in tuple form
def RcvData(sock, unpacker):
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    UDP_Packet = unpacker.unpack(data) # extract data
    print("received from client:", addr)
    print("received message:", UDP_Packet)
    CLIENT_UDP_IP = addr
    return UDP_Packet;

#Builds the packet with specified values
#Returns the built packet in tuple form
def BuildPacket (ack, seq):
    chksum = CreateChksum(ack, seq);
    values = (ack, seq, chksum)
    print("ack=", ack, ", seq=",seq, ", chksum=",chksum) 
    #Structure is as follows; AckNum, SeqNum, Chksum
    UDP_Packet_Data = struct.Struct('I I 32s')
    UDP_Packet = UDP_Packet_Data.pack(*values)
    return UDP_Packet;

#Sends the specified packet to given IP and PORT
#Only used to send ACK packets; no data.
def SendPacket (sock, packet, IP, PORT):
    sock.sendto(packet, (IP, PORT))
    return;

#Creates the checksum value for the packet to send
#Returns the checksum value
def CreateChksum(ack, seq, data = None):
    if (data != None):
        values = (ack,seq,data)
        UDP_Data = struct.Struct('I I 8s')
    else:
        values = (ack,seq)
        UDP_Data = struct.Struct('I I')
    packed_data = UDP_Data.pack(*values)
    chksum = bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")
    print("Chksum: ",chksum)
    return chksum;

#Compares computed chksum value with original packet's
#Returns ACK = 1, NAK = 0
#
#not to be confused with CreateChksum
def Checksum(UDP_Packet, chksum):
    ack = 0
    if UDP_Packet[3] == chksum:
        print ('Checksums Match')
        ack = 1
    else:
        print ('Checksums do not Match; Packet Corrupt')
    return ack;

#checks the sequence number of the current packet.
#returns True if matching, False otherwise.
def Checkseq(UDP_Packet, seq):
    if UDP_Packet[1] == seq:
        print ('Sequence numbers match: ', seq)
        return True;
    else:
        print ('Sequence number misalignment; expected ', seq)
        return False;

if __name__ == "__main__":
    main();
