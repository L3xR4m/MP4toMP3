import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
from tkinterdnd2 import TkinterDnD, DND_FILES
import ffmpeg
import os
import sys
import re

# Initialize variables with default values
selected_directory = None
selected_files = []
export_directory = None
last_output_directory = None


def center_window(window, width, height):
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y coordinates to position the window
    x = (screen_width - width) / 2
    y = (screen_height - height) / 2

    # Set the dimensions of the window and its position
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

def convert_mp4_to_mp3(input_file, output_file, bitrate):
    global last_output_directory

    if not os.path.isfile(input_file):
        status_label.config(text="Error: Input file does not exist.", fg='red')
        root.update_idletasks()
        return
    if not os.path.isdir(os.path.dirname(output_file)):
        status_label.config(text="Error: Output directory does not exist.", fg='red')
        root.update_idletasks()
        return

    probe = ffmpeg.probe(input_file)
    duration = float(probe['format']['duration'])

    try:
        process = (
            ffmpeg
            .input(input_file)
            .output(output_file, audio_bitrate=bitrate)
            .overwrite_output()
            .run_async(pipe_stdout=True, pipe_stderr=True)
        )

        time_pattern = re.compile(r"time=(\d+:\d+:\d+\.\d+)")

        status_label.config(text="Converting...", fg='yellow')
        root.update_idletasks()
        while True:
            output = process.stderr.readline().decode('utf-8')

            if output == '' and process.poll() is not None:
                break

            if 'time=' in output:
                match = time_pattern.search(output)
                if match:
                    time_str = match.group(1)
                    current_time = sum(float(x) * 60 ** i for i, x in enumerate(reversed(time_str.split(':'))))
                    progress = (current_time / duration) * 100
                    status_label.config(text=f"Converting... {progress:.2f}%")
                    root.update_idletasks()

        # Ensure status label updates after conversion
        status_label.config(text="Conversion Successful!", fg='lightgreen')
        root.update_idletasks()
        last_output_directory = os.path.dirname(output_file)
    except Exception as e:
        status_label.config(text=f"Error: {e}", fg='red')
        root.update_idletasks()


def select_file():
    global export_directory
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if file_path:
        # Clear selected files and add file
        selected_files.clear()
        selected_files.append(file_path)
        # Update the file label to show the selected file
        file_label.config(text=f"Selected File: {os.path.basename(file_path)}")
        # Reset the folder label to "No Folder Selected"
        folder_label.config(text="No Folder Selected")
        # Set the export directory to the selected directory
        export_directory = os.path.dirname(file_path)
        # Reset the status label
        status_label.config(text="Waiting for conversion", fg='yellow')


def open_directory():
    global selected_directory, export_directory
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        # Clear selected files and add files from the selected directory
        selected_files.clear()
        for file_name in os.listdir(selected_directory):
            if file_name.endswith(".mp4"):
                selected_files.append(os.path.join(selected_directory, file_name))
        # Update the folder label to show the selected directory
        folder_label.config(text=f"Selected Directory: {selected_directory}")
        # Reset the file label to "No File Selected"
        file_label.config(text="No File Selected")
        # Set the export directory to the selected directory
        export_directory = selected_directory
        # Reset the status label to "Waiting for conversion"
        status_label.config(text="Waiting for conversion", fg='yellow')


def on_drop(event):
    global export_directory, selected_directory  # Declare selected_directory as global
    # Clean the file path by stripping unwanted characters like '{' and '}'
    dropped_path = event.data.strip(' {}')  # Removes braces and extra spaces
    if os.path.isdir(dropped_path):
        # Use the global selected_directory
        selected_directory = dropped_path
        selected_files.clear()
        # Add all .mp4 files in the directory to the selected files
        for file_name in os.listdir(selected_directory):
            if file_name.endswith(".mp4"):
                selected_files.append(os.path.join(selected_directory, file_name))
        # Update the folder label to show the selected directory
        folder_label.config(text=f"Selected Directory: {selected_directory}")
        # Reset the file label to "No File Selected"
        file_label.config(text="No File Selected")
        # Set the export directory to the selected directory
        export_directory = selected_directory
        # Update status
        status_label.config(text="Folder dropped, waiting for conversion", fg='yellow')
    elif os.path.isfile(dropped_path) and dropped_path.endswith(".mp4"):
        # If a file is dropped
        selected_files.clear()
        selected_files.append(dropped_path)
        # Update the file label to show the selected file
        file_label.config(text=f"Selected File: {os.path.basename(dropped_path)}")
        # Reset the folder label to "No Directory Selected"
        folder_label.config(text="No Directory Selected")
        # Set the export directory to the file's directory
        export_directory = os.path.dirname(dropped_path)
        # Update status
        status_label.config(text="File dropped, waiting for conversion", fg='yellow')
    else:
        # If the dropped item is not valid, show a warning
        messagebox.showwarning("Invalid File", "Dropped item is not a valid MP4 file or folder.")


def run_conversion():
    global export_directory
    if selected_files:
        status_label.config(text="Converting...", fg='yellow')  # Update status to "Converting..."
        for input_file in selected_files:
            bitrate = bitrate_var.get()
            if export_directory is None:
                export_directory = os.path.dirname(input_file)
            export_directory = str(export_directory)
            input_file = str(input_file)
            output_file = os.path.join(
                export_directory,
                os.path.splitext(os.path.basename(input_file))[0] + "_" + bitrate + ".mp3"
            )
            output_file = str(output_file)
            convert_mp4_to_mp3(input_file, output_file, bitrate)
    else:
        messagebox.showwarning("No Files", "No MP4 files selected for conversion.")
        status_label.config(text="Choose a source file or folder", fg='red')

