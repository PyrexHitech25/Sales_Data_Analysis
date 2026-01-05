SELECT * FROM messy_sales_db.messy_sales_data_cleaned;

ALTER TABLE messy_sales_db.messy_sales_data_cleaned
CHANGE order_id order_number VARCHAR(20);

ALTER TABLE messy_sales_db.messy_sales_data_cleaned
CHANGE `index` id VARCHAR(20);

CREATE DATABASE messy_sales_data_analysis;
USE messy_sales_data_analysis;

CREATE TABLE dim_sales_details (
	region_id INT AUTO_INCREMENT PRIMARY KEY,
    region_date DATE,
    person VARCHAR(20) UNIQUE,
    sales_product VARCHAR(20) UNIQUE,
);






CREATE TABLE report_analysis (
	analysis_id INT AUTO_INCREMENT PRIMARY KEY,
    min_total_price DECIMAL(10,2), 
    max_total_price DECIMAL(10,2),
    max_unit_price DECIMAL(10,2),
    min_unit_price DECIMAL(10,2)
);

INSERT IGNORE INTO report_analysis (min_total_price, max_total_price, min_unit_price, max_unit_price)
SELECT 
    MIN(total_price),
    MAX(total_price),
    MIN(unit_price),
    MAX(unit_price)
FROM messy_sales_db.messy_sales_data_cleaned
