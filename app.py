from flask import Flask, request, render_template_string
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Database connection (update with your PostgreSQL details)
def get_db_connection():
    conn = psycopg2.connect(
        dbname='inventory_db',
        user='postgres',
        password='admin',
        host='localhost'
    )
    return conn

# Home page with links to features
@app.route('/')
def home():
    return render_template_string('''
    <h1>Inventory App</h1>
    <ul>
        <li><a href="/inventory">View Inventory</a></li>
        <li><a href="/sales">View Sales</a></li>
        <li><a href="/add_inventory">Add Inventory (from Vendor Order)</a></li>
    </ul>
    ''')

# View Inventory: Demonstrates JOIN between Products and Inventory
@app.route('/inventory')
def view_inventory():
    conn = get_db_connection()
    cur = conn.cursor()
    # SQL query with JOIN
    cur.execute('''
        SELECT p.name, p.description, p.price, i.quantity, i.last_updated
        FROM Products p
        JOIN Inventory i ON p.id = i.product_id
        ORDER BY p.name;
    ''')
    inventory = cur.fetchall()
    cur.close()
    conn.close()
    
    html = '<h1>Current Inventory</h1><table border="1"><tr><th>Name</th><th>Description</th><th>Price</th><th>Quantity</th><th>Last Updated</th></tr>'
    for item in inventory:
        html += f'<tr><td>{item[0]}</td><td>{item[1]}</td><td>{item[2]}</td><td>{item[3]}</td><td>{item[4]}</td></tr>'
    html += '</table><br><a href="/">Back</a>'
    return render_template_string(html)

# View Sales: Form for time interval, JOIN between Sales, Products, Users
@app.route('/sales', methods=['GET', 'POST'])
def view_sales():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        conn = get_db_connection()
        cur = conn.cursor()
        # SQL query with JOINs, WHERE for interval, GROUP BY for totals
        cur.execute('''
            SELECT s.sale_date, p.name, u.username, s.quantity, s.amount
            FROM Sales s
            JOIN Products p ON s.product_id = p.id
            JOIN Users u ON s.user_id = u.id
            WHERE s.sale_date BETWEEN %s AND %s
            ORDER BY s.sale_date;
        ''', (start_date, end_date))
        sales = cur.fetchall()
        
        # Aggregate total amount (another query demo)
        cur.execute('''
            SELECT SUM(s.amount) as total_amount
            FROM Sales s
            WHERE s.sale_date BETWEEN %s AND %s;
        ''', (start_date, end_date))
        total = cur.fetchone()[0] or 0
        
        cur.close()
        conn.close()
        
        html = f'<h1>Sales from {start_date} to {end_date}</h1><table border="1"><tr><th>Date</th><th>Product</th><th>User</th><th>Quantity</th><th>Amount</th></tr>'
        for sale in sales:
            html += f'<tr><td>{sale[0]}</td><td>{sale[1]}</td><td>{sale[2]}</td><td>{sale[3]}</td><td>{sale[4]}</td></tr>'
        html += f'</table><p>Total Amount: {total}</p><br><a href="/sales">Back</a>'
        return render_template_string(html)
    
    # GET: Show form
    today = datetime.today().strftime('%Y-%m-%d')
    return render_template_string(f'''
    <h1>View Sales</h1>
    <form method="post">
        Start Date: <input type="date" name="start_date" value="2025-08-01"><br>
        End Date: <input type="date" name="end_date" value="{today}"><br>
        <input type="submit" value="View Sales">
    </form>
    <br><a href="/">Home</a>
    ''')

# Add Inventory: Update Inventory quantity, insert into VendorOrders (demo transaction)
@app.route('/add_inventory', methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity = request.form['quantity']
        vendor_name = request.form['vendor_name']
        
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            # Insert into VendorOrders
            cur.execute('''
                INSERT INTO VendorOrders (product_id, vendor_name, quantity, status)
                VALUES (%s, %s, %s, 'completed');
            ''', (product_id, vendor_name, quantity))
            
            # Update Inventory (JOIN implicit in subquery, but simple UPDATE here)
            cur.execute('''
                UPDATE Inventory
                SET quantity = quantity + %s, last_updated = CURRENT_DATE
                WHERE product_id = %s;
            ''', (quantity, product_id))
            
            conn.commit()
            message = 'Inventory updated successfully!'
        except Exception as e:
            conn.rollback()
            message = f'Error: {str(e)}'
        finally:
            cur.close()
            conn.close()
        
        return render_template_string(f'<h1>{message}</h1><br><a href="/add_inventory">Back</a>')
    
    # GET: Show form (list products for selection)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM Products;')
    products = cur.fetchall()
    cur.close()
    conn.close()
    
    html = '<h1>Add Inventory from Vendor Order</h1><form method="post">Product: <select name="product_id">'
    for prod in products:
        html += f'<option value="{prod[0]}">{prod[1]}</option>'
    html += '</select><br>Quantity: <input type="number" name="quantity" required><br>Vendor Name: <input type="text" name="vendor_name" required><br><input type="submit" value="Add"></form><br><a href="/">Home</a>'
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)