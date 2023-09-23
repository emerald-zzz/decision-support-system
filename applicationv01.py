# -*- coding: utf-8 -*-
"""
Created on Tue May  2 09:13:52 2023

@author: ASUS
"""
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
from PyQt5 import QtWidgets, uic, QtCore, QtGui
import pandas as pd
from PyQt5.QtWidgets import  QTableWidget, QTableWidgetItem,QStyle
from PyQt5.QtCore import QSize
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QFrame
from PyQt5.QtWidgets import QMessageBox
import folium
from folium.plugins import MarkerCluster
from folium import plugins
from folium.plugins import MiniMap
from folium.raster_layers  import TileLayer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtGui import QIcon ,QPixmap, QRegion
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator ,QBrush ,QColor
import csv
from datetime import datetime
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMenu, QAction
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sys
import sqlite3
from sklearn.preprocessing import OneHotEncoder
import pickle
from PyQt5.QtWidgets import  QMainWindow, QFileDialog
from PyQt5.QtGui import QImage
import io
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QByteArray, QBuffer, QIODevice
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery,QSqlQueryModel
from apscheduler.schedulers.background import BackgroundScheduler
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import threading
import random 
import sys
import numpy as np
from smtp import Mission
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtWidgets import QCompleter
from matplotlib.ticker import MaxNLocator
from matplotlib.colors import LinearSegmentedColormap
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
        self.pushButton_3.clicked.connect(self.login)
     # Initialize your database connection
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(resource_path("spdb.db"))  # Replace with the actual database file name
        if not self.db.open():
            print("Failed to connect to the database.")
            sys.exit(1)

        # Connect button signals to slots
        self.pushButton.clicked.connect(self.selectImage)
        self.pushButton_2.clicked.connect(self.saveToDatabase)
        
        #styling the tabel
        self.tableWidget.setStyleSheet('''
    QTableWidget {
        background-color: rgb(19, 51, 76);
        border: 1px solid rgb(19, 51, 76);
        color: rgb(246, 246, 233);
    }
    
    QTableWidget::item {
        padding: 5px;
        border: 1px solid  rgb(253, 95, 0) ;
    }
    
    QHeaderView::section {
        background-color:  rgb(253, 95, 0);
        font-weight: bold;
        border: 1px solid  rgb(253, 95, 0);
        color:rgb(0, 87, 146);
    }
''')
       #styling the scroll bar
        self.tableWidget.verticalScrollBar().setStyleSheet('''
    QScrollBar:vertical {
        background: transparent;
        width: 5px;
        border-radius: 7px;
        margin: 20px 0 20px 0;
    }

    QScrollBar::handle:vertical {
        background: rgb(19, 51, 76);
        border-radius: 7px;
        min-height: 20px;
    }

    QScrollBar::add-line:vertical {
        border: none;
        background: none;
    }

    QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
''')
       #styling the scroll bar
        self.tableWidget.horizontalScrollBar().setStyleSheet('''
    QScrollBar:horizontal {
        background: transparent;
        width: 5px;
        border-radius: 7px;
        margin: 20px 0 20px 0;
    }

    QScrollBar::handle:horizontal {
        background: rgb(19, 51, 76);
        border-radius: 7px;
        min-height: 20px;
    }

    QScrollBar::add-line:horizontal {
        border: none;
        background: none;
    }

    QScrollBar::sub-line:horizontal {
        border: none;
        background: none;
    }

    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
        background: none;
    }
''')   
        # Connect to the database
        conn = sqlite3.connect(resource_path("spdb.db"))  # Replace with the actual database file name
        cursor = conn.cursor()
        
 # Retrieve data from the database table
        cursor.execute("SELECT username,password FROM users")
        data = cursor.fetchall()

 # Set the number of rows and columns in the table
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]) + 1)  # Add 1 for the delete button column
  # Assuming all rows have the same number of columns

 # Add data to the table
        for i, row in enumerate(data):
             for j, value in enumerate(row):
                 item = QTableWidgetItem(str(value))
                 self.tableWidget.setItem(i, j, item)
              # Add a delete button to the last column
             delete_button = QPushButton("")
             delete_button.setIcon(QIcon(resource_path('icons\\icons8-trash-52.png')))
             delete_button.setStyleSheet(''' QPushButton { background-color: rgb(253, 95, 0);
                                       font: 900 8pt  Arial Black;
                                     color:rgb(0, 87, 146);
                                    border:  1px solid rgb(237, 131, 0);
                                    border-radius:25%;
                                    }
                                    QPushButton:hover {
                                        background-color:qlineargradient(spread:repeat, x1:0, y1:1, x2:1, y2:0, stop:0.28436 rgba(253, 95, 0, 255), stop:0.890995 rgba(255, 193, 35, 255));
                                        border:  1px solid gray;
                                        box-shadow: 5px 10px rgb(255, 175, 15);
                                   }''')
             delete_button.clicked.connect(lambda _, row=i: self.deleteRow(row))  # Connect the delete button to the deleteRow method
             self.tableWidget.setCellWidget(i, len(row), delete_button)       
             self.tableWidget.setColumnWidth(0, 100)
             self.tableWidget.setColumnWidth(1, 100)
             self.tableWidget.setColumnWidth(2, 50)
             header_label = QTableWidgetItem("")
             self.tableWidget.setHorizontalHeaderItem(2, header_label)
 # Set table properties
        header_labels = [description[0] for description in cursor.description]
        self.tableWidget.setHorizontalHeaderLabels(header_labels)
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableWidget.verticalHeader().setVisible(False)

 # Close the database connection
        conn.close()
      
    def deleteRow(self, row):
    # Get the item in the first column (assumed to be the primary key)
        item = self.tableWidget.item(row, 0)
        username = item.text() # Assuming the primary key is an integer

    # Delete the row from the table
        self.tableWidget.removeRow(row)

    # Delete the row from the database
        conn = sqlite3.connect(resource_path("spdb.db") ) # Replace with the actual database file name
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        conn.close()
    def login(self):
        self.window1=Window1()
        self.hide()
        self.window1.show()
    def selectImage(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select Image")
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.gif)")

        try:
            if file_dialog.exec_():
                self.selected_file = file_dialog.selectedFiles()[0]
        except KeyboardInterrupt:
            print("Program execution interrupted.")
            sys.exit(0)  # Exit the program gracefully
    def saveToDatabase(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        email = self.lineEdit_3.text()
        role = self.comboBox.currentText()
        if not username or not password:
            print("Please enter both username and password.")
            self.label_3.setText("*Please enter both username and password.")
            return

        # Set a default image if no image is selected
        if not hasattr(self, 'selected_file'):
            default_image_path =resource_path( "icons8-username-96.png" ) # Replace with the path to your default image
            self.selected_file = default_image_path

        # Check if the username already exists in the database
        query = QSqlQuery()
        query.prepare("SELECT username FROM users WHERE username = ?")
        query.addBindValue(username)
        if query.exec_() and query.next():
            self.label_3.setText("*Username already exists. Please try another one.")
            return

        # Convert the image to binary data
        image = QImage(self.selected_file)
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        image.save(buffer, "PNG")

        # Implement your logic to save the data to the database
        # Here, you can use your database connection and execute the necessary SQL statements

        # Example code to insert username, password, email, role, and image into a table named 'users'
        query.prepare("INSERT INTO users (username, password, email, role, image) VALUES (?, ?, ?, ?, ?)")
        query.addBindValue(username)
        query.addBindValue(password)
        query.addBindValue(email)
        query.addBindValue(role)
        query.addBindValue(byte_array)

        if query.exec_():
            print("Data saved to the database.")
            self.label_3.setText("")
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.db.close()

     # Connect button signals to slots
        self.pushButton.clicked.connect(self.selectImage)
        self.pushButton_2.clicked.connect(self.saveToDatabase)
        
        #styling the tabel
        self.tableWidget.setStyleSheet('''
    QTableWidget {
        background-color: rgb(19, 51, 76);
        border: 1px solid rgb(19, 51, 76);
        color: rgb(246, 246, 233);
    }
    
    QTableWidget::item {
        padding: 5px;
        border: 1px solid  rgb(253, 95, 0) ;
    }
    
    QHeaderView::section {
        background-color:  rgb(253, 95, 0);
        font-weight: bold;
        border: 1px solid  rgb(253, 95, 0);
        color:rgb(0, 87, 146);
    }
''')   
       #styling the scroll bar
        self.tableWidget.verticalScrollBar().setStyleSheet('''
    QScrollBar:vertical {
        background: transparent;
        width: 5px;
        border-radius: 7px;
        margin: 20px 0 20px 0;
    }

    QScrollBar::handle:vertical {
        background: rgb(19, 51, 76);
        border-radius: 7px;
        min-height: 20px;
    }

    QScrollBar::add-line:vertical {
        border: none;
        background: none;
    }

    QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
''')
       #styling the scroll bar
        self.tableWidget.horizontalScrollBar().setStyleSheet('''
    QScrollBar:horizontal {
        background: transparent;
        width: 5px;
        border-radius: 7px;
        margin: 20px 0 20px 0;
    }

    QScrollBar::handle:horizontal {
        background: rgb(19, 51, 76);
        border-radius: 7px;
        min-height: 20px;
    }

    QScrollBar::add-line:horizontal {
        border: none;
        background: none;
    }

    QScrollBar::sub-line:horizontal {
        border: none;
        background: none;
    }

    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
        background: none;
    }
''')   

      
        # Connect to the database
        conn = sqlite3.connect(resource_path("spdb.db")) # Replace with the actual database file name
        cursor = conn.cursor()
        
 # Retrieve data from the database table
        cursor.execute("SELECT username,password FROM users")
        data = cursor.fetchall()

 # Set the number of rows and columns in the table
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]) + 1)  # Add 1 for the delete button column
  # Assuming all rows have the same number of columns

 # Add data to the table
        for i, row in enumerate(data):
             for j, value in enumerate(row):
                 item = QTableWidgetItem(str(value))
                 self.tableWidget.setItem(i, j, item)
              # Add a delete button to the last column
             delete_button = QPushButton("")
             delete_button.setIcon(QIcon(resource_path("icons\\icons8-trash-52.png")))
             delete_button.setStyleSheet(''' QPushButton { background-color: rgb(253, 95, 0);
                                       font: 900 8pt  Arial Black;
                                     color:rgb(0, 87, 146);
                                    border:  1px solid rgb(237, 131, 0);
                                    border-radius:25%;
                                    }
                                    QPushButton:hover {
                                        background-color:qlineargradient(spread:repeat, x1:0, y1:1, x2:1, y2:0, stop:0.28436 rgba(253, 95, 0, 255), stop:0.890995 rgba(255, 193, 35, 255));
                                        border:  1px solid gray;
                                        box-shadow: 5px 10px rgb(255, 175, 15);
                                   }''')
             delete_button.clicked.connect(lambda _, row=i: self.deleteRow(row))  # Connect the delete button to the deleteRow method
             self.tableWidget.setCellWidget(i, len(row), delete_button)       
             self.tableWidget.setColumnWidth(0, 100)
             self.tableWidget.setColumnWidth(1, 100)
             self.tableWidget.setColumnWidth(2, 50)
             header_label = QTableWidgetItem("")
             self.tableWidget.setHorizontalHeaderItem(2, header_label)
 # Set table properties
        header_labels = [description[0] for description in cursor.description]
        self.tableWidget.setHorizontalHeaderLabels(header_labels)
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableWidget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableWidget.verticalHeader().setVisible(False)

 # Close the database connection
        conn.close()
      

