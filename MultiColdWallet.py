

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QComboBox, QLabel, QTextEdit, QGraphicsView, QGraphicsScene, QApplication)
from PyQt5.QtGui import (QFont,QImage, QPixmap)
from PyQt5 import QtGui
from bitcoin import *

#from Ethereum import *

from ecdsa import SigningKey, SECP256k1
import sha3
import qrcode


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def showQRCode(self):
        img = qrcode.make(self.priv)
        img2 = qrcode.make(self.address)
        img.save("1.png")
        img2.save("2.png")
        pixmap = QPixmap("1.png")
        pixmap2 = QPixmap("2.png")
        self.graph1.setPixmap(pixmap)
        self.graph2.setPixmap(pixmap2)
        self.graph1.show(self)
        self.graph2.show(self)
        self.show(self)

    def getbtc(self):
        self.priv = random_key()
        pub = privtopub(self.priv)
        self.address = pubkey_to_address(pub)
        return self.priv, self.address

    def geteth(self):
        keccak = sha3.keccak_256()
        self.priv = SigningKey.generate(curve=SECP256k1)
        pub = self.priv.get_verifying_key().to_string()
        keccak.update(pub)
        self.address = keccak.hexdigest()[24:]
        return self.priv, self.address

    def click_generate(self):
        if self.comboBox1.currentText() == "SHA256":
            self.getbtc()
            self.textEdit1.setText(self.priv)
            self.textEdit2.setText(str(self.address))
        if self.comboBox1.currentText() == "Ethash":
            self.geteth()
            self.textEdit1.setText(self.priv.to_string().hex())
            self.textEdit2.setText(str(self.address))
        self.showQRCode()

    def changeC(self):
        self.comboBox2.clear()
        if self.comboBox1.currentText() == "SHA256":
            self.comboBox2.addItem("BitCoin")
            self.comboBox2.addItem("Crowd")
        if self.comboBox1.currentText() == "Ethash":
            self.comboBox2.addItem("Eth")
            self.comboBox2.addItem("Etc")


    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        label1 = QLabel('Algorithm',self)
        label1.setGeometry(90, 10,68,17)

        self.comboBox1 = QComboBox(self)
        self.comboBox1.setGeometry(30,30,200, 27)
        self.comboBox1.setEditable(False)
        self.comboBox1.setObjectName("comboBox")
        self.comboBox1.addItem("SHA256")
        self.comboBox1.addItem("Ethash")
        self.comboBox1.activated.connect(self.changeC)

        label2 = QLabel('Coin', self)
        label2.setGeometry(105, 70, 68, 17)

        self.comboBox2 = QComboBox(self)
        self.comboBox2.move(30, 30)
        self.comboBox2.setGeometry(30, 90, 200, 27)
        self.comboBox2.setEditable(False)
        self.comboBox2.setObjectName("comboBox")
        self.comboBox2.addItem("BitCoin")
        self.comboBox2.addItem("CrownCoin")

        btn = QPushButton('Generate', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(80, 130)
        btn.clicked.connect(self.click_generate)

        label3 = QLabel('Private key', self)
        label3.setGeometry(380, 180, 100, 17)

        self.textEdit1 = QTextEdit("",self);
        self.textEdit1.setGeometry(30,200,800,31)

        label4 = QLabel('Address', self)
        label4.setGeometry(390, 230, 68, 17)

        self.textEdit2 = QTextEdit("", self);
        self.textEdit2.setGeometry(30, 250, 800, 31)

        self.graph1 = QLabel(self)
        self.graph1.setGeometry(10,300,410,410)

        self.graph2 = QLabel(self)
        self.graph2.setGeometry(430, 300, 410, 410)

        btn2 = QPushButton('Print It', self)
        btn2.setToolTip('This is a <b>QPushButton</b> widget')
        btn2.resize(btn2.sizeHint())
        btn2.move(400, 710)

        #self.btnclick(self)

        #self.create_cort()

        priv = ""
        address = ""

        font = QtGui.QFont()
        font.setPointSize(13)
        self.setFont(font)
        self.setGeometry(100, 100, 850, 750)
        self.setWindowTitle('Tooltips')
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
