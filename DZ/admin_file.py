import sqlite3
import sys
from os import listdir
from os.path import isfile, join

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox, QInputDialog


class PupilDialog(QDialog):
    def __init__(self, main_window, login=None):
        super().__init__()
        uic.loadUi('edit_pupil.ui', self)
        self.main_window = main_window
        self.con = self.main_window.con
        cur = self.con.cursor()
        name, grade, books = cur.execute(f'select name, grade, books from pupils where login = {login}').fetchone()

        self.lineEdit.setText(str(login))
        self.lineEdit_2.setText(name)
        self.comboBox.setCurrentText(str(grade))
        self.lineEdit_3.setText(books)
        self.pushButton.clicked.connect(self.edit_pupil)

    def edit_pupil(self):
        login, name, grade, books = self.lineEdit.text(), self.lineEdit_2.text(), self.comboBox.currentText(), self.lineEdit_3.text()
        if not name:
            self.label_6.setText('имя указано не верно')
            return

        cur = self.con.cursor()

        if not books:
            cur.execute(
                f'update pupils set name = "{name}", grade = {grade}, books = NULL where login = {login}').fetchall()
        else:
            books_id = [str(i[0]) for i in cur.execute(f'select id from library').fetchall()]
            existing_books = all(i in books_id for i in books.split())
            if not existing_books:
                self.label_6.setText('id учебников указаны не верно')
                return
            cur.execute(
                f'update pupils set name = "{name}", grade = {grade}, books = "{books}" where login = {login}').fetchall()
        self.con.commit()
        self.destroy()
        self.main_window.updateTable()


class UserDialog(QDialog):
    def __init__(self, main_window, login=None):
        super().__init__()
        uic.loadUi('add_user.ui', self)
        self.main_window = main_window
        self.con = self.main_window.con
        cur = self.con.cursor()

        self.comboBox.currentTextChanged.connect(self.available)
        if login:  # режим редактирования
            password, user_type = cur.execute(f'select password, type from users where login = {login}').fetchone()
            self.user_type = user_type
            self.pushButton.setText('Изменить')
            self.lineEdit_2.setText(password)
            self.comboBox.setCurrentText({0: 'Ученик', 1: 'Администратор'}[user_type])

            if user_type == 0:  # ученик
                name, grade = cur.execute(f'select name, grade from pupils where login = {login}').fetchone()
                self.lineEdit_4.setText(name)
                self.comboBox_2.setCurrentText(str(grade))
            self.pushButton.clicked.connect(self.edit_user)
        else:  # режим добавления
            self.pushButton.setText('Добавить')
            login = cur.execute(f'select max(login) from users').fetchone()[0] + 1
            self.pushButton.clicked.connect(self.add_user)

        self.lineEdit.setText(str(login))

    def add_user(self):
        cur = self.con.cursor()

        login, password, user_type = self.lineEdit.text(), self.lineEdit_2.text(), {'Ученик': 0, 'Администратор': 1}[
            self.comboBox.currentText()]
        if not password:
            self.label_6.setText('password указан не верно')
            return

        if user_type == 0:  # pupil
            name, grade = self.lineEdit_4.text(), self.comboBox_2.currentText()
            if not name:
                self.label_6.setText('имя указано не верно')
                return
            cur.execute(
                f'insert into users(login, password, type) values ({login}, "{password}", {user_type})').fetchall()
            cur.execute(
                f'insert into pupils(login, name, grade) values ({login}, "{name}", {grade})').fetchall()
        else:
            cur.execute(
                f'insert into users(login, password, type) values ({login}, "{password}", {user_type})').fetchall()

        self.con.commit()
        self.destroy()
        self.main_window.updateTable()

    def edit_user(self):
        cur = self.con.cursor()

        login, password, user_type = self.lineEdit.text(), self.lineEdit_2.text(), \
                                     {'Ученик': 0, 'Администратор': 1}[self.comboBox.currentText()]
        if not password:
            self.label_6.setText('password указан не верно')
            return

        if user_type == 0:  # pupil
            name, grade = self.lineEdit_4.text(), self.comboBox_2.currentText()
            if not name:
                self.label_6.setText('имя или класс указаны не верно')
                return
            cur.execute(
                f'update users set password = "{password}", type = {user_type} where login = {login}').fetchall()
            cur.execute(f'update pupils set name = "{name}", grade = {grade} where login = {login}').fetchall()
            if self.user_type == 1:  # был админом
                cur.execute(f'insert into pupils(login, name, grade) values ({login}, "{name}", {grade})').fetchall()
        else:
            if self.user_type == 0:  # был ранее учеником
                reply = QMessageBox.question(self, 'Continue?',
                                             'Данные пользователя-ученика будут утеряны. Продолжить?', QMessageBox.Yes,
                                             QMessageBox.No)
                if reply == QMessageBox.Yes:
                    cur.execute(f'delete from pupils where login = {login}').fetchall()
                    cur.execute(
                        f'update users set password = "{password}", type = {user_type} where login = {login}').fetchall()
                else:
                    return

        self.con.commit()
        self.destroy()
        self.main_window.updateTable()

    def available(self):
        is_pupil = self.comboBox.currentText() == 'Ученик'
        self.lineEdit_4.setEnabled(is_pupil)
        self.comboBox_2.setEnabled(is_pupil)


