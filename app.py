import matplotlib.pyplot as plt
import seaborn as sns
import datetime


import streamlit as st
import pandas as pd
from faker import Faker
import random

fake = Faker()

def generate_users(num_users):
    users = []
    for _ in range(num_users):
        gender = random.choice(['Male', 'Female'])
        age = random.randint(18, 65)
        user = {
            'user_id': fake.uuid4(),
            'name': fake.name(),
            'gender': gender,
            'age': age,
            'email': fake.email(),
            'phone': fake.phone_number(),
            'company': fake.company(),
            'job_title': fake.job(),
            'address': fake.address().replace("\n", ", "),
            'created_at': fake.date_this_decade()
        }
        users.append(user)
    return pd.DataFrame(users)

def generate_transactions(users_df, num_transactions):
    transactions = []
    payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'UPI', 'Cash']
    categories = ['Electronics', 'Books', 'Clothing', 'Groceries', 'Toys']

    for _ in range(num_transactions):
        user = users_df.sample().iloc[0]
        transaction = {
            'transaction_id': fake.uuid4(),
            'user_id': user['user_id'],
            'product': fake.word().title(),
            'category': random.choice(categories),
            'quantity': random.randint(1, 5),
            'amount': round(fake.pyfloat(left_digits=3, right_digits=2, positive=True, min_value=10, max_value=1000), 2),
            'payment_method': random.choice(payment_methods),
            'transaction_date': fake.date_between(start_date=user['created_at'])
        }
        transactions.append(transaction)
    return pd.DataFrame(transactions)

# Streamlit UI
st.title("🧪 Synthetic Data Generator Dashboard")

num_users = st.slider("Number of Users", 10, 500, 50)
num_transactions = st.slider("Number of Transactions", 10, 1000, 200)

if st.button("Generate Synthetic Data"):
    users_df = generate_users(num_users)
    transactions_df = generate_transactions(users_df, num_transactions)

    st.success("✅ Data Generated!")

    st.subheader("Preview - Users")
    st.dataframe(users_df.head())

    st.subheader("Preview - Transactions")
    st.dataframe(transactions_df.head())
    
    st.subheader("📊 Filter Transactions by Category")

    # Dropdown to select category
    selected_category = st.selectbox("Choose a category", transactions_df["category"].unique())

    # Filter the dataframe
    filtered_df = transactions_df[transactions_df["category"] == selected_category]

    # Display filtered results
    st.write(f"Showing {len(filtered_df)} transactions for category: **{selected_category}**")
    st.dataframe(filtered_df)
    
    st.subheader("📅 Filter by Date Range")

    # Make sure transaction_date is datetime
    transactions_df['transaction_date'] = pd.to_datetime(transactions_df['transaction_date'])

    # Date input (min/max from data)
    min_date = transactions_df['transaction_date'].min()
    max_date = transactions_df['transaction_date'].max()

    start_date, end_date = st.date_input(
        "Select a date range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # Filter by date
    date_filtered_df = transactions_df[
        (transactions_df['transaction_date'] >= pd.to_datetime(start_date)) &
        (transactions_df['transaction_date'] <= pd.to_datetime(end_date))
    ]

    st.write(f"📊 Total Transactions: {len(date_filtered_df)} from {start_date} to {end_date}")
    st.dataframe(date_filtered_df)



    # Download buttons
    st.download_button("📥 Download Users CSV", users_df.to_csv(index=False), "users.csv", "text/csv")
    st.download_button("📥 Download Transactions CSV", transactions_df.to_csv(index=False), "transactions.csv", "text/csv")
    
    st.subheader("📊 Sales by Category")
    fig1, ax1 = plt.subplots()
    category_sales = transactions_df.groupby('category')['amount'].sum().sort_values()
    sns.barplot(x=category_sales.values, y=category_sales.index, ax=ax1)
    st.pyplot(fig1)

    st.subheader("🥧 Gender Distribution")
    gender_counts = users_df['gender'].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)

    st.subheader("📈 Daily Sales Trend (Filtered)")

    if not date_filtered_df.empty:
        daily_sales = date_filtered_df.groupby('transaction_date')['amount'].sum()
        fig3, ax3 = plt.subplots()
        daily_sales.plot(ax=ax3, marker='o', color='green')
        ax3.set_ylabel("Amount (₹)")
        ax3.set_xlabel("Date")
        st.pyplot(fig3)
    else:
        st.warning("No transactions found in the selected date range.")

    
    st.subheader("📉 Transaction Amount Distribution")
    fig4, ax4 = plt.subplots()
    ax4.hist(transactions_df['amount'], bins=15, color='orange', edgecolor='black')
    ax4.set_xlabel("Amount (₹)")
    ax4.set_ylabel("Number of Transactions")
    st.pyplot(fig4)

