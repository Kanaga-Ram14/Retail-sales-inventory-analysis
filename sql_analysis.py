import sqlite3
import pandas as pd

#connect to database
connection=sqlite3.connect("retail.db")

# Check table
tables=pd.read_sql_query(
    """Select name from sqlite_master where type='table';
    """,connection)

print("="*50)
print("Database Tables")
print("="*50)

print(tables)

#total transactions

query=""" 
select count(*) as total_transactions from sales;"""

result=pd.read_sql_query(query,connection)
print("\n total transaction")
print(result)

#total quantity sold
query="""
select sum(quantity_sold) As total_quantity from sales;
"""
result=pd.read_sql_query(query,connection)

print("\n result:", result)

#Total gross sales
query="""
Select sum(quantity_sold*unit_price) As gross_sales
from sales;"""

result=pd.read_sql_query(query,connection)

print("\n result:", result)



query="""
select 
store_id,
COUNT(*) As total_trans,
SUM(quantity_sold) As total_quantity,
SUM(quantity_sold*unit_price) As gross_sales,
AVG(quantity_sold*unit_price) As average_trans
FROM sales
Group by store_id
Order by gross_sales DESC;
"""

store_performance=pd.read_sql_query(
    query,connection)

print("\n"+"="*50)
print("store performance")
print("="*50)

print(store_performance.to_string(index=False))


query = """
SELECT
    product_id,
    COUNT(*) AS total_transactions,
    SUM(quantity_sold) AS total_quantity_sold,
    SUM(quantity_sold * unit_price) AS gross_sales,
    AVG(unit_price) AS average_unit_price
FROM sales
GROUP BY product_id
ORDER BY gross_sales DESC;
"""

product_performance = pd.read_sql_query(
    query,
    connection
)

print("\n" + "=" * 50)
print("PRODUCT PERFORMANCE")
print("=" * 50)

print(
    product_performance.to_string(index=False)
)

# --------------------------------------------------
# Top 10 Products by Gross Sales
# --------------------------------------------------

query = """
SELECT
    product_id,
    SUM(quantity_sold) AS total_quantity_sold,
    SUM(quantity_sold * unit_price) AS gross_sales
FROM sales
GROUP BY product_id
ORDER BY gross_sales DESC
LIMIT 10;
"""

top_products = pd.read_sql_query(
    query,
    connection
)

print("\n" + "=" * 50)
print("TOP 10 PRODUCTS BY GROSS SALES")
print("=" * 50)

print(
    top_products.to_string(index=False)
)

# --------------------------------------------------
# Top 10 Products by Quantity Sold
# --------------------------------------------------

query = """
SELECT
    product_id,
    SUM(quantity_sold) AS total_quantity_sold,
    SUM(quantity_sold * unit_price) AS gross_sales
FROM sales
GROUP BY product_id
ORDER BY total_quantity_sold DESC
LIMIT 10;
"""

top_quantity_products = pd.read_sql_query(
    query,
    connection
)

print("\n" + "=" * 50)
print("TOP 10 PRODUCTS BY QUANTITY SOLD")
print("=" * 50)

print(
    top_quantity_products.to_string(index=False)
)
# --------------------------------------------------
# Monthly Sales Trend
# --------------------------------------------------

query = """
SELECT
    strftime('%Y-%m', transaction_date) AS sales_month,
    COUNT(*) AS total_transactions,
    SUM(quantity_sold) AS total_quantity_sold,
    SUM(quantity_sold * unit_price) AS gross_sales
FROM sales
GROUP BY sales_month
ORDER BY sales_month;
"""

monthly_sales = pd.read_sql_query(
    query,
    connection
)

print("\n" + "=" * 50)
print("MONTHLY SALES TREND")
print("=" * 50)

print(
    monthly_sales.to_string(index=False)
)
# --------------------------------------------------
# Quarterly Sales Trend
# --------------------------------------------------

query = """
SELECT
    strftime('%Y', transaction_date) AS sales_year,
    CASE
        WHEN CAST(strftime('%m', transaction_date) AS INTEGER) BETWEEN 1 AND 3
            THEN 'Q1'
        WHEN CAST(strftime('%m', transaction_date) AS INTEGER) BETWEEN 4 AND 6
            THEN 'Q2'
        WHEN CAST(strftime('%m', transaction_date) AS INTEGER) BETWEEN 7 AND 9
            THEN 'Q3'
        ELSE 'Q4'
    END AS quarter,
    COUNT(*) AS total_transactions,
    SUM(quantity_sold) AS total_quantity_sold,
    SUM(quantity_sold * unit_price) AS gross_sales
FROM sales
GROUP BY sales_year, quarter
ORDER BY sales_year, quarter;
"""

quarterly_sales = pd.read_sql_query(
    query,
    connection
)

print("\n" + "=" * 50)
print("QUARTERLY SALES TREND")
print("=" * 50)

print(
    quarterly_sales.to_string(index=False)
)
# --------------------------------------------------
# Discount Analysis
# --------------------------------------------------

query = """
SELECT
    discount_pct,
    COUNT(*) AS total_transactions,
    SUM(quantity_sold) AS total_quantity_sold,
    SUM(quantity_sold * unit_price) AS gross_sales,
    SUM(
        quantity_sold * unit_price * discount_pct / 100
    ) AS discount_amount
FROM sales
GROUP BY discount_pct
ORDER BY discount_pct;
"""

discount_analysis = pd.read_sql_query(
    query,
    connection
)

print("\n" + "=" * 50)
print("DISCOUNT ANALYSIS")
print("=" * 50)

print(
    discount_analysis.to_string(index=False)
)
# --------------------------------------------------
# Overall Discount Impact
# --------------------------------------------------

query = """
SELECT
    SUM(quantity_sold * unit_price) AS gross_sales,

    SUM(
        quantity_sold * unit_price * discount_pct / 100
    ) AS total_discount,

    SUM(
        quantity_sold * unit_price
    ) -
    SUM(
        quantity_sold * unit_price * discount_pct / 100
    ) AS net_sales,

    AVG(discount_pct) AS average_discount
FROM sales;
"""

discount_impact = pd.read_sql_query(
    query,
    connection
)

print("\n" + "=" * 50)
print("OVERALL DISCOUNT IMPACT")
print("=" * 50)

print(
    discount_impact.to_string(index=False)
)
# --------------------------------------------------
# Average Transaction Value
# --------------------------------------------------

query = """
SELECT
    COUNT(*) AS total_transactions,
    SUM(quantity_sold * unit_price) AS gross_sales,
    AVG(quantity_sold * unit_price) AS average_transaction_value
FROM sales;
"""

transaction_value = pd.read_sql_query(
    query,
    connection
)

print("\n" + "=" * 50)
print("TRANSACTION VALUE")
print("=" * 50)

print(
    transaction_value.to_string(index=False)
)

connection.close()
tables.to_csv("../Retail_sales/sql_analysis.csv", index=False)

