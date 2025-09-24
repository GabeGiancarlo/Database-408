-- CPSC 408 Assignment 02
-- Chinook Database Queries
-- Points: 40

-- 1. Create a table Patient(patientID, name, dob, phone)
-- Note that patientID is the primary key of the table. Use appropriate data types.
-- patientID and name need to have the NOT NULL constraint.
CREATE TABLE Patient (
    patientID INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    dob DATE,
    phone VARCHAR(20),
    PRIMARY KEY (patientID)
);

-- 2. Alter the Patient table and add a new column address to it.
ALTER TABLE Patient 
ADD COLUMN address VARCHAR(200);

-- 3. Drop the Patient table.
DROP TABLE Patient;

-- 4. Write a query to retrieve the first name, last name, and email from the employees table.
SELECT FirstName, LastName, Email
FROM employees;

-- 5. Write a query to retrieve the IDs of employees who were hired in 2004.
SELECT EmployeeId
FROM employees
WHERE YEAR(HireDate) = 2004;

-- Alternative approach using date range
SELECT EmployeeId
FROM employees
WHERE HireDate >= '2004-01-01' AND HireDate < '2005-01-01';

-- 6. Write a query to retrieve all records of employees who are a manager (i.e., manager is in their job title).
SELECT *
FROM employees
WHERE Title LIKE '%Manager%';

-- 7. Write a query to return the unique billing cities from the invoices table.
SELECT DISTINCT BillingCity
FROM invoices;

-- 8. Write a query to return the unique billing countries where the invoice total is greater than 10 and invoice Date is from 2013.
SELECT DISTINCT BillingCountry
FROM invoices
WHERE Total > 10 
  AND YEAR(InvoiceDate) = 2013;

-- Alternative approach using date range for 2013
SELECT DISTINCT BillingCountry
FROM invoices
WHERE Total > 10 
  AND InvoiceDate >= '2013-01-01' 
  AND InvoiceDate < '2014-01-01';
