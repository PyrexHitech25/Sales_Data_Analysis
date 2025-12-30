# Libary imports

import pandas as pd
import numpy as np

# Pandas Settings

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 2000)

# Import Data 

df = pd.read_csv(r'C:\Users\loren\Documents\Data Analyst\Messy Daten\messy_sales_data_01.csv')

# Inspect Data

#print(df.head(20))

# Cleaning Data
    # Check NaN Function
    
def check_NaN(column):
    num_missing = df[column].isna().sum()
    perc_missing = num_missing / len(df) * 100
    print(f'Column: {column} - Missing Values: {num_missing} ({perc_missing:.2f}%)')


    # Clean order_date

#check_NaN('order_date')

    # Clean Date_column
    
df['order_date'] = df['order_date'].str.replace('/', '-')
df['order_date'] = pd.to_datetime(df['order_date'], format='mixed', dayfirst=True, errors='coerce')
    
    # Replace values
    
df['order_id'] = df['order_id'].str.replace('ORD-', '')
df['quantity'] = df['quantity'].replace('ten', 10)
df['unit_price'] = (df['unit_price'].astype(str).str.replace(r'[^\d.,]', '', regex=True).str.replace(',', '.', regex=False))

    # Fill missing total_price values

df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')


    # Fill missing quantity and unit_price values

fill = (df['total_price'].notna()) & (df['quantity'].isna()) & (df['unit_price'].isna())
df.loc[fill, 'quantity'] = 1
df.loc[fill, 'unit_price'] = df.loc[fill, 'total_price']

    # Drop rows where all three values are missing

df = df.dropna(subset=['quantity', 'unit_price', 'total_price'], how='all', ignore_index=True)

    #

mean_monitor_unit_price = int(df[df['product'] == 'Monitor']['unit_price'].mean())
monitor = df[df['product'] == 'Monitor']

fill3 = (df['unit_price'].isna()) & (df['product'] == 'Monitor')
df.loc[fill3, 'unit_price'] = mean_monitor_unit_price


df['total_price'] = df['total_price'].fillna(df['quantity'] * df['unit_price'])

print(df.head(20))
check_NaN('total_price')
print(mean_monitor_unit_price)