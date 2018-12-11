# ynabi: Spiir to YNAB import script (work in progress)

Since YNAB does not support Nordic banks, I created this Python script
to import Spiir transactions into YNAB. The script is not endorsed by Spiir
or YNAB and may stop working at any time.

## Getting started

### Basic configuration

Add your basic configuration by editing ynabi/api/config.py (see ynabi/api/config.example.py).

### Configure Spiir

Add your Spiir login credentials to ynabi/api/credentials.py
(see ynabi/api/credentials.example.py).

### Configure YNAB

Before running `ynabi` you need to get your API token and budget ID from YNAB,
as well as set up all Spiir categories in YNAB manually.

#### API token

Get your YNAB Personal Access Token by following the instructions:
https://api.youneedabudget.com/#personal-access-tokens.
Then add your API token to ynabi/api/credentials.py
(see ynabi/api/credentials.example.py).

#### Budget ID

Get your YNAB budget ID by going to http://app.youneedabudget.com, make sure
the correct budget is open and copy your budget ID from the url, e.g:
`https://app.youneedabudget.com/YOUR-BUDGET-ID-IS-HERE/budget`. Add your budget
ID to ynabi/api/credentials.py.

#### Categories

The way ynabi currently adds transactions to categories is by matching category
names by string from Spiir to YNAB. For this to work you have to manually add
all Spiir categories to YNAB, using the **exact same category names** as listed
in Spiir. You can organize the categories in YNAB the way you want, or even hide
the ones you don't need.

If a Spiir category is missing from YNAB the transaction will be uncategorized
in YNAB after import.

#### Account names

Lige categories, you need to add accounts to YNAB with the exact same names as in
Spiir.

### Install requirements

1. `pip install -r requirements.txt`

### Run ynabi

1. `python ynabi.py`

## Troubleshooting

### Duplicate transactions

If you accidentially imported transactions to YNAB that you don't want you can
safely delete them from YNAB. To avoid duplicates, all Spiir transactions has
a unique identifier which are stored in YNAB. Therefore transactions can only
be imported to the same budget once - *even if the transaction has been deleted
in YNAB!*

Therefore, in order to re-import previously imported (possibly deleted)
transactions you can change the transaction ID postfix
(`id_postfix`) in ynabi/config.py. This will allow you to re-import transactions
to YNAB. But beware that this may create duplicates in YNAB.

In general, once you are set up correctly, you should never have to change the
transaction ID postfix.

#### Optional: [Pushover](https://pushover.net/) support

1. `pip install -r optional.txt`
2. Add `pushover_user_key` and `pushover_api_token` to ynabi/api/credentials.py
