import json
import os
import csv
from pynput.keyboard import Key, Listener
import customtkinter as ctk
import string
import nltk
from nltk.corpus import words
import platform
import subprocess
from tkinter import filedialog  # For file saving dialogs

# Ensure NLTK word list is downloaded
nltk.download('words')

# Initialize global variables
key_log = {}
word_buffer = []  # To store consecutive letters
valid_words = set(words.words())  # A set of dictionary words for checking typed words
filename = 'key_log_counts.json'
keystroke_data = {}
listener = None  # Global reference to the key listener
is_logging = False  # To track if logging is active
running_text_job = None  # To store the reference to the 'after' job
running_text_index = 0  # To track the state of "Running..." animation

def load_existing_data():
    """Load existing key log data from the JSON file."""
    global keystroke_data
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                keystroke_data = json.load(f)
        except json.JSONDecodeError:
            keystroke_data = {}
    else:
        keystroke_data = {}

def save_to_json():
    """Save the key log data to a structured JSON format."""
    global keystroke_data

    structured_data = {
        "total": {
            "total_keys": 0,  # This will hold the total number of keys pressed
            "total_words": len(keystroke_data.get("words", {}))  # Total number of words captured
        },
        "letters": keystroke_data.get('letters', {}),
        "numbers": keystroke_data.get('numbers', {}),
        "other": keystroke_data.get('other', {}),
        "words": keystroke_data.get("words", {})
    }

    # Calculate total keys pressed
    structured_data['total']['total_keys'] = (
        sum(structured_data['letters'].values()) +
        sum(structured_data['numbers'].values()) +
        sum(structured_data['other'].values())
    )

    # Save the restructured data to the JSON file
    with open(filename, 'w') as f:
        json.dump(structured_data, f, indent=4)
    print(f"Keystroke counts saved to {filename} in restructured format")


# Modify the merge_logs function to use the new structure
def merge_logs():
    """Merge the current session's key log with existing data."""
    global keystroke_data

    # Merge the key_log data into keystroke_data dynamically
    for key, value in key_log.items():
        # Check if it's a letter, number, or other
        if key.isalpha():  # It's a letter
            if 'letters' not in keystroke_data:
                keystroke_data['letters'] = {}
            if key in keystroke_data['letters']:
                keystroke_data['letters'][key] += value
            else:
                keystroke_data['letters'][key] = value
        elif key.isdigit():  # It's a number
            if 'numbers' not in keystroke_data:
                keystroke_data['numbers'] = {}
            if key in keystroke_data['numbers']:
                keystroke_data['numbers'][key] += value
            else:
                keystroke_data['numbers'][key] = value
        else:  # It's a special key (other)
            if 'other' not in keystroke_data:
                keystroke_data['other'] = {}
            if key in keystroke_data['other']:
                keystroke_data['other'][key] += value
            else:
                keystroke_data['other'][key] = value

    # Save the updated keystroke data
    save_to_json()


def start_logging():
    """Start listening for key presses."""
    global listener, is_logging
    if not is_logging:  # Prevent multiple listeners from being started
        is_logging = True
        listener = Listener(on_press=on_press, on_release=on_release)
        listener.start()

def stop_logging():
    """Stop the key listener and stop periodic saving."""
    global listener, is_logging, periodic_save_job
    if is_logging:  # Ensure stop is called only once
        listener.stop()
        merge_logs()
        is_logging = False

        # Stop the periodic save job
        if periodic_save_job is not None:
            app.after_cancel(periodic_save_job)
            periodic_save_job = None


def on_press(key):
    """Handle key press event."""
    global key_log, word_buffer
    key_str = None
    try:
        key_str = key.char  # For alphanumeric keys
    except AttributeError:
        key_str = str(key)  # For special keys

    # Increment key count in the current session log
    if key_str in key_log:
        key_log[key_str] += 1
    else:
        key_log[key_str] = 1

    # Track consecutive letters (words) and store valid ones
    if key_str and key_str in string.ascii_letters:  # If the key is a letter
        word_buffer.append(key_str)
    elif key_str == ' ' or key == Key.space:  # When space is pressed, check the word
        check_and_store_word()

    # Update the key count in keystroke_data dynamically
    if key_str.isalpha():  # It's a letter
        if key_str in keystroke_data.get('letters', {}):
            keystroke_data['letters'][key_str] += 1
        else:
            if 'letters' not in keystroke_data:
                keystroke_data['letters'] = {}
            keystroke_data['letters'][key_str] = 1
    elif key_str.isdigit():  # It's a number
        if key_str in keystroke_data.get('numbers', {}):
            keystroke_data['numbers'][key_str] += 1
        else:
            if 'numbers' not in keystroke_data:
                keystroke_data['numbers'] = {}
            keystroke_data['numbers'][key_str] = 1
    else:  # It's a special key (other)
        if key_str in keystroke_data.get('other', {}):
            keystroke_data['other'][key_str] += 1
        else:
            if 'other' not in keystroke_data:
                keystroke_data['other'] = {}
            keystroke_data['other'][key_str] = 1


