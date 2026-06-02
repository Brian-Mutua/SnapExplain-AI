import json
import os
import logging
from typing import List, Dict, Any

class HistoryManager:
    """Manages the saving and loading of analysis history."""

    def __init__(self, storage_dir: str = "storage", filename: str = "history.json"):
        self.storage_dir = storage_dir
        self.filepath = os.path.join(storage_dir, filename)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """Ensures the storage directory and file exist."""
        try:
            if not os.path.exists(self.storage_dir):
                os.makedirs(self.storage_dir)
            if not os.path.exists(self.filepath):
                with open(self.filepath, 'w', encoding='utf-8') as f:
                    json.dump([], f)
        except Exception as e:
            logging.error(f"Failed to initialize storage: {e}")

    def load_history(self) -> List[Dict[str, Any]]:
        """Loads history from the JSON file."""
        try:
            if not os.path.exists(self.filepath):
                return []
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return []
        except Exception as e:
            logging.error(f"Error loading history: {e}")
            return []

    def save_history(self, history_list: List[Dict[str, Any]]) -> None:
        """Saves the entire history list to the JSON file."""
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(history_list, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Error saving history: {e}")

    def add_entry(self, timestamp: str, screenshot_name: str, analysis_summary: str, full_analysis: str = "") -> None:
        """Adds a new entry to the history."""
        history = self.load_history()
        entry = {
            "timestamp": timestamp,
            "screenshot_name": screenshot_name,
            "analysis_summary": analysis_summary,
            "full_analysis": full_analysis
        }
        history.append(entry)
        self.save_history(history)

    def search_history(self, query: str) -> List[Dict[str, Any]]:
        """Searches history based on a text query."""
        history = self.load_history()
        if not query:
            return history
            
        query = query.lower()
        results = []
        for item in history:
            if (query in item.get('screenshot_name', '').lower() or 
                query in item.get('analysis_summary', '').lower() or 
                query in item.get('full_analysis', '').lower()):
                results.append(item)
        return results
