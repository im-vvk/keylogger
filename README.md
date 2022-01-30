# keylogger

## Overview

A cross platform advance keylogger app that keep listening key strokes and send data such as formatted key-strokes, data from clipboard over mail including screenshots.

## Features

1. Listen each key-strokes and handles the data accordingly such backspace clears the previous char.

2. Save data in local system.

3. Send the key-strokes in formatted manner and screenshots over given mail to store data remotely.

4. Does have option to execute in anonymous mode, where it removes all the remains such as log files, screenshots.

5. Cross-platform app supports multiple OS.

## Technology Used

- Python

## Library Used

- pynput
- autopy
- clipboard
- socket
- email
- smtplib

## Available backends

- darwin, the default for macOS.

- win32, the default for Windows.

- uinput, an optional backend for Linux requiring root privileges and supporting only keyboards.

- xorg, the default for other operating systems.

- dummy, a non-functional, but importable, backend. This is useful as mouse backend when using the uinput backend.

## How to set-up and run

1. Clone the repo by `git clone https://github.com/im-vvk/Blur-Image-Detection`

2. Run `pip install -r requirements.txt` to install dependencies

3. `python main.py` to run the app.
