from ynabi.api import spiir, ynab
from ynabi.model.transaction import Transaction

id_postfix = "1"  # initial import

# Spiir accounts and categories
# a = spiir.accounts()
# c = spiir.categories()

# 1. Load data from Spiir (list of Transaction)
transactions = spiir.transactions(after="2018-01-01T00:00:00Z", id_postfix=id_postfix)

# 2. Save transactions to YNAB
ynab.create_transactions(transactions)

# 3. Convert "Løn" category to "To be budgeted"

# 4. Initial balance adjustments:
#      LSBPrivat Løn:  19976.85 + 3490.65 = 23467,50
#      DM Mastercard:  0
#      Fælleskonto:    0
