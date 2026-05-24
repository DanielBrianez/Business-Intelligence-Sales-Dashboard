SELECT
    category,
    ROUND(SUM(sales), 2) AS total_revenue
FROM sales
GROUP BY category
ORDER BY total_revenue DESC;