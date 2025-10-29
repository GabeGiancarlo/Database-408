-- CPSC408 In Class Activity: Joins and Set Operators
-- Chinook Database Queries

-- 1) Three different queries to return all tracks and the genres the tracks are in
-- Returns 3503 Rows

-- Query 1a: Using CROSS JOIN
SELECT t.*, g.*
FROM tracks t
CROSS JOIN genres g
WHERE t.GenreId = g.GenreId;

-- Query 1b: Using NATURAL JOIN
SELECT t.*, g.*
FROM tracks t
NATURAL JOIN genres g;

-- Query 1c: Using INNER JOIN
SELECT t.*, g.*
FROM tracks t
INNER JOIN genres g ON t.GenreId = g.GenreId;

-- 2) Query to return all employees that are not assigned as a support rep for a customer
-- Returns 5 Rows
SELECT e.*
FROM employees e
WHERE e.EmployeeId NOT IN (
    SELECT DISTINCT SupportRepId 
    FROM customers 
    WHERE SupportRepId IS NOT NULL
);

-- Alternative approach using LEFT JOIN
SELECT e.*
FROM employees e
LEFT JOIN customers c ON e.EmployeeId = c.SupportRepId
WHERE c.SupportRepId IS NULL;

-- 3) Query to return every track and the playlists they are on
-- Output: track name and playlist name columns only
-- Returns 8715 Rows
SELECT t.Name AS track_name, p.Name AS playlist_name
FROM tracks t
INNER JOIN playlist_track pt ON t.TrackId = pt.TrackId
INNER JOIN playlists p ON pt.PlaylistId = p.PlaylistId;

-- 4) Query to return the artist ID of every artist that has an album
-- Do not return artist IDs of artists that do not have albums
-- Returns 204 Rows
SELECT DISTINCT a.ArtistId
FROM artists a
INNER JOIN albums al ON a.ArtistId = al.ArtistId;

-- Alternative approach using EXISTS
SELECT a.ArtistId
FROM artists a
WHERE EXISTS (
    SELECT 1 
    FROM albums al 
    WHERE al.ArtistId = a.ArtistId
);
