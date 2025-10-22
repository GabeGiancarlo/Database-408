#!/usr/bin/env python3
"""
CPSC 408 Assignment 04 - Playlist Application
Main application file for the playlist management system.

Author: [Your Name]
Date: [Current Date]
"""

import sqlite3
import os
import sys
from db_operations import DatabaseOperations
from helper import Helper

class PlaylistApp:
    """Main application class for the playlist management system."""
    
    def __init__(self):
        """Initialize the application with database connection."""
        self.db_ops = DatabaseOperations()
        self.helper = Helper()
        self.db_ops.create_table()
    
    def display_menu(self):
        """Display the main menu options."""
        print("\n" + "="*50)
        print("           PLAYLIST MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Load new songs from CSV file")
        print("2. Display all songs")
        print("3. Search songs by name")
        print("4. Update song information")
        print("5. Delete a song")
        print("6. Bulk update songs")
        print("7. Remove songs with NULL values")
        print("8. Exit")
        print("="*50)
    
    def load_new_songs(self):
        """Load new songs from a CSV file with duplicate checking."""
        print("\n--- Load New Songs ---")
        file_path = input("Enter the path to the CSV file: ").strip()
        
        if not os.path.exists(file_path):
            print("Error: File not found!")
            return
        
        try:
            songs_loaded, duplicates_skipped = self.db_ops.bulk_load_songs(file_path)
            print(f"Successfully loaded {songs_loaded} new songs.")
            if duplicates_skipped > 0:
                print(f"Skipped {duplicates_skipped} duplicate songs.")
        except Exception as e:
            print(f"Error loading songs: {str(e)}")
    
    def display_all_songs(self):
        """Display all songs in the database."""
        print("\n--- All Songs ---")
        songs = self.db_ops.get_all_songs()
        if not songs:
            print("No songs found in the database.")
            return
        
        self.helper.display_songs_table(songs)
    
    def search_songs(self):
        """Search for songs by name."""
        print("\n--- Search Songs ---")
        song_name = input("Enter song name to search: ").strip()
        
        if not song_name:
            print("Please enter a valid song name.")
            return
        
        songs = self.db_ops.search_songs_by_name(song_name)
        if not songs:
            print("No songs found matching that name.")
            return
        
        self.helper.display_songs_table(songs)
    
    def update_song(self):
        """Update information for a specific song."""
        print("\n--- Update Song Information ---")
        song_name = input("Enter the name of the song to update: ").strip()
        
        if not song_name:
            print("Please enter a valid song name.")
            return
        
        # Find the song
        songs = self.db_ops.search_songs_by_name(song_name)
        if not songs:
            print("No song found with that name.")
            return
        
        if len(songs) > 1:
            print("Multiple songs found with that name:")
            self.helper.display_songs_table(songs)
            song_id = input("Enter the song ID to update: ").strip()
        else:
            song_id = songs[0][0]  # songID is the first column
        
        # Display current song information
        song = self.db_ops.get_song_by_id(song_id)
        if not song:
            print("Song not found.")
            return
        
        print(f"\nCurrent song information:")
        self.helper.display_song_details(song)
        
        # Get update choice
        print("\nWhat would you like to update?")
        print("1. Song name")
        print("2. Album name")
        print("3. Artist name")
        print("4. Release date")
        print("5. Explicit status")
        print("6. Cancel")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "6":
            return
        
        # Get new value and update
        if choice in ["1", "2", "3", "4", "5"]:
            new_value = input("Enter the new value: ").strip()
            if self.db_ops.update_song_field(song_id, choice, new_value):
                print("Song updated successfully!")
            else:
                print("Error updating song. Please check your input.")
        else:
            print("Invalid choice.")
    
    def delete_song(self):
        """Delete a song from the database."""
        print("\n--- Delete Song ---")
        song_name = input("Enter the name of the song to delete: ").strip()
        
        if not song_name:
            print("Please enter a valid song name.")
            return
        
        # Find the song
        songs = self.db_ops.search_songs_by_name(song_name)
        if not songs:
            print("No song found with that name.")
            return
        
        if len(songs) > 1:
            print("Multiple songs found with that name:")
            self.helper.display_songs_table(songs)
            song_id = input("Enter the song ID to delete: ").strip()
        else:
            song_id = songs[0][0]  # songID is the first column
        
        # Confirm deletion
        song = self.db_ops.get_song_by_id(song_id)
        if song:
            print(f"\nAre you sure you want to delete:")
            self.helper.display_song_details(song)
            confirm = input("Type 'yes' to confirm deletion: ").strip().lower()
            
            if confirm == 'yes':
                if self.db_ops.delete_song(song_id):
                    print("Song deleted successfully!")
                else:
                    print("Error deleting song.")
            else:
                print("Deletion cancelled.")
        else:
            print("Song not found.")
    
    def bulk_update_songs(self):
        """Bulk update songs based on album, artist, or genre."""
        print("\n--- Bulk Update Songs ---")
        print("1. Update by album name")
        print("2. Update by artist name")
        print("3. Update by genre")
        print("4. Cancel")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "4":
            return
        
        if choice == "1":
            search_value = input("Enter album name: ").strip()
            search_type = "album"
        elif choice == "2":
            search_value = input("Enter artist name: ").strip()
            search_type = "artist"
        elif choice == "3":
            search_value = input("Enter genre: ").strip()
            search_type = "genre"
        else:
            print("Invalid choice.")
            return
        
        if not search_value:
            print("Please enter a valid search value.")
            return
        
        # Find matching songs
        songs = self.db_ops.search_songs_by_criteria(search_type, search_value)
        if not songs:
            print(f"No songs found matching {search_type}: {search_value}")
            return
        
        print(f"\nFound {len(songs)} songs matching {search_type}: {search_value}")
        self.helper.display_songs_table(songs)
        
        # Get update choice
        print("\nWhat would you like to update?")
        print("1. Song name")
        print("2. Album name")
        print("3. Artist name")
        print("4. Release date")
        print("5. Explicit status")
        print("6. Cancel")
        
        update_choice = input("Enter your choice (1-6): ").strip()
        
        if update_choice == "6":
            return
        
        if update_choice in ["1", "2", "3", "4", "5"]:
            new_value = input("Enter the new value: ").strip()
            if self.db_ops.bulk_update_songs(songs, update_choice, new_value):
                print(f"Successfully updated {len(songs)} songs!")
            else:
                print("Error updating songs.")
        else:
            print("Invalid choice.")
    
    def remove_null_songs(self):
        """Remove all songs that have at least one NULL value."""
        print("\n--- Remove Songs with NULL Values ---")
        
        # Get songs with NULL values
        null_songs = self.db_ops.get_songs_with_null_values()
        if not null_songs:
            print("No songs with NULL values found.")
            return
        
        print(f"Found {len(null_songs)} songs with NULL values:")
        self.helper.display_songs_table(null_songs)
        
        confirm = input(f"\nAre you sure you want to delete {len(null_songs)} songs? Type 'yes' to confirm: ").strip().lower()
        
        if confirm == 'yes':
            if self.db_ops.delete_songs_with_null_values():
                print(f"Successfully deleted {len(null_songs)} songs with NULL values!")
            else:
                print("Error deleting songs.")
        else:
            print("Deletion cancelled.")
    
    def run(self):
        """Main application loop."""
        print("Welcome to the Playlist Management System!")
        
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-8): ").strip()
            
            if choice == "1":
                self.load_new_songs()
            elif choice == "2":
                self.display_all_songs()
            elif choice == "3":
                self.search_songs()
            elif choice == "4":
                self.update_song()
            elif choice == "5":
                self.delete_song()
            elif choice == "6":
                self.bulk_update_songs()
            elif choice == "7":
                self.remove_null_songs()
            elif choice == "8":
                print("Thank you for using the Playlist Management System!")
                break
            else:
                print("Invalid choice. Please enter a number between 1-8.")
            
            input("\nPress Enter to continue...")

def main():
    """Main entry point of the application."""
    try:
        app = PlaylistApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        print("Goodbye!")

if __name__ == "__main__":
    main()
