import tkinter as tk 
from csv import *
from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import *
import time
from datetime import datetime
import os
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

        # Label Tabs
        tabControl.add(self.tab1, text ='Media Tracker') 
        tabControl.add(self.tab2, text ='Pomodoro Focus') 
        tabControl.add(self.tab3, text ='Daily Trend') 
        tabControl.add(self.tab4, text ='Weekly Trend') 
        tabControl.add(self.tab5, text ='Display Data') 

        tabControl.pack(expand = 1, fill ="both") 

      
        # ************************** GUI FOR TAB 1 - MEDIA TRACKER *****************************************#

        # Create border
        bordered_frame = tk.Frame(self.tab1, borderwidth=2, relief="solid")
        bordered_frame.place(x=10, y=5, width=300, height=200)

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

        platform = StringVar() # Text on the button will display whatever the value of the variable is
        platform.set('Choose Media Platform')
        self.media = tk.OptionMenu(self.tab1, platform, 'TikTok', 'YouTube', 'Instagram', 'Twitter', 'Other') 
        self.media.config(width=20)
        self.media.place(x=60, y=117)

        # Once button is clicked it will follow start function, lambda used to pass on platform variable
        self.startbtn = tk.Button(self.tab1, text='Start Session', command=lambda: self.start_media(platform)) 
        self.startbtn.place(x=100, y=155)

        # Initialize variables for mediatimer - tracks total media time 
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.medialabel = tk.Label(self.tab1, font=("Times New Roman", 16), text='Total Media Time:')
        self.medialabel.place(x=33, y=190)
        self.mediatimer = tk.Label(self.tab1, font=("Times New Roman", 16), bg='light goldenrod', text='00:00:00')
        self.mediatimer.place(x=195, y = 190)
        self.is_timer_running = False # Initilize variable to False, only run when session started

        # Schedule break alert every 30 minutes
        self.schedule_alert(win)

        # ***************************************** END OF TAB 1 GUI ********************************************************#


        # ********************************** GUI FOR TAB 2 - POMODORO FOCUS ******************************************#

        # Create borders
        bordered_frame_2 = tk.Frame(self.tab2, borderwidth=2, relief="solid")
        bordered_frame_2.place(x=22, y=5, width=300, height=217)

        bordered_frame_3 = tk.Frame(self.tab2, borderwidth=2, relief="solid")
        bordered_frame_3.place(x=37, y=231, width=250, height=80)

        bordered_frame_4 = tk.Frame(self.tab2, borderwidth=2, relief="solid")
        bordered_frame_4.place(x=298, y=239, width=156, height=70)

        # Reuse of clock and date from tab 1
        self.clock2 = tk.Label(self.tab2, font=("Times New Roman", 32), bg='black', fg='white')
        self.clock2.place(x=40, y=20)
        self.update_clock2(self.tab2) # Call the method to display real-time clock
        
        self.date_label = tk.Label(self.tab2, font=("Times New Roman", 14), bg='black', fg='white')
        self.date_label.place(x=54, y=80)
        self.update_date(self.tab2)  # Call the method to display date

        # Creating GUI and button for user to input desired minutes for focus time
        self.focus_time = tk.Entry(self.tab2, text='', width=4)
        self.focus_time.place(x=175, y=120)
        self.focusbtn = tk.Button(self.tab2, text='Submit', command=lambda: self.focus(self.focus_time))
        self.focusbtn.place(x=205, y=117)
        self.focuslabel = tk.Label(self.tab2, text='Enter a focus time:', font=("Times New Roman", 12))
        self.focuslabel.place(x=55, y=118)
        
        # Creating GUI and button for user to input desired minutes for break time
        self.break_time = tk.Entry(self.tab2, text='', width=4)
        self.break_time.place(x=175, y=150)
        self.breakbtn = tk.Button(self.tab2, text='Submit', command=lambda: self.breaks(self.break_time))
        self.breakbtn.place(x=205, y=147)
        self.breaklabel = tk.Label(self.tab2, text='Enter a break time:', font=("Times New Roman", 12))
        self.breaklabel.place(x=55, y=148)

        # Adds ability to check if both focus and break time are set before starting a pomodoro session
        self.is_focustime_set = False
        self.is_breaktime_set = False

        # GUI and button to start pomodoro session + variable to toggle pomodoro session on/off
        self.is_pomodoro_started = False
        self.pomodorobtn = tk.Button(self.tab2, text='Start Pomodoro Session', command=lambda: self.start_pomo(self.focus_time, self.break_time, win))
        self.pomodorobtn.place(x=84, y=180)

        # Countdown timer that shows time until next break
        self.focustimer = tk.Label(self.tab2, font=("Times New Roman", 14), bg='light goldenrod', text='00:00')
        self.focustimer.place(x=220, y=240)
        self.focus_timer_label = tk.Label(self.tab2, text='Remaining Focus Time:', font=("Times New Roman", 13))
        self.focus_timer_label.place(x=50, y=240)

        # Countdown timer that shows time until next focus session
        self.breaktimer = tk.Label(self.tab2, font=("Times New Roman", 14), bg='light goldenrod', text='00:00')
        self.breaktimer.place(x=220, y=275)
        self.break_timer_label = tk.Label(self.tab2, text='Remaining Break Time:', font=("Times New Roman", 13))
        self.break_timer_label.place(x=50, y=275)

        # Timer that shows total time of pomodoro session
        self.focus_total_timer = tk.Label(self.tab2, font=("Times New Roman", 16), bg='light goldenrod', text='00:00:00')
        self.focus_total_timer.place(x=330, y=272)
        self.focus_total_label = tk.Label(self.tab2, font=("Times New Roman", 12), text='Total Pomodoro Time:')
        self.focus_total_label.place(x=304, y=247)

        # Toggle between focus countdown and break countdown
        self.is_focus_running = False
        self.is_break_running = False

        # CSV data will be appended to this list
        self.focus_list = []

        # Initialize variables for total time
        self.focus_minutes = 0 
        self.focus_seconds = 0
        self.focus_hours = 0

        
    # ************************************ END OF TAB 2 GUI ****************************************************** #


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


    def start_media(self, platform):
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

            # Get the current day
            current_day = datetime.now().strftime("%A")

            # Check if file is empty to add header row
            file_path = 'media_data.csv'
            is_file_empty = os.path.getsize(file_path) == 0

            # Code to append data to csv file
            with open(file_path, 'a', newline='') as file:
                csv_writer = writer(file)

                if is_file_empty:
                    csv_writer.writerow(['Day', 'Platform', 'StartMedia', 'EndMedia', 'Total Time'])  # Label header row

                csv_writer.writerow([current_day, self.platform, self.start_time, end_time, total_time])
            messagebox.showinfo(title='Session End', message=f'Media session for {self.platform} has ended.')
        
    def schedule_alert(self, win):
        # Schedule alert function every 30 minutes
        win.after(30 * 60 * 1000, self.show_alert, win)

    def show_alert(self, win):
        # Display the alert to the user every 30 minutes
        messagebox.showinfo("Rest", "It's time for a break, consider closing your device for a bit!")
        
        # Reschedule the next alert
        self.schedule_alert(win)


    # *****************************  TAB 1 FUNCTIONS END   ************************************ #

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

        
    def focus(self, focus_time_entry):
        focus_time_str = focus_time_entry.get()  # Get focus value from entry widget
        try:
            focustime = int(focus_time_str)
            if 25 <= focustime <= 60:
                messagebox.showinfo('Focus Time', f'Focus time set to {focus_time_str} minutes')
                self.is_focustime_set = True
            else:  # Focus time has to be between 25 and 60 minutes
                messagebox.showwarning('Invalid Time Frame', 'Please enter a focus time between 25 and 60 minutes')
        except ValueError:  # ValueError checks if input is a number
            messagebox.showwarning('Invalid Input', 'Please enter a valid numeric value for focus time')

    def breaks(self, break_time_entry):
        break_time_str = break_time_entry.get()  # Get break value from entry widget
        try:
            breaktime = int(break_time_str)
            if 5 <= breaktime <= 10:
                messagebox.showinfo('Break Time', f'Break time set to {break_time_str} minutes')
                self.is_breaktime_set = True
            else:  # Break time has to be between 5 and 10 minutes
                messagebox.showwarning('Invalid Time Frame', 'Please enter a break time between 5 and 10 minutes')
        except ValueError:  # ValueError checks if input is a number
            messagebox.showwarning('Invalid Input', 'Please enter a valid numeric value for break time')

    def start_pomo(self, focus_entry, break_entry, win):
        focus_time_str = focus_entry.get()
        break_time_str = break_entry.get()
        if self.is_pomodoro_started == False:
            # Start session logic
            try:
                focustime = int(focus_time_str)
                breaktime = int(break_time_str)
                if 25 <= focustime <= 60 and 5 <= breaktime <= 10:
                    self.pomodorobtn.config(text='End Pomodoro Session')
                    messagebox.showinfo('Pomodoro Session Started', f'Pomodoro Session has started.\n Work for {focustime} minutes and take a break for {breaktime} minutes!')
                    self.is_pomodoro_started = True
                    self.start_time = datetime.now().strftime("%H:%M:%S")


                    # Start the focus timer
                    self.update_focus_timer(focustime * 60)

                    # Variable to keep track of total focus time (includes break time)
                    win.after(1000, self.increment_focus, win)

                    self.focus_start_time = datetime.now().strftime("%H:%M:%S")

                else:
                    messagebox.showwarning('Invalid Time Frame', 'Please SUBMIT a valid focus and break times!')
            except ValueError:
                messagebox.showwarning('Invalid Input', 'Please SUBMIT a valid focus and break times!')

        else: 
            # End session logic
            pomo_input = messagebox.askquestion('End Pomodoro Session?', 'Are you sure you want to quit focus session?')
            if pomo_input == 'no':
                pass  # Keep running session if 'no' is clicked
            else:
                # Stop the timers
                self.is_pomodoro_started = False

                # Get the current day
                current_day = datetime.now().strftime("%A")

                self.focus_end_time = datetime.now().strftime("%H:%M:%S")

                # Get start and end time to calculate total time
                start_time_dt = datetime.strptime(self.focus_start_time, "%H:%M:%S")
                end_time_dt = datetime.strptime(self.focus_end_time, "%H:%M:%S")
                total_time = end_time_dt - start_time_dt

                messagebox.showinfo(title='Session End', message=f'Pomodoro session has ended!')
                self.pomodorobtn.config(text='Start Pomodoro Session')
                self.focustimer.config(text='00:00')  # Reset countdown timers to 00:00
                self.breaktimer.config(text='00:00')
                
                # Check if file is empty to add header row
                file_path = 'focus_data.csv'  
                is_file_empty = os.path.getsize(file_path) == 0

                with open(file_path, 'a', newline='') as file:
                    csv_writer = writer(file)
                    # Check if the file is empty, if it is empty add header
                    if is_file_empty:
                        csv_writer.writerow(['Day', 'Total Focus Time'])
                    csv_writer.writerow([current_day, total_time])

                self.pomodorobtn.config(text='Start Pomodoro Session')


    def update_focus_timer(self, focus_remaining_time=None):
        if self.is_pomodoro_started:
            if focus_remaining_time is None:
                focus_remaining_time = int(self.focus_time.get()) * 60  # Get user input for desired focus time

            if focus_remaining_time > 0:
                minutes, seconds = divmod(focus_remaining_time, 60)
                self.focustimer.config(text=self.format_time(focus_remaining_time))
                self.tab2.after(1000, self.update_focus_timer, focus_remaining_time - 1) # Decrement remianing time by 1 second
            else:
                response = messagebox.askquestion('Focus Time Ended', 'Focus time has ended. Do you want to take a break?')
                if response == 'yes':
                    # If 'yes', start the break timer
                    self.update_break_timer(int(self.break_time.get()) * 60)
                else:
                    # If 'no', end the Pomodoro session
                    self.start_pomo(self.focus_time, self.break_time, self.tab2)

    def update_break_timer(self, break_remaining_time=None):
        if self.is_pomodoro_started:
            if break_remaining_time is None:
                break_remaining_time = int(self.break_time.get()) * 60  # Get user input for desired break time

            if break_remaining_time > 0:
                minutes, seconds = divmod(break_remaining_time, 60)
                self.breaktimer.config(text=self.format_time(break_remaining_time))
                self.tab2.after(1000, self.update_break_timer, break_remaining_time - 1) # Decrement remaining time by 1 second
            else:
                response = messagebox.askquestion('Break Time Ended', 'Break time has ended. Do you want to start another focus session?')
                if response == 'yes':
                    # If 'yes', start the focus timer
                    self.update_focus_timer(int(self.focus_time.get()) * 60)
                else:
                    # If 'no', end the Pomodoro session
                    self.start_pomo(self.focus_time, self.break_time, self.tab2)
                
    def format_time(self, seconds): #formats time in mm:ss
        minutes, seconds = divmod(seconds, 60)
        return '{:02}:{:02}'.format(minutes, seconds)
    
    def increment_focus(self, win):
        # To increment total focus time
        if self.is_pomodoro_started:
            # Increment focus_seconds
            self.focus_seconds += 1

            # Update focus_minutes and reset focus_seconds when 60 seconds
            if self.focus_seconds == 60:
                self.focus_seconds = 0
                self.focus_minutes += 1

            # Update focus_hours and reset focus_minutes when 60 minutes
            if self.focus_minutes == 60:
                self.focus_minutes = 0
                self.focus_hours += 1

            focus_hour_str = str(self.focus_hours).zfill(2)
            focus_min_str = str(self.focus_minutes).zfill(2)
            focus_sec_str = str(self.focus_seconds).zfill(2)

            self.focus_total_timer.config(text=focus_hour_str + ':' + focus_min_str + ':' + focus_sec_str)
            win.after(1000, self.increment_focus, win)

    # *************************** TAB 2 FUNCTIONS END ****************************************** #

window = Tk()
mywin = Home(window)
window.title('Media & Focus Tracker')
window.geometry('470x350')
window.mainloop()
