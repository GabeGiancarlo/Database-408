-- L18: Outer Joins and Subqueries
-- CPSC408 - Sakila Database

-- OUTER JOINS

-- 1. Show the address IDs of all addresses in the 'California' District that do not have a store.
-- Expected: 9 rows
SELECT a.address_id
FROM address a
LEFT JOIN store s ON a.address_id = s.address_id
WHERE a.district = 'California'
  AND s.store_id IS NULL;

-- 2. Show me all film names and how many stores they are inventoried at.
-- Return all films, even if they are not in stock in any store.
-- Expected: 1000 rows
SELECT 
    f.title AS film_name,
    COUNT(DISTINCT i.store_id) AS store_count
FROM film f
LEFT JOIN inventory i ON f.film_id = i.film_id
GROUP BY f.film_id, f.title
ORDER BY f.film_id;

-- 3. Show me the first names of all actors and the titles of films they are in.
-- All actors should be returned, even if they have no films.
-- Expected: 5462 rows
SELECT 
    a.first_name,
    f.title AS film_title
FROM actor a
LEFT JOIN film_actor fa ON a.actor_id = fa.actor_id
LEFT JOIN film f ON fa.film_id = f.film_id
ORDER BY a.actor_id, f.title;

-- 4. Show me all actorIDs and all filmIDs, matching where the actor has been in the film
-- and still showing all actors and all films who have no matches.
-- Expected: 5465 rows
-- Note: MySQL doesn't have FULL OUTER JOIN, so we use UNION of LEFT and RIGHT JOINs
SELECT 
    a.actor_id,
    f.film_id
FROM actor a
LEFT JOIN film_actor fa ON a.actor_id = fa.actor_id
LEFT JOIN film f ON fa.film_id = f.film_id
UNION
SELECT 
    fa.actor_id,
    f.film_id
FROM film f
LEFT JOIN film_actor fa ON f.film_id = fa.film_id
WHERE fa.actor_id IS NULL
ORDER BY actor_id, film_id;

-- SUBQUERIES

-- 5. Write a query to return the rental duration of each film from the film table.
-- Return a second column in this same query that is the average rental duration of all films.
-- Expected: 1000 rows
SELECT 
    f.film_id,
    f.title,
    f.rental_duration,
    (SELECT AVG(rental_duration) FROM film) AS avg_rental_duration
FROM film f;

-- 6. Write a query to return the number of categories from the film_category table
-- that have over 60 films in them.
-- Expected: 10
SELECT COUNT(*) AS category_count
FROM (
    SELECT category_id, COUNT(*) AS film_count
    FROM film_category
    GROUP BY category_id
    HAVING COUNT(*) > 60
) AS categories_with_many_films;

-- 7. Write a query to return the average payment amount of all payments that were
-- made by customers in Mexico (this will be a long query).
-- Expected: 4.154573
SELECT AVG(p.amount) AS avg_payment_amount
FROM payment p
WHERE p.customer_id IN (
    SELECT c.customer_id
    FROM customer c
    INNER JOIN address a ON c.address_id = a.address_id
    INNER JOIN city ci ON a.city_id = ci.city_id
    INNER JOIN country co ON ci.country_id = co.country_id
    WHERE co.country = 'Mexico'
);

-- 8. Write a query that returns the same result as question 3, using NO subqueries.
-- This is the same as query 3, which already uses LEFT JOINs (no subqueries)
-- Expected: 5462 rows
SELECT 
    a.first_name,
    f.title AS film_title
FROM actor a
LEFT JOIN film_actor fa ON a.actor_id = fa.actor_id
LEFT JOIN film f ON fa.film_id = f.film_id
ORDER BY a.actor_id, f.title;

