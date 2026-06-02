import customtkinter as ctk
from typing import Callable, List, Dict, Any

class Sidebar(ctk.CTkFrame):
    """Sidebar navigation for history and settings."""

    def __init__(self, master, on_history_select: Callable[[Dict[str, Any]], None], **kwargs):
        super().__init__(master, **kwargs)
        self.on_history_select = on_history_select
        
        self.grid_rowconfigure(2, weight=1) # History list space
        
        self.create_widgets()

    def create_widgets(self):
        # App Title
        self.title_label = ctk.CTkLabel(
            self, 
            text="SnapExplain AI", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Search Entry
        self.search_entry = ctk.CTkEntry(
            self, 
            placeholder_text="Search History..."
        )
        self.search_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.on_search_change)
        
        # History List (Scrollable Frame)
        self.history_frame = ctk.CTkScrollableFrame(self, label_text="Recent Analyses")
        self.history_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        # Settings or Theme toggle
        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=3, column=0, padx=20, pady=(10, 0))
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self, 
            values=["System", "Dark", "Light"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.grid(row=4, column=0, padx=20, pady=(10, 20))
        
        # Will hold the buttons representing history items
        self.history_buttons = []
        self.full_history_data = []

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def update_history(self, history_data: List[Dict[str, Any]]):
        """Updates the history list displayed in the sidebar."""
        self.full_history_data = history_data
        self._render_history_list(history_data)

    def _render_history_list(self, history_data: List[Dict[str, Any]]):
        """Renders the buttons for history items."""
        # Clear existing buttons
        for btn in self.history_buttons:
            btn.destroy()
        self.history_buttons.clear()
        
        for item in reversed(history_data): # Show newest first
            summary_text = item.get("analysis_summary", "Unknown")
            # Truncate summary if too long
            display_text = (summary_text[:30] + '...') if len(summary_text) > 30 else summary_text
            
            btn = ctk.CTkButton(
                self.history_frame,
                text=f"{item.get('timestamp')}\n{display_text}",
                command=lambda i=item: self.on_history_select(i),
                anchor="w",
                height=50,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30")
            )
            btn.pack(fill="x", pady=2)
            self.history_buttons.append(btn)

    def on_search_change(self, event=None):
        """Filters history list based on search input."""
        query = self.search_entry.get().lower()
        if not query:
            self._render_history_list(self.full_history_data)
            return
            
        filtered = []
        for item in self.full_history_data:
            if (query in item.get('screenshot_name', '').lower() or 
                query in item.get('analysis_summary', '').lower() or 
                query in item.get('full_analysis', '').lower()):
                filtered.append(item)
        
        self._render_history_list(filtered)
