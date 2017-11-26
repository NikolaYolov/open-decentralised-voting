from PyQt5.QtCore import QThread

import election
import server

class Step1(QThread):
    def __init__(self, my_id, id_to_address, vote_mgr):
        super(Step1, self).__init__()
        eltion = election.SampleElection()
        self.server = server.Server(my_id, id_to_address, eltion, vote_mgr)

    def run(self):
        self.server.listen()
