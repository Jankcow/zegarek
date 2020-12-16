from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import datetime
import csv
from csv import *
from tkinter import Tk, Frame, Button
from tkinter import BOTH, LEFT
from tkinter import messagebox

window = Tk()
window.title("Licznik")
window.geometry('450x250')
window.iconbitmap('c:/Users/Kluska/VS/img/timer1.ico')
window.resizable(False, False)

stopwatch_counter_num = 82800
stopwatch_running = False


def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def to_integer(dt_time):
    return dt_time.hour*60*60 + dt_time.minutes*60 + dt_time.seconds

def load():
    num = None
    setting = None
    with open("czas.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            sample = row['Czas']
            if num is None: num = sample
            if sample > num: num = sample
    
    with open("czas.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for num in csv_file:                    
            wiersz=dict(row)
            break
    if 'Tak' in wiersz.values():
        #dodanie czasu
        global stopwatch_counter_num
        time = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        time_given = datetime.datetime.strptime(time, '%d-%m-%Y %H:%M:%S')
        time_saved  = datetime.datetime.strptime(wiersz.pop("Czas"), '%d-%m-%Y %H:%M:%S')
       
        #time-datetime.datetime(time_saved)
        q=0
        stopwatch_counter_num = stopwatch_counter_num + q
        
        #zmiana guzików i włączenie timera
        global stopwatch_running
        stopwatch_running = True
        start_button.config(state='disabled')
        stop_button.config(state='normal')

    print("Load complete")
    
def clock():
        time = datetime.datetime.now().strftime("%H:%M:%S")
        time_label.config(text = time)
        time_label.after(1000, clock)

def stopwatch_counter(label):
    def count():
        if stopwatch_running:
            global stopwatch_counter_num
            if stopwatch_counter_num==82800:
                display="Starting..."
            else:
                tt = datetime.datetime.fromtimestamp(stopwatch_counter_num) 
                string = tt.strftime("%H:%M:%S") 
                display=string 
            label.config(text=display)
            label.after(1000, count)
            stopwatch_counter_num += 1
    count()

def stopwatch(work):
    if work == 'start':
        global stopwatch_running
        stopwatch_running=True
        stopwatch_counter(timer_label)
    elif work == 'stop':
        global stopwatch_counter_num
        stopwatch_running=False
        timer_label.config(text=' ')
        stopwatch_counter_num=82800

def save(work):
    time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    if work == 'start':
        #stopwatch('start')
        row_contents = [time,'Tak']
        append_list_as_row('czas.csv', row_contents)
        start_button.config(state='disabled')
        stop_button.config(state='normal')
    elif work == 'stop':
        #stopwatch('stop')
        row_contents = [time,'Nie']
        append_list_as_row('czas.csv', row_contents)
        start_button.config(state='normal')
        stop_button.config(state='disabled')

def on_closing():
    if messagebox.askokcancel("Wyjście", "Czy na pewno chcesz wyjść?"):
        window.destroy()

#zegarek
time_label = Label(window, font = 'YT_Sans 40 bold', foreground = 'black')
time_label.pack(anchor='center')
#obecny czas pracy
timer_label = Label(window, font = 'YT_Sans 40 italic', foreground = 'black')
timer_label.pack(anchor='center')
#przyciski
empty_label_1 = Label(window, width=2)
empty_label_1.pack(side=tk.LEFT)
start_button = Button(window, text= "Start pracy", command=lambda:save('start'), font = 'Arial 11', width=20, height=4)
start_button.pack(side=tk.LEFT)
empty_label_2 = Label(window, width=5)
empty_label_2.pack(side=tk.LEFT)
stop_button = Button(window, text= "Stop pracy",state='disabled', font = 'Arial 11', command=lambda:save('stop'), width=20, height=4)
stop_button.pack(side=tk.LEFT)


load()
clock()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()