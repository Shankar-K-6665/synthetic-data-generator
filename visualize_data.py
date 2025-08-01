import pandas as pd
import matplotlib.pyplot as plt

# Load your CSVs
users = pd.read_csv('users.csv')
transactions = pd.read_csv('transactions.csv')

# 🟢 1. Bar Chart: Sales by Category
category_sales = transactions.groupby('category')['amount'].sum().sort_values()
category_sales.plot(kind='barh', color='skyblue')
plt.title('💰 Total Sales by Category')
plt.xlabel('Total Amount (₹)')
plt.ylabel('Category')
plt.tight_layout()
plt.show()

# 🟣 2. Pie Chart: Gender Distribution
gender_counts = users['gender'].value_counts()
plt.figure(figsize=(5, 5))
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff'])
plt.title('👥 Gender Distribution of Users')
plt.axis('equal')
plt.show()

# 🔵 3. Line Chart: Transactions Over Time
transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])
daily_sales = transactions.groupby('transaction_date')['amount'].sum()
daily_sales.plot(kind='line', marker='o', color='green')
plt.title('📈 Daily Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Amount (₹)')
plt.tight_layout()
plt.show()

# 🟠 4. Histogram: Distribution of Transaction Amounts
plt.figure(figsize=(6,4))
plt.hist(transactions['amount'], bins=15, color='orange', edgecolor='black')
plt.title('💸 Distribution of Transaction Amounts')
plt.xlabel('Transaction Amount (₹)')
plt.ylabel('Number of Transactions')
plt.tight_layout()
plt.show()