class Window1(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path('login.ui'), self)
        self.pushButton.clicked.connect(self.show_main)
        self.pushButton_2.clicked.connect(self.show_admin)
    
    def show_main(self):
    # Get the username and password from the input fields
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
    
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(resource_path("spdb.db"))  # Replace with the actual database file name

        if not db.open():
            print("Failed to connect to the database.")
            sys.exit(1)

    # Query the database for the username and password
        query = QSqlQuery()
        query.prepare("SELECT * FROM users WHERE username = :username AND password = :password")
        query.bindValue(":username", username)
        query.bindValue(":password", password)

        if query.exec_() and query.next():
            id_user = query.value(0)
            role = query.value(5)  # Assuming the role column is at index 4 in the query result

            if role == "department head":
                msg_box = QMessageBox()
                msg_box.setStyleSheet(
    "QMessageBox { background-color: #F6F6E9; }"
    "QMessageBox QLabel { color: #13334C; }"
    "QMessageBox QPushButton {"
    "   background-color: #005792;"
    "   color: #F6F6E9;"
    "   padding: 5px 10px;"
    "   border: none;"
    "}"
    "QMessageBox QPushButton:hover { background-color: #FD5F00; }"
)
                msg_box.setWindowTitle("Department Head Role Selection")
                msg_box.setIcon(QMessageBox.Information) 
                msg_box.setText("Choose an option:")
                msg_box.addButton("Plan Missions", QMessageBox.AcceptRole)
                msg_box.addButton("Log Normally", QMessageBox.RejectRole)
                choice = msg_box.exec_()
            
                if choice == QMessageBox.AcceptRole:
                # Open the plan missions window or perform any other action
                    self.planmession=Mission()
                    self.hide()
                    self.planmession.show()
                else:
                    self.show_mainwi(username, id_user, db)

            else:
                self.show_mainwi(username, id_user, db)

        else:
            print("Login failed")
            self.label_4.setText("Incorrect username or password.")

        db.commit()
        db.close()

    def show_mainwi(self,username, id_user, db):
    # Query the database for the image_data
        image_query = QSqlQuery()
        image_query.prepare("SELECT image FROM users WHERE username = ?")
        image_query.addBindValue(username)

        if image_query.exec_() and image_query.next():
            image_blob = image_query.value(0)

            if image_blob is not None:
                pixmap = QPixmap()
                pixmap.loadFromData(image_blob)

            # Assuming you have the original pixmap stored in 'pixmap'
                scaled_pixmap = pixmap.scaled(40, 40, aspectRatioMode=Qt.KeepAspectRatio,
                                          transformMode=Qt.SmoothTransformation)


        self.mainwi = mainwi()
        self.hide()
        self.mainwi.show()

        # Apply rounded border radius to the label
        mask = QRegion(self.mainwi.label_19.rect(), QRegion.Ellipse)
        self.mainwi.label_19.setMask(mask)
        self.mainwi.label_19.setStyleSheet("border-radius: 20%;")
        self.mainwi.label_19.setPixmap(scaled_pixmap)
        self.mainwi.toolButton.setText(username)
        self.mainwi.label_19.setGeometry(self.mainwi.frame.width() - 50, 10, 40, 40)
        self.mainwi.toolButton.setGeometry(self.mainwi.frame.width() - 110, 10, 100, 40)
        self.mainwi.listWidget.clear()

        # Retrieve ongoing missions for the current user
        msquery = QSqlQuery()
        msquery.prepare("SELECT * FROM messions WHERE assigned_to = ? AND state = 'ongoing'")
        msquery.addBindValue(id_user)
        msquery.exec_()

        while msquery.next():
            mission_id = msquery.value(0)
            description = msquery.value(1)
            end_date = msquery.value(3)
            end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
            remaining_time = end_date - datetime.now()

            if remaining_time.days > 365:
                remaining_text = f"{remaining_time.days // 365} years"
            elif remaining_time.days > 30:
                remaining_text = f"{remaining_time.days // 30} months"
            elif remaining_time.days > 0:
                remaining_text = f"{remaining_time.days} days"
            elif remaining_time.seconds > 3600:
                remaining_text = f"{remaining_time.seconds // 3600} hours"
            else:
                remaining_text = f"{remaining_time.seconds // 60} minutes"
            # Create a list item and make it checkable
            item = QtWidgets.QListWidgetItem(f"{description} (Remaining Time: {remaining_text})")
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)  # Initial state is unchecked
            item.setData(Qt.UserRole, mission_id)
