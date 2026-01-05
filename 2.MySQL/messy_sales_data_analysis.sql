SELECT * FROM messy_sales_db.messy_sales_data_cleaned;

USE messy_sales_data_analysis;

CREATE TABLE dim_region (
	region_id INT AUTO_INCREMENT PRIMARY KEY,
    region_date DATE,
    person VARCHAR(20) UNIQUE
);
    
    
