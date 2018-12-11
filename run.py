from ynabi.api import spiir, ynab
from ynabi.model.transaction import Transaction

from ynabi.config import start_date, id_postfix

dryrun = False

print("============== ynabi v1.0 - start ==============")

print("ynabi: importing spiir transactions to ynab")
print(f"ynabi: including transaction after {start_date}")
print(f"ynabi: using transaction id postfix {id_postfix}")

# Spiir accounts and categories
# a = spiir.accounts()
# c = spiir.categories()

# 1. Load data from Spiir (list of Transaction)
transactions = spiir.transactions(after=start_date, id_postfix=id_postfix)

# 2. Save transactions to YNAB
ynab.create_transactions(transactions, dryrun=dryrun)

print("============== ynabi v1.0 - end ==============")
