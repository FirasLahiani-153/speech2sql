test_cases = [
    {
        "question": "Give me all the offices in usa",
        "ground_truth": "SELECT * FROM offices WHERE country = 'USA';"
    },
    {
        "question": "Find all employees who work in the San Francisco office",
        "ground_truth": "SELECT e.* FROM employees e JOIN offices o ON e.officeCode = o.officeCode WHERE o.city = 'San Francisco';"
    },
    {
        "question": "What is the total payment amount received from all customers?",
        "ground_truth": "SELECT SUM(amount) AS totalPayment FROM payments;"
    },
    {
        "question": "all orders that are currently shipped",
        "ground_truth": "SELECT * FROM orders WHERE status = 'Shipped';"
    },
    {
        "question": "how many customers are from France",
        "ground_truth": "SELECT COUNT(*) AS customerCount FROM customers WHERE country = 'France';"
    },
    {
        "question": "who's the employee with the highest employee number",
        "ground_truth": "SELECT * FROM employees ORDER BY employeeNumber DESC LIMIT 1;"
    },
    {
        "question": "give me customers with a credit limit more than 100000",
        "ground_truth": "SELECT customerName, creditLimit FROM customers WHERE creditLimit > 100000;"
    },
    {
        "question": "what is the profit margin (MSRP minus buyPrice) for each product",
        "ground_truth": "SELECT productName, productCode, (MSRP - buyPrice) AS profitMargin FROM products;"
    },
    {
        "question": "Show all distinct productlines",
        "ground_truth": "SELECT DISTINCT productLine FROM productlines;"
    },
    {
        "question": "give me number of orders for every customer",
        "ground_truth": "SELECT customerNumber, COUNT(orderNumber) AS orderCount FROM orders GROUP BY customerNumber;"
    },
    {
        "question": "Find all employees and their managers",
        "ground_truth": "SELECT e.firstName, e.lastName, m.firstName AS managerFirstName, m.lastName AS managerLastName FROM employees e LEFT JOIN employees m ON e.reportsTo = m.employeeNumber;"
    },
    {
        "question": " total revenue from each order",
        "ground_truth": "SELECT orderNumber, SUM(quantityOrdered * priceEach) AS totalRevenue FROM orderdetails GROUP BY orderNumber;"
    },
    {
        "question": "products that have low stock less than 500 units",
        "ground_truth": "SELECT productCode, productName, quantityInStock FROM products WHERE quantityInStock < 500;"
    },
    {
        "question": "Show the customer name and their sales representative's name",
        "ground_truth": "SELECT c.customerName, e.firstName AS salesRepFirstName, e.lastName AS salesRepLastName FROM customers c LEFT JOIN employees e ON c.salesRepEmployeeNumber = e.employeeNumber;"
    },
    {
        "question": "give me the highest payment amount ever received",
        "ground_truth": "SELECT MAX(amount) AS maxPayment FROM payments;"
    },
    {
        "question": "what is our territories",
        "ground_truth": "SELECT DISTINCT territory FROM offices;"
    },
    {
        "question": "Count the number of employees in each office",
        "ground_truth": "SELECT officeCode, COUNT(*) AS employeeCount FROM employees GROUP BY officeCode;"
    },
    {
        "question": "give me orders that have not been shipped yet",
        "ground_truth": "SELECT orderNumber, orderDate, status FROM orders WHERE shippedDate IS NULL;"
    },
    {
        "question": "average credit limit of customers by country",
        "ground_truth": "SELECT country, AVG(creditLimit) AS avgCreditLimit FROM customers GROUP BY country;"
    },
    {
        "question": "Which products have an MSRP higher than 200",
        "ground_truth": "SELECT productCode, productName, MSRP FROM products WHERE MSRP > 200;"
    },
    {
        "question": "give me all job titles in the company",
        "ground_truth": "SELECT DISTINCT jobTitle FROM employees;"
    },
    {
        "question": "total quantity ordered for each product",
        "ground_truth": "SELECT productCode, SUM(quantityOrdered) AS totalOrdered FROM orderdetails GROUP BY productCode;"
    },
    {
        "question": "customers who have placed more than 5 orders",
        "ground_truth": "SELECT c.customerNumber, c.customerName, COUNT(o.orderNumber) AS orderCount FROM customers c JOIN orders o ON c.customerNumber = o.customerNumber GROUP BY c.customerNumber, c.customerName HAVING COUNT(o.orderNumber) > 5;"
    },
    {
        "question": "Show the email addresses of all sales represintatives",
        "ground_truth": "SELECT firstName, lastName, email FROM employees WHERE jobTitle = 'Sales Rep';"
    },
    {
        "question": "the minimum buy price among all products",
        "ground_truth": "SELECT MIN(buyPrice) AS minPrice FROM products;"
    },
    {
        "question": "Find orders with comments containing the word late",
        "ground_truth": "SELECT orderNumber, comments FROM orders WHERE comments LIKE '%late%';"
    },
    {
        "question": "give me products sorted by quantity in stock from high to low",
        "ground_truth": "SELECT productCode, productName, quantityInStock FROM products ORDER BY quantityInStock DESC;"
    },
    {
        "question": "number of products in each product line",
        "ground_truth": "SELECT productLine, COUNT(*) AS productCount FROM products GROUP BY productLine;"
    },
    {
        "question": "show me the customer company name and phone number of all customers",
        "ground_truth": "SELECT customerName, phone FROM customers;"
    },
    {
        "question": "products who is name starts with '1969'",
        "ground_truth": "SELECT productCode, productName FROM products WHERE productName LIKE '1969%';"
    },
    {
        "question": "show me orders  with thier customer names",
        "ground_truth": "SELECT o.orderNumber, o.orderDate, o.status, c.customerName FROM orders o JOIN customers c ON o.customerNumber = c.customerNumber;"
    },
    {
        "question": "Show me total payment  for each customer",
        "ground_truth": "SELECT customerNumber, SUM(amount) AS totalPayment FROM payments GROUP BY customerNumber;"
    },
    {
        "question": "customers without a sales representative assigned",
        "ground_truth": "SELECT customerNumber, customerName FROM customers WHERE salesRepEmployeeNumber IS NULL;"
    },
    {
        "question": "top 5 customers by total payment",
        "ground_truth": "SELECT c.customerNumber, c.customerName, SUM(p.amount) AS totalPayment FROM customers c JOIN payments p ON c.customerNumber = p.customerNumber GROUP BY c.customerNumber, c.customerName ORDER BY totalPayment DESC LIMIT 5;"
    },
    {
        "question": "show me products with their product line descriptions",
        "ground_truth": "SELECT p.productCode, p.productName, pl.productLine, pl.textDescription FROM products p JOIN productlines pl ON p.productLine = pl.productLine;"
    },
    {
        "question": "Show all distinct countries where we have customers",
        "ground_truth": "SELECT DISTINCT country FROM customers ORDER BY country;"
    },
    {
        "question": "Find the number of customers each sales representative handles",
        "ground_truth": "SELECT salesRepEmployeeNumber, COUNT(*) AS customerCount FROM customers WHERE salesRepEmployeeNumber IS NOT NULL GROUP BY salesRepEmployeeNumber;"
    },
    {
        "question": "Get the total inventory value  for all products",
        "ground_truth": "SELECT SUM(quantityInStock * buyPrice) AS totalInventoryValue FROM products;"
    },
    {
        "question": "orders that still on hold or canceled",
        "ground_truth": "SELECT orderNumber, orderDate, status, customerNumber FROM orders WHERE status IN ('Cancelled', 'On Hold');"
    },
    {
        "question": "total revenue by product line",
        "ground_truth": "SELECT p.productLine, SUM(od.quantityOrdered * od.priceEach) AS totalRevenue FROM orderdetails od JOIN products p ON od.productCode = p.productCode GROUP BY p.productLine;"
    },
    {
        "question": "average order value across all orders",
        "ground_truth": "SELECT AVG(orderTotal) AS avgOrderValue FROM (SELECT orderNumber, SUM(quantityOrdered * priceEach) AS orderTotal FROM orderdetails GROUP BY orderNumber) AS orderTotals;"
    },
    {
        "question": "Get customers located in California",
        "ground_truth": "SELECT customerNumber, customerName, city FROM customers WHERE state = 'CA';"
    },
    {
        "question": "Show the number of orders by status",
        "ground_truth": "SELECT status, COUNT(*) AS orderCount FROM orders GROUP BY status;"
    },
    {
        "question": "Find products with a scale of 1:18",
        "ground_truth": "SELECT productCode, productName, productScale FROM products WHERE productScale = '1:18';"
    },
    {
        "question": "all offices with their phone numbers and cities",
        "ground_truth": "SELECT officeCode, city, phone FROM offices;"
    },
    {
        "question": "show me the details of the most expensive order by total value",
        "ground_truth": "SELECT o.orderNumber, o.orderDate, o.customerNumber, SUM(od.quantityOrdered * od.priceEach) AS totalValue FROM orders o JOIN orderdetails od ON o.orderNumber = od.orderNumber GROUP BY o.orderNumber, o.orderDate, o.customerNumber ORDER BY totalValue DESC LIMIT 1;"
    },
    {
        "question": "Find employees who didn't report to anyone",
        "ground_truth": "SELECT employeeNumber, firstName, lastName, jobTitle FROM employees WHERE reportsTo IS NULL;"
    },
    {
        "question": "Show all distinct product scales available",
        "ground_truth": "SELECT DISTINCT productScale FROM products;"
    },
    {
        "question": "how many products each vendor supplies",
        "ground_truth": "SELECT productVendor, COUNT(*) AS productCount FROM products GROUP BY productVendor ORDER BY productCount DESC;"
    },
    {
        "question": "customers who have never placed an order",
        "ground_truth": "SELECT c.customerNumber, c.customerName FROM customers c LEFT JOIN orders o ON c.customerNumber = o.customerNumber WHERE o.orderNumber IS NULL;"
    },
    {
        "question": "Get the concatenated full name of all employees",
        "ground_truth": "SELECT employeeNumber, CONCAT(firstName, ' ', lastName) AS fullName FROM employees;"
    },
    {
        "question": "products where the MSRP is at least double the buy price",
        "ground_truth": "SELECT productCode, productName, buyPrice, MSRP FROM products WHERE MSRP >= 2 * buyPrice;"
    },
    {
        "question": "Show me orders shipped after the required date",
        "ground_truth": "SELECT orderNumber, requiredDate, shippedDate FROM orders WHERE shippedDate > requiredDate;"
    },
    {
        "question": "the total number of employees in the company",
        "ground_truth": "SELECT COUNT(*) AS totalEmployees FROM employees;"
    },
    {
        "question": "products that have been ordered more than 1000 times in total",
        "ground_truth": "SELECT p.productCode, p.productName, SUM(od.quantityOrdered) AS totalOrdered FROM products p JOIN orderdetails od ON p.productCode = od.productCode GROUP BY p.productCode, p.productName HAVING SUM(od.quantityOrdered) > 1000;"
    },
    {
        "question": "the average payment amount per customer",
        "ground_truth": "SELECT customerNumber, AVG(amount) AS avgPayment FROM payments GROUP BY customerNumber;"
    },
    {
        "question": "Show me all employees working in offices outside the USA",
        "ground_truth": "SELECT e.employeeNumber, e.firstName, e.lastName, o.city, o.country FROM employees e JOIN offices o ON e.officeCode = o.officeCode WHERE o.country != 'USA';"
    },
    {
        "question": "what are the top 10 best-selling products by quantity ordered",
        "ground_truth": "SELECT p.productCode, p.productName, SUM(od.quantityOrdered) AS totalQuantity FROM products p JOIN orderdetails od ON p.productCode = od.productCode GROUP BY p.productCode, p.productName ORDER BY totalQuantity DESC LIMIT 10;"
    },
    {
        "question": "all product lines with the number of products and average MSRP",
        "ground_truth": "SELECT productLine, COUNT(*) AS productCount, AVG(MSRP) AS avgMSRP FROM products GROUP BY productLine;"
    },
    {
        "question": "i wanna see the customers whose name contains 'Auto'",
        "ground_truth": "SELECT customerNumber, customerName FROM customers WHERE customerName LIKE '%Auto%';"
    },
    {
        "question": "what's the number of line items in each order",
        "ground_truth": "SELECT orderNumber, COUNT(*) AS lineItemCount FROM orderdetails GROUP BY orderNumber;"
    },
    {
        "question": "list customers who have made payments over 50000",
        "ground_truth": "SELECT DISTINCT c.customerNumber, c.customerName FROM customers c JOIN payments p ON c.customerNumber = p.customerNumber WHERE p.amount > 50000;"
    },
    {
        "question": "the total number of orders per year",
        "ground_truth": "SELECT YEAR(orderDate) AS orderYear, COUNT(*) AS orderCount FROM orders GROUP BY YEAR(orderDate) ORDER BY orderYear;"
    },
    {
        "question": "show employees and their office city and country",
        "ground_truth": "SELECT e.employeeNumber, e.firstName, e.lastName, o.city, o.country FROM employees e JOIN offices o ON e.officeCode = o.officeCode;"
    },
    {
        "question": "Show products that have never been ordered",
        "ground_truth": "SELECT p.productCode, p.productName FROM products p LEFT JOIN orderdetails od ON p.productCode = od.productCode WHERE od.productCode IS NULL;"
    },
    {
        "question": "what's the totalof direct reports for each manager",
        "ground_truth": "SELECT reportsTo AS managerNumber, COUNT(*) AS directReports FROM employees WHERE reportsTo IS NOT NULL GROUP BY reportsTo;"
    },
    {
        "question": "the customers where credit limit between 50000 and 100000",
        "ground_truth": "SELECT customerNumber, customerName, creditLimit FROM customers WHERE creditLimit BETWEEN 50000 AND 100000;"
    },
    {
        "question": "giv me  markup percentage for each product",
        "ground_truth": "SELECT productCode, productName, ROUND(((MSRP - buyPrice) / buyPrice) * 100, 2) AS markupPercentage FROM products;"
    },
    {
        "question": "List all orders in the year 2004",
        "ground_truth": "SELECT orderNumber, orderDate, customerNumber FROM orders WHERE YEAR(orderDate) = 2004;"
    },
    {
        "question": "Get the total revenue generated by each customer",
        "ground_truth": "SELECT o.customerNumber, c.customerName, SUM(od.quantityOrdered * od.priceEach) AS totalRevenue FROM orders o JOIN orderdetails od ON o.orderNumber = od.orderNumber JOIN customers c ON o.customerNumber = c.customerNumber GROUP BY o.customerNumber, c.customerName ORDER BY totalRevenue DESC;"
    },
    {
        "question": "give me vendors that have over 5 products",
        "ground_truth": "SELECT productVendor, COUNT(*) AS productCount FROM products GROUP BY productVendor HAVING COUNT(*) > 5;"
    },
    {
        "question": "whats the number of customers by city",
        "ground_truth": "SELECT city, COUNT(*) AS customerCount FROM customers GROUP BY city ORDER BY customerCount DESC;"
    },
    {
        "question": "Get the average MSRP by product scale",
        "ground_truth": "SELECT productScale, AVG(MSRP) AS avgMSRP FROM products GROUP BY productScale;"
    },
    {
        "question": "Find orders where the order date is the same as the required date",
        "ground_truth": "SELECT orderNumber, orderDate, requiredDate FROM orders WHERE orderDate = requiredDate;"#no answer
    },
    {
        "question": "what is the total stock quantity by product line",
        "ground_truth": "SELECT productLine, SUM(quantityInStock) AS totalStock FROM products GROUP BY productLine;"
    },
    {
        "question": "Show payments made in 2005",
        "ground_truth": "SELECT checkNumber, customerNumber, paymentDate, amount FROM payments WHERE YEAR(paymentDate) = 2005;"
    },
    {
        "question": "Get the total revenue and quantity for each product",
        "ground_truth": "SELECT productCode, SUM(quantityOrdered) AS totalQuantity, SUM(quantityOrdered * priceEach) AS totalRevenue FROM orderdetails GROUP BY productCode;"
    },
    {
        "question": "Find customers in the same city as an office",
        "ground_truth": "SELECT c.customerNumber, c.customerName, c.city FROM customers c WHERE c.city IN (SELECT city FROM offices);"
    },
    {
        "question": "what arethe 5 most recent orders",
        "ground_truth": "SELECT orderNumber, orderDate, customerNumber, status FROM orders ORDER BY orderDate DESC LIMIT 5;"
    },
    {
        "question": "what is the difference between required date and shipped date for each order",
        "ground_truth": "SELECT orderNumber, requiredDate, shippedDate, DATEDIFF(shippedDate, requiredDate) AS daysDifference FROM orders WHERE shippedDate IS NOT NULL;"
    },
    {
        "question": "what is the number of payments per month",
        "ground_truth": "SELECT YEAR(paymentDate) AS year, MONTH(paymentDate) AS month, COUNT(*) AS paymentCount FROM payments GROUP BY YEAR(paymentDate), MONTH(paymentDate) ORDER BY year, month;"
    },
    {
        "question": " products with the maximum quantity in stock in each product line",
        "ground_truth": "SELECT p.productLine, p.productCode, p.productName, p.quantityInStock FROM products p WHERE p.quantityInStock = (SELECT MAX(quantityInStock) FROM products WHERE productLine = p.productLine);"
    },
    {
        "question": "give me all customers from Germany or France",
        "ground_truth": "SELECT customerNumber, customerName, country FROM customers WHERE country IN ('Germany', 'France');"
    },
    {
        "question": "total sales by sales representative",
        "ground_truth": "SELECT e.employeeNumber, e.firstName, e.lastName, SUM(od.quantityOrdered * od.priceEach) AS totalSales FROM employees e JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber JOIN orders o ON c.customerNumber = o.customerNumber JOIN orderdetails od ON o.orderNumber = od.orderNumber GROUP BY e.employeeNumber, e.firstName, e.lastName ORDER BY totalSales DESC;"
    },
    {
        "question": "i wanna know the products in alphabetical order",
        "ground_truth": "SELECT productCode, productName FROM products ORDER BY productName ASC;"
    },
    {
        "question": "the number of unique products sold",
        "ground_truth": "SELECT COUNT(DISTINCT productCode) AS uniqueProductsSold FROM orderdetails;"
    },
    {
        "question": "what's the first and last payment dates",
        "ground_truth": "SELECT MIN(paymentDate) AS firstPayment, MAX(paymentDate) AS lastPayment FROM payments;"
    },
    {
        "question": "the orders that has more than 10 line items",
        "ground_truth": "SELECT orderNumber, COUNT(*) AS lineItemCount FROM orderdetails GROUP BY orderNumber HAVING COUNT(*) > 10;"
    },
    {
        "question": "Get the contact information for all customers in New York",#no respone
        "ground_truth": "SELECT customerName, contactFirstName, contactLastName, phone, addressLine1, city FROM customers WHERE city = 'New York';"
    },
    {
        "question": "the product that has  the highest MSRP",
        "ground_truth": "SELECT productCode, productName, MSRP FROM products ORDER BY MSRP DESC LIMIT 1;"
    },
    {
        "question": "give me the employees their last name starts with 'P'",
        "ground_truth": "SELECT employeeNumber, firstName, lastName, email FROM employees WHERE lastName LIKE 'P%';"
    },
    {
        "question": "the revenue trend overtime", #  "Show the monthly revenue trend"

        "ground_truth": "SELECT YEAR(o.orderDate) AS year, MONTH(o.orderDate) AS month, SUM(od.quantityOrdered * od.priceEach) AS monthlyRevenue FROM orders o JOIN orderdetails od ON o.orderNumber = od.orderNumber GROUP BY YEAR(o.orderDate), MONTH(o.orderDate) ORDER BY year, month;"
    },
    {
        "question": "orders with total valu more than 10000",
        "ground_truth": "SELECT orderNumber, SUM(quantityOrdered * priceEach) AS totalValue FROM orderdetails GROUP BY orderNumber HAVING SUM(quantityOrdered * priceEach) > 10000;"
    },
    {
        "question": "which offices in the EMEA ",
        "ground_truth": "SELECT officeCode, city, country FROM offices WHERE territory = 'EMEA';"
    },
    {
        "question": "all products in the Classic Cars category",
        "ground_truth": "SELECT productCode, productName, buyPrice, MSRP FROM products WHERE productLine = 'Classic Cars';"
    },
    {
        "question": "groupe customers into tier based on thier credit limit",
        "ground_truth": "SELECT customerNumber, customerName, creditLimit, CASE WHEN creditLimit < 25000 THEN 'Low' WHEN creditLimit BETWEEN 25000 AND 75000 THEN 'Medium' WHEN creditLimit > 75000 THEN 'High' END AS creditTier FROM customers;"
    },
    {
        "question": "how many orders did each customer make and their name",
        "ground_truth": "SELECT c.customerNumber, c.customerName, COUNT(o.orderNumber) AS orderCount FROM customers c LEFT JOIN orders o ON c.customerNumber = o.customerNumber GROUP BY c.customerNumber, c.customerName;"
    },
    {
        "question": "whats the avrage quantity ordered per order line",
        "ground_truth": "SELECT AVG(quantityOrdered) AS avgQuantityPerLine FROM orderdetails;"
    },
    {
        "question": "all the employees who are Sales Managers",
        "ground_truth": "SELECT employeeNumber, firstName, lastName, email, officeCode FROM employees WHERE jobTitle LIKE '%Sales Manager%';"
    },
    {
        "question": "product code, name, and buy price for products whose buy price is above the average buy price",
        "ground_truth": "SELECT productCode, productName, buyPrice FROM products WHERE buyPrice > (SELECT AVG(buyPrice) FROM products);"
    },
    {
        "question": "tell me total credit limit for all customers",
        "ground_truth": "SELECT SUM(creditLimit) AS totalCreditLimit FROM customers;"
    },
    {
        "question": "which orders are still in process",
        "ground_truth": "SELECT orderNumber, orderDate, customerNumber FROM orders WHERE status = 'In Process';"
    },
    {
        "question": "how much each country made", 
        "ground_truth": "SELECT c.country, SUM(od.quantityOrdered * od.priceEach) AS totalRevenue FROM customers c JOIN orders o ON c.customerNumber = o.customerNumber JOIN orderdetails od ON o.orderNumber = od.orderNumber GROUP BY c.country ORDER BY totalRevenue DESC;"
    },
    {
        "question": "how many offices are there in each country",
        "ground_truth": "SELECT country, COUNT(*) AS officeCount FROM offices GROUP BY country;"
    },
    {
        "question": "i wanna see the levels of employees that report to a manager",
        "ground_truth": "SELECT e.employeeNumber, CONCAT(e.firstName, ' ', e.lastName) AS employeeName, e.jobTitle, m.employeeNumber AS managerNumber, CONCAT(m.firstName, ' ', m.lastName) AS managerName FROM employees e JOIN employees m ON e.reportsTo = m.employeeNumber;"
    },
    {
        "question": "customers with over 3 paymets",
        "ground_truth": "SELECT c.customerNumber, c.customerName, COUNT(p.checkNumber) AS paymentCount FROM customers c JOIN payments p ON c.customerNumber = p.customerNumber GROUP BY c.customerNumber, c.customerName HAVING COUNT(p.checkNumber) > 3;"
    },
    {
        "question": "give me the total stock value for each vendor",
        "ground_truth": "SELECT productVendor, SUM(quantityInStock * buyPrice) AS totalStockValue FROM products GROUP BY productVendor ORDER BY totalStockValue DESC;"
    },
    {
        "question": "what is the second highest payment we got",
        "ground_truth": "SELECT DISTINCT amount FROM payments ORDER BY amount DESC LIMIT 1 OFFSET 1;"
    },
]

