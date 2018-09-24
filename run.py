from ynabi.api import spiir, ynab
from ynabi.model.transaction import Transaction

after = "2018-09-20T00:00:00Z"
id_postfix = "1"  # initial import
dryrun = False

print("============== ynabi v1.0 - start ==============")

print("ynabi: importing spiir transactions to ynab")
print(f"ynabi: including transaction after {after}")
print(f"ynabi: using transaction id postfix {id_postfix}")

# Spiir accounts and categories
# a = spiir.accounts()
# c = spiir.categories()

# 1. Load data from Spiir (list of Transaction)
transactions = spiir.transactions(after=after, id_postfix=id_postfix)

# 2. Save transactions to YNAB
ynab.create_transactions(transactions, dryrun=dryrun, pushover=True)

# 3. Convert "Løn" category to "To be budgeted"

# 4. Initial balance adjustments:
#      LSBPrivat Løn:  19976.85 + 3490.65 = 23467,50
#      DM Mastercard:  0
#      Fælleskonto:    0

print("============== ynabi v1.0 - end ==============")
