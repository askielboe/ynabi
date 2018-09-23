import json
import tqdm
import requests

from .credentials import ynab_api_token, ynab_budget_id

api = "https://api.youneedabudget.com/v1/"
headers = {"Authorization": "Bearer {}".format(ynab_api_token)}
bulk_transaction_chunk_size = 10

#
# Requests
#
def get_accounts():
    url = api + f"budgets/{ynab_budget_id}/accounts"
    resp = requests.get(url, headers=headers)
    return resp.json()["data"]["accounts"]


def get_category_groups():
    url = api + f"budgets/{ynab_budget_id}/categories"
    resp = requests.get(url, headers=headers)
    return resp.json()["data"]["category_groups"]


def create_transactions(transactions):
    url = api + f"/budgets/{ynab_budget_id}/transactions/bulk"

    chunks = [
        transactions[x : x + bulk_transaction_chunk_size]
        for x in range(0, len(transactions), bulk_transaction_chunk_size)
    ]

    print(f"Creating {len(transactions)} transactions in {len(chunks)} chunks")
    for chunk in tqdm.tqdm(chunks, "Bulk create transactions"):
        body = {"transactions": [t.to_dict() for t in chunk]}
        resp = requests.post(url, json=body, headers=headers)
        print(resp.status_code)

    return resp


#
# Cache
#
_ynab_accounts = None
_ynab_category_groups = None


def clear_cache():
    global _ynab_accounts
    global _ynab_category_groups
    _ynab_accounts = None
    _ynab_category_groups = None


def accounts():
    global _ynab_accounts
    if _ynab_accounts is None:
        _ynab_accounts = get_accounts()
    return _ynab_accounts


def category_groups():
    global _ynab_category_groups
    if _ynab_category_groups is None:
        _ynab_category_groups = get_category_groups()
    return _ynab_category_groups


#
# Lookups
#
def get_account_id(name):
    for account in accounts():
        if name == account["name"]:
            return account["id"]


def get_category_id(name):
    for category_group in category_groups():
        for category in category_group["categories"]:
            if name == category["name"]:
                return category["id"]
