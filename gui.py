# Import Libraries
import customtkinter as ctk
from tkinter import messagebox
from keylogger_app import KeyloggerApp

class MainApp:
    def __init__(self, root, keylogger_app):
        self.root = root
        self.keylogger_app = keylogger_app
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
        
        self.top_frame = ctk.CTkFrame(
            self.root,
            fg_color='#242424'
        )
        self.top_frame.pack(anchor='center', fill='x', expand=True, padx=25)

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
            fg_color='green')
        self.stopwatch_frame.pack(pady=(5,50))
        
        self.bottom_frame = ctk.CTkFrame(
            self.root,
            fg_color='#242424')
        self.bottom_frame.pack(fill='x', pady=(0,3))

    def build_labels(self):
        
        self.running_status_label = ctk.CTkLabel(
            self.top_frame,
            text='',
            font=('Open Sans', 12)
        )
        self.running_status_label.pack(side='left')

        ctk.CTkLabel(
            self.title_frame,
            text='Keystroke Logging Tool',
            text_color='white',
            bg_color='#242424',
            font=('Open Sans', 35, 'bold')
        ).pack()
        
        ctk.CTkLabel(
            self.title_frame,
            text='Click the Start Logging Button below to begin the program. Minimize the window and let it run in the back',
            text_color='white',
            font=('Open Sans', 18),
            width=350,
            wraplength=350
        ).pack(pady=(20,0))

        self.stopwatch_label = ctk.CTkLabel(
            self.stopwatch_frame,
            text='placeholder',
            text_color='white',
            bg_color='#242424',
            font=('Open Sans', 14)
        )
        self.stopwatch_label.pack()

        #

    def build_buttons(self):
        
        start_button = ctk.CTkButton(
            self.center_frame,
            fg_color='#4C9FFF',
            font=('Open Sans', 20, 'bold'),
            text='Start Logging',
            width=125,
            height=50,
            corner_radius=25,
            command=self.start_logging
            ).grid(row=0,column=0, padx=(15,5), pady=(20,0))
        
        stop_button = ctk.CTkButton(
            self.center_frame,
            fg_color='#4C9FFF',
            text_color='white',
            font=('Open Sans', 20, 'bold'),
            text='Stop Logging',
            width=125,
            height=50,
            corner_radius=25,
            command=self.stop_logging
        ).grid(row=0, column=1, padx=(5,15), pady=(20,0))

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
        trends_button.grid(row=1, column=0, columnspan=2, padx=10, pady=(25,10))

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
        live_stats_button.grid(row=2, column=0, columnspan=2, padx=10)

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
        settings_button.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 25))

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
        export_button.grid(row=0, column=0, padx=(5,0))

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
        run_status_button.grid(row=0, column=1, padx=5)

        reset_data_button = ctk.CTkButton(
            self.bottom_frame,
            fg_color='#FF4C4C',
            text='Reset Data',
            font=('Open Sans', 16, 'bold'),
            text_color='white',
            width=50,
            height=40,
            command=self.reset_data
        )
        reset_data_button.grid(row=0, column=2, padx=(0,5))

    # App Functions
    def start_logging(self):
        self.keylogger_app.start_logging_event(self.running_status_label, self.stopwatch_label, self.root)

    def stop_logging(self):
        self.keylogger_app.stop_logging_event(self.running_status_label, self.stopwatch_label, self.root)
    
    def open_settings(self):
        SettingsWindow(self.root, self.keylogger_app)
    
    def reset_data(self):
        confirm_window = ctk.CTkToplevel(self.root)
        confirm_window.geometry('300x150')
        confirm_window.title('Confirm Data Reset')
        confirm_window.grab_set()

        ctk.CTkLabel(
            confirm_window,
            text='Are you sure you want to continue? This action cannot be reversed',
            wraplength=175,
            font=('Open Sans', 16, 'bold')
        ).pack(pady=10)

        ctk.CTkButton(
            confirm_window,
            text='Delete ALL History',
            font=('Open Sans', 14, 'bold'),
            fg_color='#FF4C4C',
            command=self.keylogger_app.reset_data
        ).pack(side='left', padx=10, pady=10)

        ctk.CTkButton(
            confirm_window,
            text='Cancel',
            font=('Open Sans', 14, 'bold'),
            fg_color='#4C9FFF',
            command=confirm_window.destroy
        ).pack(side='right', padx=10)


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
    # keylogger_app.start_hotkey_listener(app)
    app.mainloop()



if __name__ == "__main__":
    main()