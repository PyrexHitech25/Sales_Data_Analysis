# Libary imports

import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sqlalchemy import create_engine, text

# Pandas Settings

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 2000)

# Import Data 

df = pd.read_csv(r'C:\Users\Mypath\Messy Daten\messy_sales_data_01.csv')

# Inspect Data

print(df.head(20))

# Cleaning Data
    # Check NaN Function
    
def check_NaN(column):
    num_missing = df[column].isna().sum()
    perc_missing = num_missing / len(df) * 100
    print(f'Column: {column} - Missing Values: {num_missing} ({perc_missing:.2f}%)')


    # Check order_date

check_NaN('order_date')

    # Clean Date_column
    
df['order_date'] = df['order_date'].str.replace('/', '-')

    # Timestamp Flag at 2000-01-01
    
df['order_date'].fillna(pd.Timestamp('2000-01-01'), inplace=True)

    # Convert to datetime

df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', dayfirst=True, errors='coerce')
    
    # Replace values
    
df['order_id'] = df['order_id'].str.replace('ORD-', '')
df['quantity'] = df['quantity'].replace('ten', 10)
df['unit_price'] = (df['unit_price'].astype(str).str.replace(r'[^\d.,]', '', regex=True).str.replace(',', '.', regex=False))
df['region'] = df['region'].replace({'Usa': 'US', 'eu': 'EU', np.nan: 'Unknown'})
df['sales_person'] = df['sales_person'].replace({'BOB': 'Bob', 'alice': 'Alice', 'NaN': np.nan})
df['discount'] = df['discount'].str.replace(r'[^\d.,]', '', regex=True).str.replace(',', '.', regex=False)
df['discount'] = df['discount'].replace({np.nan: 0,'5': '0.05'}).astype(float)
df['sales_person'] = df['sales_person'].replace({np.nan: 'Unknown'})
df['notes'] = df['notes'].replace({np.nan: 'No Notes', 'repeat customer': 'Repeat Customer', 'urgent': 'Urgent', 'late payment': 'Late Payment'})
df['product'] = df['product'].replace(np.nan, 'Unknown')
df['order_id'].fillna(method='ffill', inplace=True)

    # Convert to numeric

df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')

    # Drop rows where all three values are missing

df = df.dropna(subset=['quantity', 'unit_price', 'total_price'], how='all', ignore_index=True)

    # fill missing unit_price for specific products

mean_monitor_unit_price = int(df[df['product'] == 'Monitor']['unit_price'].mean())
monitor = df[df['product'] == 'Monitor']
fill = (df['unit_price'].isna()) & (df['product'] == 'Monitor')
df.loc[fill, 'unit_price'] = mean_monitor_unit_price

mean_laptop_unit_price = int(df[df['product'] == 'Laptop']['unit_price'].mean())
laptop = df[df['product'] == 'Laptop']
fill2 = (df['unit_price'].isna()) & (df['product'] == 'Laptop')
df.loc[fill2, 'unit_price'] = mean_laptop_unit_price

mean_phone_unit_price = int(df[df['product'] == 'Phone']['unit_price'].mean())
phone = df[df['product'] == 'Phone']
fill3 = (df['unit_price'].isna()) & (df['product'] == 'Phone')
df.loc[fill3, 'unit_price'] = mean_phone_unit_price

mean_Mouse_unit_price = int(df[df['product'] == 'Mouse']['unit_price'].mean())
mouse = df[df['product'] == 'Mouse']
fill4 = (df['unit_price'].isna()) & (df['product'] == 'Mouse')
df.loc[fill4, 'unit_price'] = mean_Mouse_unit_price

    # Fill missing quantity and unit_price values

fill5 = (df['total_price'].notna()) & (df['quantity'].isna()) & (df['unit_price'].isna())
df.loc[fill5, 'quantity'] = 1
df.loc[fill5, 'unit_price'] = df.loc[fill5, 'total_price']

    # Multi Imputation for missing values

numerical_col = ['quantity' , 'unit_price', 'total_price']
imp = IterativeImputer(max_iter=10, random_state=0)
df[numerical_col] = np.round(imp.fit_transform(df[numerical_col]), 1)

    #Convert quantity to int

df['quantity'] = df['quantity'].astype(int)

# Fill total_price where missing with dis

df['total_price'] = df['total_price'].fillna(df['quantity'] * df['unit_price']) * (1 - df['discount'])

# Final Inspection



# Export Cleaned Data to MySQL

# Connection

engine = create_engine('mysql+pymysql://root:Cyperpunk13579!K@localhost:3306/')

# Create Database
with engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS messy_sales_db"))
    conn.commit()

print("Database created!")

engine = create_engine('mysql+pymysql://root:MyPassword!K@localhost:3306/messy_sales_db')

df.to_sql('Messy_Sales_Data_Cleaned', con=engine, if_exists='append', index=False)
