from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class VoterTable(QTableWidget):
    cols = ("Name", "ID", "Status", "Participation", "Public key", "Public vote",
            "IP", "port")

    def __init__(self, election):
        super(VoterTable, self).__init__(0, len(self.cols))

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setHorizontalHeaderLabels(self.cols)
        self.verticalHeader().setVisible(False);
        self.setAlternatingRowColors(True)
        self.election = election
        self.id2rown = {}

        for rown, voter_info in enumerate(self.election.voters):
            self.id2rown[voter_info.id] = rown

            self.insertRow(rown)
            self.setItem(rown, 0, QTableWidgetItem(voter_info.name)) # Name
            self.setItem(rown, 1, QTableWidgetItem(str(voter_info.id))) # ID
            self.setItem(rown, 2, QTableWidgetItem("Unreachable")) # Status
            self.setItem(rown, 3, QTableWidgetItem("Has not voted")) # Particip
            self.setItem(rown, 4, QTableWidgetItem("0")) # Public Key
            self.setItem(rown, 5, QTableWidgetItem("")) # Public Vote
            self.setItem(rown, 6, QTableWidgetItem("")) # IP
            self.setItem(rown, 7, QTableWidgetItem("")) # port

        for row in range(len(self.election.voters)):
            for col in range(len(self.cols)):
                item = self.item(row, col)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)

    def update(self, id_to_address):
        for vid, (ip, port) in id_to_address.items():
            rown = self.id2rown[vid]
            self.item(rown, 2).setText("Online")
            self.item(rown, 6).setText(ip)
            self.item(rown, 7).setText(str(port))
