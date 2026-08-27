import sqlite3
import pandas as pd

#1. connect to db

connection=sqlite3.connect(
    "../Retail_sales/retail.db")

sales=pd.read_sql_query(
    "select * from sales",connection)
connection.close()

#basic information
print("=" *50)
print("data quality checks")
print("=" *50)

print("\n data shape:")
print(sales.shape)

print("\n columns:")
print(sales.columns.to_list())

#missing values

print("\n" +"=" *50)
print("missing values")
print("="*50)

print(sales.isnull().sum())

#3. dupicates rows
print("\n"+"="*50)
print("Duplicates rows")
print("="*50)

print("exact duplicate values",
      sales.duplicated().sum())

# Find duplicates ids

print("\n"+"="*50)
print("duplicates transaction ids")
print("="*50)

dup_ids=sales[sales["transaction_id"].
              duplicated(keep=False)]

print("Without duplicates rows",len(dup_ids))

print("Duplicates ids rows",
    dup_ids["transaction_id"].nunique())

print("\n examples:")
#print(dup_ids.sort_values("tranaction_id").head(10))

# Negative quanties
print("\n"+"="*50)
print("negative quality")
print("="*50)

negative_quality=sales[sales["quantity_sold"]<0]

print("NEgative quality rows",len(negative_quality))

print("\n ", negative_quality.head(10))

#7.invalid prices

print("\n"+"="*50)
print("price check")
print("="*50)
print("missing prices", 
      sales["unit_price"].isnull().sum())
print("Zero prices:",(sales["unit_price"]==0).sum())

print("Negative prices:",
      (sales["unit_price"]<0).sum())

#8.Data Inspection
print("\n"+"="*50)
print("Data Inspection")
print("="*50)

print(sales["transaction_date"].head(20).
      to_string(index=False))

#8.Numeric Summery
print("\n"+"="*50)
print("Numeric Summery")
print("="*50)

print(sales[["quantity_sold", 
             "unit_price", "discount_pct"]].describe())

# data types
print("\n"+"="*50)
print("data types")
print("="*50)

print(sales.dtypes)

#Discount check
print("\n"+"="*50)
print(" Discount check")
print("="*50)
print("Negative discounts:",
      (sales["discount_pct"]<0).sum())
print("discount above 100%",
      (sales["discount_pct"]>100).sum())

#quantity check
print("\n"+"="*50)
print(" quantity check")
print("="*50)
print("zero quantity:",(sales["quantity_sold"]==0).sum())
print("Negative quantity:",(sales["quantity_sold"]<0).sum())

#Date check
print("\n"+"="*50)
print(" Date check")
print("="*50)

sales["transaction_date"]=pd.to_datetime(
    sales["transaction_date"],errors="coerce")

print("Invalied dates",(
sales["transaction_date"].isnull()).sum())

print("Earlist date:",sales["transaction_date"].min())

print("Latest date:",sales["transaction_date"].max())

sales.to_csv("../Retail_sales/cleaned_sales.csv",index=False)
