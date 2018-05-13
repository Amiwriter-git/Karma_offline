import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QComboBox, QLabel, QTextEdit, QGraphicsView, QGraphicsScene, QApplication)
from PyQt5.QtGui import (QFont,QImage, QPixmap)
from PyQt5 import (QtGui, QtCore)
from PyQt5.QtCore import QFile
from PyQt5 import QtPrintSupport
from PyQt5.Qt import QTextStream
from bitcoin import *
from PyQt5.Qt import (QPrinter, QPrintDialog)
from ecdsa import SigningKey, SECP256k1
import sha3
import qrcode


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    #def extract_to_pdf(self):
     #   pass

    def handlePreview(self):
        f = QFile("Qrcodes.html")
        f.open(QFile.ReadOnly | QFile.Text)
        istream = QTextStream(f)
        self.textfield.setHtml(istream.readAll())
        f.close()
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.textfield.print)#self.textEdit1.print)#editor.print_)
        dialog.exec_()

    def showQRCode(self):
        img = qrcode.make(self.priv)
        img2 = qrcode.make(self.address)
        img.save("Priv.png")
        img2.save("Addr.png")
        pixmap = QPixmap("Priv.png")
        pixmap2 = QPixmap("Addr.png")
        scpixmap = pixmap.scaled(self.graph1.size(), QtCore.Qt.KeepAspectRatio)
        scpixmap2 = pixmap2.scaled(self.graph2.size(), QtCore.Qt.KeepAspectRatio)
        self.graph1.setPixmap(scpixmap)
        self.graph2.setPixmap(scpixmap2)
        self.graph1.show()
        self.graph2.show()
        self.show()

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
            #self.ipriv = self.priv
            #self.iaddress = str(self.address)
        if self.comboBox1.currentText() == "Ethash":
            self.geteth()
            self.textEdit1.setText(self.priv.to_string().hex())
            self.textEdit2.setText('0x'+str(self.address.decode('UTF-8')))
            #self.ipriv = self.priv.to_string().hex()
            #self.iaddress = '0x'+str(self.address.decode('UTF-8'))
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
        label1.setGeometry(90, 5,80,20)

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
        btn.setGeometry(250, 80, 120, 40)
        btn.clicked.connect(self.click_generate)

        label3 = QLabel('Private key', self)
        label3.setGeometry(270, 130, 100, 17)

        self.textEdit1 = QTextEdit("",self);
        self.textEdit1.setGeometry(10,150,620,50)

        label4 = QLabel('Address', self)
        label4.setGeometry(280, 210, 68, 17)

        self.textfield = QTextEdit("", self);
        self.textfield.setGeometry(10, 230, 620, 50)

        self.textEdit2 = QTextEdit("", self);
        self.textEdit2.setGeometry(10, 230, 620, 50)

        label5 = QLabel('Private key', self)
        label5.setGeometry(110, 285, 100, 17)

        label6 = QLabel('Address', self)
        label6.setGeometry(440, 285, 100, 17)

        self.graph1 = QLabel(self)
        self.graph1.setGeometry(10, 310, 300, 300)

        self.graph2 = QLabel(self)
        self.graph2.setGeometry(330, 310, 300, 300)

        btn2 = QPushButton('Print It', self)
        btn2.setToolTip('This is a <b>QPushButton</b> widget')
        btn2.resize(btn2.sizeHint())
        btn2.move(270, 620)
        btn2.clicked.connect(self.handlePreview)

        #self.btnclick(self)

        #self.create_cort()

        priv = ""
        address = ""
        ipriv = ""
        iaddress = ""

        font = QtGui.QFont()
        font.setPointSize(13)
        self.setFont(font)
        self.setGeometry(100, 100, 650, 650)
        self.setWindowTitle('Tooltips')
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
