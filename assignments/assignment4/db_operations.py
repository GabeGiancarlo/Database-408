#!/usr/bin/env python3
"""
CPSC 408 Assignment 04 - Database Operations
Database operations module for the playlist management system.

Author: [Your Name]
Date: [Current Date]
"""

import sqlite3
import csv
import os
from typing import List, Tuple, Optional

class DatabaseOperations:
    """Handles all database operations for the playlist application."""
    
    def __init__(self, db_path: str = "playlist.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_table()
    
    def connect(self):
        """Establish database connection."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            # Enable foreign key constraints
            self.cursor.execute("PRAGMA foreign_keys = ON")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def create_table(self):
        """Create the songs table if it doesn't exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS songs (
            songID TEXT PRIMARY KEY,
            song_name TEXT NOT NULL,
            artist_name TEXT NOT NULL,
            album_name TEXT NOT NULL,
            release_date TEXT,
            genre TEXT,
            explicit BOOLEAN,
            duration_ms REAL,
            danceability REAL,
            energy REAL,
            valence REAL,
            tempo REAL,
            loudness REAL
        );
        """
        
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("Songs table created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
            raise
    
    def bulk_load_songs(self, csv_file_path: str) -> Tuple[int, int]:
        """
        Load songs from CSV file with duplicate checking.
        
        Args:
            csv_file_path: Path to the CSV file
            
        Returns:
            Tuple of (songs_loaded, duplicates_skipped)
        """
        songs_loaded = 0
        duplicates_skipped = 0
        
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                
                for row in csv_reader:
                    if not row or len(row) < 13:  # Skip empty rows or incomplete data
                        continue
                    
                    song_id = row[0].strip()
                    if not song_id:  # Skip rows with empty song ID
                        continue
                    
                    # Check if song already exists
                    if self.song_exists(song_id):
                        duplicates_skipped += 1
                        continue
                    
                    # Parse the row data
                    song_data = self._parse_csv_row(row)
                    if song_data:
                        if self.insert_song(song_data):
                            songs_loaded += 1
                        else:
                            print(f"Failed to insert song: {song_data[1]}")
            
            self.connection.commit()
            return songs_loaded, duplicates_skipped
            
        except Exception as e:
            print(f"Error loading songs from CSV: {e}")
            self.connection.rollback()
            raise
    
    def _parse_csv_row(self, row: List[str]) -> Optional[Tuple]:
        """Parse a CSV row into song data tuple."""
        try:
            song_id = row[0].strip()
            song_name = row[1].strip()
            artist_name = row[2].strip()
            album_name = row[3].strip()
            release_date = row[4].strip()
            genre = row[5].strip()
            explicit = row[6].strip().lower() == 'true'
            duration_ms = float(row[7]) if row[7] else None
            danceability = float(row[8]) if row[8] else None
            energy = float(row[9]) if row[9] else None
            valence = float(row[10]) if row[10] else None
            tempo = float(row[11]) if row[11] else None
            loudness = float(row[12]) if row[12] else None
            
            return (song_id, song_name, artist_name, album_name, release_date, 
                   genre, explicit, duration_ms, danceability, energy, 
                   valence, tempo, loudness)
        except (ValueError, IndexError) as e:
            print(f"Error parsing row: {e}")
            return None
    
    def song_exists(self, song_id: str) -> bool:
        """Check if a song with the given ID already exists."""
        query = "SELECT COUNT(*) FROM songs WHERE songID = ?"
        try:
            self.cursor.execute(query, (song_id,))
            count = self.cursor.fetchone()[0]
            return count > 0
        except sqlite3.Error as e:
            print(f"Error checking if song exists: {e}")
            return False
    
    def insert_song(self, song_data: Tuple) -> bool:
        """Insert a single song into the database."""
        insert_query = """
        INSERT INTO songs (songID, song_name, artist_name, album_name, release_date,
                          genre, explicit, duration_ms, danceability, energy,
                          valence, tempo, loudness)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        try:
            self.cursor.execute(insert_query, song_data)
            return True
        except sqlite3.Error as e:
            print(f"Error inserting song: {e}")
            return False
    
    def get_all_songs(self) -> List[Tuple]:
        """Retrieve all songs from the database."""
        query = "SELECT * FROM songs ORDER BY song_name"
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving all songs: {e}")
            return []
    
    def search_songs_by_name(self, song_name: str) -> List[Tuple]:
        """Search for songs by name (case-insensitive partial match)."""
        query = "SELECT * FROM songs WHERE LOWER(song_name) LIKE LOWER(?) ORDER BY song_name"
        try:
            self.cursor.execute(query, (f"%{song_name}%",))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error searching songs by name: {e}")
            return []
    
    def get_song_by_id(self, song_id: str) -> Optional[Tuple]:
        """Get a specific song by its ID."""
        query = "SELECT * FROM songs WHERE songID = ?"
        try:
            self.cursor.execute(query, (song_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving song by ID: {e}")
            return None
    
    def update_song_field(self, song_id: str, field_choice: str, new_value: str) -> bool:
        """Update a specific field of a song."""
        field_mapping = {
            "1": "song_name",
            "2": "album_name", 
            "3": "artist_name",
            "4": "release_date",
            "5": "explicit"
        }
        
        field_name = field_mapping.get(field_choice)
        if not field_name:
            return False
        
        # Handle explicit field conversion
        if field_name == "explicit":
            if new_value.lower() in ['true', '1', 'yes', 'y']:
                new_value = 1
            elif new_value.lower() in ['false', '0', 'no', 'n']:
                new_value = 0
            else:
                print("Invalid value for explicit field. Use true/false, yes/no, or 1/0.")
                return False
        
        query = f"UPDATE songs SET {field_name} = ? WHERE songID = ?"
        try:
            self.cursor.execute(query, (new_value, song_id))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating song field: {e}")
            self.connection.rollback()
            return False
    
    def search_songs_by_criteria(self, criteria_type: str, search_value: str) -> List[Tuple]:
        """Search songs by album, artist, or genre."""
        if criteria_type == "album":
            query = "SELECT * FROM songs WHERE LOWER(album_name) LIKE LOWER(?) ORDER BY song_name"
        elif criteria_type == "artist":
            query = "SELECT * FROM songs WHERE LOWER(artist_name) LIKE LOWER(?) ORDER BY song_name"
        elif criteria_type == "genre":
            query = "SELECT * FROM songs WHERE LOWER(genre) LIKE LOWER(?) ORDER BY song_name"
        else:
            return []
        
        try:
            self.cursor.execute(query, (f"%{search_value}%",))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error searching songs by {criteria_type}: {e}")
            return []
    
    def bulk_update_songs(self, songs: List[Tuple], field_choice: str, new_value: str) -> bool:
        """Bulk update multiple songs."""
        field_mapping = {
            "1": "song_name",
            "2": "album_name",
            "3": "artist_name", 
            "4": "release_date",
            "5": "explicit"
        }
        
        field_name = field_mapping.get(field_choice)
        if not field_name:
            return False
        
        # Handle explicit field conversion
        if field_name == "explicit":
            if new_value.lower() in ['true', '1', 'yes', 'y']:
                new_value = 1
            elif new_value.lower() in ['false', '0', 'no', 'n']:
                new_value = 0
            else:
                print("Invalid value for explicit field. Use true/false, yes/no, or 1/0.")
                return False
        
        try:
            song_ids = [song[0] for song in songs]  # songID is the first column
            placeholders = ','.join(['?' for _ in song_ids])
            query = f"UPDATE songs SET {field_name} = ? WHERE songID IN ({placeholders})"
            
            self.cursor.execute(query, [new_value] + song_ids)
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error bulk updating songs: {e}")
            self.connection.rollback()
            return False
    
    def delete_song(self, song_id: str) -> bool:
        """Delete a song by its ID."""
        query = "DELETE FROM songs WHERE songID = ?"
        try:
            self.cursor.execute(query, (song_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting song: {e}")
            self.connection.rollback()
            return False
    
    def get_songs_with_null_values(self) -> List[Tuple]:
        """Get all songs that have at least one NULL value."""
        query = """
        SELECT * FROM songs 
        WHERE songID IS NULL OR song_name IS NULL OR artist_name IS NULL 
           OR album_name IS NULL OR release_date IS NULL OR genre IS NULL 
           OR explicit IS NULL OR duration_ms IS NULL OR danceability IS NULL 
           OR energy IS NULL OR valence IS NULL OR tempo IS NULL OR loudness IS NULL
        ORDER BY song_name
        """
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving songs with NULL values: {e}")
            return []
    
    def delete_songs_with_null_values(self) -> bool:
        """Delete all songs that have at least one NULL value."""
        query = """
        DELETE FROM songs 
        WHERE songID IS NULL OR song_name IS NULL OR artist_name IS NULL 
           OR album_name IS NULL OR release_date IS NULL OR genre IS NULL 
           OR explicit IS NULL OR duration_ms IS NULL OR danceability IS NULL 
           OR energy IS NULL OR valence IS NULL OR tempo IS NULL OR loudness IS NULL
        """
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting songs with NULL values: {e}")
            self.connection.rollback()
            return False
    
    def close(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def __del__(self):
        """Destructor to ensure database connection is closed."""
        try:
            self.close()
        except:
            pass  # Ignore errors during cleanup
