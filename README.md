# SnapCraft Screenshot

A Python application that lets you capture a selected area of your screen using `maim`, then applies rounded corners, a subtle drop shadow, and a custom background color to create a polished screenshot image.

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