# Add the item to the list
            self.mainwi.listWidget.addItem(item)

# Connect the item's state change to the update_mission_state function
            self.mainwi.listWidget.itemChanged.connect(self.update_mission_state)

# Retrieve upcoming missions for the current user
        upcoming_msquery = QSqlQuery()
        upcoming_msquery.prepare("SELECT * FROM messions WHERE assigned_to = ? AND state = 'pending'")
        upcoming_msquery.addBindValue(id_user)
        upcoming_msquery.exec_()

        while upcoming_msquery.next():
            mission_id = upcoming_msquery.value(0)
            description = upcoming_msquery.value(1)
            start_date = upcoming_msquery.value(2)
            start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            remaining_time = start_date - datetime.now()

            if remaining_time.days > 365:
                remaining_text = f"{remaining_time.days // 365} years"
            elif remaining_time.days > 30:
                remaining_text = f"{remaining_time.days // 30} months"
            elif remaining_time.days > 0:
                remaining_text = f"{remaining_time.days} days"
            elif remaining_time.seconds > 3600:
                remaining_text = f"{remaining_time.seconds // 3600} hours"
            else:
                remaining_text = f"{remaining_time.seconds // 60} minutes"
            
            item = QtWidgets.QListWidgetItem(f"{description} (Starts in: {remaining_text})")
            item.setData(Qt.UserRole, mission_id)
            item.setSizeHint(item.sizeHint())  # Adjust the size of the item
            
            self.mainwi.listWidget_2.addItem(item)


        db.commit()
        db.close()

   
    def update_mission_state(self, item):
        clicked_item = self.mainwi.listWidget.item(self.mainwi.listWidget.row(item))
        mession_id = clicked_item.data(Qt.UserRole)

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(resource_path("spdb.db"))  # Replace with the actual database file name

        try:
            if not db.open():
                print("Failed to connect to the database.")
                return

            update_query = QSqlQuery()
            update_query.prepare("UPDATE messions SET state = CASE WHEN end_date <= :current_date THEN 'completed' ELSE 'done late' END, end_date = :current_date WHERE mession_id = :mession_id")
            update_query.bindValue(":current_date", QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss"))
            update_query.bindValue(":mession_id", mession_id)

            if not update_query.exec_():
                print("Error while updating the database:", update_query.lastError().text())
            else:
            # Commit the transaction and remove the checked item from the list widget
                db.commit()
                self.mainwi.listWidget.takeItem(self.mainwi.listWidget.row(item))

        except Exception as e:
            print("An error occurred:", str(e))
        finally:
            db.close()  # Close the database connection


    def show_admin(self):
               # Get the username and password from the input fields
           username = self.lineEdit.text()
           password = self.lineEdit_2.text()
           db = QSqlDatabase.addDatabase("QSQLITE")
           db.setDatabaseName(resource_path("spdb.db")) # Replace with the actual database file name
           if not db.open():
             print("Failed to connect to the database.")
             sys.exit(1)

          # Query the database for the username and password
           query = QSqlQuery()
           query.prepare("SELECT * FROM admin WHERE username = :username AND password = :password")
           query.bindValue(":username", username)
           query.bindValue(":password", password)
           if query.exec_() and query.next():
              print("Login successful")
              self.admin=admin()
              self.hide()
              self.admin.show()
              db.close()
           else:
              print("Login failed")
              self.label_4.setText("Incorrect username or password.")
               
       
           
class mainwi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path('mainwindow.ui'), self)
        self.stackedWidget.setCurrentIndex(4)
        self.pushButton_2.clicked.connect(self.show_tab_2)
        self.pushButton.clicked.connect(self.show_tab_1)
        self.pushButton_4.clicked.connect(self.show_tab_3)
        self.pushButton_5.clicked.connect(self.show_tab_4)
        self.pushButton_6.clicked.connect(self.show_tab_5)
        self.radioButton.clicked.connect(self.plot_histogram)
        self.radioButton_2.clicked.connect(self.plot_histogram)
        self.radioButton_3.clicked.connect(self.plot_histogram)
        self.radioButton_4.clicked.connect(self.plot_histogram)
        self.canvas = None 
        self.scheduler = BackgroundScheduler()
        

# Schedule the job to run every minute (adjust as needed)
        self.scheduler.add_job(self.update_mission_states, 'interval', minutes=1)

# Start the scheduler


        self.scheduler.start()
        # Create a layout for the main widget
        self.layout = QVBoxLayout(self.stackedWidget.widget(3))

               # Create the map widget
        self.map_widget = QWebEngineView()
        
        # Load the map URL (OpenStreetMap example)
        self.map_widget.load(QUrl("https://www.openstreetmap.org/export/embed.html?bbox=-74.1,40.7,-73.9,40.8&layer=mapnik"))
        # creating the map object
        us_center = [39.8283, -98.5795]
        self.m = folium.Map(location=us_center, zoom_start=4,no_wrap=True)
        satellite_layer = TileLayer(
        tiles='https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.jpg?access_token=pk.eyJ1Ijoic2FyYXJhcmFyYXJhcmFyIiwiYSI6ImNsaHBmOGdyZDFxa2Uzcm9kdXRmZDR2NGMifQ.GjNfyd5TbRpFKZK5NvJAOA',
    attr='Map data &copy; <a href="https://www.mapbox.com/">Mapbox</a>',
    name='Satellite',
    overlay=True,
    control=True,
    nowrap=True
 
)   
        
        # with open("us-states.json", "r") as f:
        #     geojson_data = f.read()
            
          
        # folium.GeoJson(geojson_data, name="US States").add_to(self.m)  
            
        # Create a minimap and add it to the main map
        minimap = MiniMap()
        self.m.add_child(minimap)
            # Add the map widget to the layout
            
        self.layout.addWidget(self.map_widget)
    
            # Create a custom HTML element for the title
        title_html = """
        <h3 style="position: absolute;
                   top: 5px;
                   left: 50%;
                   transform: translateX(-50%);
                   z-index: 1000;
                   background-color: rgba(255, 255, 255, 0.5);
                   padding: 10px;
                   font: 900 11pt  Arial Black;
                   border: 1px solid rgb(19, 51, 76);
                   border-radius:25px;
                   color:rgb(0, 87, 146);
                   white-space: nowrap">
            Geographical Localization of Incidents
        </h3>
    """

    # Inject the custom HTML element into the output HTML file
        self.m.get_root().html.add_child(folium.Element(title_html))

       
        conn = sqlite3.connect(resource_path('spdb.db'))
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Incidents")
        rows = cursor.fetchall()
        marker_cluster = MarkerCluster(name='Markers').add_to(self.m)
        marker_data = []
    # icon = folium.features.CustomIcon('marker.svg', icon_size=(100, 100))


        for row in rows:
         
            ReportNumber = row[0]
            AccidentDateTime = row[1]
            OperatorID = row[2]
            PipelineFacilityName = row[3]
            PipelineType = row[4]
            LiquidType = row[5]
            AccidentState = row[6]
            AccidentLatitude = row[7]
            AccidentLongitude = row[8]
            CauseCategory = row[9]
            CauseSubcategory = row[10]
            UnintentionalRelease = row[11]
            LiquidIgnition = row[12]
            LiquidExplosion = row[13]
            PipelineShutdown = row[14]
            popup = f"Report Number: {ReportNumber}<br> Accident Date/Time: {AccidentDateTime}<br> Operator ID: {OperatorID}<br> Pipeline/Facility Name: {PipelineFacilityName}<br> Pipeline Type: {PipelineType}<br> Liquid Type: {LiquidType}<br> Accident State: {AccidentState}<br> Accident Latitude: {AccidentLatitude}<br> Accident Longitude: {AccidentLongitude}<br> Cause Category: {CauseCategory}<br> Cause Subcategory: {CauseSubcategory}<br> Unintentional Release (Barrels): {UnintentionalRelease}<br> Liquid Ignition: {LiquidIgnition}<br> Liquid Explosion: {LiquidExplosion}<br> Pipeline Shutdown: {PipelineShutdown}"
            marker = folium.Marker(location=[AccidentLatitude, AccidentLongitude],tooltip="click to see more info", popup=popup,icon=folium.Icon(icon='glyphicon-wrench', color='blue', icon_color='white', icon_size=(40, 40))
)
            marker_data.append(marker)
                
           # Add all markers to the map
        for marker in marker_data:
               marker.add_to(self.m)
               marker_cluster.add_child(marker)


            # Save the map to an HTML file
        satellite_layer.add_to(self.m)

