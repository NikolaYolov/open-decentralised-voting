import socket
import pickle
import const

def sync(hostname):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((hostname, const.server_port))
    clientsocket.send(None) # No vote, just sync
    message = clientsocket.recv(const.packet_size)
    clientsocket.close()
    el = pickle.loads(message)
    print("The message from the server is %s" %
          str((el.voters, el.polls_close)))
