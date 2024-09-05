
import os
import json
from pynput import keyboard

class KeyloggerApp:
    def __init__(self, hotkey_file='hotkey_config.json', log_file='key_log.json'):
        self.hotkey_file = hotkey_file
        self.log_file = log_file
        self.hotkey_combination = ['<ctrl>', '<shift>', 'P']
        self.key_log = {}
        self.session_log = {"letters": {}, "numbers": {}, "other": {}, "words": {}}
        self.periodic_save_job = None
        self.load_hotkey()

    def load_hotkey(self):
        if os.path.exists(self.hotkey_file):
            with open(self.hotkey_file, 'r') as f:
                data = json.load(f)
                self.hotkey_combination = data.get('hotkey', self.hotkey_combination)  # Default if not found
        else:
            print("No hotkey config file found, using default hotkey.")

    def save_hotkey(self):
        try:
            with open(self.hotkey_file, 'w') as f:
                json.dump({'hotkey': self.hotkey_combination}, f)
        except Exception as e:
            print(f"Error saving hotkey: {e}")

    def key_to_string(self, key):
        key_map = {
            'Key.ctrl_l': '<ctrl>',
            'Key.ctrl_r': '<ctrl>',
            'Key.shift': '<shift>',
            'Key.shift_r': '<shift>',
            'Key.alt_l': '<alt>',
            'Key.alt_r': '<alt>',
            'Key.cmd': '<cmd>',
            'Key.cmd_r': '<cmd>'
        }
        if hasattr(key, 'char') and key.char is not None:
            return key.char  # Return the character itself
        key_str = str(key)
        return key_map.get(key_str, key_str)  # Return mapped key or the original if not found

    def start_hotkey_listener(self, app):
        def on_activate():
            if app.state() == 'withdrawn':
                app.deiconify()  # Show the app window again
            else:
                app.withdraw()  # Hide the app window

        with keyboard.GlobalHotKeys({
            '+'.join(self.hotkey_combination): on_activate
        }) as h:
            h.join()

    def start_logging(self):
        pass  # Code to start key logging using pynput

    def stop_logging(self):
        pass  # Code to stop key logging

    def periodic_save_json(self, app, interval=60):
        self.save_log_to_json()
        self.periodic_save_job = app.after(interval * 1000, lambda: self.periodic_save_json(app))

    def save_log_to_json(self):
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.key_log, f)
        except Exception as e:
            print(f"Error saving log: {e}")

    def reset_data(self):
        self.key_log = {}
        self.session_log = {"letters": {}, "numbers": {}, "other": {}, "words": {}}

    def stop_periodic_save(self, app):
        if self.periodic_save_job is not None:
            app.after_cancel(self.periodic_save_job)
            self.periodic_save_job = None

# Example usage:
# logger_app = KeyloggerApp()
# logger_app.start_logging()