# Create a custom button to toggle the satellite layer
        folium.LayerControl(position='topleft').add_to(self.m)

        self.m.save(resource_path("map.html"))
        conn.close()
        html_path = os.path.abspath(resource_path("map.html"))
        self.map_widget.load(QUrl.fromLocalFile(html_path))
       
            
            
        QtCore.QMetaObject.connectSlotsByName(self)
        self.hamburgerbtn=QtWidgets.QPushButton(self.centralwidget)
        self.hamburgerbtn.setStyleSheet( "\n"
"background-color: rgb(19, 51, 76);"  
  "margin-top:10px;"
   "margin-left:10"
    )
        icon = QIcon(resource_path('hamburger_orng.svg'))
        
        self.hamburgerbtn.setIcon(icon)
        self.hamburgerbtn.setGeometry(5,5, 40, 40)
        self.hamburgerbtn.setObjectName("hamburgerbtn")
        self.hamburgerbtn.clicked.connect(self.toggleMenu)
        self.frame.setVisible(True)
        #self.stackedWidget.setGeometry(50,0,self.centralwidget.width()-50, self.centralwidget.height())
# Access the widgets of the stacked widgetself.page1 = self.stackedWidget.widget(0)
        self.page1 = self.stackedWidget.widget(0)
        self.page2 = self.stackedWidget.widget(1)
        self.page3 = self.stackedWidget.widget(2)
        self.page4 = self.stackedWidget.widget(3)

# Create the buttons for each widget
        self.button1 = QPushButton("", self.page1)
        self.button2 = QPushButton("", self.page2)
        self.button3 = QPushButton("", self.page3)
        self.button4 = QPushButton("", self.page4)

