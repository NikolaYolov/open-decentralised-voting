import sys
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import server
import voter_table
import election
import step1
import add_address_window

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = QWidget()
    window.resize(2048, 2048)
    window.move(0, 0)
    window.setWindowTitle('Decentralised Anonymous Voting')

    layout = QBoxLayout(QBoxLayout.TopToBottom, window)
    electionsCombo = QComboBox()
    electionsCombo.addItem("United States presidential election, 2016")
    electionsCombo.addItem("Oxford University Student Union election, 2017")
    layout.addWidget(electionsCombo)

    tabs = QTabWidget()
    overview = QWidget()
    overviewLayout = QBoxLayout(QBoxLayout.LeftToRight, overview)
    infoLayout = QBoxLayout(QBoxLayout.TopToBottom)
    infoLayout.setAlignment(Qt.AlignTop)

    for text in ("Status: Completed",
                 "Voting closed: November 8, 2016",
                 "Hillary Clinton: 48.2%",
                 "65,853,516 / 231,307,614",
                 "Donald Trump: 46.1%",
                 "62,984,825 / 231,307,614",
                 "Turnout: 55.7%",
                 "128,838,341 /  231,307,614",
                 ):
        infoLayout.addWidget(QLabel(text))
    overviewLayout.addLayout(infoLayout)
    
    series = QPieSeries()
    series.append("Hillary Clinton", 26.84)
    series.append("Donald Trump", 25.67)
    series.append("Did not vote", 44.3)
    chart = QChart()
    chart.addSeries(series)
    chart.setTitle("United States presidential election, 2016")
    overviewLayout.addWidget(QChartView(chart))
    
    tabs.addTab(overview, "Overview")

    id_to_address = {}
    myid = 0
    if len(sys.argv) >= 2:
        myid = int(sys.argv[1])
    step1 = step1.Step1(myid, id_to_address)
    step1.start()

    votersTab = QWidget()
    voterLayout = QBoxLayout(QBoxLayout.TopToBottom, votersTab)
    votersTable = voter_table.VoterTable(election.SampleElection())
    step1.server.update.connect(votersTable.update)
    voterLayout.addWidget(votersTable)
    plus_pixmap = QPixmap("plus.png")
    plus_icon = QIcon(plus_pixmap)
    plus_btn = QPushButton(plus_icon, "")
    plus_btn.setIconSize(QSize(50, 50))
    plus_btn.setMaximumWidth(100)

    set_address_window = add_address_window.SetAddressWindow(window)
    plus_btn.pressed.connect(set_address_window.exec)
    set_address_window.new_address.connect(step1.server.newAddress)
    voterLayout.addWidget(plus_btn)
    
    tabs.addTab(votersTab, "Voters")
    layout.addWidget(tabs)

    voteBtnsLayout = QBoxLayout(QBoxLayout.LeftToRight)
    layout.addLayout(voteBtnsLayout)
    btns = []

    
    voteCombo = QComboBox(window)
    voteCombo.setMaximumWidth(200)
    voteCombo.addItem("Hillary Clinton")
    voteCombo.addItem("Donald Trump")
    voteBtnsLayout.addWidget(voteCombo)
    
    btn = QPushButton("Vote", window)
    btn.setMaximumWidth(200)
    btn.pressed.connect(lambda: btn.setEnabled(False))
    btn.pressed.connect(lambda: voteCombo.setEnabled(False))
    voteBtnsLayout.addWidget(btn)

    window.show()
    
    sys.exit(app.exec_())
