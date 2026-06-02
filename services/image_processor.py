import os
from PIL import Image, ImageGrab
import logging
from typing import Optional

class ImageProcessor:
    """Handles image loading, validation, and clipboard extraction."""

    SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.webp')

    @classmethod
    def load_from_path(cls, filepath: str) -> Optional[Image.Image]:
        """Loads an image from a file path."""
        try:
            ext = os.path.splitext(filepath)[1].lower()
            if ext not in cls.SUPPORTED_FORMATS:
                raise ValueError(f"Unsupported image format: {ext}")
            
            image = Image.open(filepath)
            # Convert to RGB to avoid issues with some formats when passing to Gemini
            if image.mode != 'RGB':
                image = image.convert('RGB')
            return image
        except Exception as e:
            logging.error(f"Error loading image from path {filepath}: {e}")
            raise e

    @classmethod
    def load_from_clipboard(cls) -> Optional[Image.Image]:
        """Extracts an image from the clipboard."""
        try:
            image = ImageGrab.grabclipboard()
            if image is None:
                return None
            if isinstance(image, list):
                # Sometimes clipboard contains paths instead of direct images
                if len(image) > 0 and isinstance(image[0], str):
                    return cls.load_from_path(image[0])
                return None
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            return image
        except Exception as e:
            logging.error(f"Error extracting image from clipboard: {e}")
            raise e