test_cases1 = [
    {
        "question": "Give me all the airports in Germany",
        "ground_truth": "SELECT a.* FROM airport a JOIN airport_geo ag ON a.airport_id = ag.airport_id WHERE ag.country = 'Germany';"
    },
    {
        "question": "Find all employees who work in the Frankfurt department",
        "ground_truth": "SELECT * FROM employee WHERE city = 'Frankfurt';"
    },
    {
        "question": "all flights that have already departed",
        "ground_truth": "SELECT * FROM flight WHERE departure < NOW();"
    },
    {
        "question": "how many passengers are from France",
        "ground_truth": "SELECT COUNT(*) AS passengerCount FROM passengerdetails WHERE country = 'France';"
    },
    {
        "question": "who's the employee with the highest employee id",
        "ground_truth": "SELECT * FROM employee ORDER BY employee_id DESC LIMIT 1;"
    },
    {
        "question": "give me employees with a salary more than 100000",
        "ground_truth": "SELECT firstname, lastname, salary FROM employee WHERE salary > 100000;"
    },

    {
        "question": "Show all distinct airplane types",
        "ground_truth": "SELECT DISTINCT identifier FROM airplane_type;"
    },
    {
        "question": "give me number of bookings for every flight",
        "ground_truth": "SELECT flight_id, COUNT(booking_id) AS bookingCount FROM booking GROUP BY flight_id;"
    },
    {
        "question": "Find all airplanes and their airplane type description",
        "ground_truth": "SELECT ap.airplane_id, ap.capacity, at.identifier, at.description FROM airplane ap LEFT JOIN airplane_type at ON ap.type_id = at.type_id;"
    },
    {
        "question": "total revenue from each flight",
        "ground_truth": "SELECT flight_id, SUM(price) AS totalRevenue FROM booking GROUP BY flight_id;"
    },
    {
        "question": "airplanes with low capacity less than 100 seats",
        "ground_truth": "SELECT airplane_id, capacity, type_id FROM airplane WHERE capacity < 100;"
    },
    {
        "question": "Show the airline name and its base airport name",
        "ground_truth": "SELECT al.airlinename, ap.name AS baseAirportName FROM airline al LEFT JOIN airport ap ON al.base_airport = ap.airport_id;"
    },
    {
        "question": "give me the highest booking price ever recorded",
        "ground_truth": "SELECT MAX(price) AS maxBookingPrice FROM booking;"
    },
    {
        "question": "what are our airline IATA codes",
        "ground_truth": "SELECT DISTINCT iata FROM airline;"
    },
    {
        "question": "Count the number of employees in each department",
        "ground_truth": "SELECT department, COUNT(*) AS employeeCount FROM employee GROUP BY department;"
    },
    {
        "question": "give me flights that have not arrived yet",
        "ground_truth": "SELECT flight_id, flightno, departure, arrival FROM flight WHERE arrival > NOW();"
    },
    {
        "question": "average salary of employees by country",
        "ground_truth": "SELECT country, AVG(salary) AS avgSalary FROM employee GROUP BY country;"
    },
    {
        "question": "Which airplanes have a capacity higher than 200",
        "ground_truth": "SELECT airplane_id, capacity, type_id FROM airplane WHERE capacity > 200;"
    },
    {
        "question": "give me all departments in the company",
        "ground_truth": "SELECT DISTINCT department FROM employee;"
    },
    {
        "question": "total number of seats booked for each flight",
        "ground_truth": "SELECT flight_id, COUNT(seat) AS totalSeatsBooked FROM booking GROUP BY flight_id;"
    },
    {
        "question": "passengers who have made more than 5 bookings",
        "ground_truth": "SELECT p.passenger_id, p.firstname, p.lastname, COUNT(b.booking_id) AS bookingCount FROM passenger p JOIN booking b ON p.passenger_id = b.passenger_id GROUP BY p.passenger_id, p.firstname, p.lastname HAVING COUNT(b.booking_id) > 5;"
    },
    {
        "question": "Show the email addresses of all employees in the Sales department",
        "ground_truth": "SELECT firstname, lastname, emailaddress FROM employee WHERE department = 'Sales';"
    },
    {
        "question": "the minimum booking price among all bookings",
        "ground_truth": "SELECT MIN(price) AS minPrice FROM booking;"
    },
    {
        "question": "Find flight log entries with comments containing the word delay",
        "ground_truth": "SELECT flight_log_id, comment FROM flight_log WHERE comment LIKE '%delay%';"
    },
    {
        "question": "give me airplanes sorted by capacity from high to low",
        "ground_truth": "SELECT airplane_id, capacity, type_id FROM airplane ORDER BY capacity DESC;"
    },
    {
        "question": "number of airplanes for each airline",
        "ground_truth": "SELECT airline_id, COUNT(*) AS airplaneCount FROM airplane GROUP BY airline_id;"
    },
    {
        "question": "show me the airline name and IATA code of all airlines",
        "ground_truth": "SELECT airlinename, iata FROM airline;"
    },
    {
        "question": "airports who's name starts with 'San'",
        "ground_truth": "SELECT airport_id, name FROM airport WHERE name LIKE 'San%';"
    },
    {
        "question": "show me bookings with their passenger names",
        "ground_truth": "SELECT b.booking_id, b.flight_id, b.seat, b.price, p.firstname, p.lastname FROM booking b JOIN passenger p ON b.passenger_id = p.passenger_id;"
    },
    {
        "question": "Show me total amount paid for each passenger",
        "ground_truth": "SELECT passenger_id, SUM(price) AS totalPaid FROM booking GROUP BY passenger_id;"
    },
    {
        "question": "passengers without any booking",
        "ground_truth": "SELECT p.passenger_id, p.firstname, p.lastname FROM passenger p LEFT JOIN booking b ON p.passenger_id = b.passenger_id WHERE b.booking_id IS NULL;"
    },
    {
        "question": "top 5 passengers by total amount paid",
        "ground_truth": "SELECT p.passenger_id, p.firstname, p.lastname, SUM(b.price) AS totalPaid FROM passenger p JOIN booking b ON p.passenger_id = b.passenger_id GROUP BY p.passenger_id, p.firstname, p.lastname ORDER BY totalPaid DESC LIMIT 5;"
    },
    {
        "question": "show me airplanes with their type description",
        "ground_truth": "SELECT ap.airplane_id, ap.capacity, at.identifier, at.description FROM airplane ap JOIN airplane_type at ON ap.type_id = at.type_id;"
    },
    {
        "question": "Show all distinct countries where we have passengers",
        "ground_truth": "SELECT DISTINCT country FROM passengerdetails ORDER BY country;"
    },
    {
        "question": "Find the number of flights operated by each airline",
        "ground_truth": "SELECT airline_id, COUNT(*) AS flightCount FROM flight GROUP BY airline_id;"
    },
    {
        "question": "Get the total seating capacity across all airplanes",
        "ground_truth": "SELECT SUM(capacity) AS totalCapacity FROM airplane;"
    },
    {
        "question": "flights from JFK or LAX",
        "ground_truth": "SELECT f.flight_id, f.flightno, f.from, f.to FROM flight f JOIN airport a ON f.from = a.airport_id WHERE a.iata IN ('JFK', 'LAX');"
    },
    {
        "question": "total revenue by airline",
        "ground_truth": "SELECT f.airline_id, SUM(b.price) AS totalRevenue FROM booking b JOIN flight f ON b.flight_id = f.flight_id GROUP BY f.airline_id;"
    },
    {
        "question": "average booking price across all bookings",
        "ground_truth": "SELECT AVG(price) AS avgBookingPrice FROM booking;"
    },
    {
        "question": "Get passengers located in Berlin",
        "ground_truth": "SELECT p.passenger_id, p.firstname, p.lastname, pd.city FROM passenger p JOIN passengerdetails pd ON p.passenger_id = pd.passenger_id WHERE pd.city = 'Berlin';"
    },
    {
        "question": "Show the number of flights by airline",
        "ground_truth": "SELECT airline_id, COUNT(*) AS flightCount FROM flight GROUP BY airline_id;"
    },
    {
        "question": "Find airplanes with a capacity of exactly 180",
        "ground_truth": "SELECT airplane_id, capacity, type_id FROM airplane WHERE capacity = 180;"
    },
    {
        "question": "all airports with their cities and countries",
        "ground_truth": "SELECT a.airport_id, a.name, ag.city, ag.country FROM airport a JOIN airport_geo ag ON a.airport_id = ag.airport_id;"
    },
    {
        "question": "show me the details of the most expensive booking",
        "ground_truth": "SELECT booking_id, flight_id, seat, passenger_id, price FROM booking ORDER BY price DESC LIMIT 1;"
    },
    {
        "question": "Find airlines that don't have a base airport assigned",
        "ground_truth": "SELECT airline_id, iata, airlinename FROM airline WHERE base_airport IS NULL;"
    },
    {
        "question": "Show all distinct airplane type identifiers available",
        "ground_truth": "SELECT DISTINCT identifier FROM airplane_type;"
    },
    {
        "question": "how many airplanes each airplane type has",
        "ground_truth": "SELECT type_id, COUNT(*) AS airplaneCount FROM airplane GROUP BY type_id ORDER BY airplaneCount DESC;"
    },
    {
        "question": "flights that have no bookings",
        "ground_truth": "SELECT f.flight_id, f.flightno FROM flight f LEFT JOIN booking b ON f.flight_id = b.flight_id WHERE b.booking_id IS NULL;"
    },
    {
        "question": "Get the concatenated full name of all employees",
        "ground_truth": "SELECT employee_id, CONCAT(firstname, ' ', lastname) AS fullName FROM employee;"
    },
    {
        "question": "flights where the arrival is more than 2 hours after departure",
        "ground_truth": "SELECT flight_id, flightno, departure, arrival FROM flight WHERE TIMESTAMPDIFF(HOUR, departure, arrival) > 2;"
    },
    {
        "question": "Show me flights that arrived after their scheduled arrival",
        "ground_truth": "SELECT fl.flight_id, fl.flightno, fl.arrival AS actualArrival, fs.arrival AS scheduledArrival FROM flight fl JOIN flightschedule fs ON fl.flightno = fs.flightno WHERE fl.arrival > fs.arrival;"
    },
    {
        "question": "the total number of employees in the company",
        "ground_truth": "SELECT COUNT(*) AS totalEmployees FROM employee;"
    },
    {
        "question": "flights that have been booked more than 100 times",
        "ground_truth": "SELECT f.flight_id, f.flightno, COUNT(b.booking_id) AS bookingCount FROM flight f JOIN booking b ON f.flight_id = b.flight_id GROUP BY f.flight_id, f.flightno HAVING COUNT(b.booking_id) > 100;"
    },
    {
        "question": "the average booking price per passenger",
        "ground_truth": "SELECT passenger_id, AVG(price) AS avgPrice FROM booking GROUP BY passenger_id;"
    },
    {
        "question": "Show me all employees working in offices outside Germany",
        "ground_truth": "SELECT employee_id, firstname, lastname, city, country FROM employee WHERE country != 'Germany';"
    },
    {
        "question": "what are the top 10 most booked flights",
        "ground_truth": "SELECT f.flight_id, f.flightno, COUNT(b.booking_id) AS bookingCount FROM flight f JOIN booking b ON f.flight_id = b.flight_id GROUP BY f.flight_id, f.flightno ORDER BY bookingCount DESC LIMIT 10;"
    },
    {
        "question": "all airlines with the number of airplanes and average capacity",
        "ground_truth": "SELECT al.airline_id, al.airlinename, COUNT(ap.airplane_id) AS airplaneCount, AVG(ap.capacity) AS avgCapacity FROM airline al LEFT JOIN airplane ap ON al.airline_id = ap.airline_id GROUP BY al.airline_id, al.airlinename;"
    },
    {
        "question": "i wanna see the airlines whose name contains 'Air'",
        "ground_truth": "SELECT airline_id, airlinename FROM airline WHERE airlinename LIKE '%Air%';"
    },
    {
        "question": "what's the number of bookings per flight",
        "ground_truth": "SELECT flight_id, COUNT(*) AS bookingCount FROM booking GROUP BY flight_id;"
    },
    {
        "question": "list passengers who have made bookings over 1000",
        "ground_truth": "SELECT DISTINCT p.passenger_id, p.firstname, p.lastname FROM passenger p JOIN booking b ON p.passenger_id = b.passenger_id WHERE b.price > 1000;"
    },
    {
        "question": "the total number of flights per year",
        "ground_truth": "SELECT YEAR(departure) AS flightYear, COUNT(*) AS flightCount FROM flight GROUP BY YEAR(departure) ORDER BY flightYear;"
    },
    {
        "question": "show employees and their city and country",
        "ground_truth": "SELECT employee_id, firstname, lastname, city, country FROM employee;"
    },
    {
        "question": "Show airplanes that have never been used on a flight",
        "ground_truth": "SELECT ap.airplane_id, ap.capacity FROM airplane ap LEFT JOIN flight f ON ap.airplane_id = f.airplane_id WHERE f.flight_id IS NULL;"
    },
    {
        "question": "what's the total of bookings for each passenger",
        "ground_truth": "SELECT passenger_id, COUNT(*) AS bookingCount FROM booking GROUP BY passenger_id;"
    },
    {
        "question": "the employees where salary between 50000 and 100000",
        "ground_truth": "SELECT employee_id, firstname, lastname, salary FROM employee WHERE salary BETWEEN 50000 AND 100000;"
    },
    {
        "question": "give me load factor percentage for each flight (bookings vs capacity)",
        "ground_truth": "SELECT f.flight_id, f.flightno, ROUND((COUNT(b.booking_id) / ap.capacity) * 100, 2) AS loadFactor FROM flight f JOIN airplane ap ON f.airplane_id = ap.airplane_id LEFT JOIN booking b ON f.flight_id = b.flight_id GROUP BY f.flight_id, f.flightno, ap.capacity;"
    },
    {
        "question": "List all flights in the year 2017",
        "ground_truth": "SELECT flight_id, flightno, departure, airline_id FROM flight WHERE YEAR(departure) = 2017;"
    },
    {
        "question": "Get the total revenue generated by each passenger",
        "ground_truth": "SELECT b.passenger_id, p.firstname, p.lastname, SUM(b.price) AS totalRevenue FROM booking b JOIN passenger p ON b.passenger_id = p.passenger_id GROUP BY b.passenger_id, p.firstname, p.lastname ORDER BY totalRevenue DESC;"
    },
    {
        "question": "give me airplane types that have over 5 airplanes",
        "ground_truth": "SELECT type_id, COUNT(*) AS airplaneCount FROM airplane GROUP BY type_id HAVING COUNT(*) > 5;"
    },
    {
        "question": "what's the number of passengers by city",
        "ground_truth": "SELECT city, COUNT(*) AS passengerCount FROM passengerdetails GROUP BY city ORDER BY passengerCount DESC;"
    },
    {
        "question": "Get the average capacity by airplane type",
        "ground_truth": "SELECT at.type_id, at.identifier, AVG(ap.capacity) AS avgCapacity FROM airplane ap JOIN airplane_type at ON ap.type_id = at.type_id GROUP BY at.type_id, at.identifier;"
    },
    {
        "question": "Find flights where the departure date is the same as the arrival date",
        "ground_truth": "SELECT flight_id, flightno, departure, arrival FROM flight WHERE DATE(departure) = DATE(arrival);"
    },
    {
        "question": "what is the total airplane capacity by airline",
        "ground_truth": "SELECT airline_id, SUM(capacity) AS totalCapacity FROM airplane GROUP BY airline_id;"
    },
    {
        "question": "Show bookings made in 2018",
        "ground_truth": "SELECT b.booking_id, b.flight_id, b.passenger_id, b.price FROM booking b JOIN flight f ON b.flight_id = f.flight_id WHERE YEAR(f.departure) = 2018;"
    },
    {
        "question": "Get the total revenue and number of bookings for each flight",
        "ground_truth": "SELECT flight_id, COUNT(*) AS bookingCount, SUM(price) AS totalRevenue FROM booking GROUP BY flight_id;"
    },
    {
        "question": "Find passengers in the same city as an employee",
        "ground_truth": "SELECT p.passenger_id, p.firstname, p.lastname, pd.city FROM passenger p JOIN passengerdetails pd ON p.passenger_id = pd.passenger_id WHERE pd.city IN (SELECT city FROM employee);"
    },
    {
        "question": "what are the 5 most recent flights",
        "ground_truth": "SELECT flight_id, flightno, departure, airline_id FROM flight ORDER BY departure DESC LIMIT 5;"
    },
    {
        "question": "what is the duration in minutes between departure and arrival for each flight",
        "ground_truth": "SELECT flight_id, flightno, departure, arrival, TIMESTAMPDIFF(MINUTE, departure, arrival) AS durationMinutes FROM flight;"
    },
    {
        "question": "what is the number of bookings per month",
        "ground_truth": "SELECT YEAR(f.departure) AS year, MONTH(f.departure) AS month, COUNT(*) AS bookingCount FROM booking b JOIN flight f ON b.flight_id = f.flight_id GROUP BY YEAR(f.departure), MONTH(f.departure) ORDER BY year, month;"
    },
    {
        "question": "airplanes with the maximum capacity for each airline",
        "ground_truth": "SELECT ap.airline_id, ap.airplane_id, ap.capacity FROM airplane ap WHERE ap.capacity = (SELECT MAX(capacity) FROM airplane WHERE airline_id = ap.airline_id);"
    },
    {
        "question": "give me all passengers from Germany or France",
        "ground_truth": "SELECT p.passenger_id, p.firstname, p.lastname, pd.country FROM passenger p JOIN passengerdetails pd ON p.passenger_id = pd.passenger_id WHERE pd.country IN ('Germany', 'France');"
    },
    {
        "question": "total revenue by airline name",
        "ground_truth": "SELECT al.airline_id, al.airlinename, SUM(b.price) AS totalRevenue FROM airline al JOIN flight f ON al.airline_id = f.airline_id JOIN booking b ON f.flight_id = b.flight_id GROUP BY al.airline_id, al.airlinename ORDER BY totalRevenue DESC;"
    },
    {
        "question": "i wanna know the airports in alphabetical order",
        "ground_truth": "SELECT airport_id, name FROM airport ORDER BY name ASC;"
    },
    {
        "question": "the number of unique flights booked",
        "ground_truth": "SELECT COUNT(DISTINCT flight_id) AS uniqueFlightsBooked FROM booking;"
    },
    {
        "question": "what's the first and last flight departure dates",
        "ground_truth": "SELECT MIN(departure) AS firstFlight, MAX(departure) AS lastFlight FROM flight;"
    },
    {
        "question": "the flights that have more than 50 bookings",
        "ground_truth": "SELECT flight_id, COUNT(*) AS bookingCount FROM booking GROUP BY flight_id HAVING COUNT(*) > 50;"
    },
    {
        "question": "Get the contact information for all passengers in London",
        "ground_truth": "SELECT p.firstname, p.lastname, pd.emailaddress, pd.telephoneno, pd.street, pd.city FROM passenger p JOIN passengerdetails pd ON p.passenger_id = pd.passenger_id WHERE pd.city = 'London';"
    },
    {
        "question": "the airplane that has the highest capacity",
        "ground_truth": "SELECT airplane_id, capacity, type_id FROM airplane ORDER BY capacity DESC LIMIT 1;"
    },
    {
        "question": "give me the employees their last name starts with 'P'",
        "ground_truth": "SELECT employee_id, firstname, lastname, emailaddress FROM employee WHERE lastname LIKE 'P%';"
    },
    {
        "question": "the revenue trend overtime",
        "ground_truth": "SELECT YEAR(f.departure) AS year, MONTH(f.departure) AS month, SUM(b.price) AS monthlyRevenue FROM booking b JOIN flight f ON b.flight_id = f.flight_id GROUP BY YEAR(f.departure), MONTH(f.departure) ORDER BY year, month;"
    },
    {
        "question": "flights with total booking value more than 10000",
        "ground_truth": "SELECT flight_id, SUM(price) AS totalValue FROM booking GROUP BY flight_id HAVING SUM(price) > 10000;"
    },
    {
        "question": "which airports are in the USA",
        "ground_truth": "SELECT a.airport_id, a.name, ag.city FROM airport a JOIN airport_geo ag ON a.airport_id = ag.airport_id WHERE ag.country = 'USA';"
    },
    {
        "question": "all airplanes from a specific airplane type identifier 'Boeing 747'",
        "ground_truth": "SELECT ap.airplane_id, ap.capacity, at.identifier FROM airplane ap JOIN airplane_type at ON ap.type_id = at.type_id WHERE at.identifier = 'Boeing 747';"
    },
    {
        "question": "groupe employees into tier based on their salary",
        "ground_truth": "SELECT employee_id, firstname, lastname, salary, CASE WHEN salary < 50000 THEN 'Low' WHEN salary BETWEEN 50000 AND 100000 THEN 'Medium' WHEN salary > 100000 THEN 'High' END AS salaryTier FROM employee;"
    },
    {
        "question": "how many bookings did each passenger make and their name",
        "ground_truth": "SELECT p.passenger_id, p.firstname, p.lastname, COUNT(b.booking_id) AS bookingCount FROM passenger p LEFT JOIN booking b ON p.passenger_id = b.passenger_id GROUP BY p.passenger_id, p.firstname, p.lastname;"
    },
    {
        "question": "what's the average price per booking",
        "ground_truth": "SELECT AVG(price) AS avgPricePerBooking FROM booking;"
    },
    {
        "question": "all the employees who are in the Marketing department",
        "ground_truth": "SELECT employee_id, firstname, lastname, emailaddress, department FROM employee WHERE department = 'Marketing';"
    },
    {
        "question": "airplane id, capacity for airplanes whose capacity is above the average capacity",
        "ground_truth": "SELECT airplane_id, capacity FROM airplane WHERE capacity > (SELECT AVG(capacity) FROM airplane);"
    },
    {
        "question": "tell me total salary for all employees",
        "ground_truth": "SELECT SUM(salary) AS totalSalary FROM employee;"
    },
    {
        "question": "which scheduled flights run on Monday",
        "ground_truth": "SELECT flightno, `from`, `to`, departure, arrival FROM flightschedule WHERE monday = 1;"
    },
    {
        "question": "how much each country generated in bookings",
        "ground_truth": "SELECT pd.country, SUM(b.price) AS totalRevenue FROM passengerdetails pd JOIN booking b ON pd.passenger_id = b.passenger_id GROUP BY pd.country ORDER BY totalRevenue DESC;"
    },
    {
        "question": "how many airports are there in each country",
        "ground_truth": "SELECT country, COUNT(*) AS airportCount FROM airport_geo GROUP BY country;"
    },
    {
        "question": "i wanna see all flight log changes and the user who made them",
        "ground_truth": "SELECT flight_log_id, log_date, user, flight_id, comment FROM flight_log;"
    },
    {
        "question": "passengers with over 3 bookings",
        "ground_truth": "SELECT p.passenger_id, p.firstname, p.lastname, COUNT(b.booking_id) AS bookingCount FROM passenger p JOIN booking b ON p.passenger_id = b.passenger_id GROUP BY p.passenger_id, p.firstname, p.lastname HAVING COUNT(b.booking_id) > 3;"
    },
    {
        "question": "give me the total revenue for each airplane",
        "ground_truth": "SELECT f.airplane_id, SUM(b.price) AS totalRevenue FROM flight f JOIN booking b ON f.flight_id = b.flight_id GROUP BY f.airplane_id ORDER BY totalRevenue DESC;"
    },
    {
        "question": "what is the second highest booking price we got",
        "ground_truth": "SELECT DISTINCT price FROM booking ORDER BY price DESC LIMIT 1 OFFSET 1;"
    },
]