# Set the button positions using absolute positioning
        self.button1.setGeometry(self.page1.width() - self.button1.width() -10, 2, self.button1.width(), self.button1.height())
        self.button2.setGeometry(self.page2.width() - self.button2.width() -10, 2, self.button2.width(), self.button2.height())
        self.button3.setGeometry(self.page3.width() - self.button3.width() -10, 2, self.button3.width(), self.button3.height())
        self.button4.setGeometry(self.page4.width() - self.button4.width() -10, 2, self.button4.width(), self.button4.height())
        self.button1.setFixedSize(30, 30) 
        self.button1.setStyleSheet('''QPushButton {      
                    background-color:rgb(253, 95, 0);
                               font: 900 11pt  Arial Black;
                             color:rgb(0, 87, 146);
                            border:  1px solid rgb(237, 131, 0);
                           border-radius:15%;
                            text-align: left;
                            padding-left:3px;
                            }
                            QPushButton:hover {
                                background-color:qlineargradient(spread:repeat, x1:0, y1:1, x2:1, y2:0, stop:0.28436 rgba(253, 95, 0, 255), stop:0.890995 rgba(255, 193, 35, 255));
                                border:  1px solid gray;
                                box-shadow: 5px 10px rgb(255, 175, 15);
                           }

''')
        self.button2.setFixedSize(30, 30) 
        self.button2.setStyleSheet('''QPushButton {      
                    background-color:rgb(253, 95, 0);
                               font: 900 11pt  Arial Black;
                             color:rgb(0, 87, 146);
                            border:  1px solid rgb(237, 131, 0);
                            border-radius:15%;
                            text-align: left;
                            padding-left:3px;
                            }
                            QPushButton:hover {
                                background-color:qlineargradient(spread:repeat, x1:0, y1:1, x2:1, y2:0, stop:0.28436 rgba(253, 95, 0, 255), stop:0.890995 rgba(255, 193, 35, 255));
                                border:  1px solid gray;
                                box-shadow: 5px 10px rgb(255, 175, 15);
                           }

''')
        self.button3.setFixedSize(30, 30) 
        self.button3.setStyleSheet('''QPushButton {      
                    background-color:rgb(253, 95, 0);
                               font: 900 11pt  Arial Black;
                             color:rgb(0, 87, 146);
                            border:  1px solid rgb(237, 131, 0);
                            border-radius:15%;
                            text-align: left;
                            padding-left:3px;
                            }
                            QPushButton:hover {
                                background-color:qlineargradient(spread:repeat, x1:0, y1:1, x2:1, y2:0, stop:0.28436 rgba(253, 95, 0, 255), stop:0.890995 rgba(255, 193, 35, 255));
                                border:  1px solid gray;
                                box-shadow: 5px 10px rgb(255, 175, 15);
                           
                       }

''')
        self.button4.setFixedSize(30, 30) 
        self.button4.setStyleSheet('''QPushButton {      
                    background-color:rgb(253, 95, 0);
                            font: 900 11pt  Arial Black;
                            color:rgb(0, 87, 146);
                            border:  1px solid rgb(237, 131, 0);
                            border-radius:15%;
                            text-align: left;
                            padding-left:3px;
                            }
                            QPushButton:hover {
                                background-color:qlineargradient(spread:repeat, x1:0, y1:1, x2:1, y2:0, stop:0.28436 rgba(253, 95, 0, 255), stop:0.890995 rgba(255, 193, 35, 255));
                                border:  1px solid gray;
                                box-shadow: 5px 10px rgb(255, 175, 15);
                           }

''')    
        self.button1.setIcon(QIcon(resource_path("icons8-home-page-26.png")))
        self.button2.setIcon(QIcon(resource_path("icons8-home-page-26.png")))
        self.button3.setIcon(QIcon(resource_path("icons8-home-page-26.png")))
        self.button4.setIcon(QIcon(resource_path("icons8-home-page-26.png")))

        self.button1.clicked.connect(self.home)
        self.button2.clicked.connect(self.home)
        self.button3.clicked.connect(self.home)
        self.button4.clicked.connect(self.home)

        validator = QDoubleValidator()
        self.lineEdit.setValidator(validator)
        self.lineEdit_2.setValidator(validator)
        self.lineEdit_3.setValidator(validator)
        self.lineEdit_4.setValidator(validator)
        self.lineEdit_6.setValidator(validator)
        self.lineEdit_7.setValidator(validator)
        
        self.save.clicked.connect(self.add_value)
        self.cancel.clicked.connect(self.clear_fields)
        self.pred.clicked.connect(self.predict_shutdown)
        self.lineEdit_5.textChanged.connect(self.search_table) 

        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.dateTimeEdit_2.setDateTime(QDateTime.currentDateTime())
        self.toolButton.clicked.connect(self.show_menu)
        

        #styling the tabel
        self.tableWidget.setStyleSheet('''
    QTableWidget {
        background-color: rgb(19, 51, 76);
        border: 1px solid rgb(19, 51, 76);
        color: rgb(246, 246, 233);
    }
    
    QTableWidget::item {
        padding: 5px;
        border: 1px solid  rgb(253, 95, 0) ;
    }
    
    QHeaderView::section {
        background-color:  rgb(253, 95, 0);
        font-weight: bold;
        border: 1px solid  rgb(253, 95, 0);
        color:rgb(0, 87, 146);
    }
''')
       #styling the scroll bar
        self.tableWidget.verticalScrollBar().setStyleSheet('''
    QScrollBar:vertical {
        background: transparent;
        width: 15px;
        border-radius: 7px;
        margin: 20px 0 20px 0;
    }

    QScrollBar::handle:vertical {
        background: rgb(19, 51, 76);
        border-radius: 7px;
        min-height: 20px;
    }

    QScrollBar::add-line:vertical {
        border: none;
        background: none;
    }

    QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: #e1e1e1;  /* Set your desired background color */
        height: 15px;
        margin: 5px 0 5px 0;
        border-radius: 7px;
    }

    QScrollBar::handle:horizontal {
        background:rgb(19, 51, 76);  /* Set your desired handle color */
        min-width: 20px;
        border-radius: 7px;
     
    }

    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal {
        border: none;
        background: none;
    }

    QScrollBar::add-page:horizontal,
    QScrollBar::sub-page:horizontal {
        background: none;
    }
''')

        self.tableWidget_2.setStyleSheet('''
    QTableWidget {
        background-color: rgb(19, 51, 76);
        border: 1px solid rgb(19, 51, 76);
        color: rgb(246, 246, 233);
    }
    
    QTableWidget::item {
        padding: 5px;
        border: 1px solid  rgb(253, 95, 0) ;
    }
    
    QHeaderView::section {
        background-color:  rgb(253, 95, 0);
        font-weight: bold;
        border: 1px solid  rgb(253, 95, 0);
        color:rgb(0, 87, 146);
    }
''')
       #styling the scroll bar
        self.tableWidget_2.verticalScrollBar().setStyleSheet('''
    QScrollBar:vertical {
        background: transparent;
        width: 15px;
        border-radius: 7px;
        margin: 20px 0 20px 0;
    }

    QScrollBar::handle:vertical {
        background: rgb(19, 51, 76);
        border-radius: 7px;
        min-height: 20px;
    }

    QScrollBar::add-line:vertical {
        border: none;
        background: none;
    }

    QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
''')
        self.tableWidget_2.horizontalScrollBar().setStyleSheet('''
    QScrollBar:horizontal {
        background: #e1e1e1;  /* Set your desired background color */
        height: 15px;
        margin: 5px 0 5px 0;
        border-radius: 7px;
    }

    QScrollBar::handle:horizontal {
        background:rgb(19, 51, 76);  /* Set your desired handle color */
        min-width: 20px;
        border-radius: 7px;
     
    }

    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal {
        border: none;
        background: none;
    }

    QScrollBar::add-page:horizontal,
    QScrollBar::sub-page:horizontal {
        background: none;
    }
''')
        self.tableWidget_3.setStyleSheet('''
    QTableWidget {
        background-color: rgb(19, 51, 76);
        border: 1px solid rgb(19, 51, 76);
        color: rgb(246, 246, 233);
    }
    
    QTableWidget::item {
        padding: 5px;
        border: 1px solid  rgb(253, 95, 0) ;
    }
    
    QHeaderView::section {
        background-color:  rgb(253, 95, 0);
        font-weight: bold;
        border: 1px solid  rgb(253, 95, 0);
        color:rgb(0, 87, 146);
    }
''')
       #styling the scroll bar
        self.tableWidget_3.verticalScrollBar().setStyleSheet('''
    QScrollBar:vertical {
        background: transparent;
        width: 15px;
        border-radius: 7px;
        margin: 20px 0 20px 0;
    }

    QScrollBar::handle:vertical {
        background: rgb(19, 51, 76);
        border-radius: 7px;
        min-height: 20px;
    }

    QScrollBar::add-line:vertical {
        border: none;
        background: none;
    }

    QScrollBar::sub-line:vertical {
        border: none;
        background: none;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }
''')
        self.tableWidget_3.horizontalScrollBar().setStyleSheet('''
    QScrollBar:horizontal {
        background: #e1e1e1;  /* Set your desired background color */
        height: 15px;
        margin: 5px 0 5px 0;
        border-radius: 7px;
    }

    QScrollBar::handle:horizontal {
        background:rgb(19, 51, 76);  /* Set your desired handle color */
        min-width: 20px;
        border-radius: 7px;
     
    }

    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal {
        border: none;
        background: none;
    }

    QScrollBar::add-page:horizontal,
    QScrollBar::sub-page:horizontal {
        background: none;
    }
''')

         
                     
        
#######################################################################################
#######################################################################################
#################THE FUNCTIONSSSSSSSSSSS#############
#######################################################################################
#######################################################################################        
    def show_menu(self):
            menu = QMenu(self)
            # Apply style sheet to the menu
            menu.setStyleSheet("""
           QMenu {
               background-color: #13334C;
               border: 1px solid #005792;
               color: #005792;
               font: 700 8pt  Arial Black;
               width:100px;
           }
           QMenu::item {
               padding: 5px 30px 5px 20px;
               border: 1px solid #005792;
           }
           QMenu::item:selected {
               background-color: #F6F6E9;
               color: #FD5F00;
               border: 1px solid rgb(253, 95, 0);
           }
       """)

        # Create actions with icons
            action1 = QAction(QIcon(resource_path("icons\\icons8-more-info-26.png")), "more info", self)
            action2 = QAction(QIcon(resource_path("icons\\icons8-logout-48.png")), "Log Out", self)
            
        # Set custom style for the actions
            action1.setIconVisibleInMenu(True)
            action1.setIconText("more info")
            action1.setIcon(QIcon(resource_path("icons\\icons8-more-info-26.png")))
        
            action2.setIconVisibleInMenu(True)
            action2.setIconText("Log Out")
            action2.setIcon(QIcon(resource_path("icons\\icons8-logout-48.png")))
        
            action1.triggered.connect(self.option1_selected)
            action2.triggered.connect(self.option2_selected)
            menu.addAction(action1)
            menu.addAction(action2)
            menu.exec_(self.toolButton.mapToGlobal(self.toolButton.rect().bottomLeft()))
    
    def option1_selected(self):
        print("Option 1 selected!")

    def option2_selected(self):
        self.window1=Window1()
        self.hide()
        self.window1.show()
    def plot_histogram(self):
         conn = sqlite3.connect(resource_path('spdb.db'))
         query = "SELECT * FROM Incidents WHERE `Pipeline Shutdown` = 'YES'"
         df = pd.read_sql_query(query, conn)
         conn.close()
         df.info()

         # Get the selected radio button
         selected_button = self.sender()

         # Get the selected column name
         column_name = selected_button.text()
         print(column_name)

         # Plot the histogram based on the selected column
         plt.clf()
         fig = Figure(figsize=(6, 2))
         ax = fig.add_subplot(111)
         # Set padding values (adjust as needed)
         left = 0.2  # Left padding
         right = 0.9  # Right padding
         bottom = 0.2 # Bottom padding
         top = 0.9  # Top padding
         # Adjust subplot parameters
         fig.subplots_adjust(left=left, right=right, bottom=bottom, top=top)
         # Customize the color theme
         num_unique_values = len(df[column_name].unique())
         bar_colors = [random.choice(['#'+format(random.randint(0, 0xFFFFFF), '06x') for _ in range(6)]) for _ in range(num_unique_values)]
         background_color = 'lightgray'  # Background color of the plot
         grid_color = 'white'  # Color of the grid lines
         label_color = 'black'  # Color of the axis labels 
         # Set the colors
         ax.set_facecolor(background_color)
         ax.grid(color=grid_color)
         ax.spines['bottom'].set_color(label_color)
         ax.spines['left'].set_color(label_color)
         ax.tick_params(axis='x', colors=label_color)
         ax.tick_params(axis='y', colors=label_color)
         df[column_name].value_counts().plot(kind='bar', ax=ax, legend=False, color=bar_colors)
         ax.set_xlabel(column_name, fontsize=7)
         ax.set_xticklabels(ax.get_xticklabels(), rotation=10, ha='right')
         ax.tick_params(axis='x', labelsize=7)       
         ax.set_ylabel('Pipeline Shutdown Count')
         ax.set_title('Histogram of Pipeline Shutdown based on {}'.format(column_name))
         # Enable zoom for the entire plot
         ax.autoscale(enable=True, tight=True)
         # Create or update the canvas
         if self.canvas is None:
             self.canvas = FigureCanvas(fig)
             layout = QtWidgets.QVBoxLayout(self.frame_2)
             self.toolbar = NavigationToolbar(self.canvas, self.frame_2)  # Add the toolbar
             layout.addWidget(self.toolbar)
             layout.addWidget(self.canvas)
             self.frame_2.setLayout(layout)
         else:
             layout = self.frame_2.layout()
             layout.removeWidget(self.canvas)
             layout.removeWidget(self.toolbar)  # Remove previous toolbar
             self.canvas.close()
             self.canvas = FigureCanvas(fig)
             self.toolbar = NavigationToolbar(self.canvas, self.frame_2)  # Add the new toolbar
             layout.addWidget(self.toolbar)
             layout.addWidget(self.canvas)
         self.frame_2.setMinimumSize(self.canvas.sizeHint())
         self.canvas.draw()    
    
    def update_mission_states(self):
         database_lock = threading.Lock()
         database_lock.acquire()

         try:
            conn = sqlite3.connect(resource_path('spdb.db')) # Replace with the path to your SQLite database file
            cursor = conn.cursor()

     # Get missions with states not 'completed' or 'done late'
            cursor.execute("SELECT * FROM messions WHERE state NOT IN ('completed', 'done late')")
            missions = cursor.fetchall()

     # Update the state of each mission based on the current time
            current_time = datetime.now()
            for mission in missions:
                mission_id = mission[0]
                start_time = datetime.strptime(mission[2], "%Y-%m-%d %H:%M:%S")
                end_time = datetime.strptime(mission[3], "%Y-%m-%d %H:%M:%S")
                state = mission[5]
                if current_time < start_time:
                    state= 'pending'
                elif start_time <= current_time < end_time:
                    state = 'ongoing'

        # Update the mission's state in the database
                cursor.execute("UPDATE messions SET state = ? WHERE mession_id = ?", (state, mission_id))

            conn.commit()
            conn.close()
         except Exception as e:
    # Handle any exceptions that may occur during the database operation
            print("Error while updating the database:", str(e))
         finally:
    # Release the lock after the database operation is completed
            database_lock.release()
    def toggleMenu(self):
        # Toggle menu visibility
        
        self.frame.setVisible(not self.frame.isVisible())
        self.button1.setGeometry(self.page1.width() - self.button1.width()-20, 2, self.button1.width(), self.button1.height())
        self.button2.setGeometry(self.page2.width() - self.button2.width()-20, 2, self.button2.width(), self.button2.height())
        self.button3.setGeometry(self.page3.width() - self.button3.width()-20, 2, self.button3.width(), self.button3.height())
        self.button4.setGeometry(self.page4.width() - self.button4.width() -20 , 2, self.button4.width(), self.button4.height())

        if self.frame.isVisible():
         
          self.hamburgerbtn.setStyleSheet( "\n" "background-color: rgb(253, 95, 0);"
                                          "margin-top:10px;"
                                           "margin-left:10"
                                           )
          icon2=QIcon(resource_path('hamburger.svg'))
          self.hamburgerbtn.setIcon(icon2)
          self.stackedWidget.setGeometry(250, 0, self.centralwidget.width()-250, self.centralwidget.height())
          self.tableWidget.setGeometry(30,70,500,500)
          
          
          # self.label_19.setGeometry(self.stackedWidget.width() - 110, 10, 40, 40)
          # self.toolButton.setGeometry(self.stackedWidget.width() - 110, 10, 100, 40)
          # Set the button positions using absolute positioning
          self.button1.setGeometry(self.page1.width() - self.button1.width()-20, 2, self.button1.width(), self.button1.height())
          self.button2.setGeometry(self.page2.width() - self.button2.width()-20, 2, self.button2.width(), self.button2.height())
          self.button3.setGeometry(self.page3.width() - self.button3.width()-20, 2, self.button3.width(), self.button3.height())
          self.button4.setGeometry(self.page4.width() - self.button4.width() -20 , 2, self.button4.width(), self.button4.height())

        else :
            
            self.hamburgerbtn.setStyleSheet( "\n" " background-color: rgb(19, 51, 76);" 
                                            "margin-top:10px;"
                                             "margin-left:10")
            icon = QIcon('hamburger_orng.svg')
            self.hamburgerbtn.setIcon(icon)
            self.stackedWidget.setGeometry(50,0,self.centralwidget.width()+200, self.centralwidget.height())
            self.tableWidget.setGeometry(30,70,700,500)
            self.button1.setGeometry(self.page1.width() - self.button1.width() +50, 2, self.button1.width(), self.button1.height())
            self.button2.setGeometry(self.page2.width() - self.button2.width() +50, 2, self.button2.width(), self.button2.height())
            self.button3.setGeometry(self.page3.width()- self.button3.width()+50, 2, self.button3.width(), self.button3.height())
            self.button4.setGeometry(self.page4.width() - self.button4.width() +50, 2, self.button4.width(), self.button4.height())
            
          
            # self.label_19.setGeometry(self.stackedWidget.width() +110, 10, 40, 40)
            # self.toolButton.setGeometry(self.stackedWidget.width() + 110, 10, 100, 40)
    def home(self):
            self.stackedWidget.setCurrentIndex(4)
    def show_tab_1(self):
            self.stackedWidget.setCurrentIndex(0)
                        
    def show_tab_2(self):
            self.stackedWidget.setCurrentIndex(2) 
           
    def show_tab_3(self):
            self.stackedWidget.setCurrentIndex(1) 
            # Connect to the database
            conn = sqlite3.connect(resource_path("spdb.db"))  # Replace with the actual database file name
            cursor = conn.cursor()
            
     # Retrieve data from the database table
            cursor.execute("SELECT * FROM Incidents")
            data = cursor.fetchall()

     # Set the number of rows and columns in the table
            self.tableWidget.setRowCount(len(data))
            self.tableWidget.setColumnCount(len(data[0]))  # Assuming all rows have the same number of columns

     # Add data to the table
            for i, row in enumerate(data):
                 for j, value in enumerate(row):
                     item = QTableWidgetItem(str(value))
                     self.tableWidget.setItem(i, j, item)

     # Set table properties
            header_labels = [description[0] for description in cursor.description]
            self.tableWidget.setHorizontalHeaderLabels(header_labels)
            self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.tableWidget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
            self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
            self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.tableWidget.verticalHeader().setVisible(False)
            self.tableWidget.resizeRowsToContents()
            self.tableWidget.resizeColumnsToContents()

     # Close the database connection
            conn.close()
           
            
    def show_tab_4(self):
            self.stackedWidget.setCurrentIndex(3)
    def show_tab_5(self):
            self.stackedWidget.setCurrentIndex(5) 
            # Connect to the database
            conn = sqlite3.connect(resource_path("spdb.db"))  # Replace with the actual database file name
            cursor = conn.cursor()
            
     # Retrieve data from the database table
            cursor.execute("SELECT * FROM Pipelines")
            data = cursor.fetchall()

     # Set the number of rows and columns in the table
            self.tableWidget_2.setRowCount(len(data))
            self.tableWidget_2.setColumnCount(len(data[0]))  # Assuming all rows have the same number of columns

     # Add data to the table
            for i, row in enumerate(data):
                 for j, value in enumerate(row):
                     item = QTableWidgetItem(str(value))
                     self.tableWidget_2.setItem(i, j, item)

     # Set table properties
            header_labels = [description[0] for description in cursor.description]
            self.tableWidget_2.setHorizontalHeaderLabels(header_labels)
            self.tableWidget_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.tableWidget_2.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
            self.tableWidget_2.setEditTriggers(QTableWidget.NoEditTriggers)
            self.tableWidget_2.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.tableWidget_2.verticalHeader().setVisible(False)
            self.tableWidget_2.resizeRowsToContents()
            self.tableWidget_2.resizeColumnsToContents()

     # Retrieve data from the database table
            cursor.execute("SELECT * FROM Operators")
            df = cursor.fetchall()

     # Set the number of rows and columns in the table
            self.tableWidget_3.setRowCount(len(df))
            self.tableWidget_3.setColumnCount(len(df[0]))  # Assuming all rows have the same number of columns

     # Add data to the table
            for i, row in enumerate(df):
                 for j, value in enumerate(row):
                     item = QTableWidgetItem(str(value))
                     self.tableWidget_3.setItem(i, j, item)

     # Set table properties
            header_labels = [description[0] for description in cursor.description]
            self.tableWidget_3.setHorizontalHeaderLabels(header_labels)
            self.tableWidget_3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.tableWidget_3.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
            self.tableWidget_3.setEditTriggers(QTableWidget.NoEditTriggers)
            self.tableWidget_3.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.tableWidget_3.verticalHeader().setVisible(False)
            self.tableWidget_3.resizeRowsToContents()
            self.tableWidget_3.resizeColumnsToContents()

     # Close the database connection
            conn.close()
                      
            
    def add_value(self):
        # Connect to the database
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(resource_path("spdb.db"))  # Replace with the actual database file name
        
        if not db.open():
            print("Failed to connect to the database.")
            return

    # Get input values
        AccidentDateTime = self.dateTimeEdit.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        PipelineLocation = self.comboBox_2.currentText()
        PipelineFacilityName = self.lineEdit_8.text()
        OpertorName = self.comboBox_19.currentText()
        PipelineType = self.comboBox.currentText()
        LiquidType = self.comboBox_3.currentText()
        AccidentState = self.comboBox_14.currentText()
        AccidentLatitude = self.lineEdit.text()
        AccidentLongitude = self.lineEdit_2.text()
        CauseCategory = self.comboBox_4.currentText()
        CauseSubcategory = self.comboBox_15.currentText()
        UnintentionalRelease = self.lineEdit_3.text()
        PipelineShutdown = self.comboBox_5.currentText()
        PropertyDamageCosts = self.lineEdit_4.text()
        LiquidIgnition = self.comboBox_16.currentText()
        LiquidExplosion = self.comboBox_17.currentText()

