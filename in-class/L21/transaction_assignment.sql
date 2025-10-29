-- CPSC 408 In Class Assignment - Transactions
-- This file contains all the SQL queries required for the transaction assignment

-- Step 1: Prepare tables and set autocommit to 0
-- Delete CUBA actors to prevent foreign key failures
DELETE film_actor
FROM film_actor
INNER JOIN actor
ON actor.actor_id = film_actor.actor_id
WHERE actor.first_name = 'CUBA';

-- Turn off autocommit
SET autocommit = 0;

-- Step 3: Complete transaction with all required steps
-- a. Start a new transaction
START TRANSACTION;

-- b. Select all actors from the actor table (first select)
SELECT COUNT(*) as actor_count_before_insert FROM actor;

-- c. Insert a new actor with values (999, 'NICOLE', 'STREEP', NOW())
INSERT INTO actor (actor_id, first_name, last_name, last_update) 
VALUES (999, 'NICOLE', 'STREEP', NOW());

-- d. Set a new savepoint
SAVEPOINT after_insert;

-- e. Delete the actor with the first name 'CUBA' from the actors table
DELETE FROM actor WHERE first_name = 'CUBA';

-- f. Select all actors from the actors table again (second select)
SELECT COUNT(*) as actor_count_after_delete FROM actor;

-- g. Roll back to the savepoint you created
ROLLBACK TO SAVEPOINT after_insert;

-- h. Select all actors from the actor table a third time (third select)
SELECT COUNT(*) as actor_count_after_rollback FROM actor;

-- i. Commit the transaction
COMMIT;

-- Step 5: Reset autocommit back to 1
SET autocommit = 1;

-- Analysis of Results:
-- 1. First SELECT (before insert): Shows original count of actors
-- 2. Second SELECT (after delete): Shows count after deleting CUBA actors
-- 3. Third SELECT (after rollback): Shows count after rolling back to savepoint
--    (CUBA actors are restored, but NICOLE STREEP remains)
-- 
-- Final row count: Original count + 1 (NICOLE STREEP was inserted and not rolled back)
-- The rollback only affected the DELETE operation, not the INSERT operation
