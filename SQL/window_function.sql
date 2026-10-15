SELECT 
    department,
    employee_name,
    sale_amount,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY sale_amount DESC) AS row_num,
    RANK() OVER (PARTITION BY department ORDER BY sale_amount DESC) AS rnk,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY sale_amount DESC) AS dense_rnk
FROM sales_performance;


-- here you can see that ROW_NUMBER() function works for the the dept and orderd by sale_amount.
-- Here RANK() can help you rank the the things based on the sale_amount
-- Here DENSE_RANK() can help you rank the the things based on the sale_amount without missing the count


--Input:

--employee_id	employee_name	department	sale_date	sale_amount
--101	        Alice	        Electronics	2026-10-01	5000
--102	        Bob	            Electronics	2026-10-01	3000
--103	        Charlie	        Electronics	2026-10-02	5000
--104	        David	        Clothing	2026-10-01	4000
--105	        Eva	            Clothing	2026-10-02	2000
--106	        Frank	        Clothing	2026-10-02	4000



--Output:

--department	employee_name	sale_amount	row_num	rnk	           dense_rnk
--Electronics	Alice	            5000	     1	  1	            1
--Electronics	Charlie	            5000	     2	  1	            1
--Electronics	Bob	                3000	     3	  3 (skips 2)	2 (no skip)
--Clothing	    David	            4000	     1	  1	            1
--Clothing	    Frank	            4000	     2	  1	            1
--Clothing	     Eva	            2000	     3	  3	            2