# Check for empty fields
        if (
                not AccidentDateTime
                or not PipelineFacilityName
                or not OpertorName
                or not AccidentLatitude
                or not AccidentLongitude
                or not UnintentionalRelease
                or not PropertyDamageCosts
                ):
                    QMessageBox.warning(
                        self,
                        "Empty Fields",
                        "Please fill in all the required fields.",
                        QMessageBox.Ok,
                        )
                    return

    # Convert input values to float
        try:
            AccidentLatitude = float(AccidentLatitude)
            AccidentLongitude = float(AccidentLongitude)
            UnintentionalRelease = float(UnintentionalRelease)
            PropertyDamageCosts = float(PropertyDamageCosts)
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Values",
                "Please enter valid numeric values for latitude, longitude, unintentional release, and property damage costs.",
                QMessageBox.Ok,
                )
            return
        # Validate latitude and longitude
        if not self.is_valid_location(AccidentLatitude, AccidentLongitude):
            QMessageBox.warning(self, "Invalid Location", "Invalid latitude and longitude. Please provide a location within the continental United States.", QMessageBox.Ok)
            return
        #check for empty fields

        # Perform other necessary validations and error handling here
        # Retrieve the accident year
        accident_year = self.dateTimeEdit.date().year()
        # Generate report number
        count_query = QSqlQuery()
        count_query.prepare("SELECT MAX(\"Report Number\") FROM Incidents")
        count_query.exec_()
        count_query.next()
        last_report_number = count_query.value(0)
        if last_report_number is not None:
            last_report_number_str = str(last_report_number)
            last_report_number_numeric = int(last_report_number_str[len(str(accident_year)):])
            count = last_report_number_numeric + 1
        else:
            count = 1
        reportnumber = int(f"{accident_year}{count:04d}")



    # Check if the entered Facility Name exists in the Pipelines table
        facility_name = PipelineFacilityName.strip()
        pipeline_query = QSqlQuery()
        pipeline_query.prepare("SELECT COUNT(*) FROM Pipelines WHERE \"Pipeline/Facility Name\" = ?")
        pipeline_query.addBindValue(facility_name)
        pipeline_query.exec_()
        pipeline_query.next()
        count = pipeline_query.value(0)

        if count == 0:
            QMessageBox.warning(self, "Invalid Facility Name", "Please enter a valid Facility Name.")
            return


        # Prepare the SQL query
        query = QSqlQuery()
        operatorQuery = QSqlQuery()
        operatorQuery.prepare("SELECT \"Operator ID\" FROM Operators WHERE \"Operator Name\" = ?")
        operatorQuery.addBindValue(OpertorName)
        operatorQuery.exec()
        operatorQuery.next()
        operatorId = operatorQuery.value(0)
        query.prepare("INSERT INTO Incidents (\"Report Number\", \"Accident Date/Time\", \"Operator ID\", \"Pipeline/Facility Name\", \"Pipeline Type\", \"Liquid Type\", \"Accident State\", \"Accident Latitude\", \"Accident Longitude\", \"Cause Category\", \"Cause Subcategory\", \"Unintentional Release (Barrels)\", \"Liquid Ignition\", \"Liquid Explosion\", \"Pipeline Shutdown\") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        query.addBindValue(reportnumber)
        query.addBindValue(AccidentDateTime)
        query.addBindValue(operatorId)
        query.addBindValue(PipelineFacilityName)
        query.addBindValue(PipelineType)
        query.addBindValue(LiquidType)
        query.addBindValue(AccidentState)
        query.addBindValue(AccidentLatitude)
        query.addBindValue(AccidentLongitude)
        query.addBindValue(CauseCategory)
        query.addBindValue(CauseSubcategory)
        query.addBindValue(UnintentionalRelease)
        query.addBindValue(LiquidIgnition)
        query.addBindValue(LiquidExplosion)
        query.addBindValue(PipelineShutdown)
        
    # Execute the SQL query
        if not query.exec_():
            print("Failed to insert values into the table.")
            print(query.lastError().text())
            db.rollback()
        else:
            db.commit()
            QMessageBox.information(self, "Success", "The incident was successfully added.")

        # Close the database connection
        db.close()

        # Clear the input fields
        self.clear_fields()

    def clear_fields(self):
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.comboBox_2.setCurrentIndex(0)
        self.lineEdit_8.clear()
        self.comboBox_19.setCurrentIndex(0)
        self.comboBox.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_14.setCurrentIndex(0)
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_15.setCurrentIndex(0)
        self.lineEdit_3.clear()
        self.comboBox_5.setCurrentIndex(0)
        self.lineEdit_4.clear()
        self.comboBox_16.setCurrentIndex(0)
        self.comboBox_17.setCurrentIndex(0)
    def is_valid_location(self, latitude, longitude):
        # Define the valid range for latitude and longitude within the continental United States
        valid_latitude_range = (24.396308, 49.384358)
        valid_longitude_range = (-125.000000, -66.934570)

        # Check if latitude and longitude values are within the valid range
        if latitude >= valid_latitude_range[0] and latitude <= valid_latitude_range[1] and \
                longitude >= valid_longitude_range[0] and longitude <= valid_longitude_range[1]:
                return True
        else:
            return False    
    def search_table(self):
        search_text = self.lineEdit_5.text().lower()

        for row in range(self.tableWidget.rowCount()):
            row_match = False
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, column)
                if item.text().lower().startswith(search_text):
                    row_match = True
                    item.setBackground(QBrush(QColor(255, 255, 153)))  # Highlight the cell background color
                else:
                    item.setBackground(QBrush(Qt.NoBrush))  # Reset the cell background color

            self.tableWidget.setRowHidden(row, not row_match)  # Show/hide the row based on the match
    

    def predict_shutdown(self):
   
        accident_datetime =self.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        pipeline_location = self.comboBox_6.currentText()
        pipeline_type = self.comboBox_7.currentText()
        liquid_type = self.comboBox_8.currentText()
        accident_state=self.comboBox_10.currentText()
        accident_latitude = self.lineEdit_6.text()
        accident_longitude =self.lineEdit_7.text()
        cause_category = self.comboBox_9.currentText()
        cause_subcategory=self.comboBox_11.currentText()
        liquid_ignition=self.comboBox_12.currentText()
        liquid_explosion=self.comboBox_13.currentText()
        if (
                 not accident_latitude
                or not accident_longitude
            
                ):
                    QMessageBox.warning(
                        self,
                        "Empty Fields",
                        "Please fill in all the required fields.",
                        QMessageBox.Ok,
                        )
                    return
        accident_latitude = float(accident_latitude)
        accident_longitude = float(accident_longitude)        
        print(accident_datetime)
        print(pipeline_location)
        print(pipeline_type)
        print(liquid_type)
        print(accident_latitude)
        print(accident_longitude)
        print(cause_category)
        
        if not self.is_valid_location(accident_latitude, accident_longitude):
            QMessageBox.warning(self, "Invalid Location", "Invalid latitude and longitude. Please provide a location within the continental United States.", QMessageBox.Ok)
            return
    # Load the trained model
        with open('model.pkl', 'rb') as file:
            model = pickle.load(file)
    
    # Create a DataFrame with the input values
        input_data = pd.DataFrame({
    'Pipeline Location': [pipeline_location],
    'Pipeline Type': [pipeline_type],
    'Liquid Type': [liquid_type],
    'Accident Latitude': [accident_latitude],
    'Accident Longitude': [accident_longitude],
    'Cause Category': [cause_category]
})
    
        column_names = [ 'Accident Latitude', 'Accident Longitude', 'OFFHORE', 'ONSHORE', 'ABOVEGROUND', 'TANK', 'TRANSITION AREA', 'UNDERGROUND', 'ALL OTHER CAUSES', 'CORROSION', 'EXCAVATION DAMAGE', 'INCORRECT OPERATION', 'MATERIAL/WELD/EQUIP FAILURE', 'NATURAL FORCE DAMAGE', 'OTHER OUTSIDE FORCE DAMAGE', 'BIOFUEL / ALTERNATIVE FUEL(INCLUDING ETHANOL BLENDS)', 'CO2 (CARBON DIOXIDE)', 'CRUDE OIL', 'HVL OR OTHER FLAMMABLE OR TOXIC FLUID, GAS', 'REFINED AND/OR PETROLEUM PRODUCT (NON-HVL), LIQUID']


        categorical_cols = ['Pipeline Location', 'Pipeline Type', 'Liquid Type', 'Cause Category']
