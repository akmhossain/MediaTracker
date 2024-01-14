from csv import *
from tkinter import *
from tkinter import messagebox
from tkinter.font import *
import time
from datetime import datetime
#import matplotlib as plt


class Home:
    def __init__(self, win): 
        self.clock1 = Label(win, font=("Times New Roman", 32), bg='grey', fg='white')
        self.clock1.place(x=30, y=20)
        self.update_clock(win) # Call the method to display real-time clock

        self.date_label = Label(win, font=("Times New Roman", 14), bg='green')
        self.date_label.place(x=44, y=80)
        self.update_date(win)  # Call the method to display date

        platform = StringVar() # the text on the button will display whatever the value of the variable is
        platform.set('Choose Media Platform')
        self.media = OptionMenu(win, platform, 'TikTok', 'YouTube', 'Instagram', 'Twitter') 
        self.media.config(width=20)
        self.media.place(x=60, y=117)
        
        #Once button is clicked it will follow start function, lambda used to pass on platform variable
        self.startbtn = Button(win, text='Start Session', command=lambda: self.start(platform)) 
        self.startbtn.place(x=95, y=155)

        #Initilize variables to be accessed later by start function
        self.day = None 
        self.startmedia = None
        self.endmedia = None
        
        #variable adds ability to toggle start/end session button
        self.is_session_started = False  
        self.info_list = []



    def update_clock(self, win):
        hour = time.strftime('%I')
        minute = time.strftime('%M')
        sec = time.strftime('%S')
        am_pm = time.strftime('%p')

        self.hour = hour
        self.minute = minute
        self.sec = sec
        self.clock1.config(text= ' ' + hour + ':' + minute + ':' + sec + ' ' + am_pm + ' ')
        win.after(1000, self.update_clock, win) #after method updates text after 1000 milliseconds (1 second)
    
    def update_date(self, win):
        month = time.strftime('%B')
        day = time.strftime('%A')
        year = time.strftime('%Y')
        date = time.strftime('%d')

        self.date_label.config(text=day + ' ' + month + ' ' + date + ', ' + year)
        win.after(1000, self.update_date, win)
    

    def start(self, platform):
        if not self.is_session_started:
            # Start session logic
            self.platform = platform.get() 
            self.day = datetime.now().strftime("%m-%d-%Y")  # Record start time
            self.start_time = datetime.now().strftime("%H:%M:%S")
            self.startbtn.config(text='End Session')
            self.is_session_started = True
            messagebox.askquestion("Start Session?", f"Are you done with all important tasks?") 
            messagebox.showinfo(title='Session Start', message=f'Media session for {self.platform} has started.')
        else:
            # End session logic
            end_time = datetime.now().strftime("%H:%M:%S")
            self.startbtn.config(text='Start Session')
            self.is_session_started = False
            self.info_list.append([self.day, self.platform, self.start_time, end_time]) 
            messagebox.showinfo(title='Session End', message=f'Media session for {self.platform} has ended.')
            with open('media_data.csv', 'w', newline='') as file:
                csv_writer = writer(file)
                csv_writer.writerow(['Day', 'Platform', 'StartMedia', 'EndMedia', 'Total Time'])  # name of header row
                csv_writer.writerows(self.info_list)  # adds list to new row each time button is clicked to start/end session
            with open('media_data.csv', 'r', newline='') as file:
                Reader = reader(file)
                data = list(Reader)

info_list = []
window = Tk()
mywin = Home(window)
window.title('Media Tracker')
window.geometry('390x220')
window.mainloop()
