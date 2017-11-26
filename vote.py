import socket
import pickle
import const

def vote(hostname):
    for vote in (
        ('Alida Zurita', 0, 1,),
        ('Avril Eichenlaub', 1, 0,),
        ('Rozanne Brannum', 2, 1,),
        ('Wilhemina Nees', 3, 1,),
        ('Kina Hudnall', 4, 1,),
        ('Micha Soderlund', 5, 0,),
        ('Graig Granda', 6,  1,),
    ):
    
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect((hostname, const.server_port))
        clientsocket.send(pickle.dumps(vote))
        response = clientsocket.recv(const.packet_size)
        clientsocket.close()
        results = pickle.loads(response)
        print("Results so far are %s" % str(results))
