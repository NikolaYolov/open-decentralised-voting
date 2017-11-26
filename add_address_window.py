from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SetAddressWindow(QDialog):
    new_address = pyqtSignal(int, str, int)

    def __init__(self, parent):
        super(SetAddressWindow, self).__init__(parent)

        self.resize(120, 120);
        self.setWindowTitle("Set address")

        self.mainLayout = QBoxLayout(QBoxLayout.TopToBottom, self)
        self.fillLayout = QGridLayout()

        self.fillLayout.addWidget(QLabel("ID:"), 0, 0)
        self.idTextEdit = QLineEdit()
        self.idTextEdit.setValidator(QIntValidator(self))
        self.idTextEdit.setMaximumHeight(20)
        self.fillLayout.addWidget(self.idTextEdit, 0, 1)

        self.fillLayout.addWidget(QLabel("IP:"), 1, 0)
        self.ipTextEdit = QLineEdit()
        rx = QRegExp("[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}")
        ipValidator = QRegExpValidator(rx)
        self.ipTextEdit.setValidator(ipValidator)
        self.ipTextEdit.setMaximumHeight(20)
        self.fillLayout.addWidget(self.ipTextEdit, 1, 1)

        self.fillLayout.addWidget(QLabel("port:"), 2, 0)
        self.portTextEdit = QLineEdit()
        self.portTextEdit.setValidator(QIntValidator(self))
        self.portTextEdit.setMaximumHeight(20)
        self.fillLayout.addWidget(self.portTextEdit, 2, 1)

        self.mainLayout.addLayout(self.fillLayout)
        self.okCancelLayout = QBoxLayout(QBoxLayout.LeftToRight)

        self.okBtn = QPushButton("Ok")
        self.okCancelLayout.addWidget(self.okBtn)
        self.cancelBtn = QPushButton("Cancel")
        self.okCancelLayout.addWidget(self.cancelBtn)
        self.mainLayout.addLayout(self.okCancelLayout)

        for signal in (self.accepted, self.rejected):
            for edit in (self.idTextEdit, self.ipTextEdit, self.portTextEdit):
                signal.connect(edit.clear)
                
        self.okBtn.pressed.connect(self.confim)
        self.cancelBtn.pressed.connect(self.reject)

    def confim(self):
        vid_text = self.idTextEdit.text()
        vid_text = vid_text if vid_text else "0"
        port_text = self.portTextEdit.text()
        port_text = port_text if port_text else "0"
        self.new_address.emit(
            int(vid_text),
            self.ipTextEdit.text(),
            int(port_text))
        self.accept()
