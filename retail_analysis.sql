-- =========================================================
-- Retail Sales & Inventory Performance Analysis — SQL queries
-- Run against retail.db (cleaned sales data + products/stores/inventory)
-- =========================================================

-- 1. Total revenue and profit
SELECT
    ROUND(SUM(s.quantity_sold * s.unit_price * (1 - s.discount_pct)), 2) AS total_revenue,
    ROUND(SUM(s.quantity_sold * (s.unit_price * (1 - s.discount_pct) - p.unit_cost)), 2) AS total_profit
FROM sales s
JOIN products p ON p.product_id = s.product_id;

-- 2. Revenue by category
SELECT
    p.category,
    ROUND(SUM(s.quantity_sold * s.unit_price * (1 - s.discount_pct)), 2) AS revenue
FROM sales s
JOIN products p ON p.product_id = s.product_id
GROUP BY p.category
ORDER BY revenue DESC;

-- 3. Revenue by region
SELECT
    st.region,
    ROUND(SUM(s.quantity_sold * s.unit_price * (1 - s.discount_pct)), 2) AS revenue
FROM sales s
JOIN stores st ON st.store_id = s.store_id
GROUP BY st.region
ORDER BY revenue DESC;

-- 4. Discount impact on average transaction value
SELECT
    CASE WHEN s.discount_pct > 0 THEN 'Discounted' ELSE 'Full price' END AS txn_type,
    ROUND(AVG(s.quantity_sold * s.unit_price * (1 - s.discount_pct)), 2) AS avg_txn_value,
    COUNT(*) AS num_transactions
FROM sales s
GROUP BY txn_type;

-- 5. Top 5 profit-driving products
SELECT
    p.product_name,
    ROUND(SUM(s.quantity_sold * (s.unit_price * (1 - s.discount_pct) - p.unit_cost)), 2) AS total_profit
FROM sales s
JOIN products p ON p.product_id = s.product_id
GROUP BY p.product_name
ORDER BY total_profit DESC
LIMIT 5;

-- 6. Monthly revenue trend (find peak month)
SELECT
    strftime('%Y-%m', s.transaction_date) AS month,
    ROUND(SUM(s.quantity_sold * s.unit_price * (1 - s.discount_pct)), 2) AS monthly_revenue
FROM sales s
GROUP BY month
ORDER BY month;

-- 7. Inventory at or below reorder point (stockout risk), by category
SELECT
    p.category,
    COUNT(*) AS store_product_combos_at_risk
FROM inventory i
JOIN products p ON p.product_id = i.product_id
WHERE i.stock_on_hand <= i.reorder_point
GROUP BY p.category
ORDER BY store_product_combos_at_risk DESC;

-- 8. % of all store-product combinations currently at risk of stockout
SELECT
    ROUND(100.0 * SUM(CASE WHEN stock_on_hand <= reorder_point THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_at_risk
FROM inventory;
