import pandas as pd

# load cleaned dataset

sales=pd.read_csv("cleaned_sales.csv")
print(type(sales))
print(sales.head())


print("="*50)
print("Feature engineering")
print("="*50)

#convert date

sales["transaction_date"] = pd.to_datetime(
    sales["transaction_date"]
)

#Gross sales
sales["gross_sales"]=(sales
    ["quantity_sold"]*sales["unit_price"])

#Discount Amount
sales["discount_amt"]=(sales
    ["gross_sales"]*sales["discount_pct"]/100)

#Net Sales

sales["net_sales"]=(sales
    ["gross_sales"]-sales["discount_amt"])

#year

sales["year"]=(sales
     ["transaction_date"].dt.year)

#Month
sales["month"]=(
    sales["transaction_date"].dt.month)

#MonthName

sales["month_name"]=(
    sales["transaction_date"].dt.month_name())

#Day of Week

sales["day_of_week"]=(
    sales["transaction_date"].dt.day_name())

#Quarter
sales["quarter"]=(
    sales["transaction_date"].dt.quarter)

# Display results

print("\n New columns created")

print([" gross_sales",
    "discount_amt",
    "net_sales",
    "year",
    "month",
    "month_name",
    "day_of_week",
    "quarter"])

print(sales.head(10).to_string(index=False))

#Sales Summary

print(sales[
    ["gross_sales",
    "discount_amt",
    "net_sales"]
].describe())

sales.to_csv("../Retail_sales/sales_analysis.csv",
             index=False)
