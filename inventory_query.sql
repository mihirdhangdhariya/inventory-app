CREATE TABLE Products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE Inventory (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES Products(id),
    quantity INTEGER NOT NULL,
    last_updated DATE DEFAULT CURRENT_DATE
);

CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    role VARCHAR(20)
);

CREATE TABLE Sales (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES Products(id),
    user_id INTEGER REFERENCES Users(id),
    quantity INTEGER NOT NULL,
    sale_date DATE NOT NULL,
    amount NUMERIC(10, 2) NOT NULL
);

CREATE TABLE VendorOrders (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES Products(id),
    vendor_name VARCHAR(100),
    quantity INTEGER NOT NULL,
    order_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'pending'
);


INSERT INTO Products (name, description, price) VALUES
('Laptop', 'High-end gaming laptop', 50000.00),
('Phone', 'Smartphone with camera', 20000.00),
('Headphones', 'Noise-cancelling', 5000.00);

INSERT INTO Inventory (product_id, quantity) VALUES
(1, 10),
(2, 20),
(3, 15);

INSERT INTO Users (username, email, role) VALUES
('Mihir', 'Mihir@example.com', 'customer'),
('atman', 'atman@example.com', 'admin');

INSERT INTO Sales (product_id, user_id, quantity, sale_date, amount) VALUES
(1, 1, 2, '2025-08-01', 100000.00),
(2, 1, 1, '2025-08-10', 20000.00),
(3, 2, 3, '2025-08-15', 15000.00);

INSERT INTO VendorOrders (product_id, vendor_name, quantity, status) VALUES
(1, 'VendorA', 5, 'completed');


SELECT * FROM Products;
SELECT * FROM Inventory;
SELECT * FROM Users;
SELECT * FROM Sales;
SELECT * FROM VendorOrders;


SELECT s.id, p.name AS product, u.username, s.quantity, s.sale_date, s.amount
FROM Sales s
JOIN Products p ON s.product_id = p.id
JOIN Users u ON s.user_id = u.id;