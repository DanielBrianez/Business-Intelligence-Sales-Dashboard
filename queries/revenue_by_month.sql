SELECT
    year,
    month,
    month_name,
    ROUND(SUM(sales), 2) AS total_revenue
FROM sales
GROUP BY
    year,
    month,
    month_name
ORDER BY
    year,
    month;