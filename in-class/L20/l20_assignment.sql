-- L20 In Class Assignment: Views, Triggers, and Stored Procedures
-- Using the Sakila database for MySQL

-- ============================================================================
-- 1) Create a view that shows all films released in 2006 whose title begins with A.
-- ============================================================================

CREATE OR REPLACE VIEW films_2006_starting_with_a AS
SELECT 
    film_id,
    title,
    description,
    release_year,
    language_id,
    rental_duration,
    rental_rate,
    length,
    replacement_cost,
    rating,
    special_features,
    last_update
FROM film
WHERE release_year = 2006
  AND title LIKE 'A%'
ORDER BY title;

-- ============================================================================
-- 2) Write a query that prints all records from the view created in question 1.
-- ============================================================================

SELECT * FROM films_2006_starting_with_a;

-- ============================================================================
-- 3) Using the below query, create a ratings log table in the Sakila DB. 
--    Then, using this log table, create a trigger AFTER INSERT on the film 
--    table that warns us if a user inserts a movie with an R rating.
-- ============================================================================

-- Create the rating_log table
CREATE TABLE IF NOT EXISTS rating_log(
    user VARCHAR(50),
    action VARCHAR(120)
);

-- Create the trigger
DELIMITER $$

CREATE TRIGGER film_rating_warning
AFTER INSERT ON film
FOR EACH ROW
BEGIN
    IF NEW.rating = 'R' THEN
        INSERT INTO rating_log (user, action)
        VALUES (USER(), CONCAT('Warning: R-rated film inserted - Title: ', NEW.title, ' (Film ID: ', NEW.film_id, ')'));
    END IF;
END$$

DELIMITER ;

-- ============================================================================
-- 4) Create a query to insert an R rated movie into the film table. 
--    What record is inserted into the rating_log table?
-- ============================================================================

-- First, let's check what language_id values exist (we'll need one for the insert)
-- Typically language_id 1 is English, but we'll use a subquery to be safe
INSERT INTO film (
    title,
    description,
    release_year,
    language_id,
    rental_duration,
    rental_rate,
    length,
    replacement_cost,
    rating,
    special_features
) VALUES (
    'A Dangerous Movie',
    'A thrilling action film with intense scenes',
    2024,
    (SELECT language_id FROM language WHERE name = 'English' LIMIT 1),
    3,
    4.99,
    120,
    19.99,
    'R',
    'Trailers,Commentaries'
);

-- Check what was inserted into the rating_log table
SELECT * FROM rating_log;

-- ============================================================================
-- 5) Create a stored procedure that returns the release year of a movie as an 
--    OUT variable, using the title of the movie as an IN variable.
-- ============================================================================

DELIMITER $$

CREATE PROCEDURE get_release_year_by_title(
    IN movie_title VARCHAR(255),
    OUT release_year_result SMALLINT
)
BEGIN
    SELECT release_year INTO release_year_result
    FROM film
    WHERE title = movie_title
    LIMIT 1;
END$$

DELIMITER ;

-- ============================================================================
-- 6) Create a query to call your stored procedure and Select the result
-- ============================================================================

-- Call the stored procedure
SET @movie_year = 0;
CALL get_release_year_by_title('A Dangerous Movie', @movie_year);
SELECT @movie_year AS release_year;

-- Alternative: Call with an existing film title from the database
SET @movie_year = 0;
CALL get_release_year_by_title('ACADEMY DINOSAUR', @movie_year);
SELECT @movie_year AS release_year;

