# Import Libraries
import customtkinter as ctk
from keylogger_app import KeyloggerApp

# Initiate KeyLogger Functions 
keylogger_app = KeyloggerApp()

ctk.set_appearance_mode('dark')
app = ctk.CTk()  # This is the main Tkinter application instance

# Window Configuration
app_width=500
app_height=630
app.update_idletasks()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x_pos = (screen_width // 2) - (app_width // 2)
y_pos = (screen_height // 2) - (app_height // 2)
app.geometry(f'{app_width}x{app_height}+{x_pos}+{y_pos}')
app.resizable(False, False)

# Load Existing JSON Data
keylogger_app.load_existing_data()

# Button Functions
def start_logging():
    keylogger_app.start_logging_event(stats_label, running_label, app)

def stop_logging():
    keylogger_app.stop_logging_event(stats_label, running_label, app)

def show_trends():
    keylogger_app.show_trends_event(stats_label)

# Window Frames
buffer_frame = ctk.CTkFrame(app, fg_color="#242424", height=0) # Change height to change space between title and top of window
buffer_frame.pack(pady=(0), anchor='center')

title_frame = ctk.CTkFrame(app, fg_color="#242424")
title_frame.pack(pady=10, anchor='center')

start_frame = ctk.CTkFrame(app, fg_color="#242424")
start_frame.pack(pady=10, anchor='center')

trends_frame = ctk.CTkFrame(app, fg_color="#242424")
trends_frame.pack(pady=(0, 0), fill='x', expand=True)

bottom_frame = ctk.CTkFrame(app, fg_color="#242424")
bottom_frame.pack(pady=(90, 0), fill='x', expand=True)

# Window UI Elements
running_label = ctk.CTkLabel(
    app, 
    text="", 
    text_color='green', 
    font=("Open Sans", 14))
running_label.pack(pady=10)

app_title = ctk.CTkLabel(
    title_frame, 
    text="Keystroke Logger Tool", 
    text_color='white', 
    font=("Open Sans", 35, 'bold'))
app_title.pack(pady=(0,0), anchor='n')

app_desc = ctk.CTkLabel(
    title_frame, 
    text="Click the 'Start Logging' button below to begin the program. Minimize the window and let it run in the back", 
    text_color='white', 
    font=("Open Sans", 18), 
    width=350, 
    wraplength=350)
app_desc.pack(pady=(20,0))

stats_label = ctk.CTkLabel(
    title_frame, 
    text="", 
    text_color='white', 
    font=("Open Sans", 18, 'bold'), 
    wraplength=500)
stats_label.pack(pady=20)

start_button = ctk.CTkButton(
    start_frame, 
    text="Start Logging", 
    fg_color='#4C9FFF', 
    font=('Open Sans Bold', 20), 
    text_color='white', 
    width=200, 
    height=100, 
    command=start_logging)
start_button.pack(side='left', pady=10)

stop_button = ctk.CTkButton(
    start_frame, 
    text="Stop Logging", 
    fg_color='#4C9FFF', 
    font=('Open Sans Bold', 20), 
    text_color='white', 
    width=200, 
    height=100, 
    command=stop_logging)
stop_button.pack(side='left', padx=10)

trends_button = ctk.CTkButton(
    trends_frame, 
    text="Show Trends", 
    fg_color='#4C9FFF', 
    font=('Open Sans Bold', 20), 
    text_color='white', 
    width=410, 
    height=70, 
    command=show_trends)
trends_button.pack(pady=(0, 0), anchor='center')

live_stats_button = ctk.CTkButton(
    trends_frame, 
    text="Live Session Stats", 
    fg_color='#4C9FFF', 
    font=('Open Sans Bold', 20), 
    text_color='white', 
    width=410, 
    height=70, 
    command=lambda: keylogger_app.show_live_stats(app))
live_stats_button.pack(pady=(10, 0), anchor='center')

reset_button = ctk.CTkButton(
    bottom_frame, 
    text="Reset Data", 
    fg_color='#FF4C4C', 
    font=('Open Sans Bold', 16, 'bold'), 
    text_color='white', 
    width=50, 
    height=40, 
    command=lambda: keylogger_app.confirm_reset(app, stats_label))
reset_button.pack(side='right')

export_button = ctk.CTkButton(
    bottom_frame, 
    text="Export Data", 
    fg_color='#228b22', 
    font=('Open Sans Bold', 16, 'bold'), 
    text_color='white', 
    width=50, 
    height=40, 
    command=lambda: keylogger_app.export_popup(app))
export_button.pack(side='left')

# Run Application
app.mainloop()
