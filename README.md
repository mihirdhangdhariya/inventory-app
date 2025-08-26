# Inventory App

A simple web application for inventory and sales management, built with Flask and PostgreSQL. This project demonstrates PostgreSQL queries with JOINs for inventory management and sales reporting, as per the requirements for a Software Engineer role.

## Features
- **Inventory Management**: View current inventory with product details (uses JOIN between `Products` and `Inventory` tables).
- **Sales Reporting**: View sales within a date range, including total amount (uses JOINs between `Sales`, `Products`, and `Users` tables).
- **Add Inventory**: Update inventory via vendor orders, logging to `VendorOrders` and updating `Inventory`.

## Tech Stack
- **Backend**: Python, Flask
- **Database**: PostgreSQL
- **Frontend**: Basic HTML (minimal effort, as per task requirements)
- **Dependencies**: Listed in `requirements.txt`

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mihirdhangdhariya/inventory-app.git
   cd inventory-app
   ```

2. **Set Up PostgreSQL**:
   - Install PostgreSQL (https://www.postgresql.org/download/).
   - Create a database named `inventory_db`.
   - Run the SQL script in `inventory_query.sql` to create tables (`Products`, `Inventory`, `Sales`, `Users`, `VendorOrders`) and insert sample data.
   - Example (in psql or pgAdmin):
     ```bash
     psql -U postgres -d inventory_db -f inventory_query.sql
     ```

3. **Install Dependencies**:
   - Set up a Python virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
   - Install required packages:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the Application**:
   - Start the Flask server:
     ```bash
     python app.py
     ```
   - Access the app at `http://localhost:5000` on your computer or via your local IP (e.g., `http://192.168.1.100:5000`) on your phone (same Wi-Fi network).

## Key PostgreSQL Queries
- **Inventory View** (`/inventory` route):
  - Uses a JOIN to combine `Products` and `Inventory`:
    ```sql
    SELECT p.name, p.description, p.price, i.quantity, i.last_updated
    FROM Products p
    JOIN Inventory i ON p.id = i.product_id
    ORDER BY p.name;
    ```
- **Sales Report** (`/sales` route):
  - Uses JOINs across `Sales`, `Products`, and `Users`, with a date filter:
    ```sql
    SELECT s.sale_date, p.name, u.username, s.quantity, s.amount
    FROM Sales s
    JOIN Products p ON s.product_id = p.id
    JOIN Users u ON s.user_id = u.id
    WHERE s.sale_date BETWEEN %s AND %s
    ORDER BY s.sale_date;
    ```
  - Aggregates total sales amount:
    ```sql
    SELECT SUM(s.amount) as total_amount
    FROM Sales s
    WHERE s.sale_date BETWEEN %s AND %s;
    ```
- **Add Inventory** (`/add_inventory` route):
  - Inserts into `VendorOrders` and updates `Inventory` within a transaction.

## File Structure
- `app.py`: Main Flask application with routes and SQL queries.
- `inventory_query.sql`: SQL script to set up the database schema and sample data.
- `requirements.txt`: Python dependencies.
- `.gitignore`: Excludes `venv/`, `__pycache__/`, etc.

## Notes
- The app is designed to run on a local network, accessible on a phone via the host’s IP address.
- Minimal frontend effort, focusing on backend logic and PostgreSQL queries, as per the task.
- For the interview, the GitHub repository showcases the code, with emphasis on SQL JOINs and query logic.