SELECT
    ROUND(SUM(sales), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS average_ticket
FROM sales;