def on_release(key):
    """Handle key release event."""
    if key == Key.esc:
        stop_logging()
        stop_running_text()  # Stop the animation when the logger stops
        return False  # Stop listener when ESC is pressed

def check_and_store_word():
    """Check if the letters in the buffer form a valid word and store it."""
    global word_buffer, keystroke_data
    word = ''.join(word_buffer).lower()
    if word in valid_words:
        if 'words' not in keystroke_data:
            keystroke_data['words'] = {}
        if word in keystroke_data['words']:
            keystroke_data['words'][word] += 1
        else:
            keystroke_data['words'][word] = 1
    word_buffer = []  # Reset buffer after checking

def get_stats():
    """Get the current keystroke stats (number of key presses for each key)."""
    return keystroke_data

def get_trends():
    """Display the keystroke trends in a readable format."""
    trend = "\n".join([f"{key}: {count}" for key, count in keystroke_data.items() if key != 'total' and key != 'words'])
    word_trend = "\n".join([f"{word}: {count}" for word, count in keystroke_data.get('words', {}).items()])
    return f"{trend}\nWords:\n{word_trend}\nTotal: {keystroke_data.get('total', 0)}"

def reset_data():
    """Clear all keystroke data (current session and stored data)."""
    global key_log, keystroke_data, word_buffer
    key_log = {}
    keystroke_data = {}
    word_buffer = []
    save_to_json()

# Function to update the "Running. .. ..." label
def update_running_text():
    global running_text_index, running_text_job
    running_states = ["Running.", "Running..", "Running..."]
    running_text_index = (running_text_index + 1) % 3
    running_label.configure(text=running_states[running_text_index])
    # Update the label every 500 milliseconds
    running_text_job = app.after(500, update_running_text)

def stop_running_text():
    """Stop the running text animation."""
    global running_text_job
    if running_text_job is not None:
        app.after_cancel(running_text_job)  # Stop the cyclic updating
        running_text_job = None
    running_label.configure(text="")  # Clear the running label when logging stops

### Quick View Function ###
def quick_view_json():
    """Open the existing JSON file for quick viewing."""
    if os.path.exists(filename):
        # Open the JSON file on the local machine
        open_file(filename)
    else:
        print(f"File {filename} does not exist!")

def open_file(filepath):
    """Open a file on the local machine."""
    if platform.system() == 'Windows':
        os.startfile(filepath)
    elif platform.system() == 'Darwin':  # macOS
        subprocess.Popen(['open', filepath])
    else:  # Linux
        subprocess.Popen(['xdg-open', filepath])

### Popup for Export Options with Quick View ###
def export_popup():
    """Display a popup with options to download CSV, JSON, or Quick View JSON."""
    popup = ctk.CTkToplevel(app)
    popup.geometry("300x200")
    popup.title("Export Options")
    
    # Make sure popup has focus and stays on top
    popup.lift()
    popup.focus_force()
    popup.grab_set()  # Modal dialog behavior

    label = ctk.CTkLabel(popup, text="Choose an option to export data", font=("Open Sans", 16, 'bold'))
    label.pack(pady=10)

    # Button to save CSV
    csv_button = ctk.CTkButton(popup, text="Download CSV", command=lambda: [save_csv(), popup.destroy()])
    csv_button.pack(pady=5)

    # Button to save JSON
    json_button = ctk.CTkButton(popup, text="Download JSON", command=lambda: [save_json(), popup.destroy()])
    json_button.pack(pady=5)

    # Button for Quick View
    quick_view_button = ctk.CTkButton(popup, text="Developer View", command=lambda: [quick_view_json(), popup.destroy()])
    quick_view_button.pack(pady=5)

### Save JSON ###
def save_json():
    """Save JSON data to a user-specified file location with a default file name."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json", 
        filetypes=[("JSON files", "*.json")], 
        initialfile="keystroke_data.json"  # Default file name
    )
    if file_path:
        with open(file_path, 'w') as json_file:
            json.dump(keystroke_data, json_file, indent=4)
        print(f"JSON saved at {file_path}")

### Save CSV ###
def save_csv():
    """Convert JSON data to CSV and save to a user-specified file location with a default file name."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv", 
        filetypes=[("CSV files", "*.csv")], 
        initialfile="keystroke_data.csv"  # Default file name
    )
    if not file_path:
        return

    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Key/Word', 'Count'])  # Header

        # Write keys and counts
        for key, value in keystroke_data.items():
            if key == 'words':
                for word, count in value.items():
                    csv_writer.writerow([word, count])
            else:
                csv_writer.writerow([key, value])
        print(f"CSV saved at {file_path}")

