import tkinter as tk 
from csv import *
from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import *
import time
from datetime import datetime
#import matplotlib as plt


class Home:
    def __init__(self, win): 
        # Creating Tabs
        tabControl = ttk.Notebook(win) 

        self.tab1 = ttk.Frame(tabControl) 
        self.tab2 = ttk.Frame(tabControl) 
        self.tab3 = ttk.Frame(tabControl) 
        self.tab4 = ttk.Frame(tabControl) 
        self.tab5 = ttk.Frame(tabControl) 

        tabControl.add(self.tab1, text ='Media Tracker') 
        # create border
        bordered_frame = tk.Frame(self.tab1, borderwidth=2, relief="solid")
        bordered_frame.place(x=10, y=5, width=300, height=200)
        # label tabs
        tabControl.add(self.tab2, text ='Paramodo Focus') 
        tabControl.add(self.tab3, text ='Daily Trend') 
        tabControl.add(self.tab4, text ='Weekly Trend') 
        tabControl.add(self.tab5, text ='Display Data') 

        tabControl.pack(expand = 1, fill ="both") 

      
        # ************************** GUI FOR TAB 1 - MEDIA TRACKER *****************************************#

        # Initilize variables to be accessed later by start function
        self.day = None 
        self.startmedia = None
        self.endmedia = None

        # Variable adds ability to toggle start/end session button
        self.is_session_started = False  
        self.info_list = []

        self.clock1 = tk.Label(self.tab1, font=("Times New Roman", 32), bg='black', fg='white')
        self.clock1.place(x=30, y=20)
        self.update_clock(self.tab1) # Call the method to display real-time clock

        self.date_label = tk.Label(self.tab1, font=("Times New Roman", 14), bg='black', fg='white')
        self.date_label.place(x=44, y=80)
        self.update_date(self.tab1) # Call the method to display date

        platform = StringVar() # the text on the button will display whatever the value of the variable is
        platform.set('Choose Media Platform')
        self.media = tk.OptionMenu(self.tab1, platform, 'TikTok', 'YouTube', 'Instagram', 'Twitter', 'Other') 
        self.media.config(width=20)
        self.media.place(x=60, y=117)

        # Once button is clicked it will follow start function, lambda used to pass on platform variable
        self.startbtn = tk.Button(self.tab1, text='Start Session', command=lambda: self.start(platform)) 
        self.startbtn.place(x=100, y=155)

        # Initialize variables for mediatimer - tracks total media time 
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.medialabel = tk.Label(self.tab1, font=("Times New Roman", 16), text='Total Media Time:')
        self.medialabel.place(x=33, y=190)
        self.mediatimer = tk.Label(self.tab1, font=("Times New Roman", 16), bg='light goldenrod', text='00:00:00')
        self.mediatimer.place(x=195, y = 190)
        self.is_timer_running = False # Initilize variable to only run when session started

        # Schedule break alert every 30 minutes
        self.schedule_alert(win)

        # ***************************************** END OF TAB 1 GUI ********************************************************#


        # GUI FOR TAB 2 - PARAMODO FOCUS #

        self.clock2 = tk.Label(self.tab2, font=("Times New Roman", 32), bg='grey', fg='white')
        self.clock2.place(x=30, y=20)
        self.update_clock2(self.tab2) # Call the method to display real-time clock
        
        self.date_label = tk.Label(self.tab2, font=("Times New Roman", 14), bg='green')
        self.date_label.place(x=44, y=80)
        self.update_date(self.tab2)  # Call the method to display date

        self.focus_time = Entry(self.tab2)


    # ********************************** START OF TAB 1 FUNCTIONS ***************************************** #
  
    def update_clock(self, win):
        hour = time.strftime('%I')
        minute = time.strftime('%M')
        sec = time.strftime('%S')
        am_pm = time.strftime('%p')

        self.hour = hour
        self.minute = minute
        self.sec = sec
        self.clock1.config(text= ' ' + hour + ':' + minute + ':' + sec + ' ' + am_pm + ' ')
        win.after(1000, self.update_clock, win) # After method updates text after 1000 milliseconds (1 second)

    def update_date(self, win):
        month = time.strftime('%B')
        day = time.strftime('%A')
        year = time.strftime('%Y')
        date = time.strftime('%d')

        self.date_label.config(text=' ' + day + ' ' + month + ' ' + date + ', ' + year + ' ')
        win.after(1000, self.update_date, win)

    def update_timer(self, win):
        if self.is_session_started and self.is_timer_running:
            # Increment seconds
            self.seconds += 1

            # Update minutes and reset seconds when 60 seconds
            if self.seconds == 60:
                self.seconds = 0
                self.minutes += 1

            # Update hours and reset minutes when 60 minutes
            if self.minutes == 60:
                self.minutes = 0
                self.hours += 1

            # Convert values to string format, zfill for leading zeros
            hour_str = str(self.hours).zfill(2)
            min_str = str(self.minutes).zfill(2)
            sec_str = str(self.seconds).zfill(2)

            self.mediatimer.config(text=hour_str + ':' + min_str + ':' + sec_str)
            win.after(1000, self.update_timer, win)


    def start(self, platform):
        if not self.is_session_started:
            # Warn user if platform is not chosen
            if platform.get() == 'Choose Media Platform':
                # Display an alert if the user didn't choose a media platform
                messagebox.showwarning("Invalid Platform", "Please choose a media platform.")
                return
            
            # Double check to see if client is finished with all tasks
            alert = messagebox.askquestion("Start Session?", f"Are you done with all important tasks?") 
            if alert == 'no':
                # If client pressed 'no', return to the home screen without any action
                self.startbtn.config(text='Start Session')
                self.is_session_started = False
                self.is_timer_running = False
                return
            
            # Start session if all conditions above are met 
            else:
                self.platform = platform.get() 
                self.day = datetime.now().strftime("%m-%d-%Y")  # Record start time
                self.start_time = datetime.now().strftime("%H:%M:%S")
                self.startbtn.config(text='End Session')
                self.is_session_started = True
                self.is_timer_running = True # Start media timer
                
                
                messagebox.showinfo(title='Session Start', message=f'Media session for {self.platform} has started.')
                # Start the timer after confirming the session has started
                self.update_timer(self.tab1)
        else:
            # End session logic
            end_time = datetime.now().strftime("%H:%M:%S")
            self.startbtn.config(text='Start Session')
            self.is_session_started = False
            self.is_timer_running = False
            
            # Code to find total time
            start_time_dt = datetime.strptime(self.start_time, "%H:%M:%S")
            end_time_dt = datetime.strptime(end_time, "%H:%M:%S")
            total_time = end_time_dt - start_time_dt

            # Code to add data to csv file
            self.info_list.append([self.day, self.platform, self.start_time, end_time, total_time]) 
            messagebox.showinfo(title='Session End', message=f'Media session for {self.platform} has ended.')
            with open('media_data.csv', 'w', newline='') as file:
                csv_writer = writer(file)
                csv_writer.writerow(['Day', 'Platform', 'StartMedia', 'EndMedia', 'Total Time'])  # Label header row
                csv_writer.writerows(self.info_list)  # Adds list to new row each time button is clicked to start/end session
            with open('media_data.csv', 'r', newline='') as file:
                Reader = reader(file)
                data = list(Reader)
        
    def schedule_alert(self, win):
        # Schedule alert function every 30 minutes
        win.after(30 * 60 * 1000, self.show_alert, win)

    def show_alert(self, win):
        # Display the alert to the user every 30 minutes
        messagebox.showinfo("Rest", "It's time for a break, consider ending your media session!")
        
        # Reschedule the next alert
        self.schedule_alert(win)


        # ***************************** TAB 1 FUNCTIONS END   ************************************* #

        # ***************************** TAB 2 FUNCTIONS START ************************************* #
                
    def update_clock2(self, win):
        hour = time.strftime('%I')
        minute = time.strftime('%M')
        sec = time.strftime('%S')
        am_pm = time.strftime('%p')

        self.hour = hour
        self.minute = minute
        self.sec = sec
           
        self.clock2.config(text= ' ' + hour + ':' + minute + ':' + sec + ' ' + am_pm + ' ')
        win.after(1000, self.update_clock2, win) # After method updates text after 1000 milliseconds (1 second)

        # *************************** TAB 2 FUNCTIONS END ****************************************** #

info_list = []
window = Tk()
mywin = Home(window)
window.title('Media Tracker')
window.geometry('470x300')
window.mainloop()
