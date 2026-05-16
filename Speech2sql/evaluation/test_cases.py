test_cases = [
    # ─────────────────────────────────────────────
    #  EASY — Simple SELECT (5 queries)
    # ─────────────────────────────────────────────
    {
        "question": "Show all employees",
        "ground_truth": "SELECT * FROM employees"
    },
    {
        "question": "List all offices",
        "ground_truth": "SELECT * FROM offices"
    },
    {
        "question": "Show product names and their prices",
        "ground_truth": "SELECT productName, buyPrice FROM products"
    },
    {
        "question": "Display all payment amounts",
        "ground_truth": "SELECT amount FROM payments"
    },
    {
        "question": "What are the different product lines?",
        "ground_truth": "SELECT DISTINCT productLine FROM products"
    },

    # ─────────────────────────────────────────────
    #  MEDIUM — Simple JOINs and WHERE (7 queries)
    # ─────────────────────────────────────────────
    {
        "question": "Show customer names and their country",
        "ground_truth": "SELECT customerName, country FROM customers"
    },
    {
        "question": "List employees who work in San Francisco office",
        "ground_truth": """
            SELECT e.firstName, e.lastName
            FROM employees e
            JOIN offices o ON e.officeCode = o.officeCode
            WHERE o.city = 'San Francisco'
        """
    },
    {
        "question": "Find all orders placed in 2003",
        "ground_truth": """
            SELECT orderNumber, orderDate
            FROM orders
            WHERE YEAR(orderDate) = 2003
        """
    },
    {
        "question": "Show product names in the 'Classic Cars' product line",
        "ground_truth": """
            SELECT productName
            FROM products
            WHERE productLine = 'Classic Cars'
        """
    },
    {
        "question": "Which customers are from the USA?",
        "ground_truth": """
            SELECT customerName, city, state
            FROM customers
            WHERE country = 'USA'
        """
    },
    {
        "question": "List products with price higher than $100",
        "ground_truth": """
            SELECT productName, buyPrice
            FROM products
            WHERE buyPrice > 100
        """
    },
    {
        "question": "Find payments made in 2004",
        "ground_truth": """
            SELECT customerNumber, amount, paymentDate
            FROM payments
            WHERE YEAR(paymentDate) = 2004
        """
    },

    # ─────────────────────────────────────────────
    #  HARD — Aggregations, GROUP BY (4 queries)
    # ─────────────────────────────────────────────
    {
        "question": "How many employees work in each office?",
        "ground_truth": """
            SELECT o.officeCode, o.city, COUNT(e.employeeNumber) AS employeeCount
            FROM offices o
            LEFT JOIN employees e ON o.officeCode = e.officeCode
            GROUP BY o.officeCode, o.city
        """
    },
    {
        "question": "What is the total amount paid by each customer?",
        "ground_truth": """
            SELECT c.customerNumber, c.customerName, SUM(p.amount) AS totalPaid
            FROM customers c
            JOIN payments p ON c.customerNumber = p.customerNumber
            GROUP BY c.customerNumber, c.customerName
            ORDER BY totalPaid DESC
        """
    },
    {
        "question": "Count how many products are in each product line",
        "ground_truth": """
            SELECT productLine, COUNT(productCode) AS productCount
            FROM products
            GROUP BY productLine
        """
    },
    {
        "question": "Find the average buy price for each product line",
        "ground_truth": """
            SELECT productLine, AVG(buyPrice) AS avgPrice
            FROM products
            GROUP BY productLine
        """
    },

    # ─────────────────────────────────────────────
    #  VERY HARD — Complex JOINs, HAVING, LEFT JOIN with NULL (4 queries)
    # ─────────────────────────────────────────────
    {
        "question": "Which product lines have more than 50 products?",
        "ground_truth": """
            SELECT productLine, COUNT(productCode) AS productCount
            FROM products
            GROUP BY productLine
            HAVING COUNT(productCode) > 50
        """
    },
    {
        "question": "Find employees who are not managers",
        "ground_truth": """
            SELECT e.employeeNumber, e.firstName, e.lastName
            FROM employees e
            LEFT JOIN employees m ON e.employeeNumber = m.reportsTo
            WHERE m.employeeNumber IS NULL
        """
    },
    {
        "question": "Show the total quantity ordered for each product",
        "ground_truth": """
            SELECT p.productCode, p.productName, SUM(od.quantityOrdered) AS totalOrdered
            FROM products p
            JOIN orderdetails od ON p.productCode = od.productCode
            GROUP BY p.productCode, p.productName
            ORDER BY totalOrdered DESC
        """
    },
    {
        "question": "Which customers have made more than 5 payments?",
        "ground_truth": """
            SELECT c.customerNumber, c.customerName, COUNT(p.checkNumber) AS paymentCount
            FROM customers c
            JOIN payments p ON c.customerNumber = p.customerNumber
            GROUP BY c.customerNumber, c.customerName
            HAVING COUNT(p.checkNumber) > 5
        """
    },

    # ═════════════════════════════════════════════
    #  NEW TEST CASES — 30 additional queries
    # ═════════════════════════════════════════════

    # ─────────────────────────────────────────────
    #  EASY — Simple SELECT (7 queries)
    # ─────────────────────────────────────────────
    {
        "question": "Show all customers",
        "ground_truth": "SELECT * FROM customers"
    },
    {
        "question": "List all products",
        "ground_truth": "SELECT * FROM products"
    },
    {
        "question": "Display all orders",
        "ground_truth": "SELECT * FROM orders"
    },
    {
        "question": "Show all product lines",
        "ground_truth": "SELECT * FROM productlines"
    },
    {
        "question": "List employee first names and last names",
        "ground_truth": "SELECT firstName, lastName FROM employees"
    },
    {
        "question": "Show customer names and their credit limits",
        "ground_truth": "SELECT customerName, creditLimit FROM customers"
    },
    {
        "question": "What are the distinct countries where customers are located?",
        "ground_truth": "SELECT DISTINCT country FROM customers"
    },

    # ─────────────────────────────────────────────
    #  MEDIUM — WHERE, JOINs, date filters (10 queries)
    # ─────────────────────────────────────────────
    {
        "question": "Find all orders that have been shipped",
        "ground_truth": """
            SELECT orderNumber, orderDate, shippedDate
            FROM orders
            WHERE status = 'Shipped'
        """
    },
    {
        "question": "List products with quantity in stock less than 100",
        "ground_truth": """
            SELECT productName, quantityInStock
            FROM products
            WHERE quantityInStock < 100
        """
    },
    {
        "question": "Show employees with the job title 'Sales Rep'",
        "ground_truth": """
            SELECT firstName, lastName, email
            FROM employees
            WHERE jobTitle = 'Sales Rep'
        """
    },
    {
        "question": "Find customers with a credit limit greater than 100000",
        "ground_truth": """
            SELECT customerName, creditLimit
            FROM customers
            WHERE creditLimit > 100000
        """
    },
    {
        "question": "List all offices located in the USA",
        "ground_truth": """
            SELECT officeCode, city, state
            FROM offices
            WHERE country = 'USA'
        """
    },
    {
        "question": "Show orders placed in 2005",
        "ground_truth": """
            SELECT orderNumber, orderDate, status
            FROM orders
            WHERE YEAR(orderDate) = 2005
        """
    },
    {
        "question": "Find products in the 'Motorcycles' product line",
        "ground_truth": """
            SELECT productName, buyPrice, quantityInStock
            FROM products
            WHERE productLine = 'Motorcycles'
        """
    },
    {
        "question": "Show the order number and quantity ordered for each order detail",
        "ground_truth": """
            SELECT orderNumber, productCode, quantityOrdered, priceEach
            FROM orderdetails
        """
    },
    {
        "question": "List customers who do not have an assigned sales representative",
        "ground_truth": """
            SELECT customerName, country
            FROM customers
            WHERE salesRepEmployeeNumber IS NULL
        """
    },
    {
        "question": "Show payments with an amount greater than 10000",
        "ground_truth": """
            SELECT customerNumber, checkNumber, amount, paymentDate
            FROM payments
            WHERE amount > 10000
        """
    },

    # ─────────────────────────────────────────────
    #  HARD — Aggregations, GROUP BY, ORDER BY (7 queries)
    # ─────────────────────────────────────────────
    {
        "question": "What is the total revenue generated from each order?",
        "ground_truth": """
            SELECT orderNumber, SUM(quantityOrdered * priceEach) AS totalRevenue
            FROM orderdetails
            GROUP BY orderNumber
            ORDER BY totalRevenue DESC
        """
    },
    {
        "question": "How many orders has each customer placed?",
        "ground_truth": """
            SELECT customerNumber, COUNT(orderNumber) AS orderCount
            FROM orders
            GROUP BY customerNumber
            ORDER BY orderCount DESC
        """
    },
    {
        "question": "Find the most expensive product in each product line",
        "ground_truth": """
            SELECT productLine, MAX(buyPrice) AS maxPrice
            FROM products
            GROUP BY productLine
        """
    },
    {
        "question": "Show the total number of orders per status",
        "ground_truth": """
            SELECT status, COUNT(orderNumber) AS orderCount
            FROM orders
            GROUP BY status
        """
    },
    {
        "question": "What is the average credit limit per country?",
        "ground_truth": """
            SELECT country, AVG(creditLimit) AS avgCreditLimit
            FROM customers
            GROUP BY country
            ORDER BY avgCreditLimit DESC
        """
    },
    {
        "question": "Show the total payment amount received per year",
        "ground_truth": """
            SELECT YEAR(paymentDate) AS paymentYear, SUM(amount) AS totalAmount
            FROM payments
            GROUP BY YEAR(paymentDate)
            ORDER BY paymentYear
        """
    },
    {
        "question": "Find the number of customers assigned to each sales representative",
        "ground_truth": """
            SELECT salesRepEmployeeNumber, COUNT(customerNumber) AS customerCount
            FROM customers
            WHERE salesRepEmployeeNumber IS NOT NULL
            GROUP BY salesRepEmployeeNumber
            ORDER BY customerCount DESC
        """
    },

    # ─────────────────────────────────────────────
    #  VERY HARD — Subqueries, HAVING, multi-JOIN, NULL (6 queries)
    # ─────────────────────────────────────────────
    {
        "question": "Which customers have never placed an order?",
        "ground_truth": """
            SELECT c.customerNumber, c.customerName
            FROM customers c
            LEFT JOIN orders o ON c.customerNumber = o.customerNumber
            WHERE o.orderNumber IS NULL
        """
    },
    {
        "question": "Find the top 5 customers by total payment amount",
        "ground_truth": """
            SELECT c.customerNumber, c.customerName, SUM(p.amount) AS totalPaid
            FROM customers c
            JOIN payments p ON c.customerNumber = p.customerNumber
            GROUP BY c.customerNumber, c.customerName
            ORDER BY totalPaid DESC
            LIMIT 5
        """
    },
    {
        "question": "Show product lines where the average buy price exceeds 50",
        "ground_truth": """
            SELECT productLine, AVG(buyPrice) AS avgPrice
            FROM products
            GROUP BY productLine
            HAVING AVG(buyPrice) > 50
        """
    },
    {
        "question": "List employees and the name of their direct manager",
        "ground_truth": """
            SELECT e.firstName, e.lastName, m.firstName AS managerFirstName, m.lastName AS managerLastName
            FROM employees e
            LEFT JOIN employees m ON e.reportsTo = m.employeeNumber
        """
    },
    {
        "question": "Find orders that contain more than 5 distinct products",
        "ground_truth": """
            SELECT orderNumber, COUNT(productCode) AS productCount
            FROM orderdetails
            GROUP BY orderNumber
            HAVING COUNT(productCode) > 5
        """
    },
    {
        "question": "Show the total quantity ordered and total revenue for each product",
        "ground_truth": """
            SELECT p.productCode, p.productName,
                   SUM(od.quantityOrdered) AS totalQuantity,
                   SUM(od.quantityOrdered * od.priceEach) AS totalRevenue
            FROM products p
            JOIN orderdetails od ON p.productCode = od.productCode
            GROUP BY p.productCode, p.productName
            ORDER BY totalRevenue DESC
        """
    },
]