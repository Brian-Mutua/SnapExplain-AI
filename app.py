import sys
import os
import datetime
import logging
import customtkinter as ctk

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Attempt to import tkinterdnd2 for drag-and-drop support
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    HAS_DND = True
except ImportError:
    HAS_DND = False
    logging.warning("tkinterdnd2 not installed. Drag and drop may not work. Install with pip install tkinterdnd2")

from ui.sidebar import Sidebar
from ui.main_window import MainWindow
from storage.history_manager import HistoryManager

# Set default appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk if not HAS_DND else TkinterDnD.Tk):
    """Main application class for SnapExplain AI."""
    
    def __init__(self):
        super().__init__()

        self.title("SnapExplain AI")
        self.geometry("1100x700")
        self.minsize(900, 600)
        
        # If we use TkinterDnD.Tk, we need to apply ctk settings manually as it overrides CTk
        if HAS_DND:
            self.configure(bg=ctk.ThemeManager.theme["CTk"]["fg_color"][1])
        
        self.history_manager = HistoryManager()

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Initialize UI Components
        self.sidebar = Sidebar(self, on_history_select=self.load_history_item, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.main_window = MainWindow(self, on_analysis_complete=self.save_new_analysis)
        self.main_window.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Load initial history
        self.refresh_history()

    def refresh_history(self):
        """Reloads history from storage and updates the sidebar."""
        history_data = self.history_manager.load_history()
        self.sidebar.update_history(history_data)

    def save_new_analysis(self, screenshot_name: str, summary: str, full_text: str):
        """Callback from MainWindow when a new analysis completes."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history_manager.add_entry(timestamp, screenshot_name, summary, full_text)
        self.refresh_history()

    def load_history_item(self, item: dict):
        """Callback from Sidebar when a history item is clicked."""
        self.main_window.result_panel.display_results(item.get("full_analysis", ""))
        self.main_window.preview_label.configure(text=f"Loaded from history:\n{item.get('screenshot_name')}", image="")
        self.main_window.current_image = None
        self.main_window.analyze_btn.configure(state="disabled")

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
