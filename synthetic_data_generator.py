from faker import Faker
import pandas as pd
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

def main():
    num_users = 50
    num_transactions = 200

    users_df = generate_users(num_users)
    transactions_df = generate_transactions(users_df, num_transactions)

    users_df.to_csv('users.csv', index=False)
    transactions_df.to_csv('transactions.csv', index=False)

    print("✨ Enhanced synthetic data generated: 'users.csv' and 'transactions.csv'")

if __name__ == "__main__":
    main()
