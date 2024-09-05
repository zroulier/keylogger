import customtkinter as ctk
from tkinter import messagebox
from keylogger_app import KeyloggerApp


class MainPage:
    def __init__(self, root, keylogger_app):
        self.root = root
        self.keylogger_app = keylogger_app
        self.running_label = None
        self.time_elapsed_label = None
        self.create_ui()

    def create_ui(self):
        """Configure the main UI layout and components."""
        # Window configuration
        self.configure_window()

        # Load existing JSON data
        self.keylogger_app.load_existing_data()

        # Build UI components
        self.build_frames()
        self.build_labels()
        self.build_buttons()

    def configure_window(self):
        """Configure the main window geometry."""
        app_width, app_height = 500, 630
        self.root.update_idletasks()
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x_pos = (screen_width // 2) - (app_width // 2)
        y_pos = (screen_height // 2) - (app_height // 2)
        self.root.geometry(f'{app_width}x{app_height}+{x_pos}+{y_pos}')
        self.root.resizable(False, False)

    def build_frames(self):
        """Build UI frames."""
        self.title_frame = ctk.CTkFrame(self.root, fg_color="#242424")
        self.title_frame.pack(pady=0, anchor='center')

        self.buttons_frame = ctk.CTkFrame(self.root, fg_color="#2E2E2E", corner_radius=50, border_color='white', border_width=2)
        self.buttons_frame.pack(anchor='center', expand=True, padx=10, pady=(25, 0))

        self.start_frame = ctk.CTkFrame(self.buttons_frame)
        self.start_frame.pack(pady=(15, 10), padx=20, anchor='center', expand=True)

        self.trends_frame = ctk.CTkFrame(self.buttons_frame)
        self.trends_frame.pack(pady=0, padx=10, anchor='center', expand=True)

        self.sessions_frame = ctk.CTkFrame(self.buttons_frame)
        self.sessions_frame.pack(pady=(10, 10), padx=10, anchor='center', expand=True)

        self.settings_frame = ctk.CTkFrame(self.buttons_frame)
        self.settings_frame.pack(pady=(0, 15), anchor='center', expand=True)

        self.time_frame = ctk.CTkFrame(self.root, bg_color='#2e2e2e')
        self.time_frame.pack(pady=(0, 0))

        self.bottom_frame = ctk.CTkFrame(self.root, bg_color='#2e2e2e')
        self.bottom_frame.pack(pady=(110, 0), anchor='center', fill='x', expand=True)

    def build_labels(self):
        """Build UI labels."""
        self.time_elapsed_label = ctk.CTkLabel(self.time_frame, text='', text_color='white', bg_color='#242424', font=("Open Sans", 14))
        self.time_elapsed_label.pack()

        self.running_label = ctk.CTkLabel(self.title_frame, text="", text_color='green', font=("Open Sans", 14))
        self.running_label.pack(pady=10)

        app_title = ctk.CTkLabel(self.title_frame, text="Keystroke Logger Tool", text_color='white', font=("Open Sans", 35, 'bold'))
        app_title.pack(anchor='n')

        app_desc = ctk.CTkLabel(self.title_frame, text="Click the 'Start Logging' button below to begin the program. Minimize the window and let it run in the background", text_color='white', font=("Open Sans", 18), width=350, wraplength=350)
        app_desc.pack(pady=(20, 0))

    def build_buttons(self):
        """Build UI buttons."""
        start_button = ctk.CTkButton(self.start_frame, text="Start Logging", fg_color='#4C9FFF', bg_color='#2e2e2e', font=('Open Sans Bold', 20), text_color='white', width=150, height=50, corner_radius=25, command=self.start_logging)
        start_button.pack(side='left', padx=(5, 5))

        stop_button = ctk.CTkButton(self.start_frame, text="Stop Logging", fg_color='#4C9FFF', bg_color='#2e2e2e', font=('Open Sans Bold', 20), text_color='white', width=150, height=50, corner_radius=25, command=self.stop_logging)
        stop_button.pack(side='left', padx=(5, 5))

        trends_button = ctk.CTkButton(self.trends_frame, text="Show Trends", fg_color='#4C9FFF', bg_color='#2e2e2e', font=('Open Sans Bold', 20), text_color='white', width=355, height=50, corner_radius=25, command=self.show_trends)
        trends_button.pack(anchor='center')

        live_stats_button = ctk.CTkButton(self.sessions_frame, text="Live Session Stats", fg_color='#4C9FFF', bg_color='#2e2e2e', font=('Open Sans Bold', 20), text_color='white', width=355, height=50, corner_radius=25, command=self.show_live_stats)
        live_stats_button.pack(anchor='center')

        settings_button = ctk.CTkButton(self.settings_frame, text="Settings", fg_color='#4C9FFF', font=('Open Sans Bold', 20), text_color='white', width=355, height=35, corner_radius=25, command=self.open_settings)
        settings_button.pack(anchor='center')

        export_button = ctk.CTkButton(self.bottom_frame, text="Export Data", fg_color='#228b22', font=('Open Sans Bold', 16, 'bold'), text_color='white', width=50, height=40, command=self.export_data)
        export_button.pack(side='left')

        run_in_background_button = ctk.CTkButton(self.bottom_frame, text='Run in Background', fg_color='#ffa500', font=("Open Sans Bold", 16, 'bold'), text_color='white', width=280, height=40, command=self.run_in_background)
        run_in_background_button.pack(side='left', padx=10)

        reset_button = ctk.CTkButton(self.bottom_frame, text="Reset Data", fg_color='#FF4C4C', font=('Open Sans Bold', 16, 'bold'), text_color='white', width=50, height=40, command=self.reset_data)
        reset_button.pack(side='right')

    def start_logging(self):
        """Start logging by calling start_logging and updating UI."""
        self.keylogger_app.start_logging()
        self.keylogger_app.update_running_text(self.running_label, self.root)
        self.keylogger_app.start_stopwatch(self.time_elapsed_label)
        self.keylogger_app.periodic_save_json(self.root)

    def stop_logging(self):
        """Stop logging and stop the stopwatch."""
        self.keylogger_app.stop_logging()
        self.keylogger_app.stop_running_text(self.running_label, self.root)
        self.keylogger_app.stop_stopwatch(self.time_elapsed_label, self.root)

    def run_in_background(self):
        """Hide the window to run the keylogger in the background."""
        self.root.withdraw()

    def open_settings(self):
        """Open the settings window."""
        SettingsWindow(self.root, self.keylogger_app)

    def show_trends(self):
        """Placeholder for trends functionality."""
        messagebox.showinfo("Trends", "Trends feature is not implemented yet.")

    def show_live_stats(self):
        """Display live session stats."""
        self.keylogger_app.show_live_stats(self.root)

    def export_data(self):
        """Trigger data export options."""
        self.keylogger_app.export_data(self.root)

    def reset_data(self):
        """Confirm and reset data."""
        self.keylogger_app.confirm_reset(self.root)


class SettingsWindow:
    def __init__(self, parent_app, keylogger_app):
        self.keylogger_app = keylogger_app
        self.settings_popup = ctk.CTkToplevel(parent_app)
        self.settings_popup.geometry("400x300")
        self.settings_popup.title("Settings")
        self.settings_popup.grab_set()
        self.build_ui()

    def build_ui(self):
        """Build the settings window UI."""
        settings_label = ctk.CTkLabel(self.settings_popup, text="Settings Page", font=("Open Sans", 20, 'bold'), text_color='white')
        settings_label.pack(pady=20)

        hotkey_label = ctk.CTkLabel(self.settings_popup, text="Change Background Hotkey:", font=("Open Sans", 16), text_color='white')
        hotkey_label.pack(pady=10)

        self.hotkey_status_label = ctk.CTkLabel(self.settings_popup, text="Press the button below and then type your new hotkey combination.", font=("Open Sans", 14), text_color='white')
        self.hotkey_status_label.pack(pady=10)

        capture_button = ctk.CTkButton(self.settings_popup, text="Set New Hotkey", font=("Open Sans Bold", 16), width=150, command=self.capture_hotkey)
        capture_button.pack(pady=20)

        close_button = ctk.CTkButton(self.settings_popup, text="Close", font=("Open Sans Bold", 16), width=150, command=self.settings_popup.destroy)
        close_button.pack(pady=10)

    def capture_hotkey(self):
        """Capture the new hotkey."""
        self.hotkey_status_label.configure(text="Listening for new hotkey... Press and release keys.")

        def on_hotkey_captured(new_hotkey):
            self.keylogger_app.update_hotkey_combination(new_hotkey)
            messagebox.showinfo("Success", f"Hotkey updated to: {new_hotkey}")
            self.hotkey_status_label.configure(text=f"Hotkey set to: {new_hotkey}")

        self.keylogger_app.listen_for_new_hotkey(on_hotkey_captured)


def main():
    # Initialize the main app
    app = ctk.CTk()
    app.geometry("500x630")
    ctk.set_appearance_mode('dark')

    # Initialize the keylogger functionality
    keylogger_app = KeyloggerApp()

    # Load the main page
    main_page = MainPage(app, keylogger_app)

    # Start the hotkey listener and main loop
    keylogger_app.start_hotkey_listener(app)
    app.mainloop()


if __name__ == "__main__":
    main()
