import pandas as pd

# Load CSV files
users = pd.read_csv('users.csv')
transactions = pd.read_csv('transactions.csv')

print("\n📊 Total Users:", len(users))
print("💳 Total Transactions:", len(transactions))

# 🧑‍🤝‍🧑 Count users by gender
gender_count = users['gender'].value_counts()
print("\n👥 User count by Gender:")
print(gender_count)

# 📊 Sales by category
category_sales = transactions.groupby('category')['amount'].sum().sort_values(ascending=False)
print("\n🛍️ Total Sales by Category:")
print(category_sales)

# 💰 Average transaction amount
avg_amount = transactions['amount'].mean()
print(f"\n💸 Average Transaction Amount: ₹{avg_amount:.2f}")

# 📈 Top 5 high-spending users
user_spending = transactions.groupby('user_id')['amount'].sum().sort_values(ascending=False)
top_users = user_spending.head(5).reset_index()
top_users = top_users.merge(users[['user_id', 'name']], on='user_id')

print("\n🏆 Top 5 High-Spending Users:")
print(top_users[['name', 'amount']])
