import sqlite3
import sys
import admin_file
import user_file

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from admin_file import MainAdminWindow
from user_file import MainPupilWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('start_window.ui', self)  # Загружаем дизайн
        self.pushButton.clicked.connect(self.run_login)
        self.pushButton.setEnabled(False)
        self.lineEdit.textChanged.connect(self.update_button)
        self.lineEdit_2.textChanged.connect(self.update_button)
        # Обратите внимание: имя элемента такое же как в QTDesigner

        self.db = None
        self.con = None

    def run_login(self):
        self.statusBar().clearMessage()
        self.db = self.comboBox.currentText()
        login, password = self.lineEdit.text(), self.lineEdit_2.text()
        self.con = sqlite3.connect(self.db)

        cur = self.con.cursor()
        exist = cur.execute(f'select type from users '
                            f'where login = "{login}" and password = "{password}"').fetchall()
        print(exist)
        if exist:
            print('Успешно')
            user_type = exist[0][0]
            if user_type == 0:
                self.pupil_window = MainPupilWindow(login, self.db)
                self.pupil_window.show()
            elif user_type == 1:
                self.admin_window = MainAdminWindow(self.db)
                self.admin_window.show()
        else:
            self.statusBar().showMessage('login или password указаны не верно')

    def update_button(self):
        self.pushButton.setEnabled(bool(self.lineEdit.text()) and bool(self.lineEdit_2.text()))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())