### Confirmation Dialog for Reset ###
def confirm_reset():
    # Create a toplevel window for confirmation
    confirm_window = ctk.CTkToplevel(app)
    confirm_window.geometry("300x150")
    confirm_window.title("Confirm Reset")
    confirm_window.lift()  # Bring the window to the front
    confirm_window.focus_force()
    confirm_window.grab_set()  # Force focus on this window

    label = ctk.CTkLabel(confirm_window, text="This will delete ALL history of keystrokes. Are you sure you want to continue?", wraplength=175, font=('Open Sans', 16, 'bold'))
    label.pack(pady=10)

    # Yes button
    yes_button = ctk.CTkButton(confirm_window, text="Yes", fg_color='#FF4C4C', command=lambda: reset_and_close(confirm_window))
    yes_button.pack(side="left", padx=10, pady=10)

    # No button
    no_button = ctk.CTkButton(confirm_window, text="No", fg_color='#4C9FFF', command=confirm_window.destroy)
    no_button.pack(side="right", padx=10, pady=10)

def reset_and_close(window):
    """Reset the data and close the confirmation window."""
    reset_data()  # Reset the data
    window.destroy()  # Close the confirmation window
    stats_label.configure(text="Data reset successfully.")  # Update the main label

periodic_save_job = None  # Global variable to store the job reference for periodic save

def periodic_save_json():
    """Periodically save key log data to JSON to prevent data loss."""
    global periodic_save_job
    save_to_json()  # Save the data to JSON
    periodic_save_job = app.after(5000, periodic_save_json)  # Call this function every 5 seconds (5000 ms)


### CustomTkinter Example without Class ###
def start_logging_event():
    global key_log
    key_log = {}  # Initialize key_log at the start of each session to avoid overwriting old data
    stats_label.configure(text="Logging keystrokes... Press ESC to stop.")
    start_logging()
    update_running_text()  # Start the animation when the logger starts
    periodic_save_json()  # Start periodic saving



def stop_logging_event():
    stop_logging()
    stats_label.configure(text="Keystrokes saved! Click 'Show Trends' to see the stats.")
    stop_running_text()  # Stop the animation when logging stops

def show_trends_event():
    trends = get_trends()
    stats_label.configure(text=f"Keystroke Trends:\n{trends}")

ctk.set_appearance_mode('dark')
# Main Application using CustomTkinter
app = ctk.CTk()
app.geometry('500x630')
app.resizable(False, False)

# Load existing data at the start
load_existing_data()

# Green label to show running status
running_label = ctk.CTkLabel(
    app,
    text="",
    text_color='green',
    font=("Open Sans", 14))
running_label.pack(pady=10)

# UI Elements
app_title = ctk.CTkLabel(
    app,
    text="Keystroke Logger Tool",
    text_color='white',
    font=("Open Sans", 35,'bold'))
app_title.pack(pady=(0,0), anchor='n')

app_desc = ctk.CTkLabel(
    app,
    text="Click the 'Start Logging' button below to begin the program. Minimize the window and let it run in the back",
    text_color='white',
    font=("Open Sans", 18),
    width=350, wraplength=350)
app_desc.pack(pady=(20,0))

stats_label = ctk.CTkLabel(
    app,
    text="",
    text_color='white',
    font=("Open Sans", 18, 'bold'),
    wraplength=500)
stats_label.pack(pady=20)

# Start and Stop Button Frame

start_frame = ctk.CTkFrame(app, fg_color="#242424")
start_frame.pack(pady=10, anchor='center')

trends_frame = ctk.CTkFrame(app, fg_color="#242424")
trends_frame.pack(pady=(0, 125), fill='x', expand=True)

bottom_frame = ctk.CTkFrame(app, fg_color="#242424")
bottom_frame.pack(pady=0, fill='x', expand=True)

start_button = ctk.CTkButton(start_frame, text="Start Logging", fg_color='#4C9FFF', font=('Open Sans Bold', 20), text_color='white', width=200, height=100, command=start_logging_event)
start_button.pack(side='left', pady=10)

stop_button = ctk.CTkButton(start_frame, text="Stop Logging", fg_color='#4C9FFF', font=('Open Sans Bold', 20), text_color='white', width=200, height=100, command=stop_logging_event)
stop_button.pack(side='left', padx=10)

trends_button = ctk.CTkButton(trends_frame, text="Show Trends", fg_color='#4C9FFF', font=('Open Sans Bold', 20), text_color='white', width=410, height=70, command=show_trends_event)
trends_button.pack(pady=(0, 0), anchor='center')

reset_button = ctk.CTkButton(bottom_frame, text="Reset Data", fg_color='#FF4C4C', font=('Open Sans Bold', 16, 'bold'), text_color='white', width=50, height=40, command=confirm_reset)
reset_button.pack(side='right')

# Add a Button to Export and Choose Format
export_button = ctk.CTkButton(bottom_frame, text="Export Data", fg_color='#228b22', font=('Open Sans Bold', 16, 'bold'), text_color='white', width=50, height=40, command=export_popup)
export_button.pack(side='left')

# Start the application
app.mainloop()