# One-hot encode the categorical columns in the input data without prefix
        input_data_encoded = pd.get_dummies(input_data, columns=categorical_cols, prefix='', prefix_sep='')

# Get the feature names after one-hot encoding
        feature_names = input_data_encoded.columns.tolist()

# Make sure the input data columns are in the same order as the trained model's features
        input_data_encoded = input_data_encoded.reindex(columns=column_names, fill_value=0)

# Add missing columns if any (i.e., if the input data has fewer categories than the trained model)
        missing_cols = set(column_names) - set(input_data_encoded.columns)
        for col in missing_cols:
            input_data_encoded[col] = 0
        print(input_data_encoded.to_string(index=False))
# Make the prediction
        prediction = model.predict(input_data_encoded)

        print(prediction[0])
    # Display the prediction
        if prediction[0] == 0 :
            self.label_22.setText("NO")
            predicted_value="NO"
        else:
            self.label_22.setText("YES")
            predicted_value="YES"
         # Connexion à la base de données
        conn = sqlite3.connect('spdb.db')
        cursor = conn.cursor()
   
          # Obtenir le nombre total de lignes dans la table "Prediction"
        # cursor.execute("SELECT COUNT(*) FROM Prediction")
        # result = cursor.fetchone()
        # num_predictions = result[0] + 1
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_query = "INSERT INTO Prediction (\"Accident Date/Time\", \"Pipeline Type\", \"Liquid Type\", \"Accident State\", \"Accident Latitude\", \"Accident Longitude\", \"Cause Category\", \"Cause Subcategory\", \"Liquid Ignition\", \"Liquid Explosion\", \"Predicted Shutdown\", \"Prediction Date/Time\") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        values = (accident_datetime, pipeline_type, liquid_type, accident_state, accident_latitude, accident_longitude, cause_category, cause_subcategory, liquid_ignition, liquid_explosion, predicted_value, current_date)

        cursor.execute(insert_query, values)
      

        conn.commit()
        conn.close()
        self.dateTimeEdit_2.setDateTime(QtCore.QDateTime.currentDateTime())  # Set the date/time to current date/time
        self.comboBox_6.setCurrentIndex(0)  # Set the pipeline location to the default value (index 0)
        self.comboBox_7.setCurrentIndex(0)  # Set the pipeline type to the default value (index 0)
        self.comboBox_8.setCurrentIndex(0)  # Set the liquid type to the default value (index 0)
        self.comboBox_10.setCurrentIndex(0) # Set the accident state to the default value (index 0)
        self.lineEdit_6.clear()  # Clear the accident latitude input
        self.lineEdit_7.clear()  # Clear the accident longitude input
        self.comboBox_9.setCurrentIndex(0)  # Set the cause category to the default value (index 0)
        self.comboBox_11.setCurrentIndex(0) # Set the cause subcategory to the default value (index 0)
        self.comboBox_12.setCurrentIndex(0) # Set the liquid ignition to the default value (index 0)
        self.comboBox_13.setCurrentIndex(0)
     
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window1 = Window1()
    window1.show()
    app.exec_()
