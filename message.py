import enum

class MessageType(enum.Enum):
    IDENTIFICATION = 0
    TINYVOTE = 1
    BCBLOCKCHAIN = 2

class Message(object):
    def make_identification(self, id_to_address):
        '''
        id_to_address is a dict mapping voter ids to (ip, port)
        '''
        self.type = MessageType.IDENTIFICATION
        self.id_to_address = id_to_address

    def make_tiny_vote(self, from_voter, to_voter, tiny_vote):
        self.type = MessageType.TINYVOTE
        self.from_vtr = from_voter
        self.to_vtr = to_voter
        self.encr_part = tiny_vote

    def make_blockhcian(self, blockchain):
        self.type = MessageType.BCBLOCKHAIN
        self.blockchian = blockchain
