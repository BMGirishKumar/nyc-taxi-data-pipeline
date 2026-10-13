-- Create the table
CREATE TABLE products(
    product_id INT PRIMARY KEY,
    name VARCHAR(50),
    category VARCHAR(50),
    price DECIMAL(10,2)
);

CREATE TABLE order_items(
    item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT
);
INSERT INTO products (product_id, name, category, price) VALUES 
(1, 'Wireless Mouse', 'Accessories', 25.99),
(2, 'Mechanical Keyboard', 'Accessories', 79.99),
(3, 'Gaming Monitor', 'Monitors', 299.99),
(4, 'USB-C Cable', 'Cables', 12.50); -- Note: This item has never been ordered!

INSERT INTO order_items (item_id, order_id, product_id, quantity) VALUES 
(101, 5001, 1, 2), -- Order 5001 has 2 mice
(102, 5001, 2, 1), -- Order 5001 has 1 keyboard
(103, 5002, 1, 5), -- Order 5002 has 5 mice
(104, 5003, 3, 1); -- Order 5003 has 1 monitor
