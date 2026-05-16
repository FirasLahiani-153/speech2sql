from langchain_core.documents import Document


def get_rag():

    # =========================================================
    # SCHEMA DOCUMENTS
    # =========================================================
    schema_docs = [
        Document(page_content="""
TABLE: productlines
COLUMNS: productLine, textDescription, htmlDescription, image
DESCRIPTION: Stores product line categories like Classic Cars, Motorcycles, Planes, etc.
PRIMARY KEY: productLine
""", metadata={"type": "schema"}),

        Document(page_content="""
TABLE: products
COLUMNS: productCode, productName, productLine, productScale, productVendor,
         productDescription, quantityInStock, buyPrice, MSRP
DESCRIPTION: Stores individual product details including pricing and inventory.
PRIMARY KEY: productCode
FOREIGN KEY: productLine → productlines.productLine
IMPORTANT: MSRP is Not price of a product
""", metadata={"type": "schema"}),

        Document(page_content="""
TABLE: offices
COLUMNS: officeCode, city, phone, addressLine1, addressLine2,
         state, country, postalCode, territory
DESCRIPTION: Stores office locations across different territories (NA, EMEA, APAC, Japan).
PRIMARY KEY: officeCode
""", metadata={"type": "schema"}),

        Document(page_content="""
TABLE: employees
COLUMNS: employeeNumber, lastName, firstName, extension, email,
         officeCode, reportsTo, jobTitle
DESCRIPTION: Stores employee data. reportsTo is a self-referencing FK for manager hierarchy.
PRIMARY KEY: employeeNumber
FOREIGN KEYS:
- officeCode → offices.officeCode
- reportsTo → employees.employeeNumber (self-join for manager)
NULLABLE: reportsTo (NULL = top-level employee with no manager)
""", metadata={"type": "schema"}),

        Document(page_content="""
TABLE: customers
COLUMNS: customerNumber, customerName, contactLastName, contactFirstName,
         phone, addressLine1, addressLine2, city, state, postalCode,
         country, salesRepEmployeeNumber, creditLimit
DESCRIPTION: Stores customer information. salesRepEmployeeNumber can be NULL if no rep assigned.
PRIMARY KEY: customerNumber
FOREIGN KEY: salesRepEmployeeNumber → employees.employeeNumber
NULLABLE: salesRepEmployeeNumber (NULL = customer has no assigned sales representative)
""", metadata={"type": "schema"}),

        Document(page_content="""
TABLE: payments
COLUMNS: customerNumber, checkNumber, paymentDate, amount
DESCRIPTION: Stores customer payment transactions. Each payment identified by checkNumber.
PRIMARY KEY: (customerNumber, checkNumber)
FOREIGN KEY: customerNumber → customers.customerNumber
""", metadata={"type": "schema"}),

        Document(page_content="""
TABLE: orders
COLUMNS: orderNumber, orderDate, requiredDate, shippedDate, status, comments, customerNumber
DESCRIPTION: Stores customer orders.
IMPORTANT:
- status values: 'Shipped', 'In Process', 'Cancelled', 'On Hold', 'Disputed', 'Resolved'
- Use `status` to filter by order state (e.g., WHERE status = 'Shipped')
- Use `shippedDate IS NULL` when question means "not yet physically dispatched/shipped"
- Use `shippedDate IS NOT NULL` when the order has been physically dispatched
- These are DIFFERENT: status='Shipped' vs shippedDate IS NULL
PRIMARY KEY: orderNumber
FOREIGN KEY: customerNumber → customers.customerNumber
""", metadata={"type": "schema"}),

        Document(page_content="""
TABLE: orderdetails
COLUMNS: orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber
DESCRIPTION: Stores line items for each order. Revenue = quantityOrdered * priceEach.
PRIMARY KEY: (orderNumber, productCode)
FOREIGN KEYS:
- orderNumber → orders.orderNumber
- productCode → products.productCode
""", metadata={"type": "schema"}),
    ]

    # =========================================================
    # RELATIONSHIPS
    # =========================================================
    relationships = [
        Document(page_content="""
RELATIONSHIPS:
- customers.customerNumber = orders.customerNumber
- customers.customerNumber = payments.customerNumber
- customers.salesRepEmployeeNumber = employees.employeeNumber
- employees.officeCode = offices.officeCode
- employees.reportsTo = employees.employeeNumber  (self-join for manager hierarchy)
- orders.orderNumber = orderdetails.orderNumber
- orderdetails.productCode = products.productCode
- products.productLine = productlines.productLine

REVENUE FORMULA: quantityOrdered * priceEach (from orderdetails)
INVENTORY VALUE:  quantityInStock * buyPrice  (from products)
PROFIT MARGIN:    MSRP - buyPrice              (from products)
MARKUP %:         ((MSRP - buyPrice) / buyPrice) * 100
""", metadata={"type": "relationship"}),
    ]

    # =========================================================
    # EXAMPLES — organised by pattern
    # =========================================================
    examples = [

        # ── BASIC SELECT ─────────────────────────────────────

        Document(page_content="""
PATTERN: SELECT all rows from a table
Question: List all offices.
SQL: SELECT * FROM offices
""", metadata={"type": "example", "pattern": "basic_select"}),

        Document(page_content="""
PATTERN: SELECT specific columns
Question: Show product names and their vendors.
SQL: SELECT productName, productVendor FROM products
""", metadata={"type": "example", "pattern": "basic_select"}),

        Document(page_content="""
PATTERN: DISTINCT to remove duplicates
Question: What are the distinct countries where offices are located?
SQL: SELECT DISTINCT country FROM offices
""", metadata={"type": "example", "pattern": "distinct"}),

        Document(page_content="""
PATTERN: DISTINCT on multiple columns
Question: List all distinct country and territory combinations present in the offices.
SQL: SELECT DISTINCT country, territory FROM offices
""", metadata={"type": "example", "pattern": "distinct"}),

        # ── WHERE FILTERS ────────────────────────────────────

        Document(page_content="""
PATTERN: WHERE with string equality
Question: Find the employee holding the title of President.
SQL: SELECT employeeNumber, firstName, lastName FROM employees WHERE jobTitle = 'President'
""", metadata={"type": "example", "pattern": "where_string"}),

        Document(page_content="""
PATTERN: WHERE with numeric comparison greater than
Question: List products with a buy price exceeding 50.
SQL: SELECT productName, buyPrice FROM products WHERE buyPrice > 50
""", metadata={"type": "example", "pattern": "where_numeric"}),

        Document(page_content="""
PATTERN: WHERE with numeric comparison less than
Question: Find products with fewer than 200 units remaining in stock.
SQL: SELECT productCode, productName, quantityInStock FROM products WHERE quantityInStock < 200
""", metadata={"type": "example", "pattern": "where_numeric"}),

        Document(page_content="""
PATTERN: Filter orders not yet physically shipped — use shippedDate IS NULL
Question: Retrieve orders that have not been shipped yet
SQL: SELECT orderNumber, orderDate, status
FROM orders
WHERE shippedDate IS NULL
""", metadata={"type": "example", "pattern": "where_null"}),

        Document(page_content="""
PATTERN: WHERE IS NOT NULL — find present values
Question: List employees who have an assigned manager.
SQL: SELECT employeeNumber, firstName, lastName FROM employees WHERE reportsTo IS NOT NULL
""", metadata={"type": "example", "pattern": "where_null"}),

        Document(page_content="""
PATTERN: WHERE with IN list
Question: Retrieve all orders with a status of Cancelled or Disputed.
SQL: SELECT orderNumber, orderDate, status FROM orders WHERE status IN ('Cancelled', 'Disputed')
""", metadata={"type": "example", "pattern": "where_in"}),

        Document(page_content="""
PATTERN: WHERE with NOT IN list
Question: List offices not located in the USA or UK.
SQL: SELECT officeCode, city, country FROM offices WHERE country NOT IN ('USA', 'UK')
""", metadata={"type": "example", "pattern": "where_in"}),

        Document(page_content="""
PATTERN: WHERE BETWEEN for range filter
Question: Find payments with an amount between 10000 and 30000.
SQL: SELECT checkNumber, customerNumber, amount FROM payments WHERE amount BETWEEN 10000 AND 30000
""", metadata={"type": "example", "pattern": "where_between"}),

        Document(page_content="""
PATTERN: WHERE LIKE with wildcard — starts with
Question: List employees whose first name begins with the letter J.
SQL: SELECT employeeNumber, firstName, lastName FROM employees WHERE firstName LIKE 'J%'
""", metadata={"type": "example", "pattern": "where_like"}),

        Document(page_content="""
PATTERN: WHERE LIKE with wildcard — contains
Question: Find products whose name contains the word Ford.
SQL: SELECT productCode, productName FROM products WHERE productName LIKE '%Ford%'
""", metadata={"type": "example", "pattern": "where_like"}),

        Document(page_content="""
PATTERN: WHERE LIKE with wildcard — ends with
Question: Retrieve customers whose name ends with Inc.
SQL: SELECT customerNumber, customerName FROM customers WHERE customerName LIKE '%Inc'
""", metadata={"type": "example", "pattern": "where_like"}),

        Document(page_content="""
PATTERN: WHERE with AND — multiple conditions
Question: List Motorcycles products with an MSRP greater than 100.
SQL: SELECT productCode, productName, MSRP FROM products WHERE productLine = 'Motorcycles' AND MSRP > 100
""", metadata={"type": "example", "pattern": "where_and_or"}),

        Document(page_content="""
PATTERN: WHERE with OR — alternative conditions
Question: Retrieve customers located in Spain or Italy.
SQL: SELECT customerNumber, customerName, country FROM customers WHERE country = 'Spain' OR country = 'Italy'
""", metadata={"type": "example", "pattern": "where_and_or"}),

        # ── ORDER BY / LIMIT ─────────────────────────────────

        Document(page_content="""
PATTERN: ORDER BY ascending
Question: List all employees sorted alphabetically by last name.
SQL: SELECT employeeNumber, firstName, lastName FROM employees ORDER BY lastName ASC
""", metadata={"type": "example", "pattern": "order_limit"}),

        Document(page_content="""
PATTERN: ORDER BY descending with LIMIT — top N
Question: Identify the three most expensive products by MSRP.
SQL: SELECT productCode, productName, MSRP FROM products ORDER BY MSRP DESC LIMIT 3
""", metadata={"type": "example", "pattern": "order_limit"}),

        Document(page_content="""
PATTERN: ORDER BY with LIMIT and OFFSET — nth record
Question: Retrieve the second most recent order placed.
SQL: SELECT orderNumber, orderDate FROM orders ORDER BY orderDate DESC LIMIT 1 OFFSET 1
""", metadata={"type": "example", "pattern": "order_limit"}),

        # ── AGGREGATIONS ─────────────────────────────────────

        Document(page_content="""
PATTERN: COUNT all rows
Question: What is the total number of products in the catalog?
SQL: SELECT COUNT(*) AS totalProducts FROM products
""", metadata={"type": "example", "pattern": "aggregation"}),

        Document(page_content="""
PATTERN: SUM aggregation
Question: What is the total inventory value across all products?
SQL: SELECT SUM(quantityInStock * buyPrice) AS totalInventoryValue FROM products
""", metadata={"type": "example", "pattern": "aggregation"}),

        Document(page_content="""
PATTERN: AVG aggregation
Question: What is the average buy price across all products?
SQL: SELECT AVG(buyPrice) AS avgBuyPrice FROM products
""", metadata={"type": "example", "pattern": "aggregation"}),

        Document(page_content="""
PATTERN: MIN and MAX aggregation
Question: What are the minimum and maximum credit limits assigned to customers?
SQL: SELECT MIN(creditLimit) AS minCredit, MAX(creditLimit) AS maxCredit FROM customers
""", metadata={"type": "example", "pattern": "aggregation"}),

        Document(page_content="""
PATTERN: Computed column — arithmetic expression
Question: Calculate the profit margin for each product.
SQL: SELECT productCode, productName, (MSRP - buyPrice) AS profitMargin FROM products
""", metadata={"type": "example", "pattern": "computed_column"}),

        Document(page_content="""
PATTERN: Computed column — percentage formula with ROUND
Question: Display the markup percentage for each product.
SQL: SELECT productCode, productName, ROUND(((MSRP - buyPrice) / buyPrice) * 100, 2) AS markupPct FROM products
""", metadata={"type": "example", "pattern": "computed_column"}),

        # ── GROUP BY ─────────────────────────────────────────

        Document(page_content="""
PATTERN: GROUP BY with COUNT
Question: Count the number of products in each product line.
SQL: SELECT productLine, COUNT(*) AS productCount FROM products GROUP BY productLine
""", metadata={"type": "example", "pattern": "group_by"}),

        Document(page_content="""
PATTERN: GROUP BY with SUM
Question: What is the total amount paid by each customer?
SQL: SELECT customerNumber, SUM(amount) AS totalPaid FROM payments GROUP BY customerNumber
""", metadata={"type": "example", "pattern": "group_by"}),

        Document(page_content="""
PATTERN: GROUP BY with AVG
Question: What is the average MSRP for each product scale?
SQL: SELECT productScale, AVG(MSRP) AS avgMSRP FROM products GROUP BY productScale
""", metadata={"type": "example", "pattern": "group_by"}),

        Document(page_content="""
PATTERN: GROUP BY with multiple columns
Question: Provide a breakdown of order count by year and status.
SQL: SELECT YEAR(orderDate) AS orderYear, status, COUNT(*) AS orderCount
FROM orders
GROUP BY YEAR(orderDate), status
ORDER BY orderYear
""", metadata={"type": "example", "pattern": "group_by"}),

        # ── HAVING ───────────────────────────────────────────

        Document(page_content="""
PATTERN: HAVING with COUNT filter
Question: Which vendors supply more than 3 products?
SQL: SELECT productVendor, COUNT(*) AS productCount
FROM products
GROUP BY productVendor
HAVING COUNT(*) > 3
""", metadata={"type": "example", "pattern": "having"}),

        Document(page_content="""
PATTERN: HAVING with SUM filter
Question: Which product lines have a total stock value exceeding 500000?
SQL: SELECT productLine, SUM(quantityInStock * buyPrice) AS stockValue
FROM products
GROUP BY productLine
HAVING SUM(quantityInStock * buyPrice) > 500000
""", metadata={"type": "example", "pattern": "having"}),

        # ── JOINS ────────────────────────────────────────────

        Document(page_content="""
PATTERN: INNER JOIN — two tables
Question: Show each employee alongside the city of their assigned office.
SQL: SELECT e.firstName, e.lastName, o.city
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
""", metadata={"type": "example", "pattern": "join"}),

        Document(page_content="""
PATTERN: JOIN with WHERE filter
Question: List customers managed by a sales representative based in the London office.
SQL: SELECT c.customerName, e.firstName, e.lastName
FROM customers c
JOIN employees e ON c.salesRepEmployeeNumber = e.employeeNumber
JOIN offices o ON e.officeCode = o.officeCode
WHERE o.city = 'London'
""", metadata={"type": "example", "pattern": "join_where"}),

        Document(page_content="""
PATTERN: JOIN with GROUP BY and ORDER BY
Question: What is the total revenue generated by each product?
SQL: SELECT p.productCode, p.productName, SUM(od.quantityOrdered * od.priceEach) AS totalRevenue
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
GROUP BY p.productCode, p.productName
ORDER BY totalRevenue DESC
""", metadata={"type": "example", "pattern": "join_group"}),

        Document(page_content="""
PATTERN: Three-table JOIN
Question: Display each order along with the customer name and total order value.
SQL: SELECT o.orderNumber, c.customerName, SUM(od.quantityOrdered * od.priceEach) AS orderTotal
FROM orders o
JOIN customers c ON o.customerNumber = c.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
GROUP BY o.orderNumber, c.customerName
""", metadata={"type": "example", "pattern": "join_three"}),

        Document(page_content="""
PATTERN: Four-table JOIN for sales pipeline
Question: What is the total sales revenue generated by each office?
SQL: SELECT of.city, SUM(od.quantityOrdered * od.priceEach) AS totalSales
FROM offices of
JOIN employees e ON of.officeCode = e.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders o ON c.customerNumber = o.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
GROUP BY of.city
ORDER BY totalSales DESC
""", metadata={"type": "example", "pattern": "join_four"}),

        # ── LEFT JOIN ────────────────────────────────────────

        Document(page_content="""
PATTERN: LEFT JOIN to include unmatched rows
Question: List all customers along with their orders, including those who have never placed an order.
SQL: SELECT c.customerNumber, c.customerName, o.orderNumber
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
""", metadata={"type": "example", "pattern": "left_join"}),

        Document(page_content="""
PATTERN: LEFT JOIN with IS NULL to find missing relationships
Question: Identify products that have never been included in any order.
SQL: SELECT p.productCode, p.productName
FROM products p
LEFT JOIN orderdetails od ON p.productCode = od.productCode
WHERE od.productCode IS NULL
""", metadata={"type": "example", "pattern": "left_join_null"}),

        Document(page_content="""
PATTERN: LEFT JOIN to find customers without payments
Question: Which customers have never made a payment?
SQL: SELECT c.customerNumber, c.customerName
FROM customers c
LEFT JOIN payments p ON c.customerNumber = p.customerNumber
WHERE p.customerNumber IS NULL
""", metadata={"type": "example", "pattern": "left_join_null"}),

        # ── SELF JOIN ────────────────────────────────────────

        Document(page_content="""
PATTERN: Self-join to resolve manager hierarchy
Question: List each employee along with the name of their direct manager.
SQL: SELECT e.firstName AS empFirst, e.lastName AS empLast,
       m.firstName AS mgrFirst, m.lastName AS mgrLast
FROM employees e
LEFT JOIN employees m ON e.reportsTo = m.employeeNumber
""", metadata={"type": "example", "pattern": "self_join"}),

        Document(page_content="""
PATTERN: Self-join with WHERE to filter hierarchy
Question: List all employees who report directly to employee number 1002.
SQL: SELECT employeeNumber, firstName, lastName, jobTitle
FROM employees
WHERE reportsTo = 1002
""", metadata={"type": "example", "pattern": "self_join"}),

        # ── DATE FUNCTIONS ───────────────────────────────────

        Document(page_content="""
PATTERN: YEAR() filter on date column
Question: Retrieve all payments received during the year 2004.
SQL: SELECT checkNumber, customerNumber, paymentDate, amount
FROM payments
WHERE YEAR(paymentDate) = 2004
""", metadata={"type": "example", "pattern": "date_filter"}),

        Document(page_content="""
PATTERN: MONTH() filter on date column
Question: Find all orders placed during the month of March.
SQL: SELECT orderNumber, orderDate, customerNumber
FROM orders
WHERE MONTH(orderDate) = 3
""", metadata={"type": "example", "pattern": "date_filter"}),

        Document(page_content="""
PATTERN: GROUP BY YEAR and MONTH for time series
Question: How many orders were placed each month across all years?
SQL: SELECT YEAR(orderDate) AS yr, MONTH(orderDate) AS mo, COUNT(*) AS orderCount
FROM orders
GROUP BY YEAR(orderDate), MONTH(orderDate)
ORDER BY yr, mo
""", metadata={"type": "example", "pattern": "date_group"}),

        Document(page_content="""
PATTERN: DATEDIFF to compute delay between two dates
Question: How many days elapsed between the required date and the actual shipment date for each order?
SQL: SELECT orderNumber, requiredDate, shippedDate,
       DATEDIFF(shippedDate, requiredDate) AS daysLate
FROM orders
WHERE shippedDate IS NOT NULL
""", metadata={"type": "example", "pattern": "date_diff"}),

        Document(page_content="""
PATTERN: Compare two date columns directly
Question: Retrieve all orders that were shipped before the required date.
SQL: SELECT orderNumber, orderDate, requiredDate, shippedDate
FROM orders
WHERE shippedDate < requiredDate
""", metadata={"type": "example", "pattern": "date_compare"}),

        # ── SUBQUERIES ───────────────────────────────────────

        Document(page_content="""
PATTERN: Subquery in WHERE — scalar comparison
Question: Find all products with a buy price above the overall average buy price.
SQL: SELECT productCode, productName, buyPrice
FROM products
WHERE buyPrice > (SELECT AVG(buyPrice) FROM products)
""", metadata={"type": "example", "pattern": "subquery_scalar"}),

        Document(page_content="""
PATTERN: Subquery in WHERE — max value
Question: Which customer holds the highest credit limit?
SQL: SELECT customerNumber, customerName, creditLimit
FROM customers
WHERE creditLimit = (SELECT MAX(creditLimit) FROM customers)
""", metadata={"type": "example", "pattern": "subquery_scalar"}),

        Document(page_content="""
PATTERN: Subquery with IN — semi-join
Question: List customers located in a city where the company also has an office.
SQL: SELECT customerNumber, customerName, city
FROM customers
WHERE city IN (SELECT city FROM offices)
""", metadata={"type": "example", "pattern": "subquery_in"}),

        Document(page_content="""
PATTERN: Subquery with NOT IN — anti-join
Question: Identify products that have never appeared in any order.
SQL: SELECT productCode, productName
FROM products
WHERE productCode NOT IN (SELECT DISTINCT productCode FROM orderdetails)
""", metadata={"type": "example", "pattern": "subquery_in"}),

        Document(page_content="""
PATTERN: Derived table subquery in FROM clause
Question: What is the average total value across all orders?
SQL: SELECT AVG(orderTotal) AS avgOrderValue
FROM (
    SELECT orderNumber, SUM(quantityOrdered * priceEach) AS orderTotal
    FROM orderdetails
    GROUP BY orderNumber
) AS orderTotals
""", metadata={"type": "example", "pattern": "subquery_from"}),

        Document(page_content="""
PATTERN: Correlated subquery — per-group max
Question: Which product has the highest quantity in stock within each product line?
SQL: SELECT productLine, productCode, productName, quantityInStock
FROM products p
WHERE quantityInStock = (
    SELECT MAX(quantityInStock) FROM products WHERE productLine = p.productLine
)
""", metadata={"type": "example", "pattern": "subquery_correlated"}),

        # ── CASE WHEN ────────────────────────────────────────

        Document(page_content="""
PATTERN: CASE WHEN for conditional bucketing
Question: Classify each product as Cheap, Mid-Range, or Expensive based on its buy price.
SQL: SELECT productCode, productName, buyPrice,
       CASE
           WHEN buyPrice < 30  THEN 'Cheap'
           WHEN buyPrice BETWEEN 30 AND 80 THEN 'Mid-Range'
           ELSE 'Expensive'
       END AS priceCategory
FROM products
""", metadata={"type": "example", "pattern": "case_when"}),

        Document(page_content="""
PATTERN: CASE WHEN with COUNT for pivot-style summary
Question: How many orders are currently active compared to those that are closed?
SQL: SELECT
    SUM(CASE WHEN status IN ('Shipped', 'Resolved') THEN 1 ELSE 0 END) AS closedOrders,
    SUM(CASE WHEN status IN ('In Process', 'On Hold') THEN 1 ELSE 0 END) AS activeOrders
FROM orders
""", metadata={"type": "example", "pattern": "case_when"}),

        # ── STRING FUNCTIONS ─────────────────────────────────

        Document(page_content="""
PATTERN: CONCAT to build full name
Question: Display the full name of each employee in a single column.
SQL: SELECT employeeNumber, CONCAT(firstName, ' ', lastName) AS fullName FROM employees
""", metadata={"type": "example", "pattern": "string_functions"}),

        Document(page_content="""
PATTERN: CONCAT in JOIN context
Question: Show each customer alongside the full name of their assigned sales representative.
SQL: SELECT c.customerName,
       CONCAT(e.firstName, ' ', e.lastName) AS salesRepName
FROM customers c
LEFT JOIN employees e ON c.salesRepEmployeeNumber = e.employeeNumber
""", metadata={"type": "example", "pattern": "string_functions"}),

        # ── COUNT DISTINCT ───────────────────────────────────

        Document(page_content="""
PATTERN: COUNT DISTINCT for unique values
Question: How many distinct countries are represented in the customer base?
SQL: SELECT COUNT(DISTINCT country) AS uniqueCountries FROM customers
""", metadata={"type": "example", "pattern": "count_distinct"}),

        Document(page_content="""
PATTERN: COUNT DISTINCT products in orders
Question: How many distinct products have been ordered at least once?
SQL: SELECT COUNT(DISTINCT productCode) AS uniqueProducts FROM orderdetails
""", metadata={"type": "example", "pattern": "count_distinct"}),

        # ── COMPLEX MULTI-JOIN WITH AGGREGATION ──────────────

        Document(page_content="""
PATTERN: Full sales pipeline — employee to revenue
Question: What is the total revenue generated by each sales representative?
SQL: SELECT e.employeeNumber, e.firstName, e.lastName,
       SUM(od.quantityOrdered * od.priceEach) AS totalRevenue
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders o ON c.customerNumber = o.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
GROUP BY e.employeeNumber, e.firstName, e.lastName
ORDER BY totalRevenue DESC
""", metadata={"type": "example", "pattern": "complex_join"}),

        Document(page_content="""
PATTERN: Revenue grouped by product line via multi-join
Question: Which product line generated the highest total revenue?
SQL: SELECT p.productLine, SUM(od.quantityOrdered * od.priceEach) AS totalRevenue
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
GROUP BY p.productLine
ORDER BY totalRevenue DESC
""", metadata={"type": "example", "pattern": "complex_join"}),

        Document(page_content="""
PATTERN: Revenue grouped by country via multi-join
Question: What is the total revenue generated from customers in each country?
SQL: SELECT c.country, SUM(od.quantityOrdered * od.priceEach) AS totalRevenue
FROM customers c
JOIN orders o ON c.customerNumber = o.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
GROUP BY c.country
ORDER BY totalRevenue DESC
""", metadata={"type": "example", "pattern": "complex_join"}),

        # ── SINGLE-TABLE AGGREGATION (no unnecessary JOIN) ────

        Document(page_content="""
PATTERN: Single-table aggregation — count customers per sales rep without joining employees
Question: How many customers are assigned to each sales representative?
SQL: SELECT salesRepEmployeeNumber, COUNT(*) AS customerCount
FROM customers
WHERE salesRepEmployeeNumber IS NOT NULL
GROUP BY salesRepEmployeeNumber
""", metadata={"type": "example", "pattern": "single_table_agg"}),

        Document(page_content="""
PATTERN: Single-table aggregation — total quantity per product from orderdetails only
Question: What is the total quantity ordered for each product?
SQL: SELECT productCode, SUM(quantityOrdered) AS totalOrdered
FROM orderdetails
GROUP BY productCode
ORDER BY totalOrdered DESC
""", metadata={"type": "example", "pattern": "single_table_agg"}),

        # ── CASE WHEN PER-ROW CLASSIFICATION ────────────────

        Document(page_content="""
PATTERN: CASE WHEN per-row classification — individual rows, no GROUP BY
Question: Classify each customer into a credit tier based on their credit limit.
SQL: SELECT customerNumber, customerName, creditLimit,
       CASE
           WHEN creditLimit < 25000 THEN 'Low'
           WHEN creditLimit BETWEEN 25000 AND 75000 THEN 'Medium'
           ELSE 'High'
       END AS creditTier
FROM customers
""", metadata={"type": "example", "pattern": "case_when_per_row"}),

        # ── LIKE ON JOB TITLE ────────────────────────────────

        Document(page_content="""
PATTERN: LIKE filter on jobTitle to find roles containing a word
Question: List all employees whose job title contains the word Manager.
SQL: SELECT employeeNumber, firstName, lastName, email, jobTitle
FROM employees
WHERE jobTitle LIKE '%Manager%'
""", metadata={"type": "example", "pattern": "where_like_jobtitle"}),

        # ── WHERE FILTER WITH ENTITY DEFAULT COLUMNS ─────────

        Document(page_content="""
PATTERN: WHERE filter on orders — return identifying columns by default
Question: Retrieve all orders with a status of Cancelled.
SQL: SELECT orderNumber, orderDate, status, customerNumber
FROM orders
WHERE status = 'Cancelled'
""", metadata={"type": "example", "pattern": "where_entity_columns"}),

        # ── SINGLE-TABLE COUNT PATTERNS (no unnecessary JOIN) ─

        Document(page_content="""
PATTERN: Count orders per customer — use orders table only, do NOT join customers
Question: Give me number of orders for every customer.
SQL: SELECT customerNumber, COUNT(orderNumber) AS orderCount
FROM orders
GROUP BY customerNumber
""", metadata={"type": "example", "pattern": "single_table_count"}),

        Document(page_content="""
PATTERN: Count employees per office — use employees table only, do NOT join offices
Question: Count the number of employees in each office.
SQL: SELECT officeCode, COUNT(*) AS employeeCount
FROM employees
GROUP BY officeCode
""", metadata={"type": "example", "pattern": "single_table_count"}),

        Document(page_content="""
PATTERN: Count customers per sales rep — use customers table only, do NOT join employees
Question: Find the number of customers each sales representative handles.
SQL: SELECT salesRepEmployeeNumber, COUNT(*) AS customerCount
FROM customers
WHERE salesRepEmployeeNumber IS NOT NULL
GROUP BY salesRepEmployeeNumber
""", metadata={"type": "example", "pattern": "single_table_count"}),

        Document(page_content="""
PATTERN: Count direct reports per manager — single-table self-group, no self-join
Question: What is the total number of direct reports for each manager?
SQL: SELECT reportsTo AS managerNumber, COUNT(*) AS directReports
FROM employees
WHERE reportsTo IS NOT NULL
GROUP BY reportsTo
""", metadata={"type": "example", "pattern": "single_table_count"}),

        # ── EMPLOYEE ROLE / JOBTITLE ─────────────────────────

        Document(page_content="""
PATTERN: Find employees by job title — use WHERE jobTitle, NOT subquery on customers
Question: Show the email addresses of all sales representatives.
SQL: SELECT firstName, lastName, email
FROM employees
WHERE jobTitle = 'Sales Rep'
""", metadata={"type": "example", "pattern": "jobtitle_filter"}),

        Document(page_content="""
PATTERN: Find employees by partial job title using LIKE
Question: List all employees who are Sales Managers.
SQL: SELECT employeeNumber, firstName, lastName, email, officeCode
FROM employees
WHERE jobTitle LIKE '%Sales Manager%'
""", metadata={"type": "example", "pattern": "jobtitle_filter"}),

        # ── HAVING — always include aggregated value in SELECT ─

        Document(page_content="""
PATTERN: HAVING filter — ALWAYS include the COUNT/SUM in SELECT
Question: Find the orders that have more than 10 line items.
SQL: SELECT orderNumber, COUNT(*) AS lineItemCount
FROM orderdetails
GROUP BY orderNumber
HAVING COUNT(*) > 10
""", metadata={"type": "example", "pattern": "having_with_agg"}),

        Document(page_content="""
PATTERN: HAVING with DISTINCT — include aggregated value in SELECT
Question: List customers who have made payments over 50000.
SQL: SELECT DISTINCT c.customerNumber, c.customerName
FROM customers c
JOIN payments p ON c.customerNumber = p.customerNumber
WHERE p.amount > 50000
""", metadata={"type": "example", "pattern": "having_distinct"}),

        # ── JOIN COLUMN SETS ─────────────────────────────────

        Document(page_content="""
PATTERN: Employees + offices JOIN — include employeeNumber and office location columns
Question: Show me all employees working in offices outside the USA.
SQL: SELECT e.employeeNumber, e.firstName, e.lastName, o.city, o.country
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
WHERE o.country != 'USA'
""", metadata={"type": "example", "pattern": "join_cols"}),

        Document(page_content="""
PATTERN: Employees + offices JOIN — include employeeNumber and office city and country
Question: Show employees and their office city and country.
SQL: SELECT e.employeeNumber, e.firstName, e.lastName, o.city, o.country
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
""", metadata={"type": "example", "pattern": "join_cols"}),

        Document(page_content="""
PATTERN: Orders + customers JOIN — include standard order columns (orderNumber, orderDate, status) and customerName
Question: Show me orders with their customer names.
SQL: SELECT o.orderNumber, o.orderDate, o.status, c.customerName
FROM orders o
JOIN customers c ON o.customerNumber = c.customerNumber
""", metadata={"type": "example", "pattern": "join_cols"}),

        Document(page_content="""
PATTERN: Products + productlines JOIN — include productLine column from productlines
Question: Show me products with their product line descriptions.
SQL: SELECT p.productCode, p.productName, pl.productLine, pl.textDescription
FROM products p
JOIN productlines pl ON p.productLine = pl.productLine
""", metadata={"type": "example", "pattern": "join_cols"}),

        Document(page_content="""
PATTERN: Customers + orders JOIN COUNT — include customerNumber and customerName in SELECT
Question: How many orders did each customer make and their name?
SQL: SELECT c.customerNumber, c.customerName, COUNT(o.orderNumber) AS orderCount
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
GROUP BY c.customerNumber, c.customerName
""", metadata={"type": "example", "pattern": "join_cols"}),

        Document(page_content="""
PATTERN: Sales pipeline JOIN COUNT — include employeeNumber in SELECT
Question: What is the total sales by sales representative?
SQL: SELECT e.employeeNumber, e.firstName, e.lastName,
       SUM(od.quantityOrdered * od.priceEach) AS totalSales
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders o ON c.customerNumber = o.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
GROUP BY e.employeeNumber, e.firstName, e.lastName
ORDER BY totalSales DESC
""", metadata={"type": "example", "pattern": "join_cols"}),

        Document(page_content="""
PATTERN: Average aggregation — include GROUP BY column in SELECT
Question: What is the average payment amount per customer?
SQL: SELECT customerNumber, AVG(amount) AS avgPayment
FROM payments
GROUP BY customerNumber
""", metadata={"type": "example", "pattern": "group_by_col"}),

        Document(page_content="""
PATTERN: CONCAT with identifier — always include the primary key alongside computed columns
Question: Get the concatenated full name of all employees.
SQL: SELECT employeeNumber, CONCAT(firstName, ' ', lastName) AS fullName
FROM employees
""", metadata={"type": "example", "pattern": "concat_with_id"}),

        Document(page_content="""
PATTERN: SELECT * for "all [entities]" queries with no specific field mentioned
Question: Show all orders that are currently shipped.
SQL: SELECT * FROM orders WHERE status = 'Shipped'
""", metadata={"type": "example", "pattern": "select_star_all"}),

        Document(page_content="""
PATTERN: SELECT * for single-entity lookup ("who is the...")
Question: Who is the employee with the highest employee number?
SQL: SELECT * FROM employees ORDER BY employeeNumber DESC LIMIT 1
""", metadata={"type": "example", "pattern": "select_star_who"}),

        Document(page_content="""
PATTERN: Recent N records — include all standard entity columns
Question: What are the 5 most recent orders?
SQL: SELECT orderNumber, orderDate, customerNumber, status
FROM orders
ORDER BY orderDate DESC
LIMIT 5
""", metadata={"type": "example", "pattern": "recent_n"}),

        Document(page_content="""
PATTERN: Most expensive order — use orders+orderdetails only, include orderDate and customerNumber
Question: Show me the details of the most expensive order by total value.
SQL: SELECT o.orderNumber, o.orderDate, o.customerNumber,
       SUM(od.quantityOrdered * od.priceEach) AS totalValue
FROM orders o
JOIN orderdetails od ON o.orderNumber = od.orderNumber
GROUP BY o.orderNumber, o.orderDate, o.customerNumber
ORDER BY totalValue DESC
LIMIT 1
""", metadata={"type": "example", "pattern": "most_expensive_order"}),

        Document(page_content="""
PATTERN: Manager hierarchy self-join — include employeeNumber, full name, jobTitle, and manager info
Question: Show the levels of employees and their managers.
SQL: SELECT e.employeeNumber, CONCAT(e.firstName, ' ', e.lastName) AS employeeName,
       e.jobTitle, m.employeeNumber AS managerNumber,
       CONCAT(m.firstName, ' ', m.lastName) AS managerName
FROM employees e
LEFT JOIN employees m ON e.reportsTo = m.employeeNumber
""", metadata={"type": "example", "pattern": "self_join_hierarchy"}),

    ]

    return schema_docs + relationships + examples