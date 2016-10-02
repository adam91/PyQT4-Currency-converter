import sys
from PyQt4 import QtGui, QtCore
import bs4
import requests

dict = {
    'PLN': 0,
    'USD': 3,
    'EUR': 6,
    'GBP': 9,
    'INR': 12,
    'AUD': 15,
    'CAD': 18,
    'SGD': 21,
    'MYR': 24,
    'JPY': 27,
}


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Currency Converter")

        self.main()

    def main(self):

        self.label = QtGui.QLabel("Your currency", self)
        self.label.move(50, 20)

        self.firstCurrency = QtGui.QComboBox(self)
        for key, value in dict.iteritems():
            self.firstCurrency.addItem(key)
        self.firstCurrency.move(50, 50)

        self.secondlabel = QtGui.QLabel("New currency", self)
        self.secondlabel.move(250, 20)

        self.secondCurrency = QtGui.QComboBox(self)
        for key, value in dict.iteritems():
            self.secondCurrency.addItem(key)
        self.secondCurrency.move(250, 50)

        self.checkBox = QtGui.QCheckBox('automate it', self)
        self.checkBox.move(160, 50)
        self.checkBox.stateChanged.connect(self.checkbox_changed)

        self.thirdlabel = QtGui.QLabel("Amount", self)
        self.thirdlabel.move(100, 150)

        self.edit = QtGui.QDoubleSpinBox(self)
        self.edit.setValue(0)
        self.edit.move(150, 150)

        self.result = QtGui.QLabel("Score", self)
        self.result.move(150, 200)

        self.button = QtGui.QPushButton('Convert', self)
        self.button.clicked.connect(self.exchange)
        self.button.move(300, 150)

        self.show()

    def checkbox_changed(self, int):
        if self.checkBox.isChecked():
            self.connect(self.firstCurrency,
                         QtCore.SIGNAL("currentIndexChanged(int)"), self.exchange)
            self.connect(self.secondCurrency,
                         QtCore.SIGNAL("currentIndexChanged(int)"), self.exchange)
            self.connect(self.edit,
                         QtCore.SIGNAL("valueChanged(double)"), self.exchange)

    def exchange(self):
        my_currency = unicode(self.firstCurrency.currentText())
        currency = unicode(self.secondCurrency.currentText())
        amount = self.edit.value()

        website = requests.get('http://www.x-rates.com/table/?from=PLN&amount=1')
        website.raise_for_status()
        soup = bs4.BeautifulSoup(website.text, 'html.parser')
        if dict[my_currency] == 0:
            my_rate = 1
        else:
            my_rate = '.ratesTable td:nth-of-type(' + str(dict[my_currency]) + ')'
            my_rate = soup.select(my_rate)
            my_rate = my_rate[0].text
        if dict[currency] == 0:
            rate = 1
        else:
            rate = '.ratesTable td:nth-of-type(' + str(dict[currency]) + ')'
            rate = soup.select(rate)
            rate = rate[0].text
        score = float(my_rate) / float(rate) * float(amount)
        score = round(score, 2)
        score = str(score)
        self.result.setText("You'll get " + score + " " + currency)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
