import json
import os
import csv
import webbrowser
from pynput.keyboard import Key, Listener, Controller
from pynput import keyboard
import string
import nltk
from nltk.corpus import words
import platform
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import datetime, timedelta

# Ensure NLTK word list is downloaded
nltk.download('words')

class KeyloggerApp:
    def __init__(self):
        self.keystroke_data = {}
        self.key_log = {}
        self.word_buffer = []
        self.valid_words = set(words.words())
        self.filename = 'key_log_counts.json'
        self.session_log = {
            "letters": {},
            "numbers": {},
            "other": {},
            "words": {}
        }
        self.listener = None
        self.is_logging = False
        self.running_text_job = None
        self.running_text_index = 0
        self.live_stats_popup = None
        self.live_status_label_popup = None
        self.running_live_stats_job = None
        self.elapsed_time = timedelta(0)
        self.start_time = None
        self.time_elapsed_label = None
        self.stopwatch_running = False
        self.hotkey_listener = None
        self.key_controller = Controller()


    def start_hotkey_listener(self, app):
        """Start a listener to capture the Ctrl+Shift+P key combo and toggle the window."""
        def on_activate():
            if app.state() == 'withdrawn':
                print("Ctrl+Shift+P pressed - Showing the app window")
                app.deiconify()  # Show the app window again
            else:
                print("Ctrl+Shift+P pressed - Hiding the app window")
                app.withdraw()  # Hide the app window

        # Define the hotkey (Ctrl+Shift+P)
        hotkey = keyboard.HotKey(
            keyboard.HotKey.parse('<ctrl>+<shift>+p'),
            on_activate
        )

        def for_canonical(f):
            return lambda k: f(self.hotkey_listener.canonical(k))

        # Create and start the keyboard listener
        self.hotkey_listener = keyboard.Listener(
            on_press=for_canonical(hotkey.press),
            on_release=for_canonical(hotkey.release)
        )
        self.hotkey_listener.start()

    def stop_hotkey_listener(self):
        if self.hotkey_listener:
            self.hotkey_listener.stop()

    def load_existing_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.keystroke_data = json.load(f)
            except json.JSONDecodeError:
                self.keystroke_data = {}
        else:
            self.keystroke_data = {}

    def quick_view_json(self):
        file_path = os.path.abspath(self.filename)
        try:
            firefox_path, chrome_path = None, None
            if platform.system() == "Windows":
                firefox_path = "C:/Program Files/Mozilla Firefox/firefox.exe"
                chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
            elif platform.system() == "Darwin":
                firefox_path = "/Applications/Firefox.app/Contents/MacOS/firefox"
                chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            elif platform.system() == "Linux":
                firefox_path = "/usr/bin/firefox"
                chrome_path = "/usr/bin/google-chrome"

            if firefox_path and os.path.exists(firefox_path):
                subprocess.Popen([firefox_path, file_path])
                return
            if chrome_path and os.path.exists(chrome_path):
                subprocess.Popen([chrome_path, file_path])
                return
            if platform.system() == "Windows":
                subprocess.Popen(["notepad", file_path])
            else:
                print("No supported browser found.")

        except Exception as e:
            print(f"Failed to open the file: {e}")

    def save_to_json(self):
        """Save the key log data to a structured JSON format."""
        structured_data = {
            "total": {
                "total_keys": 0,  # This will hold the total number of keys pressed
                "total_unique_words": len(self.keystroke_data.get("words", {})),  # Total number of unique words
                "total_words_count": self.keystroke_data.get('total_words_count', 0)  # Total word count
            },
            "letters": self.keystroke_data.get('letters', {}),
            "numbers": self.keystroke_data.get('numbers', {}),
            "other": self.keystroke_data.get('other', {}),
            "words": self.keystroke_data.get("words", {})
        }

        # Calculate total keys pressed
        structured_data['total']['total_keys'] = (
            sum(structured_data['letters'].values()) +
            sum(structured_data['numbers'].values()) +
            sum(structured_data['other'].values())
        )

        # Save the restructured data to the JSON file
        with open(self.filename, 'w') as f:
            json.dump(structured_data, f, indent=4)
        print(f"Refreshed {self.filename}")

    def merge_logs(self):
        """Merge the current session's key log with existing data in keystroke_data."""
        for key, value in self.key_log.items():
            if key.isalpha():
                if 'letters' not in self.keystroke_data:
                    self.keystroke_data['letters'] = {}
                self.keystroke_data['letters'][key] = self.keystroke_data['letters'].get(key, 0) + value
            elif key.isdigit():
                if 'numbers' not in self.keystroke_data:
                    self.keystroke_data['numbers'] = {}
                self.keystroke_data['numbers'][key] = self.keystroke_data['numbers'].get(key, 0) + value
            else:
                if 'other' not in self.keystroke_data:
                    self.keystroke_data['other'] = {}
                self.keystroke_data['other'][key] = self.keystroke_data['other'].get(key, 0) + value

        # Words should only be merged once after they are fully typed
        # Do not merge words during periodic save
        self.key_log = {}
        self.session_log = {
            "letters": {},
            "numbers": {},
            "other": {},
            "words": {}
        }

        self.save_to_json()


    def start_logging(self):
        if not self.is_logging:
            self.is_logging = True
            self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
            self.listener.start()



    def stop_logging(self):
        """Stop the logging process."""
        if self.is_logging:
            self.listener.stop()
            self.merge_logs()  # Final merge of the log data
            self.save_to_json()  # Save the final state of the data to JSON
            self.is_logging = False


    def on_press(self, key):
        key_str = None
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)

        # Update the key log for letters, digits, and other keys
        if key_str in self.key_log:
            self.key_log[key_str] += 1
        else:
            self.key_log[key_str] = 1

        if key_str.isalpha():
            self.session_log['letters'][key_str] = self.session_log['letters'].get(key_str, 0) + 1
            self.word_buffer.append(key_str)
        elif key_str.isdigit():
            self.session_log['numbers'][key_str] = self.session_log['numbers'].get(key_str, 0) + 1
        else:
            self.session_log['other'][key_str] = self.session_log['other'].get(key_str, 0) + 1

        # Call check_and_store_word only when space or a boundary key is pressed
        if key == Key.space or key_str == ' ':
            self.check_and_store_word()

    def check_and_store_word(self):
        """Check if the letters in the buffer form a valid word and store it."""
        word = ''.join(self.word_buffer).lower()
        
        # Only process the word if it's not empty
        if word and word in self.valid_words:
            if 'words' not in self.keystroke_data:
                self.keystroke_data['words'] = {}

            # Update the word count in both keystroke_data and session_log
            self.keystroke_data['words'][word] = self.keystroke_data['words'].get(word, 0) + 1
            self.session_log['words'][word] = self.session_log['words'].get(word, 0) + 1

            # Increment total word count
            if 'total_words_count' not in self.keystroke_data:
                self.keystroke_data['total_words_count'] = 0
            self.keystroke_data['total_words_count'] += 1

        # Clear the buffer after processing to prevent double counting
        self.word_buffer = []


    def on_release(self, key):
    # Stop the logging process if ESC key is pressed
        if key == Key.esc:
            self.stop_logging()
            self.stop_running_text()
            return False

    def reset_data(self):
        self.key_log = {}
        self.keystroke_data = {}
        self.session_log = {
            "letters": {},
            "numbers": {},
            "other": {},
            "words": {}
        }
        self.word_buffer = []
        self.save_to_json()

    def update_running_text(self, running_label, app):
        running_states = ["Running. | Press Ctrl+Shift+P to Toggle Window", "Running.. | Press Ctrl+Shift+P to Toggle Window", "Running... | Press Ctrl+Shift+P to Toggle Window"]
        self.running_text_index = (self.running_text_index + 1) % 3
        running_label.configure(text=running_states[self.running_text_index])
        self.running_text_job = app.after(1000, lambda: self.update_running_text(running_label, app))

    def stop_running_text(self, running_label, app):
        """Stop the running text animation."""
        if self.running_text_job is not None:
            app.after_cancel(self.running_text_job)
            self.running_text_job = None
        running_label.configure(text='Key Logging Has Stopped. Resume Program to Continue Tracking', text_color='green')
        app.after(5000, lambda: running_label.configure(text=''))

    def start_stopwatch(self, time_elapsed_label):
        self.elapsed_time = timedelta(0)
        self.start_time = datetime.now()
        self.time_elapsed_label = time_elapsed_label
        self.stopwatch_running = True
        self.update_stopwatch()
    
    def update_stopwatch(self):
        if self.stopwatch_running:
            self.elapsed_time = datetime.now() - self.start_time
            time_str = self.format_time(self.elapsed_time)
            self.time_elapsed_label.configure(text=f'Session Time: {time_str}', text_color='white')
            self.time_elapsed_label.after(1000, self.update_stopwatch)

    def stop_stopwatch(self, time_elapsed_label, app):
        self.stopwatch_running = False
        time_elapsed_label.configure(text_color='#FF4C4C')
        
        def clear_label():
            time_elapsed_label.configure(text='') 

        app.after(5000, clear_label)

    def format_time(self, delta):
        """Formats a timedelta object into a HH:MM:SS string."""
        seconds = int(delta.total_seconds())
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"


    def periodic_save_json(self, app):
        """Periodically save key log data to JSON to prevent data loss."""
        # Merge the logs and save
        self.merge_logs()

        # Only continue if logging is still active
        if self.is_logging:
            self.periodic_save_job = app.after(1000, lambda: self.periodic_save_json(app))

    def show_live_stats(self, app):
        if not self.live_stats_popup or not self.live_stats_popup.winfo_exists():
            self.live_stats_popup = ctk.CTkToplevel(app)
            self.live_stats_popup.geometry("400x500")
            self.live_stats_popup.title("Live Session Stats")

            self.live_status_label_popup = ctk.CTkLabel(self.live_stats_popup, text="", text_color='white', font=("Open Sans", 14), justify='left', anchor='w', wraplength=380)
            self.live_status_label_popup.pack(pady=20)

            self.live_stats_popup.protocol("WM_DELETE_WINDOW", self.stop_live_stats_update)

        live_stats_text = "Key: Count\n"
        live_stats_text += "\n".join([f"{key}: {count}" for key, count in self.session_log.get("letters", {}).items()])
        live_stats_text += "\n\nNumbers:\n"
        live_stats_text += "\n".join([f"{key}: {count}" for key, count in self.session_log.get("numbers", {}).items()])
        live_stats_text += "\n\nOther Keys:\n"
        live_stats_text += "\n".join([f"{key}: {count}" for key, count in self.session_log.get("other", {}).items()])
        live_stats_text += "\n\nWords:\n"
        live_stats_text += "\n".join([f"{word}: {count}" for word, count in self.session_log.get("words", {}).items()])

        self.live_status_label_popup.configure(text=live_stats_text)
        self.running_live_stats_job = app.after(5000, self.show_live_stats)

    def stop_live_stats_update(self, app):
        if self.running_live_stats_job:
            app.after_cancel(self.running_live_stats_job)
            self.running_live_stats_job = None

        if self.live_stats_popup:
            self.live_stats_popup.destroy()
            self.live_stats_popup = None

    def export_popup(self, app):
        popup = ctk.CTkToplevel(app)
        popup.geometry("300x200")
        popup.title("Export Options")

        popup.lift()
        popup.focus_force()
        popup.grab_set()

        label = ctk.CTkLabel(popup, text="Choose an option to export data", font=("Open Sans", 16, 'bold'))
        label.pack(pady=10)

        csv_button = ctk.CTkButton(popup, text="Download CSV", command=lambda: [self.save_csv(), popup.destroy()])
        csv_button.pack(pady=5)

        json_button = ctk.CTkButton(popup, text="Download JSON", command=lambda: [self.save_json(), popup.destroy()])
        json_button.pack(pady=5)

        quick_view_button = ctk.CTkButton(popup, text="Developer View", command=lambda: [self.quick_view_json(), popup.destroy()])
        quick_view_button.pack(pady=5)

    def save_json(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json", 
            filetypes=[("JSON files", "*.json")], 
            initialfile="keystroke_data.json"
        )
        if file_path:
            with open(file_path, 'w') as json_file:
                json.dump(self.keystroke_data, json_file, indent=4)
            print(f"JSON saved at {file_path}")

    def save_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv", 
            filetypes=[("CSV files", "*.csv")], 
            initialfile="keystroke_data.csv"
        )
        if not file_path:
            return

        with open(file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Key/Word', 'Count'])

            for key, value in self.keystroke_data.items():
                if key == 'words':
                    for word, count in value.items():
                        csv_writer.writerow([word, count])
                else:
                    csv_writer.writerow([key, value])
            print(f"CSV saved at {file_path}")

    def confirm_reset(self, app):
        confirm_window = ctk.CTkToplevel(app)
        confirm_window.geometry("300x150")
        confirm_window.title("Confirm Reset")
        confirm_window.lift()
        confirm_window.focus_force()
        confirm_window.grab_set()

        label = ctk.CTkLabel(confirm_window, text="Are you sure you want to continue? This action cannot be reversed", wraplength=175, font=('Open Sans', 16, 'bold'))
        label.pack(pady=10)

        yes_button = ctk.CTkButton(confirm_window, text="Delete All History", fg_color='#FF4C4C', command=lambda: self.reset_and_close(confirm_window))
        yes_button.pack(side="left", padx=10, pady=10)

        no_button = ctk.CTkButton(confirm_window, text="Cancel", fg_color='#4C9FFF', command=confirm_window.destroy)
        no_button.pack(side="right", padx=10, pady=10)

    def reset_and_close(self, window):
        self.reset_data()
        messagebox.showinfo("Confirmation", "Your data has been erased successfully.")
        window.destroy()

    def start_logging_event(self, running_label, time_elapsed_label, app):
        """Start logging keystrokes and reset session log."""
        self.key_log = {}
        self.session_log = {
            "letters": {},
            "numbers": {},
            "other": {},
            "words": {}
        }
        self.start_logging()
        self.update_running_text(running_label, app)
        self.start_stopwatch(time_elapsed_label)
        self.periodic_save_json(app)  # Start periodic saving

    def stop_logging_event(self, running_label, time_elapsed_label, app):
        """Stop logging keystrokes and cancel the periodic save job."""
        self.stop_logging()

        # Cancel the periodic save job if it exists
        if self.periodic_save_job is not None:
            app.after_cancel(self.periodic_save_job)
            self.periodic_save_job = None

        self.stop_running_text(running_label, app)
        self.stop_stopwatch(time_elapsed_label, app)

    def show_trends_event(self):
        """Display trends for the session."""
        trends = self.get_trends()  # Assuming you have a get_trends method