def specify_export_directory():
    global export_directory
    export_directory = filedialog.askdirectory()
    if export_directory:
        export_label.config(text=f"Export Directory: {export_directory}")

def open_destination():
    if export_directory:
        if isinstance(export_directory, str) and export_directory:
            os.startfile(export_directory)
        else:
            messagebox.showwarning("Invalid Directory", "Export directory is not valid.")
    elif last_output_directory:
        if isinstance(last_output_directory, str) and last_output_directory:
            os.startfile(last_output_directory)
        else:
            messagebox.showwarning("Invalid Directory", "Last output directory is not valid.")
    else:
        messagebox.showwarning("No Directory", "No export directory specified and no files converted yet.")

def show_about():
    messagebox.showinfo("About", "MP4 to MP3 Converter\nVersion 1.1\nReleased by L3xR4m")

def exit_application():
    root.destroy()


# noinspection PyProtectedMember
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller-specific
        base_path = sys._MEIPASS  # This is only for PyInstaller packaged version
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


### === /// === ### === /// === ###

# Create the main application window with TkinterDnD
root = TkinterDnD.Tk()
root.title("MP4 to MP3 Converter")

# Set the window size
window_width = 700
window_height = 600

# Center the window
center_window(root, window_width, window_height)

# Load the icon file
icon = PhotoImage(file=resource_path('icon.png'))

# Set the window icon
root.iconphoto(False, icon)

# Define Background Color
background_color = 'grey15'
button_color = 'grey40'

# Apply dark grey theme
root.configure(bg=background_color)

# Font specification
font_name = 'Helvetica'  # Use a known Sans-Serif font

# Create a menu bar
menu_bar = tk.Menu(root, bg=background_color, fg='white')
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0, bg=background_color, fg='white')
menu_bar.add_cascade(label="File", menu=file_menu)
# file_menu.add_command(label="Select File", command=select_file)
# file_menu.add_command(label="Select Directory", command=open_directory)
# file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_application)

# About menu
help_menu = tk.Menu(menu_bar, tearoff=0, bg=background_color, fg='white')
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=show_about)

# Group 1: File and Folder Selection
selection_frame = tk.Frame(root, bg=background_color)
selection_frame.pack(pady=10)

file_label = tk.Label(selection_frame, text="No File Selected", bg=background_color, fg='white', font=(font_name, 12))
file_label.pack(pady=5)

select_file_button = tk.Button(selection_frame, text="Select File", command=select_file, bg=button_color, fg='white', font=(font_name, 12), relief='raised', bd=5)
select_file_button.pack(pady=5)

folder_label = tk.Label(selection_frame, text="No Folder Selected", bg=background_color, fg='white', font=(font_name, 12))
folder_label.pack(pady=5)

select_folder_button = tk.Button(selection_frame, text="Select Folder", command=open_directory, bg=button_color, fg='white', font=(font_name, 12), relief='raised', bd=5)
select_folder_button.pack(pady=5)

# Group 2: Export Directory Selection
export_frame = tk.Frame(root, bg=background_color)
export_frame.pack(pady=10)

export_label = tk.Label(export_frame, text="No Export Directory Selected", bg=background_color, fg='white', font=(font_name, 12))
export_label.pack(pady=5)

select_export_directory_button = tk.Button(export_frame, text="Select Export Directory", command=specify_export_directory, bg=button_color, fg='white', font=(font_name, 12), relief='raised', bd=5)
select_export_directory_button.pack(pady=5)

# Bitrate Selection
bitrate_frame = tk.Frame(root, bg=background_color)
bitrate_frame.pack(pady=10)

bitrate_label = tk.Label(bitrate_frame, text="Select Bitrate:", bg=background_color, fg='white', font=(font_name, 12))
bitrate_label.pack(side=tk.LEFT, padx=5)

bitrate_var = tk.StringVar(root)
bitrate_var.set("192k")

bitrate_options = ["128k", "192k", "256k", "320k"]
bitrate_menu = tk.OptionMenu(bitrate_frame, bitrate_var, *bitrate_options)
bitrate_menu.configure(bg=background_color, fg='white')
bitrate_menu.pack(side=tk.LEFT, padx=5)

# Convert Button and Status
convert_frame = tk.Frame(root, bg=background_color)
convert_frame.pack(pady=10)

convert_button = tk.Button(convert_frame, text="Convert", command=run_conversion, bg=button_color, fg='white', font=(font_name, 16, 'bold'), relief='raised', bd=5)
convert_button.pack(pady=10)

open_destination_button = tk.Button(convert_frame, text="Open Export Directory", command=open_destination, bg=button_color, fg='white', font=(font_name, 10), relief='raised', bd=5)
open_destination_button.pack(pady=0)

status_label = tk.Label(root, text="Choose a source file or folder", bg=background_color, fg='red', font=(font_name, 12))
status_label.pack(pady=5)

# Bind drag-and-drop functionality
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# Start the GUI loop
root.mainloop()
