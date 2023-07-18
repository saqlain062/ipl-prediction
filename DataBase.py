#database
import mysql.connector
# from PyQt6.QtCore import QRegExp
# from PyQt6.QtGui import QRegExpValidator
# import re
# from PyQt6.QtCore import QRegularExpression
from PyQt6.QtWidgets import (QLabel, QApplication,QSpinBox, QWidget, QLineEdit, QPushButton, QFormLayout,
                             QTableWidget,QTableWidgetItem,QMessageBox)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123@",
            database="ipl"
        )
        self.win()
        self.table = None
    def win(self):

        self.setWindowTitle("Standings Data")
        self.TeamName = QLineEdit()

        # self.regex = QRegExp("[a-zA-Z]+")
        self.TeamName.setPlaceholderText("Name")
        # validator = QRegularExpressionValidator(QRegularExpression('[a-zA-Z]*'), self.TeamName)
        # self.TeamName.setValidator(validator)
        self.WinMatch = QSpinBox(minimum=0, maximum=10)
        self.LossMatch = QSpinBox(minimum=0, maximum=10)
        self.drawMatch = QSpinBox(minimum=0, maximum=10)

        self.insert_button = QPushButton("Insert")
        self.show_button = QPushButton("Show")
        self.insert_button.clicked.connect(self.insert_data)
        self.show_button.clicked.connect(self.show_data)
        self.delete_button = QPushButton("Delete Data")
        self.delete_button.clicked.connect(self.delete_data)
        self.update_button = QPushButton("Update Data")
        self.update_button.clicked.connect(self.update_data)
        layout = QFormLayout()
        layout.addRow("Team Name",self.TeamName)
        layout.addRow("Win",self.WinMatch)
        layout.addRow("Lose",self.LossMatch)
        layout.addRow("Total Match",self.drawMatch)
        # layout.addWidget(self.TeamName)
        # layout.addWidget(self.WinMatch)
        # layout.addWidget(self.LossMatch)
        # layout.addWidget(self.drawMatch)
        layout.addWidget(self.insert_button)
        layout.addWidget(self.show_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.update_button)
        self.errLabel = QLabel('')
        layout.addWidget(self.errLabel)
        self.setLayout(layout)
        
    def insert_data(self):
        cursor = self.db_connection.cursor()
        TeamName = str(self.TeamName.text())
        # For validation
        if len(TeamName) == 0:
            self.errLabel.setText('Enter all fields!')
            return
        elif TeamName.isdigit():
            self.errLabel.setText('Enter valid Characters')
            return
        for x in TeamName:
            if x.isdigit():
                self.errLabel.setText('Enter valid Characters')
                return
   
        WinMatch = (self.WinMatch.text())
        lossmatch = (self.LossMatch.text())
        drawmatch = (self.drawMatch.text())
        query = "INSERT INTO standings ( TeamName, Win, Lose, TotalMatch) VALUES (%s, %s,%s, %s)"
        values = (TeamName, WinMatch,lossmatch,drawmatch)
        cursor.execute(query, values)
        self.db_connection.commit()
        cursor.close()
        self.TeamName.clear()
        self.WinMatch.clear()
        self.LossMatch.clear()
        self.drawMatch.clear()

    def show_data(self):
        cursor = self.db_connection.cursor()
        query = "SELECT * FROM standings"
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        cursor.close()
        num_rows = len(data)
        num_columns = len(data[0])
        self.table = QTableWidget(num_rows, num_columns)
        self.table.setHorizontalHeaderLabels(["Team Name", "Win Match", "Lose Match","Total Match"])
        for i in range(num_rows):
            for j in range(num_columns):
                self.table.setItem(i, j, QTableWidgetItem(str(data[i][j])))
        self.table.setWindowTitle("Standings Data")
        self.table.resize(400, 300)
        self.table.show()

    def delete_data(self):
        cursor = self.db_connection.cursor()
        TeamName = str(self.TeamName.text())
        query = "DELETE FROM standings WHERE TeamName = %s"
        values = (TeamName,)
        cursor.execute(query, values)
        self.db_connection.commit()
        if cursor.rowcount == 0:
            msg = QMessageBox()
            msg.setWindowTitle("Delete Data")
            msg.setText("No data found to delete!")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Delete Data")
            msg.setText(f"{cursor.rowcount} row(s) deleted successfully!")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
        cursor.close()

    def update_data(self):
        cursor = self.db_connection.cursor()
        TeamName = str(self.TeamName.text())
        WinMatch = (self.WinMatch.text())
        lossmatch = (self.LossMatch.text())
        drawmatch = (self.drawMatch.text())

        query = "UPDATE standings SET Win = %s, Lose = %s, TotalMatch = %s WHERE TeamName = %s"
        values = (TeamName, WinMatch,lossmatch,drawmatch)
        cursor.execute(query, values)
        self.db_connection.commit()
        if cursor.rowcount == 0:
            msg = QMessageBox()
            msg.setWindowTitle("Update Data")
            msg.setText("No data found to Update!")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Updata Data")
            msg.setText(f"{cursor.rowcount} row(s) updated successfully!")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
        cursor.close()
        self.TeamName.clear()
        self.WinMatch.clear()
        self.LossMatch.clear()
        self.drawMatch.clear()
        

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
