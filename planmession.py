from PyQt5 import QtWidgets, uic
import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class Admin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addmession.ui', self)
        self.retrieve_users()
        self.save.clicked.connect(self.savemession)
        
    def retrieve_users(self):
        connection = sqlite3.connect("spdb.db")
        cursor = connection.cursor()
        
        # Assuming the users table has a 'username' column
        cursor.execute("SELECT username FROM users")
        users = cursor.fetchall()
    
        self.comboBox.clear()
        self.comboBox.addItems([user[0] for user in users])
    
        connection.close()
    
    def savemession(self):
        description = self.lineEdit.text()
        start_date = self.dateEdit.dateTime().toPyDateTime()
        end_date = self.dateEdit_2.dateTime().toPyDateTime()
        assigned_to = self.comboBox.currentText()
        
        # Check if end_date is less than start_date
        if end_date < start_date:
            print("Error: end date cannot be less than start date")
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
        connection = sqlite3.connect("spdb.db")
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

        # Send an email to the assigned user
        email_subject = "New Mission Assigned"
        email_message = f"Dear {assigned_to},\n\nYou have been assigned to a new mission. Please check your dashboard for more details."

        # Set up the Gmail API authentication
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        credentials = flow.run_local_server(port=0)
        service = build('gmail', 'v1', credentials=credentials)

        # Create the email message
        message = MIMEText(email_message)
        message['to'] = user_email
        message['subject'] = email_subject

        # Send the email using the Gmail API
        service.users().messages().send(userId='me', body={'raw': message.as_string()}).execute()
        print("Email sent successfully")

        # Close the connection
        connection.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Admin()
    window.show()
    app.exec_()

