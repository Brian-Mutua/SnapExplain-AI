# SnapExplain AI

SnapExplain AI is an AI-powered desktop application that helps users instantly understand screenshots containing error messages, code, system notifications, or technical issues. It uses Google's Gemini Vision API to analyze images and provide clear, beginner-friendly explanations and step-by-step solutions.

## Features

- **Modern Desktop Interface**: Built with CustomTkinter for a sleek, dark-mode, responsive UI.
- **Easy Uploads**: Supports click-to-upload, drag-and-drop, and clipboard pasting of images.
- **AI Analysis**: Powered by Google Gemini Vision to explain technical issues in simple terms.
- **Structured Results**: Problem summary, root cause, suggested fix, technical details, and prevention tips.
- **Export Options**: Copy to clipboard, save as TXT, or export to PDF.
- **History Management**: Keeps a local history of past analyses with search functionality.

## Prerequisites

- Python 3.12+
- A Google Gemini API Key. You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Installation

1. **Clone or Download the Repository**
2. **Navigate to the Project Directory**
   ```bash
   cd snap_explain_ai
   ```
3. **Create a Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
5. **Configure Environment Variables**
   - Copy `.env.example` to `.env`.
   - Open `.env` and add your Gemini API key:
     ```env
     GEMINI_API_KEY=your_actual_api_key_here
     ```

## Usage

Run the application:
```bash
python app.py
```

## Packaging into a Windows Executable

You can package this application into a standalone `.exe` file using PyInstaller.

1. Ensure PyInstaller is installed (`pip install pyinstaller`).
2. Run the following command from the `snap_explain_ai` directory:
   ```bash
   pyinstaller --noconfirm --onedir --windowed --add-data "assets;assets" app.py
   ```
   *Note: If `tkinterdnd2` causes issues with PyInstaller, you may need to add `--collect-all tkinterdnd2` to the command.*
   
   Updated robust build command:
   ```bash
   pyinstaller --noconfirm --onedir --windowed --add-data "assets;assets" --collect-all tkinterdnd2 app.py
   ```
3. The executable will be located in the `dist/app/` folder.

## Architecture

The project follows a modular, object-oriented design:
- `app.py`: Main entry point.
- `ui/`: CustomTkinter interface components.
- `services/`: Core logic (Gemini API interactions, image processing, exporting).
- `storage/`: Local data management (JSON history).

## Technologies Used
- **Python**
- **CustomTkinter** for UI styling.
- **tkinterdnd2** for drag-and-drop file support.
- **Pillow (PIL)** for image processing.
- **google-generativeai** for Gemini AI integration.
- **ReportLab** for PDF generation.
