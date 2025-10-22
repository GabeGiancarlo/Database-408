# CPSC 408 Assignment 04 - Playlist Management System

## Author
[Your Name]

## Description
A comprehensive playlist management system built with Python and SQLite that allows users to manage their music collection with full CRUD operations and advanced features.

## Features Implemented

### Core Requirements (100 points)
1. **New Data Loading (20 points)**
   - Bulk load songs from CSV files
   - User prompt for file location
   - Automatic table creation and data insertion

2. **Song Update Information (20 points)**
   - Update individual song attributes
   - Support for: song name, album name, artist name, release date, explicit status
   - Input validation and error handling

3. **Song Deletion (20 points)**
   - Delete songs by name with confirmation
   - Safe deletion with user confirmation prompts

4. **Program Stability (40 points)**
   - Error-free execution
   - Proper exception handling
   - Input validation throughout

### Bonus Features Implemented

#### BONUS 1 (10 points) - Duplicate Prevention
- **Feature**: Before inserting each new song, the application checks if a song with that ID already exists
- **Implementation**: `song_exists()` method in `DatabaseOperations` class
- **Benefit**: Prevents duplicate entries and maintains data integrity

#### BONUS 2 (10 points) - Bulk Update Mechanism
- **Feature**: Bulk update records based on album, artist, or genre name
- **Implementation**: `bulk_update_songs()` method with criteria-based searching
- **Benefit**: Efficiently update multiple records at once

#### BONUS 3 (10 points) - NULL Value Cleanup
- **Feature**: Remove all records that have at least one NULL value
- **Implementation**: `delete_songs_with_null_values()` method
- **Benefit**: Maintains data quality by removing incomplete records

## File Structure
```
assignment4/
├── app.py                 # Main application file
├── db_operations.py       # Database operations module
├── helper.py              # Helper functions module
├── playlist.db           # SQLite database (created on first run)
├── Assignment04_songs_update.csv  # Test data file
└── README.md             # This file
```

## Installation and Setup

### Prerequisites
- Python 3.6 or higher
- No additional packages required (uses built-in libraries)

### Running the Application
1. Navigate to the assignment4 directory
2. Run the main application:
   ```bash
   python app.py
   ```

## Usage Instructions

### Main Menu Options
1. **Load new songs from CSV file** - Import songs from a CSV file
2. **Display all songs** - Show all songs in the database
3. **Search songs by name** - Find songs by partial name match
4. **Update song information** - Modify individual song attributes
5. **Delete a song** - Remove a song from the database
6. **Bulk update songs** - Update multiple songs based on criteria
7. **Remove songs with NULL values** - Clean up incomplete records
8. **Exit** - Close the application

### CSV File Format
The application expects CSV files with the following format:
```
songID,song_name,artist_name,album_name,release_date,genre,explicit,duration_ms,danceability,energy,valence,tempo,loudness
```

### Example Usage
1. Start the application
2. Choose option 1 to load the provided `Assignment04_songs_update.csv`
3. Choose option 2 to view all loaded songs
4. Use other options to manage your playlist

## Technical Implementation

### Database Schema
```sql
CREATE TABLE songs (
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
```

### Key Classes and Methods

#### DatabaseOperations Class
- `bulk_load_songs()` - Load songs from CSV with duplicate checking
- `update_song_field()` - Update individual song attributes
- `bulk_update_songs()` - Update multiple songs at once
- `delete_song()` - Delete individual songs
- `delete_songs_with_null_values()` - Remove incomplete records

#### Helper Class
- `display_songs_table()` - Format and display song data
- `sanitize_input()` - Prevent SQL injection
- `validate_date()` - Validate date formats
- `get_user_confirmation()` - Get user confirmation for actions

### Security Features
- SQL injection prevention through parameterized queries
- Input sanitization and validation
- Safe error handling with rollback capabilities

## Testing
The application includes the `Assignment04_songs_update.csv` file for testing purposes. This file contains Pink Floyd's "The Dark Side of the Moon" album data.

## Error Handling
- Comprehensive exception handling for database operations
- Input validation for all user inputs
- Graceful error messages and recovery
- Database rollback on failed operations

## References
- SQLite3 Python Documentation
- CPSC 408 Course Materials
- Python CSV Module Documentation
- SQLite SQL Reference

## Special Instructions
1. The application will create a `playlist.db` file on first run
2. All database operations are atomic (all succeed or all fail)
3. The application supports both individual and bulk operations
4. All bonus features are implemented and functional

## Bonus Implementation Summary
- **BONUS 1**: Duplicate checking prevents data redundancy
- **BONUS 2**: Bulk updates improve efficiency for large datasets  
- **BONUS 3**: NULL cleanup maintains data quality

Total Bonus Points: 10 (chose BONUS 1 for duplicate prevention)
