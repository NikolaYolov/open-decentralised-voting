import socket
import pickle
import time

from PyQt5.QtCore import *

import election
import const
import message

def OwnIP():
    '''
    A bit hacky, but it works well...
    socket.gethostbyname(socket.gethostname()) hangs or returns 127.0.0.1
    from time to time.
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def OwnPort(vid):
    return vid + const.port_start


class Server(QObject):
    update = pyqtSignal(dict)
    
    def __init__(self, my_id, id_to_address, eltion):
        super(Server, self).__init__()

        self.election = eltion
        self.my_id = my_id
        self.ids = { v.id for v in eltion.voters }
        assert my_id in self.ids
        self.id_to_address = id_to_address
        self.id_to_address[my_id] = self.ownAddress()
        print("P2P network : %s" % str(self.id_to_address))
        self.last_broadcast = 0

        socket.setdefaulttimeout(1)

    def newAddress(self, vid, ip, port):
        if vid in self.ids and vid != self.my_id:
            self.id_to_address[vid] = (ip, port)

    def ownAddress(self):
        return OwnIP(), OwnPort(self.my_id)

    def listen(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Binding to address %s" % str(self.ownAddress()))
        serversocket.bind(self.ownAddress())
        serversocket.listen()
        print("Listening")
        while time.time() < self.election.polls_close:
            self.update.emit(self.id_to_address)
            self.broadcast()
            try:
                clientsocket, addr = serversocket.accept()
                print("Got a connection from %s" % str(addr))
                message = pickle.loads(clientsocket.recv(const.packet_size))
                print("Received message %s" % str(message.__dict__))
                self.process_message(message)
                clientsocket.close()
            except socket.timeout:
                pass

    def process_message(self, msg):
        if type(msg) is not message.Message:
            print("Received an incorrect message")
            return

        if msg.type == message.MessageType.IDENTIFICATION:
            for vid, address in msg.id_to_address.items():
                if vid in self.ids:
                    self.id_to_address[vid] = address
        elif msg.type == message.MessageType.TINYVOTE:
            pass
        elif msg.type == message.MessageType.BCBLOCK:
            pass
        else:
            print("Received a message of an unknown type")
            return

    def broadcast(self):
        if time.time() < self.last_broadcast + 5:
            return
        # Time to broadcast :)
        print("Broadcasting")
        self.last_broadcast = time.time()
        for vid, (ip, port) in self.id_to_address.items():
            assert (vid == self.my_id) == ((ip, port) == self.ownAddress())
            if vid == self.my_id:
                continue

            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                print("Broadcasting to %s" % str((ip, port)))
                clientsocket.connect((ip, port))
                msg = message.Message()
                msg.make_identification(self.id_to_address)
                clientsocket.send(pickle.dumps(msg))
            except:
                pass
            finally:
                clientsocket.close()


def serve(my_id, id_to_address):
    eltion = election.SampleElection()
    server = Server(my_id, id_to_address, eltion)
    server.listen()
