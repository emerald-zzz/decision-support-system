# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 10:44:46 2023

@author: ASUS
"""
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.uic import loadUi
import sqlite3
from PyQt5.QtCore import Qt ,QDate
from matplotlib.animation import FuncAnimation
import sys
import matplotlib.patches as patches
from PyQt5.QtWidgets import  QFrame
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.colors as mcolors
import plotly.graph_objects as go
from PyQt5.QtCore import QDateTime
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import os
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
class MyMissions(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(resource_path('missionm.ui'), self)
        self.load_missions()
        self.retrieve_users()
        current_datetime = QDateTime.currentDateTime()
        self.dateEdit.setDateTime(current_datetime)
        self.dateEdit.setMaximumDate(QDate.currentDate())
        # Connect buttons to sorting functions
        self.button1.clicked.connect(self.sort_by_start_date)
        self.button2.clicked.connect(self.sort_by_state)
        self.pushButton.clicked.connect(self.go_back)
        # Draw ring graph for each frame
        self.plot_ring_graph(self.frame, 'ongoing')
        self.plot_ring_graph(self.frame_2, 'pending')
        self.plot_ring_graph(self.frame_3, 'completed')
        self.plot_ring_graph(self.frame_4, 'done late')
        self.comboBox.currentIndexChanged.connect(lambda: self.display_mission_graph())
        self.dateEdit.dateChanged.connect(lambda: self.display_mission_graph())
        self.figure, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
     
       # Customize the figure background color
        self.figure.patch.set_facecolor((19/255, 51/255, 76/255))  # RGB values normalized to [0, 1]
        self.ax.set_facecolor((19/255, 51/255, 76/255))
        self.frame_5_layout = QVBoxLayout(self.frame_5)
        self.frame_5_layout.addWidget(self.canvas)
       
        
     
    def go_back(self):
        from smtp import Mission
        self.planmession=Mission()
        self.hide()
        self.planmession.show()
    def retrieve_users(self):
        connection = sqlite3.connect(resource_path("spdb.db"))
        cursor = connection.cursor()
        
        # Assuming the users table has a 'username' column
        cursor.execute("SELECT username FROM users")
        users = cursor.fetchall()
    
        self.comboBox.clear()
        self.comboBox.addItems([user[0] for user in users])
    
        connection.close()   
    def plot_ring_graph(self, frame, state):
        plt.ioff()
        # Connect to the SQLite database
        db = sqlite3.connect(resource_path('spdb.db')) # Replace with your database file path
        cursor = db.cursor()

        # Fetch mission count based on state
        cursor.execute("SELECT COUNT(*) FROM messions WHERE state = ?", (state,))
        mission_count = cursor.fetchone()[0]

        # Fetch total mission count
        cursor.execute("SELECT COUNT(*) FROM messions")
        total_missions = cursor.fetchone()[0]

        # Calculate percentage
        percentage = (mission_count / total_missions) * 100
        remainder_percentage = 100 - percentage

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(8, 8))  # Adjust the size as needed
        fig.patch.set_alpha(0)  # Set the figure background to transparent

        # Create a gradient colormap for the orange part of the ring
        gradient_colors = mcolors.LinearSegmentedColormap.from_list('gradient_colors', ['#ff8c00', '#fd5f00'])
        # Create a shadow effect using patches
        shadow = patches.Circle((0, 0), 0.75, color='black', alpha=0.3)  # Adjust alpha for shadow intensity
        ax.add_patch(shadow)

        # Plot the ring chart with gradient color and outer shadow
        explode = (0.1, 0) 
        outer_wedge, _ = ax.pie([percentage, remainder_percentage], startangle=90,explode=explode,
                                colors=[gradient_colors(0.5), '#f0f0f0'], radius=0.75,
                                wedgeprops=dict(width=0.15, edgecolor='none', capstyle='round'))

        # Add the percentage value to the middle of the ring
        text=ax.text(0, 0, f"{percentage:.2f}%", ha='center', va='center', fontsize=10, color='white')
        # Create a white stroke effect
        white_stroke = path_effects.Stroke(linewidth=1, foreground='#005792')
        text.set_path_effects([white_stroke])
        # Set aspect ratio to be equal, and remove x and y ticks
        ax.set_aspect('equal')
        ax.axis('off')
        def update_explode(frame, explode_start, explode_end):
            """
            Update the explosion of the segment based on the current frame.
            
            Args:
                frame (int): Current frame of the animation.
                explode_start (list): List of initial explosion values.
                explode_end (list): List of final explosion values.
            """
            progress = frame / 100.0  # Calculate the progress from 0 to 1
        
            # Interpolate between initial and final explosion values
            current_explode = [
                start + (end - start) * progress for start, end in zip(explode_start, explode_end)
            ]
        
            # Update the explode attribute of the wedge
            outer_wedge[1].set_explode(current_explode)

                # Animate the explosion of the segment
        explode_start = [0.0, 0.0]  # Initial explosion values
        explode_end = [0.1, 0.0]  # Final explosion values
        anim = FuncAnimation(fig, update_explode, frames=range(101),
                              fargs=(explode_start, explode_end), interval=15, repeat=False)

        # Create a canvas for the plot and add it to the frame
        canvas = FigureCanvas(fig)
        plt.close(fig)
        canvas.setStyleSheet("background-color: rgba(0, 0, 0, 0);")  # Set the canvas background to transparent

        layout = QVBoxLayout()
        layout.addWidget(canvas)
        frame.setLayout(layout)
        
        # Close the database connection
        db.close()


    
    def load_missions(self):
    # Connect to the SQLite database
        db = sqlite3.connect(resource_path('spdb.db')) # Replace with your database file path
        cursor = db.cursor()

    # Fetch column names from the messions table
        cursor.execute("PRAGMA table_info(messions)")
        columns = [col[1] for col in cursor.fetchall()]
        self.column_names = columns 

    # Set table headers
        self.tableWidget.setColumnCount(len(columns) + 2)  # Add two columns for buttons
        self.tableWidget.setHorizontalHeaderLabels(columns + ["", ""])
        self.tableWidget.verticalHeader().setVisible(False) 
    # Fetch all missions from the messions table
        cursor.execute("SELECT * FROM messions")
        missions = cursor.fetchall()

    # Populate the QTableWidget with missions
        self.tableWidget.setRowCount(len(missions))
        for row, mission in enumerate(missions):
            for col, value in enumerate(mission):
               if col == 4:  # Assuming assigned_to is in the 4th column
                    # Fetch the user name based on user ID from the user table
                    user_id = mission[col]
                    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
                    user_name_result = cursor.fetchone()
                
                    if user_name_result is not None:
                        user_name = user_name_result[0]  # Fetch the first (and only) result
                        item = QTableWidgetItem(str(user_name))  # Display user name
                    else:
                        item = QTableWidgetItem("User Not Found")  # Or any other appropriate value
               else:
                    item = QTableWidgetItem(str(value))

               self.tableWidget.setItem(row, col, item)
               # Make columns 2 and 4 non-editable
               if col == 2 or col == 4:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Use Qt.ItemIsEditable

               
        # Add delete button to each row
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda checked, row=row: self.delete_mission(row))
            self.tableWidget.setCellWidget(row, len(columns), delete_button)

        # Add edit button to each row
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda checked, row=row: self.edit_mission(row))
            self.tableWidget.setCellWidget(row, len(columns) + 1, edit_button)

    # Close the database connection
        db.close()
    
         
    def display_mission_graph(self):
        selected_user = self.comboBox.currentText()
        start_date = self.dateEdit.date().toPyDate()

        dates = []  # List of dates
        ongoing = []  # List of counts for ongoing missions
        pending = []  # List of counts for pending missions
        completed = []  # List of counts for completed missions
        done_late = []  # List of counts for done late missions

    # Assuming mission records have a "start_date" column and a "state" column
        mission_records = self.fetch_mission_data(selected_user, start_date)

    # Initialize counts for different mission types
        ongoing_count = 0
        pending_count = 0
        completed_count = 0
        done_late_count = 0

    # Iterate through mission records
        for record in mission_records:
            mission_date, status = record
         # Convert the mission_date string to a datetime object
            mission_date = datetime.strptime(mission_date, '%Y-%m-%d %H:%M:%S')

         # Keep only the date portion and discard the time
            mission_date = mission_date.date()

            # Increment counts based on mission status and date
            if status == "ongoing" and mission_date <= datetime.now().date():
                ongoing_count += 1
            elif status == "pending" and mission_date <= datetime.now().date():
                pending_count += 1
            elif status == "completed" and mission_date <= datetime.now().date():
                completed_count += 1
            elif status == "done late" and mission_date <= datetime.now().date():
                done_late_count += 1

        # Collect dates for the X-axis of the graph
            dates.append(mission_date)

        # Collect counts for each mission type for the Y-axis of the graph
            ongoing.append(ongoing_count)
            pending.append(pending_count)
            completed.append(completed_count)
            done_late.append(done_late_count)

    # Sort the lists based on dates
        dates, ongoing, pending, completed, done_late = zip(*sorted(zip(dates, ongoing, pending, completed, done_late)))

    # Clear the previous content of the frame
        self.ax.clear()
 
        # Inside the display_mission_graph function
        # After customizing the graph appearance
        self.ax.plot(dates, ongoing, label='Ongoing', color='blue', linewidth=2, marker='o')
        self.ax.plot(dates, pending, label='Pending', color='orange', linewidth=2, marker='s')
        self.ax.plot(dates, completed, label='Completed', color='green', linewidth=2, marker='^')
        self.ax.plot(dates, done_late, label='Done Late', color='red', linewidth=2, marker='x')
        
        # Customize the legend
        self.ax.legend(loc='upper right', fontsize=10)
        
        # Add a shaded area to indicate weekends
        weekends = [d for d in dates if d.weekday() >= 5]  # Saturday and Sunday
        for weekend in weekends:
            self.ax.axvspan(weekend, weekend + timedelta(days=1), facecolor='gray', alpha=0.2)
        
        # Enhance the grid
        self.ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add data labels to the data points
        for date, o, p, c, dl in zip(dates, ongoing, pending, completed, done_late):
            self.ax.text(date, o, str(o), ha='center', va='bottom', color='blue')
            self.ax.text(date, p, str(p), ha='center', va='bottom', color='orange')
            self.ax.text(date, c, str(c), ha='center', va='bottom', color='green')
            self.ax.text(date, dl, str(dl), ha='center', va='bottom', color='red')
        # Customize the angle of the x-axis labels
        self.ax.set_xticks(dates)  # Set the x-axis tick positions to the dates
        self.ax.set_xticklabels([d.strftime('%Y-%m-%d') for d in dates], rotation=15, ha='right')  # Format and set the labels

        # Add vertical line at today's date
        today = datetime.now().date()
        self.ax.axvline(today, color='gray', linestyle='--', linewidth=1, alpha=0.7)
        
        # Customize the text color
        self.ax.set_title('Mission Improvement', color='black', fontsize=16)
        self.ax.set_xlabel('Date', color='black', fontsize=12)
        self.ax.set_ylabel('Number of Missions', color='black', fontsize=12)
        self.ax.tick_params(axis='both', colors='black', labelsize=10)
        
        # Adjust layout
        #self.ax.tight_layout()
        
        self.canvas.draw()
        
        
        



    def fetch_mission_data(self, selected_user, start_date):
        db = sqlite3.connect(resource_path('spdb.db')) # Replace with your database file path
        cursor = db.cursor()
        # Fetch the user ID based on the selected username
        cursor.execute("SELECT id FROM users WHERE username = ?", (selected_user,))
        user_id = cursor.fetchone()[0]
        # Query to fetch mission data for the selected user and start date
        cursor.execute("SELECT start_date, state FROM messions WHERE assigned_to = ? AND start_date >= ? AND start_date <= ?",
               (user_id, start_date, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        mission_records = cursor.fetchall()

        db.close()

        return mission_records
    def sort_by_start_date(self):
        self.tableWidget.sortItems(2, Qt.AscendingOrder)  # Replace 2 with the column index of start_date

    def sort_by_state(self):
        self.tableWidget.sortItems(5, Qt.AscendingOrder)  
    def delete_mission(self, row):
        # Connect to the SQLite database
        db = sqlite3.connect(resource_path('spdb.db'))  # Replace with your database file path
        cursor = db.cursor()

        # Get the mission_id from the selected row
        mission_id = self.tableWidget.item(row, 0).text()

        # Delete the mission from the database
        cursor.execute("DELETE FROM messions WHERE mession_id = ?", (mission_id,))
        db.commit()

        # Remove the row from the table
        self.tableWidget.removeRow(row)

        # Close the database connection
        db.close()

    def edit_mission(self, row):
    # Make the item editable
        for col in range(self.tableWidget.columnCount() - 2):  # Exclude the buttons column
            item = self.tableWidget.item(row, col)
            #item.setFlags(item.flags() | Qt.ItemIsEditable)

    # Connect the editingFinished signal to the save_edited_mission method
        edit_button = self.tableWidget.cellWidget(row, self.tableWidget.columnCount() - 1)
        if edit_button is not None:
            edit_button.clicked.connect(lambda _, row=row: self.save_edited_mission(row))

    def save_edited_mission(self, row):
    # Get the new values from the edited cells
        new_values = []
        for col in range(self.tableWidget.columnCount() - 2):  # Exclude the buttons column
            item = self.tableWidget.item(row, col)
            new_values.append(item.text())

    # Get the mission_id from the first column
        mission_id = self.tableWidget.item(row, 0).text()

    # Connect to the SQLite database
        db = sqlite3.connect(resource_path('spdb.db'))  # Replace with your database file path
        cursor = db.cursor()

    # Construct the UPDATE query dynamically
        update_query = f"UPDATE messions SET {', '.join([f'{self.column_names[col]} = ?' for col in range(len(new_values))])} WHERE mession_id = ?"
    
        new_values.append(mission_id)  # Add mission_id to the end

        cursor.execute(update_query, new_values)
        db.commit()

    # Close the database connection
        db.close()




if __name__ == "__main__":
    app = QApplication([])
    main_window = MyMissions()
    main_window.show()
    app.exec_()

