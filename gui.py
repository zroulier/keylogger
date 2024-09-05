# Import Libraries
import customtkinter as ctk
from keylogger_app import KeyloggerApp

# Initiate KeyLogger Functions 
keylogger_app = KeyloggerApp()

# Initiate Application
ctk.set_appearance_mode('dark')
app = ctk.CTk()

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
    keylogger_app.start_logging_event(running_label, time_elapsed_label, app)

def stop_logging():
    keylogger_app.stop_logging_event(running_label, time_elapsed_label, app)

def run_in_background():
    app.withdraw()

# Start the hotkey listener to reopen the window
keylogger_app.start_hotkey_listener(app)

# def show_trends():
#     keylogger_app.show_trends_event()

# Window Frames
title_frame = ctk.CTkFrame(app, fg_color="#242424")
title_frame.pack(pady=0, anchor='center')

buttons_frame = ctk.CTkFrame(app, fg_color="#2E2E2E", corner_radius=50)
buttons_frame.pack(anchor='center', expand=True, padx=10, pady=(25,0))
buttons_frame.configure(border_color='white', border_width=2)

start_frame = ctk.CTkFrame(buttons_frame)
start_frame.pack(pady=(15,20), padx=20, anchor='center', expand=True)

trends_frame = ctk.CTkFrame(buttons_frame)
trends_frame.pack(pady=0, padx=10, anchor='center', expand=True)

sessions_frame = ctk.CTkFrame(buttons_frame)
sessions_frame.pack(pady=(20,15), padx=10, anchor='center', expand=True)

time_frame = ctk.CTkFrame(app, bg_color='#2e2e2e')
time_frame.pack(pady=(0,0))

bottom_frame = ctk.CTkFrame(app, bg_color='#2e2e2e')
bottom_frame.pack(pady=(75, 0), anchor='center', fill='x', expand=True)

# Window UI Elements
time_elapsed_label = ctk.CTkLabel(
    time_frame,
    text='',
    text_color='white',
    bg_color='#242424',
    font=("Open Sans", 14))
time_elapsed_label.pack()

running_label = ctk.CTkLabel(
    title_frame, 
    text="", 
    text_color='green', 
    font=("Open Sans", 14))
running_label.pack(pady=10)

app_title = ctk.CTkLabel(
    title_frame, 
    text="Keystroke Logger Tool", 
    text_color='white', 
    font=("Open Sans", 35, 'bold'))
app_title.pack(anchor='n')

app_desc = ctk.CTkLabel(
    title_frame, 
    text="Click the 'Start Logging' button below to begin the program. Minimize the window and let it run in the back", 
    text_color='white', 
    font=("Open Sans", 18), 
    width=350, 
    wraplength=350)
app_desc.pack(pady=(20,0))

start_button = ctk.CTkButton(
    start_frame, 
    text="Start Logging", 
    fg_color='#4C9FFF',
    bg_color='#2e2e2e',
    font=('Open Sans Bold', 20), 
    text_color='white', 
    width=150, 
    height=75,
    corner_radius=25, 
    command=start_logging)
start_button.pack(side='left', padx=(5,5))

stop_button = ctk.CTkButton(
    start_frame, 
    text="Stop Logging", 
    fg_color='#4C9FFF',
    bg_color='#2e2e2e', 
    font=('Open Sans Bold', 20), 
    text_color='white', 
    width=150, 
    height=75,
    corner_radius=25, 
    command=stop_logging)
stop_button.pack(side='left', padx=(5,5))

trends_button = ctk.CTkButton(
    trends_frame, 
    text="Show Trends", 
    fg_color='#4C9FFF',
    bg_color='#2e2e2e', 
    font=('Open Sans Bold', 20), 
    text_color='white', 
    width=355, 
    height=70,
    corner_radius=25, 
    command=None)
trends_button.pack(anchor='center')

live_stats_button = ctk.CTkButton(
    sessions_frame, 
    text="Live Session Stats", 
    fg_color='#4C9FFF',
    bg_color='#2e2e2e', 
    font=('Open Sans Bold', 20), 
    text_color='white', 
    width=355, 
    height=70,
    corner_radius=25, 
    command=lambda: keylogger_app.show_live_stats(app))
live_stats_button.pack(anchor='center')

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

run_in_background_button = ctk.CTkButton(
    bottom_frame,
    text='Run in Background',
    fg_color='#ffa500',
    font=("Open Sans Bold", 16, 'bold'),
    text_color='white',
    width=280,
    height=40,
    command=run_in_background
)
run_in_background_button.pack(side='left', padx=10)

reset_button = ctk.CTkButton(
    bottom_frame, 
    text="Reset Data", 
    fg_color='#FF4C4C', 
    font=('Open Sans Bold', 16, 'bold'), 
    text_color='white', 
    width=50, 
    height=40, 
    command=lambda: keylogger_app.confirm_reset(app))
reset_button.pack(side='right')

# Run Application
app.mainloop()