class BookDialog(QDialog):
    def __init__(self, main_window, book_id=None):
        super().__init__()
        uic.loadUi('add_book.ui', self)
        self.main_window = main_window
        self.con = self.main_window.con
        cur = self.con.cursor()

        if book_id:  # редактирование
            self.pushButton.setText('Сохранить')
            self.pushButton.clicked.connect(self.edit_book)
            name, author, grade, image, n = cur.execute(f'select name, author, grade, image, n from library where id = {book_id}').fetchone()
            self.lineEdit_2.setText(name)
            self.lineEdit_3.setText(author)
            self.lineEdit_4.setText(str(grade))
            self.lineEdit_5.setText(str(image))
            self.lineEdit_6.setText(str(n))
        else:  # создание
            self.pushButton.setText('Добавить')
            book_id = cur.execute(f'select max(id) from library').fetchone()[0] + 1
            self.pushButton.clicked.connect(self.add_book)
        self.lineEdit.setText(str(book_id))

    def add_book(self):
        book_id, name, author, grade, image, n = self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), self.lineEdit_5.text(), self.lineEdit_6.text()
        if not (name and author and grade and len(str(n))):
            self.label_7.setText('не все поля заполнены')
            return

        images_path = 'images'
        images_files = [f.split('.')[0] for f in listdir(images_path) if isfile(join(images_path, f))]

        if not image:
            image = 'NULL'
        elif image not in images_files:
            self.label_7.setText('данное изображение отсутствует')
            return
        else:
            image = f'"{image}"'
        if not n.isdigit():
            self.label_7.setText('не верный формат кол-ва учебников')
            return
        cur = self.con.cursor()
        cur.execute(f'insert into library(id, name, author, grade, image, n) values ({book_id}, "{name}", "{author}", "{grade}", {image}, {n})').fetchall()

        self.con.commit()
        self.destroy()
        self.main_window.updateTable()

    def edit_book(self):
        book_id, name, author, grade, image, n = self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), self.lineEdit_5.text(), self.lineEdit_6.text()
        if not (name and author and grade and len(str(n))):
            self.label_7.setText('не все поля заполнены')
            return

        images_path = 'images'
        images_files = [f.split('.')[0] for f in listdir(images_path) if isfile(join(images_path, f))]

        if not image:
            image = 'NULL'
        elif image not in images_files:
            self.label_7.setText('данное изображение отсутствует')
            return
        else:
            image = f'"{image}"'
        if not n.isdigit():
            self.label_7.setText('не верный формат кол-ва учебников')
            return
        cur = self.con.cursor()

        cur.execute(f'update library set name = "{name}", author = "{author}", grade = "{grade}", image = {image}, n = {n} where id = {book_id}').fetchall()
        self.con.commit()
        self.destroy()
        self.main_window.updateTable()


class MainAdminWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        uic.loadUi('admin_window.ui', self)  # Загружаем дизайн
        self.con = sqlite3.connect(db)
        self.updateTable()

        #  books
        self.pushButton.clicked.connect(self.add_book)
        self.pushButton_2.clicked.connect(self.edit_book)
        self.pushButton_3.clicked.connect(self.delete_book)
        self.pushButton_2.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.tableWidget.itemSelectionChanged.connect(self.available_books)

        #  users
        self.pushButton2.clicked.connect(self.add_user)
        self.pushButton2_2.clicked.connect(self.edit_user)
        self.pushButton2_3.clicked.connect(self.delete_user)
        self.pushButton2_2.setEnabled(False)
        self.pushButton2_3.setEnabled(False)
        self.tableWidget2.itemSelectionChanged.connect(self.available_users)

        #  pupils
        self.pushButton3.clicked.connect(self.edit_pupil)
        self.pushButton3_2.clicked.connect(self.update_grade)
        self.pushButton3.setEnabled(False)
        self.tableWidget3.itemSelectionChanged.connect(self.available_pupils)

    def add_book(self):
        self.second_form = BookDialog(self)
        self.second_form.show()

    def add_user(self):
        self.second_form = UserDialog(self)
        self.second_form.show()

    def edit_book(self):
        row = self.tableWidget.selectedItems()[0].row()
        book_id = self.tableWidget.item(row, 0).text()
        self.second_form = BookDialog(self, book_id)
        self.second_form.show()

    def edit_user(self):
        row = self.tableWidget2.selectedItems()[0].row()
        login = self.tableWidget2.item(row, 0).text()
        self.second_form = UserDialog(self, login)
        self.second_form.show()

    def edit_pupil(self):
        row = self.tableWidget3.selectedItems()[0].row()
        login = self.tableWidget3.item(row, 0).text()
        self.second_form = PupilDialog(self, login)
        self.second_form.show()

    def delete_book(self):
        reply = QMessageBox.question(self, 'Continue?', 'Данные учебника будут удалены. Продолжить?',
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            cur = self.con.cursor()
            row = self.tableWidget.selectedItems()
            info = list(self.tableWidget.item(i.row(), 0).text() for i in row)
            for book_id in info:
                cur.execute(f'delete from library where id = {book_id}').fetchall()
            self.con.commit()
            self.updateTable()

    def delete_user(self):
        reply = QMessageBox.question(self, 'Continue?', 'Данные пользователя будут удалены. Продолжить?',
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            cur = self.con.cursor()
            row = self.tableWidget2.selectedItems()
            info = list(self.tableWidget2.item(i.row(), 0).text() for i in row)
            for login in info:
                cur.execute(f'delete from pupils where login = {login}').fetchall()
                cur.execute(f'delete from users where login = {login}').fetchall()
            self.con.commit()
            self.updateTable()

    def update_grade(self):
        reply = QMessageBox.question(self, 'Continue?', 'Данные учеников 11 класса будут удалены. Продолжить?',
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute(f'delete from pupils where grade > 10').fetchall()
            cur.execute(f'delete from users where type = 0 and login not in (select login from pupils)').fetchall()
            cur.execute(f'update pupils set grade = grade + 1').fetchall()

        self.con.commit()
        self.updateTable()

    def updateTable(self):
        cur = self.con.cursor()
        for table, query in ((self.tableWidget, 'select * from library'),
                             (self.tableWidget2, 'select u.login, u.password, t.type as type from users u '
                                                 'join types t on u.type = t.id'),
                             (self.tableWidget3, 'select * from pupils')):
            info = cur.execute(query).fetchall()
            title = [description[0] for description in cur.description]

            table.setColumnCount(len(title))
            table.setHorizontalHeaderLabels(title)
            table.setRowCount(0)
            for i, row in enumerate(info):
                table.setRowCount(table.rowCount() + 1)
                for j, elem in enumerate(row):
                    table.setItem(i, j, QTableWidgetItem(str(elem)))
            table.resizeColumnsToContents()

    def available_books(self):
        is_selected = len(self.tableWidget.selectedItems())
        self.pushButton_2.setEnabled(is_selected == 1)
        self.pushButton_3.setEnabled(is_selected)

    def available_users(self):
        selected = len(self.tableWidget2.selectedItems())
        self.pushButton2_2.setEnabled(selected == 1)
        self.pushButton2_3.setEnabled(selected)

    def available_pupils(self):
        is_selected = len(self.tableWidget3.selectedItems()) == 1
        self.pushButton3.setEnabled(is_selected)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    ex = MainAdminWindow('library.db')
    ex.show()
    sys.exit(app.exec_())
