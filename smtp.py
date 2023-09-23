# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 00:47:29 2023

@author: ASUS
"""
from PyQt5 import QtWidgets, uic
import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt5 import QtCore
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
class Mission(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path('addmession.ui'), self)
        self.retrieve_users()
        self.save.clicked.connect(self.savemession)
        # Set the date and time of the QDateEdit widgets to the current date and time
        current_datetime = QtCore.QDateTime.currentDateTime()
        self.dateEdit.setDateTime(current_datetime)
        self.dateEdit_2.setDateTime(current_datetime)
        self.pushButton_3.clicked.connect(self.login)
        self.pushButton_4.clicked.connect(self.trackmissions)
    def retrieve_users(self):
        connection = sqlite3.connect(resource_path("spdb.db"))
        cursor = connection.cursor()
        
        # Assuming the users table has a 'username' column
        cursor.execute("SELECT username FROM users")
        users = cursor.fetchall()
    
        self.comboBox.clear()
        self.comboBox.addItems([user[0] for user in users])
    
        connection.close()
    def login(self):
        from applicationv01 import Window1
        self.window1=Window1()
        self.hide()
        self.window1.show()
    def trackmissions(self):
        from missionmange import MyMissions
        self.missiont=MyMissions()
        self.hide()
        self.missiont.show()
    def savemession(self):
        description = self.lineEdit.text()
        start_date = self.dateEdit.dateTime().toPyDateTime()
        end_date = self.dateEdit_2.dateTime().toPyDateTime()
        assigned_to = self.comboBox.currentText()
        
        # Check if end_date is less than start_date
        if end_date < start_date:
            print("Error: end date cannot be less than start date")
            self.label_6.setText("Error: end date cannot be less than start date")
            return
            
        # Determine the status based on the start_date and end_date
        current_datetime = datetime.now()
        status = ""
        if start_date > current_datetime and end_date > current_datetime:
            status = "pending"
        elif start_date <= current_datetime and end_date >= current_datetime:
            status = "ongoing"
        else:
            status = "completed"
        
        start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S")
        
        # Assuming you have a SQLite connection and cursor
        connection = sqlite3.connect(resource_path("spdb.db"))
        cursor = connection.cursor()

        # Retrieve the user ID based on the username
        user_query = "SELECT id, email FROM users WHERE username = ?"
        cursor.execute(user_query, (assigned_to,))
        user_id, user_email = cursor.fetchone()

        # Insert the values into the missions table
        insert_query = "INSERT INTO messions (description, start_date, end_date, assigned_to, state) VALUES (?, ?, ?, ?, ?)"
        values = (description, start_date_str, end_date_str, user_id, status)
        cursor.execute(insert_query, values)

        # Commit the changes
        connection.commit()

        # Send an email to the assigned user based on the mission status
        if status == "pending":
            email_subject = "New Mission Assigned"
            email_text = f"Dear {assigned_to},\n\nYou have been assigned to a new mission. Please check your dashboard for more details."
            email_html = f"""
            <html>
              <body>
                <p>Dear {assigned_to},</p>
                <p>You have been assigned to a new mission. Please check your dashboard for more details.</p>
              </body>
            </html>
            """
        elif status == "ongoing":
            email_subject = "Mission Update: Ongoing"
            email_text = f"Dear {assigned_to},\n\nYou are currently working on the following mission:\n\nMission Description: {description}"
            email_html = f"""
            <html>
              <body>
                <p>Dear {assigned_to},</p>
                <p>You are currently working on the following mission:</p>
                <p><strong>Mission Description:</strong> {description}</p>
              </body>
            </html>
            """
        else:
            # No need to send an email for completed missions
            connection.close()
            return

        # Replace with your SMTP server details
        smtp_server = "smtp.elasticemail.com"
        smtp_port = 2525
        smtp_username = "bantangsaran1011@gmail.com"
        smtp_password = "4281FC537F8E50C820869FD0A0B8CB229014"
        sender_email = "pipeshield <bantangsaran1011@gmail.com>"

        # Create the email message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = email_subject
        msg["From"] = sender_email
        msg["To"] = user_email

        # Attach the plain text and HTML versions of the email
        msg.attach(MIMEText(email_text, "plain"))
        msg.attach(MIMEText(email_html, "html"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, [user_email], msg.as_string())
                print("Email sent successfully")
        except smtplib.SMTPException as e:
            print("Error sending email:", str(e))

        # Close the connection
        connection.close()
        # Clear the form fields
        self.lineEdit.clear()
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        self.dateEdit_2.setDate(QtCore.QDate.currentDate())
        self.comboBox.setCurrentIndex(0)
        self.label_6.setText("")

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Mission()
    window.show()
    app.exec_()
