from ynabi.api import spiir, ynab
from ynabi.model.transaction import Transaction

id_postfix = ""

# List Spiir accounts and categories
# a = spiir.list_all_accounts()
# c = spiir.list_all_categories()

# Load data from Spiir
transactions = spiir.get_transactions(
    after="2018-01-01T00:00:00Z", id_postfix=id_postfix
)  # [Transaction]

# Save transactions to YNAB
ynab.create_transactions(transactions)

