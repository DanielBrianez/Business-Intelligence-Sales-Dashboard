SELECT
    customer_name,
    ROUND(SUM(sales), 2) AS total_revenue
FROM sales
GROUP BY customer_name
ORDER BY total_revenue DESC
LIMIT 10;