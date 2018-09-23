from ynabi.api import spiir, ynab
from ynabi.model.transaction import Transaction

id_postfix = "TEST1"

# Load data from Spiir
transactions = spiir.get_transactions(id_postfix)  # [Transaction]

# List Spiir accounts and categories
# a = spiir.list_all_accounts()
# c = spiir.list_all_categories()

# Create transactions
for transaction in transactions[0:5]:
    print(transaction.to_json())

# Save transactions to YNAB
resp = ynab.create_transactions(transactions[0:5])

print(resp.request.body)
print(resp.json())
