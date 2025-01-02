# SnapCraft Screenshot

A Python application that lets you capture a selected area of your screen, then applies rounded corners, a subtle drop shadow, and a custom background color to create a polished screenshot image.

## Features

- **Interactive area selection**: Uses `maim -s` so you can select any region on your screen.  
- **Rounded corners**: Adjustable corner radius.  
- **Drop shadow**: Customizable shadow offset, blur iterations, and color.  
- **Background color**: Overlay your screenshot on a colored background (chosen via GUI).

## Requirements

- **Python 3.6+**  
- **maim** (for capturing screenshots)  
- **PIL/Pillow** (for image manipulation)  
- **Tkinter** (for GUI; on Debian/Ubuntu: `sudo apt-get install python3-tk`)  

## Installation

1. **Install dependencies**:

   On Ubuntu/Debian:
   ```bash
   sudo apt-get update
   sudo apt-get install -y maim python3-tk

## Usage

1. **Via Terminal**  
   - **Make the script executable** (if not already):
     ```bash
     chmod +x snap-craft.py
     ```
   - **Run**:
     ```bash
     ./snap-craft.py
     ```
   - This will open the GUI where you can select your screenshot directory, pick a background color, and then take a screenshot.

2. **Double-Click**  
   - Again, make sure the file is **executable**:
     ```bash
     chmod +x snap-craft.py
     ```
   - In many Linux desktop environments, double-clicking an executable file might prompt you to “Run” or “Edit” the file.
   - **Choose “Run”** to open the GUI.  

