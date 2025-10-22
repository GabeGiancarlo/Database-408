#!/usr/bin/env python3
"""
CPSC 408 Assignment 04 - Helper Functions
Helper functions module for the playlist management system.

Author: [Your Name]
Date: [Current Date]
"""

from typing import List, Tuple

class Helper:
    """Helper class containing utility functions for the playlist application."""
    
    def __init__(self):
        """Initialize the helper class."""
        pass
    
    def display_songs_table(self, songs: List[Tuple]):
        """
        Display a formatted table of songs.
        
        Args:
            songs: List of song tuples from the database
        """
        if not songs:
            print("No songs to display.")
            return
        
        # Define column headers and widths
        headers = [
            "ID", "Song Name", "Artist", "Album", "Release Date", 
            "Genre", "Explicit", "Duration (ms)", "Danceability", 
            "Energy", "Valence", "Tempo", "Loudness"
        ]
        
        # Calculate column widths
        col_widths = [len(header) for header in headers]
        
        # Adjust widths based on data
        for song in songs:
            for i, value in enumerate(song):
                if value is not None:
                    col_widths[i] = max(col_widths[i], len(str(value)))
        
        # Limit column widths for readability
        max_width = 20
        col_widths = [min(width, max_width) for width in col_widths]
        
        # Print header
        header_row = " | ".join(header.ljust(col_widths[i]) for i, header in enumerate(headers))
        print(header_row)
        print("-" * len(header_row))
        
        # Print data rows
        for song in songs:
            row_data = []
            for i, value in enumerate(song):
                if value is None:
                    display_value = "NULL"
                elif isinstance(value, bool):
                    display_value = "Yes" if value else "No"
                elif isinstance(value, float):
                    display_value = f"{value:.2f}"
                else:
                    display_value = str(value)
                
                # Truncate long values
                if len(display_value) > col_widths[i]:
                    display_value = display_value[:col_widths[i]-3] + "..."
                
                row_data.append(display_value.ljust(col_widths[i]))
            
            print(" | ".join(row_data))
    
    def display_song_details(self, song: Tuple):
        """
        Display detailed information for a single song.
        
        Args:
            song: A single song tuple from the database
        """
        if not song:
            print("No song data to display.")
            return
        
        # Map column indices to field names
        fields = [
            "Song ID", "Song Name", "Artist Name", "Album Name", 
            "Release Date", "Genre", "Explicit", "Duration (ms)",
            "Danceability", "Energy", "Valence", "Tempo", "Loudness"
        ]
        
        print("\n" + "="*50)
        print("SONG DETAILS")
        print("="*50)
        
        for i, field in enumerate(fields):
            value = song[i] if i < len(song) else None
            
            if value is None:
                display_value = "NULL"
            elif isinstance(value, bool):
                display_value = "Yes" if value else "No"
            elif isinstance(value, float):
                display_value = f"{value:.2f}"
            else:
                display_value = str(value)
            
            print(f"{field:15}: {display_value}")
        
        print("="*50)
    
    def format_duration(self, duration_ms: float) -> str:
        """
        Format duration from milliseconds to MM:SS format.
        
        Args:
            duration_ms: Duration in milliseconds
            
        Returns:
            Formatted duration string
        """
        if duration_ms is None:
            return "Unknown"
        
        total_seconds = int(duration_ms / 1000)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        
        return f"{minutes:02d}:{seconds:02d}"
    
    def validate_date(self, date_string: str) -> bool:
        """
        Validate date string format (YYYY-MM-DD).
        
        Args:
            date_string: Date string to validate
            
        Returns:
            True if valid date format, False otherwise
        """
        try:
            parts = date_string.split('-')
            if len(parts) != 3:
                return False
            
            year, month, day = parts
            
            # Check if all parts are numeric
            if not (year.isdigit() and month.isdigit() and day.isdigit()):
                return False
            
            year = int(year)
            month = int(month)
            day = int(day)
            
            # Basic range checks
            if not (1900 <= year <= 2100):
                return False
            if not (1 <= month <= 12):
                return False
            if not (1 <= day <= 31):
                return False
            
            return True
        except:
            return False
    
    def validate_boolean_input(self, value: str) -> bool:
        """
        Validate boolean input from user.
        
        Args:
            value: String input from user
            
        Returns:
            True if valid boolean input, False otherwise
        """
        valid_true = ['true', '1', 'yes', 'y', 't']
        valid_false = ['false', '0', 'no', 'n', 'f']
        
        return value.lower().strip() in valid_true + valid_false
    
    def convert_to_boolean(self, value: str) -> bool:
        """
        Convert string input to boolean.
        
        Args:
            value: String input from user
            
        Returns:
            Boolean value
        """
        true_values = ['true', '1', 'yes', 'y', 't']
        return value.lower().strip() in true_values
    
    def sanitize_input(self, user_input: str) -> str:
        """
        Sanitize user input to prevent SQL injection.
        
        Args:
            user_input: Raw user input
            
        Returns:
            Sanitized input string
        """
        # Remove or escape potentially harmful characters
        sanitized = user_input.replace("'", "''")  # Escape single quotes
        sanitized = sanitized.replace(";", "")     # Remove semicolons
        sanitized = sanitized.replace("--", "")    # Remove SQL comments
        sanitized = sanitized.replace("/*", "")    # Remove block comment starts
        sanitized = sanitized.replace("*/", "")    # Remove block comment ends
        
        return sanitized.strip()
    
    def get_user_confirmation(self, message: str) -> bool:
        """
        Get user confirmation for an action.
        
        Args:
            message: Confirmation message to display
            
        Returns:
            True if user confirms, False otherwise
        """
        while True:
            response = input(f"{message} (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")
    
    def format_file_size(self, file_path: str) -> str:
        """
        Get formatted file size string.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Formatted file size string
        """
        try:
            import os
            size_bytes = os.path.getsize(file_path)
            
            if size_bytes < 1024:
                return f"{size_bytes} B"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.1f} KB"
            else:
                return f"{size_bytes / (1024 * 1024):.1f} MB"
        except:
            return "Unknown"
    
    def truncate_text(self, text: str, max_length: int = 50) -> str:
        """
        Truncate text to specified length with ellipsis.
        
        Args:
            text: Text to truncate
            max_length: Maximum length of the text
            
        Returns:
            Truncated text string
        """
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
