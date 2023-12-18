import sqlite3
import sys
from os import listdir
from os.path import isfile, join

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox, QInputDialog


class Private_space(QMainWindow):
    def __init__(self, db, login):
        super().__init__()
        uic.loadUi('private_space.ui', self)
        self.con = sqlite3.connect(db)
        cur = self.con.cursor()
        self.login = login
        name, grade = cur.execute(
             f'select name, grade from pupils where login = {self.login}').fetchone()
        password = cur.execute(
            f'select password from users where login = {self.login}').fetchone()
        self.lineEdit.setText(str(self.login))
        self.lineEdit_2.setText(str(password[0]))
        self.lineEdit_3.setText(name)
        self.lineEdit_4.setText(str(grade))
        self.lineEdit.setEnabled(False)
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_4.setEnabled(False)
        self.pushButton.clicked.connect(self.edit_password)

    def edit_password(self):
        password = self.lineEdit_2.text()
        if not password:
            self.label_5.setText('пароль указан не верно')
            return

        cur = self.con.cursor()
        cur.execute(
            f'update users set password = "{password}" Where login = "{self.login}"').fetchall()
        self.con.commit()
        self.destroy()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = Private_space('library.db', 4)
    ex.show()
    sys.exit(app.exec_())
