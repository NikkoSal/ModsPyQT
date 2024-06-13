from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
import sqlite3
from xlsxwriter import *

ui, _ = loadUiType('untitled.ui')
login, _ = loadUiType('login.ui')


class Login(QMainWindow, login):
    def __init__(self):
        self.db_path = 'news.db'
        QWidget.__init__(self)
        self.setupUi(self)
        self.Set_Vesible()
        self.pushButton_4.clicked.connect(self.Open_Regist)
        self.pushButton_2.clicked.connect(self.Open_Login)
        self.pushButton.clicked.connect(self.Handle_Login)
        self.pushButton_3.clicked.connect(self.Regist)


    def Set_Vesible(self):
        self.tabWidget.tabBar().setVisible(False)

    def Open_Regist(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Login(self):
        self.tabWidget.setCurrentIndex(1)

    def Handle_Login(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        name = self.lineEdit.text()
        password = self.lineEdit_2.text()

        sql = '''SELECT * FROM Users'''

        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if name == row[1] and password == row[2]:
                self.statusBar().showMessage('user match')
                self.window2 = MainApp()
                self.close()
                self.window2.show()

    import sqlite3

    def Regist(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        name = self.lineEdit_4.text().strip()
        password = self.lineEdit_3.text().strip()

        # Check for empty fields
        if not name or not password:
            self.statusBar().showMessage('Fields cannot be empty')
            return

        # Проверка, существует ли уже пользователь с таким именем
        self.cur.execute('''
        SELECT * FROM Users WHERE name = ?
        ''', (name,))
        existing_user = self.cur.fetchone()

        if existing_user:
            self.statusBar().showMessage('User already exists')
        else:
            self.cur.execute('''
            INSERT INTO Users (name, password)
            VALUES (?, ?)
            ''', (name, password))
            self.db.commit()
            self.statusBar().showMessage('Add New User')


class MainApp(QMainWindow, ui):
    def __init__(self):
        self.db_path = 'news.db'
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI_Changes()
        self.Handle_Buttons()

        self.Show_Category()
        self.Show_Creator()
        self.Show_Games()


        self.Show_Category_Combobox()
        self.Show_Games_Combobox()
        self.Show_Creator_Combobox()

        self.Show_All_Mods()
        self.Show_Daybook()

    def Handle_UI_Changes(self):
      #  self.Hiding_Show_Inform()
        self.tabWidget.tabBar().setVisible(False)

    def Handle_Buttons(self):
        self.pushButton.clicked.connect(self.Open_Act_Day)
        self.pushButton_2.clicked.connect(self.Open_Mods_Tab)
        self.pushButton_4.clicked.connect(self.Open_Users_Tab)
        self.pushButton_3.clicked.connect(self.Open_Settings)
        self.pushButton_5.clicked.connect(self.Show_Infrom)

        self.pushButton_13.clicked.connect(self.Delete_Games)
        self.pushButton_7.clicked.connect(self.Add_New_Mods)
        self.pushButton_16.clicked.connect(self.Add_Category)
        self.pushButton_15.clicked.connect(self.Delete_Category)
        self.pushButton_14.clicked.connect(self.Add_Games)
        self.pushButton_19.clicked.connect(self.Delete_Creator)
        self.pushButton_17.clicked.connect(self.Add_Creator)

        self.pushButton_9.clicked.connect(self.Search)
        self.pushButton_10.clicked.connect(self.Edit_Mods)
        self.pushButton_11.clicked.connect(self.Delete_Mod)

        self.pushButton_12.clicked.connect(self.Login)
        self.pushButton_18.clicked.connect(self.Edit_Login)

        self.pushButton_6.clicked.connect(self.Daybook)
        self.pushButton_8.clicked.connect(self.Clear_Daybook)

        self.pushButton_20.clicked.connect(self.Export_Daybook)
        self.pushButton_21.clicked.connect(self.Export_Mods)

    def Show_Infrom(self):
        self.groupBox_4.show()

    def Hiding_Show_Inform(self):
        pass

    # Opening tabs #
    def Open_Act_Day(self):
        self.tabWidget.setCurrentIndex(0)


    def Open_Mods_Tab(self):
        self.tabWidget.setCurrentIndex(1)


    def Open_Users_Tab(self):
        self.tabWidget.setCurrentIndex(2)


    def Open_Settings(self):
        self.tabWidget.setCurrentIndex(3)




    def Daybook(self):

        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()



        mod_title = self.lineEdit.text()
        game_title = self.lineEdit_19.text()
        release_time = self.lineEdit_10.text()
        degree_time = self.comboBox.currentText()

        self.cur.execute('''
        INSERT INTO Daybook(mod_title, game_title, release_time, degree_time)
        VALUES (?, ?, ?, ?)
        ''',(mod_title, game_title, release_time, degree_time))

        self.db.commit()
        self.statusBar().showMessage('New Note Added')

        self.Show_Daybook()

    def Show_Daybook(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        self.cur.execute('''
        SELECT mod_title, game_title, release_time, degree_time FROM Daybook
        ''')

        data = self.cur.fetchall()

        # Clear existing rows
        self.tableWidget.setRowCount(0)

        for row_index, row_data in enumerate(data):
            self.tableWidget.insertRow(row_index)
            for column_index, item in enumerate(row_data):
                self.tableWidget.setItem(row_index, column_index, QTableWidgetItem(str(item)))


    def Clear_Daybook(self):
        # Connect to the database
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()



        warning = QMessageBox.warning(self, 'Delete Mod', "Are you sure you want to delete this mod",
                                  QMessageBox.Yes | QMessageBox.No)

        if warning == QMessageBox.Yes:
            sql = '''DELETE FROM Daybook '''
            self.cur.execute(sql)
            self.db.commit()
            self.statusBar().showMessage('Table Clear')
            self.Show_Daybook()

    def Show_All_Mods(self):

        self.cur.execute(
            ''' SELECT mod_title, mod_game, mod_category, mod_creator, mod_link, mod_version,mod_discription FROM Mods''')
        data = self.cur.fetchall()

        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_position)

        self.db.close()

    def Add_New_Mods(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        mod_title = self.lineEdit_7.text()
        mod_game = self.comboBox_2.currentText()
        mod_category = self.comboBox_4.currentText()
        mod_creator = self.comboBox_5.currentText()
        mod_link = self.lineEdit_6.text()
        mod_version = self.lineEdit_3.text()
        mod_discription = self.lineEdit_14.text()

        self.cur.execute('''
        INSERT INTO Mods (mod_title, mod_game, mod_category,mod_discription,mod_version, mod_link, mod_creator)
         VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (mod_title, mod_game, mod_category, mod_discription, mod_version, mod_link, mod_creator))

        self.db.commit()
        self.statusBar().showMessage('New Mod Added')

        # Clear the input fields
        self.lineEdit_7.setText('')
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.lineEdit_6.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_14.setText('')

        self.Show_All_Mods()

    def Search(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        mods_title = self.lineEdit_28.text()

        sql = '''SELECT * FROM Mods WHERE mod_title = ?'''

        self.cur.execute(sql, (mods_title,))
        data = self.cur.fetchone()

        if data:
            self.lineEdit_13.setText(data[1])
            self.comboBox_9.setCurrentText(data[2])
            self.comboBox_10.setCurrentText(data[3])
            self.comboBox_11.setCurrentText(data[4])
            self.lineEdit_12.setText(data[5])
            self.lineEdit_11.setText(data[6])
            self.lineEdit_15.setText(data[7])
        else:
            self.statusBar().showMessage('Mod not found')

    def Edit_Mods(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        mod_title = self.lineEdit_13.text()
        mod_game = self.comboBox_9.currentText()
        mod_category = self.comboBox_10.currentText()
        mod_creator = self.comboBox_11.currentText()
        mod_link = self.lineEdit_12.text()
        mod_version = self.lineEdit_11.text()
        mod_discription = self.lineEdit_15.text()

        search_mod = self.lineEdit_28.text()

        self.cur.execute('''
            UPDATE Mods 
            SET mod_title = ?, mod_game = ?, mod_category = ?, mod_discription = ?, mod_version = ?, mod_link = ?, mod_creator = ?
            WHERE mod_title = ?
        ''', (mod_title, mod_game, mod_category, mod_discription, mod_version, mod_link, mod_creator, search_mod))

        self.db.commit()
        self.statusBar().showMessage('Successfully updated')

        self.lineEdit_13.setText('')
        self.comboBox_9.setCurrentText('')
        self.comboBox_10.setCurrentText('')
        self.comboBox_11.setCurrentText('')
        self.lineEdit_12.setText('')
        self.lineEdit_11.setText('')
        self.lineEdit_15.setText('')
        self.lineEdit_28.setText('')

        self.Show_All_Mods()

    def Delete_Mod(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        search_mod = self.lineEdit_28.text()


        warning = QMessageBox.warning(self , 'Delete Mod', "Are you sure you want to delete this mod" , QMessageBox.Yes | QMessageBox.No)

        if warning == QMessageBox.Yes:
            sql =  '''DELETE FROM Mods WHERE mod_title = ? '''
            self.cur.execute(sql, [(search_mod)])
            self.db.commit()
            self.statusBar().showMessage('Mod Deleted')

            self.Show_All_Mods()


    def Add_Category(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        category_name = self.lineEdit_4.text()

        self.cur.execute('''
        INSERT INTO Categories (category_name) VALUES (?)
        ''', (category_name,))

        self.db.commit()
        self.statusBar().showMessage('New Category Added')
        self.lineEdit_4.setText('')
        self.Show_Category()
        self.Show_Category_Combobox()  # обновление комбобокса


    def Delete_Category(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        games = self.lineEdit_17.text()

        self.cur.execute('SELECT * FROM Categories WHERE category_name = ?', (games,))
        row = self.cur.fetchone()

        if row:
            self.cur.execute('DELETE FROM Categories WHERE category_name = ?', (games,))
            self.db.commit()
            self.statusBar().showMessage('Category Deleted')
            self.lineEdit_17.setText('')
            self.Show_Category()
            self.Show_Category_Combobox()
        else:
            self.statusBar().showMessage('Category not found')

    def Show_Category(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        self.cur.execute('SELECT category_name FROM Categories')
        data = self.cur.fetchall()

        self.tableWidget_3.setRowCount(0)
        if data:
            for row, form in enumerate(data):
                self.tableWidget_3.insertRow(row)
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))

    def Add_Creator(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        creator_name = self.lineEdit_5.text()

        self.cur.execute('''
        INSERT INTO Creator (creator_name) VALUES (?)
        ''', (creator_name,))

        self.db.commit()
        self.statusBar().showMessage('New Creator Added')
        self.lineEdit_5.setText('')
        self.Show_Creator()
        self.Show_Creator_Combobox()


    def Delete_Creator(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        games = self.lineEdit_18.text()

        self.cur.execute('SELECT * FROM Creator WHERE creator_name = ?', (games,))
        row = self.cur.fetchone()

        if row:
            self.cur.execute('DELETE FROM Creator WHERE creator_name = ?', (games,))
            self.db.commit()
            self.statusBar().showMessage('Creator Deleted')
            self.lineEdit_18.setText('')
            self.Show_Creator()
            self.Show_Creator_Combobox()
        else:
            self.statusBar().showMessage('Creator not found')


    def Show_Creator(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        self.cur.execute('SELECT creator_name FROM Creator')
        data = self.cur.fetchall()

        self.tableWidget_4.setRowCount(0)
        if data:
            for row, form in enumerate(data):
                self.tableWidget_4.insertRow(row)
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))

    def Add_Games(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        games_name = self.lineEdit_2.text()

        self.cur.execute('''
        INSERT INTO Games (games_name) VALUES (?)
        ''', (games_name,))

        self.db.commit()
        self.statusBar().showMessage('New Game Added')
        self.lineEdit_2.setText('')
        self.Show_Games()
        self.Show_Games_Combobox()

    def Delete_Games(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        games = self.lineEdit_16.text()

        # Используем параметризованный запрос для поиска и удаления игры
        self.cur.execute('SELECT * FROM Games WHERE games_name = ?', (games,))
        row = self.cur.fetchone()

        if row:
            self.cur.execute('DELETE FROM Games WHERE games_name = ?', (games,))
            self.db.commit()
            self.statusBar().showMessage('Game Deleted')
            self.lineEdit_16.setText('')
            self.Show_Games()
            self.Show_Games_Combobox()
        else:
            self.statusBar().showMessage('Game not found')


    def Show_Games(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        self.cur.execute('SELECT games_name FROM Games')
        data = self.cur.fetchall()

        self.tableWidget_2.setRowCount(0)
        if data:
            for row, form in enumerate(data):
                self.tableWidget_2.insertRow(row)
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))

    #Setting data
    def Show_Category_Combobox(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        self.cur.execute(''' 
        SELECT category_name FROM Categories
        ''')
        data = self.cur.fetchall()

        for Categories in data:
            self.comboBox_4.addItem(Categories[0])
            self.comboBox_10.addItem(Categories[0])


    def Show_Creator_Combobox(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        self.cur.execute(''' 
        SELECT creator_name FROM Creator
        ''')
        data = self.cur.fetchall()

        for Creator in data:
            self.comboBox_5.addItem(Creator[0])
            self.comboBox_11.addItem(Creator[0])

    def Show_Games_Combobox(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        self.cur.execute(''' 
        SELECT games_name FROM Games
        ''')
        data = self.cur.fetchall()

        for Games in data:
            self.comboBox_2.addItem(Games[0])
            self.comboBox_9.addItem(Games[0])


    def Login(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        name = self.lineEdit_8.text()
        password = self.lineEdit_9.text()


        sql = '''SELECT * FROM Users'''

        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if name == row[1] and password == row[2]:
                self.statusBar().showMessage('Valid Username and Password')
                self.groupBox_3.setEnabled(True)
                self.pushButton_18.setEnabled(True)

                self.lineEdit_22.setText(row[1])
        else:
            self.statusBar().showMessage('The data was entered incorrectly')

    def Edit_Login(self):

        name = self.lineEdit_22.text()
        password = self.lineEdit_23.text()
        password2 = self.lineEdit_24.text()


        if password == password2:
            self.db = sqlite3.connect(self.db_path)
            self.cur = self.db.cursor()


            self.cur.execute('''
            UPDATE Users set name = ?, password = ?
            ''', (name, password))

            self.db.commit()
            self.statusBar().showMessage('User Data Updated')

        else:
            self.statusBar().showMessage('Passwords must match')


    def Export_Daybook(self):
        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()

        self.cur.execute('''
        SELECT mod_title, game_title, release_time, degree_time FROM Daybook 
        ''')

        data = self.cur.fetchall()
        wb = Workbook('Notebook.xlsx')
        sheet1 = wb.add_worksheet()

        sheet1.write(0,0,'Mod Title')
        sheet1.write(0, 1, 'Game Title')
        sheet1.write(0, 2, 'Relese Date')
        sheet1.write(0, 3, 'Actualy')

        row_number = 1
        for row in data :
            column_number = 0
            for item in row :
                sheet1.write(row_number , column_number , str(item))
                column_number += 1
            row_number += 1

        wb.close()
        self.statusBar().showMessage('Report Created Successfully')

    def Export_Mods(self):

        self.db = sqlite3.connect(self.db_path)
        self.cur = self.db.cursor()


        self.cur.execute(
            ''' SELECT mod_title, mod_game, mod_category, mod_creator, mod_link, mod_version,mod_discription FROM Mods'''
        )

        data = self.cur.fetchall()
        wb = Workbook('Mods.xlsx')
        sheet1 = wb.add_worksheet()

        sheet1.write(0, 0, 'Mod Title')
        sheet1.write(0, 1, 'Game')
        sheet1.write(0, 2, 'Category')
        sheet1.write(0, 3, 'Discription')
        sheet1.write(0, 4, 'Actual version')
        sheet1.write(0, 5, 'Link')
        sheet1.write(0, 6, 'Creator')


        row_number = 1
        for row in data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1

        wb.close()
        self.statusBar().showMessage('Report Created Successfully')

def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
