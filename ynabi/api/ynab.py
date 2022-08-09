import time
import json
import requests

try:
    from ynabi.api.pushover import log
except ImportError:
    log = lambda *s: None  # If pushover is not installed, don't log anything

from .credentials import ynab_api_token, ynab_budget_id

api = "https://api.youneedabudget.com/v1/"
headers = {"Authorization": "Bearer {}".format(ynab_api_token)}

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


def create_transactions(transactions, chunk_size=100, dryrun=False):
    """
    Uploads transactions to YNAB. No return value.
    """
    url = api + f"/budgets/{ynab_budget_id}/transactions/bulk"

    if len(transactions) == 0:
        log("ynab", "no transactions to upload")
        return 0, 0

    chunks = [
        transactions[x : x + chunk_size]
        for x in range(0, len(transactions), chunk_size)
    ]

    print(f"ynab: creating {len(transactions)} transactions in {len(chunks)} chunks")

    n_duplicates = 0

    for i, chunk in enumerate(chunks):
        body = {"transactions": [t.to_dict() for t in chunk]}

        if dryrun:
            print(f"ynab dryrun: would post transaction chunk {i}/{len(chunks)}..")
            time.sleep(0.5)
        else:
            print(f"ynab: posting transaction chunk {i+1}/{len(chunks)}.. ", end="")
            resp = requests.post(url, json=body, headers=headers)

            if not 200 <= resp.status_code < 300:
                print("\n")
                log("ynab error", f"bulk create request failed ({resp.status_code})")
                print("request: ", resp.request.body)
                print("response: ", resp.json())

                return 0, 0

            n = len(resp.json()["data"]["bulk"]["duplicate_import_ids"])
            if n > 0:
                print(f"({n} duplicates ignored)")
                n_duplicates += n

    n_created = len(transactions) - n_duplicates

    log("ynab", f"created {n_created} transactions, {n_duplicates} duplicates ignored")
    print(f"ynab: created {n_created} transactions ({n_duplicates} duplicates ignored)")

    return n_created, n_duplicates


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
    raise(TypeError(f"ynab account id not found for account {name}"))

def get_category_id(name):
    for category_group in category_groups():
        for category in category_group["categories"]:
            if name == category["name"]:
                return category["id"]
