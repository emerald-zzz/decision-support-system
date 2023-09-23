# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 19:10:43 2023

@author: ASUS
"""
import sqlite3
from PyQt5.QtWidgets import  QMainWindow, QFileDialog
from PyQt5.QtGui import QImage
import io
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QByteArray, QBuffer, QIODevice
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sys
import os
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
class admin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path('admin.ui'), self)
        self.pushButton.clicked.connect(self.selectImage)
        self.pushButton_2.clicked.connect(self.saveToDatabase)
# Initialize your database connection
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(resource_path("spdb.db"))  # Replace with the actual database file name
        if not self.db.open():
          print("Failed to connect to the database.")
          sys.exit(1)

    def selectImage(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select Image")
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.gif)")
       # file_dialog.fileSelected.connect(self.displayImage)

        if file_dialog.exec_():
            self.selected_file = file_dialog.selectedFiles()[0]
          
    def saveToDatabase(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        if not username or not password:
            print("Please enter both username and password.")
            return

        # Set a default image if no image is selected
        if not hasattr(self, 'selected_file'):
            default_image_path = resource_path("C:\\Users\\ASUS\\Desktop\\pipelineapp\\icons8-username-96.png" ) # Replace with the path to your default image
            self.selected_file = default_image_path

        # Check if the username already exists in the database
        query = QSqlQuery()
        query.prepare("SELECT username FROM users WHERE username = ?")
        query.addBindValue(username)
        if query.exec_() and query.next():
            self.label_3.setText("*Username already exists. Please try another one.")
            return

        # Convert the image to a Blob
        image = QImage(self.selected_file)
        blob = sqlite3.Binary(self.imageToBlob(image))

        # Implement your logic to save the data to the database
        # Here, you can use your database connection and execute the necessary SQL statements

        # Example code to insert username, password, and image into a table named 'users'
        
        query = QSqlQuery()
        query.prepare("INSERT INTO users (username, password, image) VALUES (?, ?, ?)")
        query.addBindValue(username)
        query.addBindValue(password)
        query.addBindValue(blob)

        if query.exec_():
            print("Data saved to the database.")
            self.label_3.setText("")
        else:
            print("Error inserting data:", query.lastError().text())

        self.db.close()
    def imageToBlob(self, image):
        # Convert the QImage to a bytes object
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        image.save(buffer, "PNG")

        return byte_array.data()

    
  
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = admin()
    window.show()
    app.exec_()
