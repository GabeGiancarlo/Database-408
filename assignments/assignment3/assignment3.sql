-- CPSC 408 Assignment 3
-- Using the Chinook Database
-- SET 1

-- 1) Write a query to return the average duration of tracks (in milliseconds) for each composer.
SELECT Composer, AVG(Milliseconds) as AverageDuration
FROM tracks
WHERE Composer IS NOT NULL
GROUP BY Composer;

-- 2) Write a query to return the total number of unique customers.
SELECT COUNT(DISTINCT CustomerId) as TotalUniqueCustomers
FROM customers;

-- 3) Write a query to get the total number of records and the max unit price for each media type, genre combination.
SELECT 
    mt.Name as MediaType,
    g.Name as Genre,
    COUNT(*) as TotalRecords,
    MAX(t.UnitPrice) as MaxUnitPrice
FROM tracks t
JOIN media_types mt ON t.MediaTypeId = mt.MediaTypeId
JOIN genres g ON t.GenreId = g.GenreId
GROUP BY mt.MediaTypeId, g.GenreId, mt.Name, g.Name;

-- 4) Write a query to get the average duration of tracks (in milliseconds) for each genre. Your result must have Genre Name in the result.
SELECT 
    g.Name as GenreName,
    AVG(t.Milliseconds) as AverageDuration
FROM tracks t
JOIN genres g ON t.GenreId = g.GenreId
GROUP BY g.GenreId, g.Name;

-- 5) Write a query to show the total number of albums per artist name.
SELECT 
    a.Name as ArtistName,
    COUNT(al.AlbumId) as TotalAlbums
FROM artists a
LEFT JOIN albums al ON a.ArtistId = al.ArtistId
GROUP BY a.ArtistId, a.Name;

-- 6) Write a query to return the number of invoices per billing city, billed in the USA.
SELECT 
    BillingCity,
    COUNT(*) as NumberOfInvoices
FROM invoices
WHERE BillingCountry = 'USA'
GROUP BY BillingCity;

-- SET 2

-- 1) Write a query to return the average duration of tracks (in milliseconds) for each composer, for tracks with a duration shorter than 375000 milliseconds.
SELECT 
    Composer,
    AVG(Milliseconds) as AverageDuration
FROM tracks
WHERE Composer IS NOT NULL 
    AND Milliseconds < 375000
GROUP BY Composer;

-- 2) Write a query to return the average duration of tracks (in milliseconds) for each composer, where the average duration is less than 375000 milliseconds.
SELECT 
    Composer,
    AVG(Milliseconds) as AverageDuration
FROM tracks
WHERE Composer IS NOT NULL
GROUP BY Composer
HAVING AVG(Milliseconds) < 375000;

-- 3) Find the names of all billing countries that have fewer than 10 records.
SELECT 
    BillingCountry,
    COUNT(*) as RecordCount
FROM invoices
GROUP BY BillingCountry
HAVING COUNT(*) < 10;

-- 4) Find the name of the billing country that has 8 cities in the invoices table.
SELECT 
    BillingCountry,
    COUNT(DISTINCT BillingCity) as CityCount
FROM invoices
GROUP BY BillingCountry
HAVING COUNT(DISTINCT BillingCity) = 8;

-- 5) Write a query to find billing countries and the sum of their totals, that have more than 5 records each, from the year 2010.
SELECT 
    BillingCountry,
    SUM(Total) as SumOfTotals,
    COUNT(*) as RecordCount
FROM invoices
WHERE strftime('%Y', InvoiceDate) = '2010'
GROUP BY BillingCountry
HAVING COUNT(*) > 5;
