import os
import logging
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiService:
    """Service to interact with Google's Gemini Vision API."""

    PROMPT = (
        "You are an expert technical support assistant.\n\n"
        "Analyze the screenshot carefully.\n\n"
        "Return your response in the following format:\n\n"
        "## Problem Summary\n\n"
        "...\n\n"
        "## Root Cause\n\n"
        "...\n\n"
        "## Suggested Fix\n\n"
        "1. \n"
        "2. \n"
        "3. \n\n"
        "## Technical Details\n\n"
        "...\n\n"
        "## Prevention Tips\n\n"
        "...\n\n"
        "Use beginner-friendly language whenever possible."
    )

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logging.warning("GEMINI_API_KEY not found in environment variables.")
        else:
            genai.configure(api_key=self.api_key)
            # Use gemini-1.5-flash as the standard for multimodal tasks
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    def is_configured(self) -> bool:
        """Checks if the API key is configured."""
        return bool(self.api_key and self.api_key.strip() and self.api_key != "your_api_key_here")

    def analyze_image(self, image: Image.Image) -> str:
        """Sends the image and prompt to Gemini and returns the response."""
        if not self.is_configured():
            raise ValueError("Gemini API key is missing or invalid. Please check your .env file.")
        
        try:
            # We don't need to specify the model since it's instantiated in __init__
            response = self.model.generate_content([self.PROMPT, image])
            response.resolve() # Ensure the stream is complete if it was streaming
            return response.text
        except Exception as e:
            logging.error(f"Error communicating with Gemini API: {e}")
            raise Exception(f"Failed to analyze image with AI: {str(e)}")
