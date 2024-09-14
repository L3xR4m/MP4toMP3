# 🎶 MP4 to MP3 Converter 🎧

A simple, user-friendly desktop application for converting MP4 video files to MP3 audio files. Built with Python and Tkinter, it supports custom bitrates, drag-and-drop functionality, and directory export options.

## 🚀 Features

    Convert MP4 to MP3: Quickly extract audio from MP4 files.
    Custom Bitrates: Select from multiple audio bitrates (128k, 192k, 256k, 320k).
    Drag-and-Drop Support: Simply drag and drop your MP4 files into the window to start converting.
    Dark Mode: Enjoy a sleek and modern dark-themed interface.
    Export Directory: Choose where the converted files should be saved.
    Batch Conversion: Convert multiple MP4 files from a selected folder.


## 🛠️ Installation

**1. Clone the repository:**
```sh
git clone https://github.com/yourusername/mp4-to-mp3-converter.git
cd mp4-to-mp3-converter
```

**2. Set up a virtual environment (optional but recommended):**

bash

python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`

Install the required dependencies:

bash

pip install -r requirements.txt

Run the application:

bash

    python main.py

📦 Packaging as an Executable

If you want to package the project into an executable for Windows:

    Install PyInstaller:

    bash

pip install pyinstaller

Build the executable:

bash

    pyinstaller --onefile --windowed main.py

    The output executable will be found in the dist/ folder.

📂 Directory Structure

bash

mp4-to-mp3-converter/
│
├── build/                   # Build artifacts created by PyInstaller
├── dist/                    # Contains the executable file after building
├── venv/                    # Python virtual environment (not included in repo)
├── main.py                  # Main application script
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
├── .gitignore               # Files and directories to be ignored by git
└── src/                     # Source files and modules

🖥️ Usage

    Select a File: Use the Select File button to choose an MP4 file or drag-and-drop it into the window.
    Choose Bitrate: Select the desired bitrate from the dropdown.
    Select Export Directory: Specify the output folder for the converted files.
    Convert: Click the Convert button and watch the progress in the status bar.
    Open Export Directory: After conversion, click Open Export Directory to view your MP3 files.

❓ FAQ

    Q: Can I convert multiple files at once?
        A: Yes! Select a directory containing MP4 files, and all of them will be converted.

    Q: Why does my terminal open when I run the .exe?
        A: Make sure you use the --windowed option when building the executable with PyInstaller to prevent the terminal from appearing.

🤝 Contributing

Feel free to fork this project and submit pull requests if you'd like to contribute! Suggestions, bug reports, and feature requests are welcome.
📝 License

This project is licensed under the MIT License - see the LICENSE file for details.