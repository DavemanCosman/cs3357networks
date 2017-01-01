#UDP_Client.py
#David Cosman
#
#A simple UDP Client implementing rdt2.2
#Coded in Python 3.5

import binascii
import socket
import struct
import sys
import hashlib

def main():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    MY_UDP_IP = "192.168.131.129"
    unpacker = struct.Struct('I I 32s')
    
    print("UDP target IP:", UDP_IP)
    print("UDP target port:", UDP_PORT)

    #byte data to be sent in packets
    data = [b'NCC-1701', b'NCC-1664', b'NCC-1017']
    #Create client socket
    clientSock = CreateSocket(MY_UDP_IP, UDP_PORT);
    #Set seqNum to 0 as default.
    seq = 0
    for i in range(len(data)):
        print("\n+++Sending packet to server with values:+++")
        #ACK = 0 by default (1 is NAK)
        ack = 0;
        print("ACK: ", ack)
        print("Seq num: ", seq)
        #Build the UDP Packet
        UDP_Packet = BuildPacket(ack, seq, data[i]);
        #Send the UDP Packet
        SendPacket (clientSock, UDP_Packet, UDP_IP, UDP_PORT);
        print("Packet successfully sent")
        #Wait for ACK
        ack = 1;
        while ack == 1:
            #Receive ACK reply
            UDP_Packet = RcvData(clientSock, unpacker);
            if UDP_Packet[0] != ack:
                print("Packet ACK")
            else:
                print("Packet NAK")
            #Create the Checksum for comparison
            chksum = CreateChksum(UDP_Packet[0],UDP_Packet[1]);
       	    #Compare Checksums to test for corrupt acks
            ack = Checksum(UDP_Packet, chksum);
            #Is the sequence order correct?
            seqCorrect = Checkseq(UDP_Packet, seq);
            #Update the seq number
            if seq == 0:
                seq = 1
            else:
                seq = 0
            if ack == 1 or seqCorrect == False:
                #send again if corrupt or no seq match.
                print ('Sending previous to server again')
                ack = 1
                UDP_Packet = BuildPacket (0, seq, data[i]);
                SendPacket (clientSock, UDP_Packet, UDP_IP, UDP_PORT);
    clientSock.close(); #terminate client connection

#Method to recieve and unpack data from packets
#Used for ACK packets from server
#Returns packet in tuple form
def RcvData(sock, unpacker):
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    UDP_Packet = unpacker.unpack(data) # extract data
    print("--Reply Received!--")
    print("received from:", addr)
    print("received reply:", UDP_Packet)
    return UDP_Packet; 

#Creates a Socket that can send and recieve packets
#Using bind because we need to recieve acks from server
def CreateSocket(IP, PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, PORT))
    return sock;

#Sends the specified packet to given IP and PORT
def SendPacket (sock, packet, IP, PORT):
    sock.sendto(packet, (IP, PORT))
    return;

#Builds the packet with specified values
#Returns the built packet in tuple form
def BuildPacket (ack, seq, data):
    print("data: ",data)
    #Create Checksum
    chksum = CreateChksum(ack, seq, data);
    values = (ack,seq,data,chksum)
    #Structure is as follows; AckNum, SeqNum, data, Chksum
    UDP_Packet_Data = struct.Struct('I I 8s 32s')
    UDP_Packet = UDP_Packet_Data.pack(*values)
    return UDP_Packet;

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
#Returns ACK = 0, NAK = 1
#
#not to be confused with CreateChksum
def Checksum(UDP_Packet, chksum):
    ack = 1 #ACK = 0. NACK = 1
    if UDP_Packet[2] == chksum:
        print ('Checksums Match; ACK packet correct')
        ack = 0
    else:
        print ('Checksums do not Match; ACK packet corrupted')
    return ack;

#checks the sequence number of the current packet.
#returns True if matching, False otherwise.
def Checkseq(UDP_Packet, seq):
    if UDP_Packet[1] == seq:
        print ('Sequence numbers match')
        return True;
    else:
        print ('Sequence number misalignment')
        return False;

if __name__ == "__main__":
    main();
