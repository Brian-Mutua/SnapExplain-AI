import tkinter as tk
from tkinter import messagebox
from typing import Optional
import logging

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    logging.warning("ReportLab not installed. PDF export will be disabled.")


class ExportService:
    """Handles exporting analysis results to Clipboard, TXT, and PDF."""

    @staticmethod
    def copy_to_clipboard(content: str) -> None:
        """Copies text to the system clipboard."""
        try:
            root = tk.Tk()
            root.withdraw() # Hide the main window
            root.clipboard_clear()
            root.clipboard_append(content)
            root.update() # Keeps the clipboard content after destruction
            root.destroy()
        except Exception as e:
            logging.error(f"Failed to copy to clipboard: {e}")
            raise RuntimeError(f"Clipboard copy failed: {e}")

    @staticmethod
    def save_as_txt(content: str, filepath: str) -> None:
        """Saves content to a plain text file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            logging.error(f"Failed to save TXT: {e}")
            raise RuntimeError(f"TXT save failed: {e}")

    @staticmethod
    def save_as_pdf(content: str, filepath: str) -> None:
        """Saves content to a PDF file."""
        if not REPORTLAB_AVAILABLE:
            raise RuntimeError("ReportLab library is required for PDF export.")

        try:
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
            
            story = []
            
            # Split content by newlines and handle markdown-like headers roughly
            lines = content.split('\n')
            for line in lines:
                if not line.strip():
                    story.append(Spacer(1, 12))
                    continue
                
                # Basic markdown header to PDF style
                if line.startswith('## '):
                    p = Paragraph(line.replace('## ', '<b>', 1) + '</b>', styles['Heading2'])
                elif line.startswith('# '):
                    p = Paragraph(line.replace('# ', '<b>', 1) + '</b>', styles['Heading1'])
                elif line.startswith('**') and line.endswith('**'):
                    p = Paragraph(f"<b>{line[2:-2]}</b>", styles['Normal'])
                else:
                    p = Paragraph(line, styles['Normal'])
                    
                story.append(p)
                story.append(Spacer(1, 6))

            doc.build(story)
        except Exception as e:
            logging.error(f"Failed to save PDF: {e}")
            raise RuntimeError(f"PDF save failed: {e}")
