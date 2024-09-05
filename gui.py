# Import Libraries
import customtkinter as ctk
from tkinter import messagebox
from keylogger_app import KeyloggerApp

class MainApp:
    def __init__(self, root, keylogger_app):
        self.root = root
        self.keylogger_app = keylogger_app
        self.keylogger_app.load_existing_data() # Preload JSON file
        self.running_label = None
        self.stopwatch_label = None
        self.build_ui()

    def build_ui(self):

        self.configure_window()
        self.build_frames()
        self.build_labels()
        self.build_buttons()
    
    def configure_window(self):
        
        w,h = 500,630
        self.root.update_idletasks()
        ws,hs = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x_pos = (ws // 2) - (w // 2)
        y_pos = (hs // 2) - (h // 2)
        self.root.geometry('%dx%d+%d+%d' % (w,h,x_pos,y_pos))
        self.root.resizable(False, False) # Window not resizable at default

        # self.root.mainloop()

    def build_frames(self):
        
        self.title_frame = ctk.CTkFrame(
            self.root,
            fg_color='#242424')
        self.title_frame.pack(anchor='center')
        
        self.center_frame = ctk.CTkFrame(
            self.root,
            fg_color='#242424',
            border_color='white',
            border_width=2,
            corner_radius=50)
        self.center_frame.pack(anchor='center', expand=True, padx=10, pady=(25,0))
        
        self.stopwatch_frame = ctk.CTkFrame(
            self.root,
            fg_color='#242424')
        self.stopwatch_frame.pack()
        
        self.bottom_frame = ctk.CTkFrame(
            self.root,
            fg_color='#242424')
        self.bottom_frame.pack(pady=(110,0), anchor='center', fill='x')

    def build_labels(self):
        
        running_status_label = ctk.CTkLabel(
            self.title_frame,
            text='',
            font=('Open Sans', 14)
        )
        running_status_label.pack(pady=(0,10))

        ctk.CTkLabel(
            self.title_frame,
            text='Keystroke Logging Tool',
            text_color='white',
            bg_color='#242424',
            font=('Open Sans', 35, 'bold')
        ).pack(pady=(20,0))
        
        ctk.CTkLabel(
            self.root,
            text='Click the Start Logging Button below to begin the program. Minimize the window and let it run in the back',
            text_color='white',
            font=('Open Sans', 18),
            width=350,
            wraplength=350
        ).pack(pady=(20,0))

        #

    def build_buttons(self):
        
        start_button = ctk.CTkButton(
            self.center_frame,
            fg_color='#4C9FFF',
            text='Start Logging',
            width=150,
            height=50,
            corner_radius=25,
            command=None
            ).pack()
        
        stop_button = ctk.CTkButton(
            self.center_frame,
            fg_color='#4C9FFF',
            text='Stop Logging'
        ).pack()

        trends_button = ctk.CTkButton(
            self.center_frame,
            fg_color='#4C9FFF',
            text='Show Trends',
            font=('Open Sans', 20, 'bold'),
            text_color='white',
            width=355,
            height=50,
            corner_radius=25,
            command=None
        )
        trends_button.pack()

        live_stats_button = ctk.CTkButton(
            self.center_frame,
            fg_color='#4C9FFF',
            text='Live Session Stats',
            font=('Open Sans', 20, 'bold'),
            text_color='white',
            width=355,
            height=50,
            corner_radius=50,
            command=None
        )
        live_stats_button.pack()

        settings_button = ctk.CTkButton(
            self.center_frame,
            fg_color='#4C9FFF',
            text='Settings',
            font=('Open Sans', 20, 'bold'),
            text_color='white',
            width=355,
            height=35,
            corner_radius=25,
            command=self.open_settings
        )
        settings_button.pack()

        export_button = ctk.CTkButton(
            self.bottom_frame,
            fg_color='#228b22',
            text='Export Data',
            font=('Open Sans', 16, 'bold'),
            text_color='white',
            width=50,
            height=40,
            command=None
        )
        export_button.pack(side='left')

        run_status_button = ctk.CTkButton(
            self.bottom_frame,
            fg_color='#ffa500',
            text='Run in Background',
            font=('Open Sans', 16, 'bold'),
            text_color='white',
            width=280,
            height=40,
            command=None
        )
        run_status_button.pack(side='bottom', padx=10)

        reset_data_button = ctk.CTkButton(
            self.bottom_frame,
            fg_color='#FF4C4C',
            text='Reset Data',
            font=('Open Sans', 16, 'bold'),
            text_color='white',
            width=50,
            height=40,
            command=None
        )
        reset_data_button.pack(side='right')

    # App Functions
    def open_settings(self):
        SettingsWindow(self.root, self.keylogger_app)



class SettingsWindow:
    def __init__(self, parent, keylogger_app):
        self.keylogger_app = keylogger_app
        self.settings_page = ctk.CTkToplevel(parent)
        self.settings_page.geometry('420x300')
        self.settings_page.title('Keylogger Settings')
        self.settings_page.grab_set() # Brings settings window to focus
        self.build_ui()
    
    def build_ui(self):
        
        ctk.CTkLabel(
            self.settings_page,
            text='Keylogger Settings',
            font=('Open Sans', 24, 'bold'),
            text_color='white'
        ).pack(anchor='center', pady=15)

        ctk.CTkLabel(
            self.settings_page,
            text='Toggle Run Mode: ',
            font=('Open Sans', 16),
            text_color='white'
        ).pack(padx=5,pady=5)


def main():
    app = ctk.CTk()
    ctk.set_appearance_mode('dark')

    # Initialize logic
    keylogger_app = KeyloggerApp()

    # Load main page
    main_app = MainApp(app, keylogger_app)

    # Initialize shortcut listener
    keylogger_app.start_hotkey_listener(app)
    app.mainloop()



if __name__ == "__main__":
    main()

# # Initiate KeyLogger Functions 
# keylogger_app = KeyloggerApp()

# # Initiate Application
# ctk.set_appearance_mode('dark')
# app = ctk.CTk()

# # Window Configuration
# app_width=500
# app_height=630
# app.update_idletasks()
# screen_width = app.winfo_screenwidth()
# screen_height = app.winfo_screenheight()
# x_pos = (screen_width // 2) - (app_width // 2)
# y_pos = (screen_height // 2) - (app_height // 2)
# app.geometry(f'{app_width}x{app_height}+{x_pos}+{y_pos}')
# # app.resizable(False, False)

# # Load Existing JSON Data
# keylogger_app.load_existing_data()

# # Button Functions
# def start_logging():
#     keylogger_app.start_logging_event(running_label, time_elapsed_label, app)

# def stop_logging():
#     keylogger_app.stop_logging_event(running_label, time_elapsed_label, app)

# def run_in_background():
#     app.withdraw()

# def open_settings():
#     settings_popup = ctk.CTkToplevel(app)
#     settings_popup.geometry("400x300")
#     settings_popup.title("Settings")

#     settings_popup.grab_set()

#     settings_label = ctk.CTkLabel(
#         settings_popup,
#         text="Settings Page",
#         font=("Open Sans", 20, 'bold'),
#         text_color='white'
#     )
#     settings_label.pack(pady=20)

#     # Label for changing hotkey
#     hotkey_label = ctk.CTkLabel(
#         settings_popup,
#         text="Change Background Hotkey:",
#         font=("Open Sans", 16),
#         text_color='white'
#     )
#     hotkey_label.pack(pady=10)

#     hotkey_status_label = ctk.CTkLabel(
#         settings_popup,
#         text="Press the button below and then type your new hotkey combination.",
#         font=("Open Sans", 14),
#         text_color='white'
#     )
#     hotkey_status_label.pack(pady=10)

#     # Function to save the new hotkey
#     def capture_hotkey():
#         hotkey_status_label.configure(text="Listening for new hotkey... Press and release keys.")
        
#         # Callback when hotkey is captured
#         def on_hotkey_captured(new_hotkey):
#             keylogger_app.update_hotkey_combination(new_hotkey, app)
#             messagebox.showinfo("Success", f"Hotkey updated to: {new_hotkey}")
#             hotkey_status_label.configure(text=f"Hotkey set to: {new_hotkey}")

#         # Start listening for a new hotkey
#         keylogger_app.listen_for_new_hotkey(on_hotkey_captured)

#     # Button to capture the new hotkey
#     capture_button = ctk.CTkButton(
#         settings_popup,
#         text="Set New Hotkey",
#         command=capture_hotkey,
#         font=("Open Sans Bold", 16),
#         width=150
#     )
#     capture_button.pack(pady=20)

#     # Close button to exit settings
#     close_button = ctk.CTkButton(
#         settings_popup,
#         text="Close",
#         command=settings_popup.destroy,
#         font=("Open Sans Bold", 16),
#         width=150
#     )
#     close_button.pack(pady=10)

# # Start the hotkey listener to reopen the window
# keylogger_app.start_hotkey_listener(app)

# # def show_trends():
# #     keylogger_app.show_trends_event()

# # Window Frames
# title_frame = ctk.CTkFrame(app, fg_color="#242424")
# title_frame.pack(pady=0, anchor='center')

# buttons_frame = ctk.CTkFrame(app, fg_color="#2E2E2E", corner_radius=50)
# buttons_frame.pack(anchor='center', expand=True, padx=10, pady=(25,0))
# buttons_frame.configure(border_color='white', border_width=2)

# start_frame = ctk.CTkFrame(buttons_frame)
# start_frame.pack(pady=(15,10), padx=20, anchor='center', expand=True)

# trends_frame = ctk.CTkFrame(buttons_frame)
# trends_frame.pack(pady=0, padx=10, anchor='center', expand=True)

# sessions_frame = ctk.CTkFrame(buttons_frame)
# sessions_frame.pack(pady=(10,10), padx=10, anchor='center', expand=True)

# settings_frame = ctk.CTkFrame(buttons_frame)
# settings_frame.pack(pady=(0,15), anchor='center', expand=True)

# time_frame = ctk.CTkFrame(app, bg_color='#2e2e2e')
# time_frame.pack(pady=(0,0))

# bottom_frame = ctk.CTkFrame(app, bg_color='#2e2e2e')
# bottom_frame.pack(pady=(110, 0), anchor='center', fill='x', expand=True)

# # Window UI Elements
# time_elapsed_label = ctk.CTkLabel(
#     time_frame,
#     text='',
#     text_color='white',
#     bg_color='#242424',
#     font=("Open Sans", 14))
# time_elapsed_label.pack()

# running_label = ctk.CTkLabel(
#     title_frame, 
#     text="", 
#     text_color='green', 
#     font=("Open Sans", 14))
# running_label.pack(pady=10)

# app_title = ctk.CTkLabel(
#     title_frame, 
#     text="Keystroke Logger Tool", 
#     text_color='white', 
#     font=("Open Sans", 35, 'bold'))
# app_title.pack(anchor='n')

# app_desc = ctk.CTkLabel(
#     title_frame, 
#     text="Click the 'Start Logging' button below to begin the program. Minimize the window and let it run in the back", 
#     text_color='white', 
#     font=("Open Sans", 18), 
#     width=350, 
#     wraplength=350)
# app_desc.pack(pady=(20,0))

# start_button = ctk.CTkButton(
#     start_frame, 
#     text="Start Logging", 
#     fg_color='#4C9FFF',
#     bg_color='#2e2e2e',
#     font=('Open Sans Bold', 20), 
#     text_color='white', 
#     width=150, 
#     height=50,
#     corner_radius=25, 
#     command=start_logging)
# start_button.pack(side='left', padx=(5,5))

# stop_button = ctk.CTkButton(
#     start_frame, 
#     text="Stop Logging", 
#     fg_color='#4C9FFF',
#     bg_color='#2e2e2e', 
#     font=('Open Sans Bold', 20), 
#     text_color='white', 
#     width=150, 
#     height=50,
#     corner_radius=25, 
#     command=stop_logging)
# stop_button.pack(side='left', padx=(5,5))

# trends_button = ctk.CTkButton(
#     trends_frame, 
#     text="Show Trends", 
#     fg_color='#4C9FFF',
#     bg_color='#2e2e2e', 
#     font=('Open Sans Bold', 20), 
#     text_color='white', 
#     width=355, 
#     height=50,
#     corner_radius=25, 
#     command=None)
# trends_button.pack(anchor='center')

# live_stats_button = ctk.CTkButton(
#     sessions_frame, 
#     text="Live Session Stats", 
#     fg_color='#4C9FFF',
#     bg_color='#2e2e2e', 
#     font=('Open Sans Bold', 20), 
#     text_color='white', 
#     width=355, 
#     height=50,
#     corner_radius=25, 
#     command=lambda: keylogger_app.show_live_stats(app))
# live_stats_button.pack(anchor='center')

# settings_button = ctk.CTkButton(
#     settings_frame,
#     text="Settings",
#     fg_color='#4C9FFF',
#     font=('Open Sans Bold', 20),
#     text_color='white',
#     width=355,
#     height=35,
#     corner_radius=25,
#     command=open_settings
# )
# settings_button.pack(anchor='center')


# export_button = ctk.CTkButton(
#     bottom_frame, 
#     text="Export Data", 
#     fg_color='#228b22', 
#     font=('Open Sans Bold', 16, 'bold'), 
#     text_color='white', 
#     width=50, 
#     height=40, 
#     command=lambda: keylogger_app.export_popup(app))
# export_button.pack(side='left')

# run_in_background_button = ctk.CTkButton(
#     bottom_frame,
#     text='Run in Background',
#     fg_color='#ffa500',
#     font=("Open Sans Bold", 16, 'bold'),
#     text_color='white',
#     width=280,
#     height=40,
#     command=run_in_background
# )
# run_in_background_button.pack(side='left', padx=10)

# reset_button = ctk.CTkButton(
#     bottom_frame, 
#     text="Reset Data", 
#     fg_color='#FF4C4C', 
#     font=('Open Sans Bold', 16, 'bold'), 
#     text_color='white', 
#     width=50, 
#     height=40, 
#     command=lambda: keylogger_app.confirm_reset(app))
# reset_button.pack(side='right')

# # Run Application
# app.mainloop()
