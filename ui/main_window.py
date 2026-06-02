import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import threading
from typing import Callable, Optional

from services.image_processor import ImageProcessor
from services.gemini_service import GeminiService
from ui.result_panel import ResultPanel

class MainWindow(ctk.CTkFrame):
    """Main window area for image upload, preview, and analysis."""

    def __init__(self, master, on_analysis_complete: Callable[[str, str, str], None], **kwargs):
        super().__init__(master, **kwargs)
        self.on_analysis_complete = on_analysis_complete
        self.current_image_path = None
        self.current_image = None
        self.gemini_service = GeminiService()

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_widgets()
        
        # Setup clipboard binding
        self.bind_all("<Control-v>", self.paste_from_clipboard)

    def create_widgets(self):
        # Left side: Image Upload & Preview
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=1)

        self.upload_label = ctk.CTkLabel(
            self.left_frame, 
            text="Screenshot Preview", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.upload_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # Image preview area
        self.preview_label = ctk.CTkLabel(
            self.left_frame, 
            text="Drag & Drop image here,\nor paste from clipboard (Ctrl+V)", 
            fg_color=("gray80", "gray25"),
            corner_radius=10
        )
        self.preview_label.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Setup drag and drop if tkinterdnd2 is available
        try:
            self.preview_label.drop_target_register("DND_Files")
            self.preview_label.dnd_bind("<<Drop>>", self.on_drop)
        except Exception as e:
            # Silently fallback if dnd not available
            pass

        # Buttons
        self.upload_btn = ctk.CTkButton(
            self.left_frame, 
            text="Upload Screenshot", 
            command=self.upload_image
        )
        self.upload_btn.grid(row=2, column=0, padx=20, pady=10)

        self.analyze_btn = ctk.CTkButton(
            self.left_frame, 
            text="Analyze Screenshot", 
            command=self.start_analysis,
            fg_color="#2B7A0B",
            hover_color="#3A9A1B",
            state="disabled"
        )
        self.analyze_btn.grid(row=3, column=0, padx=20, pady=(10, 20))

        # Right side: Results Panel
        self.result_panel = ResultPanel(self)
        self.result_panel.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")

    def on_drop(self, event):
        """Handle drag and drop event."""
        # Sometimes tkinterdnd2 wraps paths in curly braces
        file_path = event.data.strip('{}')
        self.load_and_preview_image(file_path)

    def upload_image(self):
        """Open file dialog to upload an image."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.webp")]
        )
        if file_path:
            self.load_and_preview_image(file_path)

    def paste_from_clipboard(self, event=None):
        """Handle Ctrl+V to paste image from clipboard."""
        try:
            image = ImageProcessor.load_from_clipboard()
            if image:
                self.set_image(image, "clipboard_image")
            else:
                messagebox.showinfo("Clipboard", "No image found in clipboard.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to paste from clipboard: {e}")

    def load_and_preview_image(self, file_path: str):
        """Loads image using ImageProcessor and updates preview."""
        try:
            image = ImageProcessor.load_from_path(file_path)
            self.set_image(image, os.path.basename(file_path))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    def set_image(self, image: Image.Image, name: str):
        """Sets the current image and updates the UI preview."""
        self.current_image = image
        self.current_image_path = name
        
        # Resize for preview
        # Calculate aspect ratio to fit within a max size
        max_size = (400, 400)
        img_copy = image.copy()
        img_copy.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        photo = ctk.CTkImage(light_image=img_copy, dark_image=img_copy, size=img_copy.size)
        
        self.preview_label.configure(image=photo, text="")
        self.analyze_btn.configure(state="normal")
        
        # Reset result panel
        self.result_panel.result_textbox.configure(state="normal")
        self.result_panel.result_textbox.delete("0.0", "end")
        self.result_panel.result_textbox.insert("0.0", "Click 'Analyze Screenshot' to proceed.")
        self.result_panel.result_textbox.configure(state="disabled")

    def start_analysis(self):
        """Starts the analysis in a separate thread to prevent UI freezing."""
        if not self.current_image:
            return

        # Check API key configuration first
        if not self.gemini_service.is_configured():
            messagebox.showerror(
                "Missing API Key", 
                "Gemini API key is not configured. Please add it to your .env file."
            )
            return

        self.analyze_btn.configure(state="disabled", text="Analyzing...")
        self.result_panel.show_loading()
        
        # Run analysis in a thread
        threading.Thread(target=self._run_analysis_thread, daemon=True).start()

    def _run_analysis_thread(self):
        """The actual analysis process running in a background thread."""
        try:
            result = self.gemini_service.analyze_image(self.current_image)
            
            # Update UI from main thread
            self.after(0, self._on_analysis_success, result)
        except Exception as e:
            # Update UI from main thread
            self.after(0, self._on_analysis_error, str(e))

    def _on_analysis_success(self, result: str):
        """Called when analysis completes successfully."""
        self.result_panel.display_results(result)
        self.analyze_btn.configure(state="normal", text="Analyze Screenshot")
        
        # Extract a brief summary for history
        summary = "Analysis Complete"
        for line in result.split('\n'):
            if line.strip() and not line.startswith('#'):
                summary = line[:50] + "..."
                break
                
        # Notify app.py to save history
        if self.on_analysis_complete:
            self.on_analysis_complete(self.current_image_path or "Unknown Image", summary, result)

    def _on_analysis_error(self, error_message: str):
        """Called when analysis fails."""
        self.result_panel.display_error(error_message)
        self.analyze_btn.configure(state="normal", text="Analyze Screenshot")
