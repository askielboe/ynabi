import json
import glob
import shutil
import datetime

import requests

from ynabi.config import download_path
from ynabi.model.transaction import Transaction
from ynabi.utils import string_to_datetime

from .credentials import spiir_username, spiir_password

spiir_datetime_format = "%Y-%m-%dT%H:%M:%SZ"
after_time = datetime.datetime.now() + datetime.timedelta(days=1)  # tomorrow
before_time = string_to_datetime("1000-01-01T00:00:00Z", spiir_datetime_format)


def _to_datetime(date_string):
    return string_to_datetime(date_string, spiir_datetime_format)


def _filename_today():
    now = datetime.datetime.now()
    filename = download_path + "/alle-poster-{}-{}-{}.json".format(
        str(now.year), str(now.month).zfill(2), str(now.day).zfill(2)
    )
    return filename


def _get_transactions(filename=None):
    """
    Downloads raw spiir transactions and optionally saves to filename.
    """
    print("spiir: get transactions")

    url_login = "https://mine.spiir.dk/log-ind"
    url_download = "https://mine.spiir.dk/Profile/ExportAllPostingsToJson"

    payload = {"Email": spiir_username, "Password": spiir_password}

    with requests.Session() as s:
        s.post(url_login, data=payload)
        resp = s.get(url_download)

    if filename is not None:
        print(f"spiir: save transactions to {filename}")
        with open(filename, "w", encoding="utf-8") as outfile:
            json.dump(resp.json(), outfile, ensure_ascii=False)

    return resp.json()


def _load_transactions(filename):
    """
    Loads raw spiir transactions form filename.
    """
    print(f"spiir: load transactions from {filename}")

    with open(filename, encoding="utf-8") as f:
        data = f.readline()

    return json.loads(data)


def _cached_transactions(use_cache=False):
    """
    Returns raw spiir transactions. Uses file cache if file was updated today.
    """
    if use_cache and len(glob.glob(_filename_today())) > 0:
        print(f"spiir: using cached transactions (overwrite using --no-cache)")
        return _load_transactions(_filename_today())
    return _get_transactions(filename=_filename_today())


def transactions(before=after_time, after=before_time, id_postfix="", use_cache=False):
    """
    Returns list of Transation objects from raw transactions.
    Before and after time formatted as "2018-01-01T00:00:00Z".
    """
    if isinstance(before, str):
        before = _to_datetime(before)

    if isinstance(after, str):
        after = _to_datetime(after)

    return [
        Transaction.from_spiir_dict(spiir_dict, id_postfix)
        for spiir_dict in _cached_transactions(use_cache=use_cache)
        if after < _to_datetime(spiir_dict["Date"]) <= before
    ]


def accounts():
    accounts = []
    for transaction in _cached_transactions():
        accounts.append(transaction["AccountName"])
    return list(set(accounts))


def categories():
    categories = []
    for transaction in _cached_transactions():
        categories.append(transaction["CategoryName"])
    return list(set(categories))
