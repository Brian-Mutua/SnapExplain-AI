import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from services.export_service import ExportService

class ResultPanel(ctk.CTkFrame):
    """Panel to display analysis results, errors, and export options."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Current result content
        self.current_content = ""
        
        self.create_widgets()

    def create_widgets(self):
        # Header
        self.header_label = ctk.CTkLabel(
            self, 
            text="Analysis Results", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.header_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Textbox for results
        self.result_textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(size=14))
        self.result_textbox.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.result_textbox.insert("0.0", "Upload a screenshot and click 'Analyze Screenshot' to see results here.")
        self.result_textbox.configure(state="disabled") # Read-only
        
        # Action buttons frame
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.grid(row=2, column=0, padx=20, pady=20, sticky="e")
        
        self.copy_btn = ctk.CTkButton(
            self.actions_frame, 
            text="Copy Text", 
            command=self.copy_to_clipboard,
            state="disabled"
        )
        self.copy_btn.pack(side="left", padx=5)
        
        self.save_txt_btn = ctk.CTkButton(
            self.actions_frame, 
            text="Save TXT", 
            command=self.save_as_txt,
            state="disabled"
        )
        self.save_txt_btn.pack(side="left", padx=5)
        
        self.save_pdf_btn = ctk.CTkButton(
            self.actions_frame, 
            text="Save PDF", 
            command=self.save_as_pdf,
            state="disabled"
        )
        self.save_pdf_btn.pack(side="left", padx=5)

    def display_results(self, content: str):
        """Displays the analysis content in the textbox."""
        self.current_content = content
        
        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", content)
        self.result_textbox.configure(state="disabled")
        
        # Enable buttons
        self.copy_btn.configure(state="normal")
        self.save_txt_btn.configure(state="normal")
        self.save_pdf_btn.configure(state="normal")
        
    def display_error(self, error_message: str):
        """Displays an error message in the textbox."""
        self.current_content = ""
        
        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", f"Error: {error_message}")
        self.result_textbox.configure(state="disabled")
        
        # Disable buttons on error
        self.copy_btn.configure(state="disabled")
        self.save_txt_btn.configure(state="disabled")
        self.save_pdf_btn.configure(state="disabled")

    def show_loading(self):
        """Shows a loading state."""
        self.current_content = ""
        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", "Analyzing image... Please wait...")
        self.result_textbox.configure(state="disabled")
        
        self.copy_btn.configure(state="disabled")
        self.save_txt_btn.configure(state="disabled")
        self.save_pdf_btn.configure(state="disabled")

    def copy_to_clipboard(self):
        if self.current_content:
            try:
                ExportService.copy_to_clipboard(self.current_content)
                messagebox.showinfo("Success", "Results copied to clipboard.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_as_txt(self):
        if self.current_content:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                title="Save Results as TXT"
            )
            if filepath:
                try:
                    ExportService.save_as_txt(self.current_content, filepath)
                    messagebox.showinfo("Success", "Results saved as TXT.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def save_as_pdf(self):
        if self.current_content:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")],
                title="Save Results as PDF"
            )
            if filepath:
                try:
                    ExportService.save_as_pdf(self.current_content, filepath)
                    messagebox.showinfo("Success", "Results saved as PDF.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
