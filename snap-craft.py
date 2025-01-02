#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime
from PIL import Image, ImageDraw, ImageFilter, ImageColor

import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox

########################################
# Image processing functions
########################################

def round_corners(img, radius=30):
    """Adds rounded corners to the given image."""
    width, height = img.size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # Draw rectangles
    draw.rectangle([radius, 0, width - radius, height], fill=255)
    draw.rectangle([0, radius, width, height - radius], fill=255)

    # Draw corner arcs
    draw.pieslice([0, 0, 2 * radius, 2 * radius], 180, 270, fill=255)  # top-left
    draw.pieslice([width - 2*radius, 0, width, 2*radius], 270, 360, fill=255)  # top-right
    draw.pieslice([0, height - 2*radius, 2*radius, height], 90, 180, fill=255)  # bottom-left
    draw.pieslice([width - 2*radius, height - 2*radius, width, height], 0, 90, fill=255)  # bottom-right

    img.putalpha(mask)
    return img

def add_shadow(
    img,
    offset=(10, 10),
    background_color=(0,0,0,0),
    shadow_color=(0,0,0,80),
    border=50,
    iterations=5
):
    """Adds a blurred shadow behind the given image."""
    total_width = img.size[0] + abs(offset[0]) + border*2
    total_height = img.size[1] + abs(offset[1]) + border*2

    shadow = Image.new("RGBA", (total_width, total_height), background_color)
    shadow_x = border + max(offset[0], 0)
    shadow_y = border + max(offset[1], 0)

    shadow_draw = ImageDraw.Draw(shadow)
    alpha_mask = img.split()[-1]
    shadow_draw.bitmap((shadow_x, shadow_y), alpha_mask, fill=shadow_color)

    for _ in range(iterations):
        shadow = shadow.filter(ImageFilter.BLUR)

    # Paste original image over shadow
    shadow.paste(img, (border, border), img)
    return shadow

########################################
# Main Application (Tkinter GUI)
########################################

class ScreenshotApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Beautiful Screenshot Tool")
        self.geometry("400x250")

        # Default directory (dynamic). Try ~/Pictures/screenshots or fallback to ~/Pictures
        home_dir = os.path.expanduser("~")
        default_dir = os.path.join(home_dir, "Pictures", "screenshots")
        if not os.path.isdir(default_dir):
            # If ~/Pictures/screenshots doesn't exist, use ~/Pictures
            default_dir = os.path.join(home_dir, "Pictures")

        self.screenshot_directory = tk.StringVar(value=default_dir)
        self.bg_color = "#263238"  # default background color (dark grey)

        # Create UI
        self.create_widgets()

    def create_widgets(self):
        # Directory selection
        dir_label = ttk.Label(self, text="Screenshot Directory:")
        dir_label.pack(pady=5)

        dir_frame = ttk.Frame(self)
        dir_frame.pack(pady=5)
        dir_entry = ttk.Entry(dir_frame, textvariable=self.screenshot_directory, width=40)
        dir_entry.pack(side=tk.LEFT, padx=5)
        dir_button = ttk.Button(dir_frame, text="Browse...", command=self.choose_directory)
        dir_button.pack(side=tk.LEFT)

        # Choose color
        color_label = ttk.Label(self, text="Background Color:")
        color_label.pack(pady=5)

        color_frame = ttk.Frame(self)
        color_frame.pack(pady=5)
        color_button = ttk.Button(color_frame, text="Pick a Color", command=self.pick_color)
        color_button.pack(side=tk.LEFT, padx=5)
        self.color_preview = ttk.Label(color_frame, text="  ", background=self.bg_color)
        self.color_preview.pack(side=tk.LEFT, padx=5, ipady=5, ipadx=15)

        # Take screenshot
        screenshot_button = ttk.Button(
            self, text="Take Screenshot", command=self.take_screenshot
        )
        screenshot_button.pack(pady=20)

    def choose_directory(self):
        """Let user pick a directory for storing screenshots."""
        chosen_dir = filedialog.askdirectory(initialdir=self.screenshot_directory.get())
        if chosen_dir:
            self.screenshot_directory.set(chosen_dir)

    def pick_color(self):
        """Open the color chooser dialog to pick a background color."""
        color_tuple = colorchooser.askcolor(color=self.bg_color)
        if color_tuple and color_tuple[1] is not None:
            # color_tuple = ((r, g, b), "#rrggbb")
            self.bg_color = color_tuple[1]
            self.color_preview.configure(background=self.bg_color)

    def take_screenshot(self):
        """Capture screenshot with maim, round corners, add shadow, apply background."""
        # Ensure directory exists
        out_dir = self.screenshot_directory.get()
        if not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir, exist_ok=True)
            except OSError as e:
                messagebox.showerror("Error", f"Could not create directory: {out_dir}\n{e}")
                return

        # Generate a timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(out_dir, f"screenshot_{timestamp}.png")

        temp_file = "temp_screenshot.png"

        # Run maim to select area
        try:
            messagebox.showinfo("Screenshot", "Select the area you want to screenshot...")
            subprocess.run(["maim", "-s", temp_file], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to take screenshot.\n{e}")
            return
        except FileNotFoundError:
            messagebox.showerror("Error", "Could not find 'maim'. Please install maim first.")
            return

        # Process the screenshot
        try:
            img = Image.open(temp_file).convert("RGBA")
            # Round corners
            img = round_corners(img, radius=15)
            # Add shadow
            img = add_shadow(
                img,
                offset=(10, 10),
                background_color=(0, 0, 0, 0),
                shadow_color=(0, 0, 0, 80),
                border=50,
                iterations=5
            )
            # Apply background color
            bg_rgba = self.parse_color(self.bg_color)
            bg = Image.new("RGBA", img.size, bg_rgba)
            final_img = Image.alpha_composite(bg, img)
            final_img.save(output_file, format="PNG")

            messagebox.showinfo("Success", f"Screenshot saved as:\n{output_file}")

        finally:
            # Remove temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)

    @staticmethod
    def parse_color(color_str: str):
        """Convert a color string like '#263238' or 'red' into an RGBA tuple."""
        try:
            return ImageColor.getcolor(color_str, "RGBA")
        except ValueError:
            # fallback if parse fails
            return ImageColor.getcolor("#263238", "RGBA")


def main():
    app = ScreenshotApp()
    app.mainloop()

if __name__ == "__main__":
    main()

