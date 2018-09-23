import json
import glob
import datetime

from selenium import webdriver

from ynabi.model.transaction import Transaction

from .credentials import spiir_username, spiir_password


def _filename_today():
    now = datetime.datetime.now()
    filename = "/Users/askielboe/Downloads/alle-poster-{}-{}-{}.json".format(
        str(now.year), str(now.month).zfill(2), str(now.day).zfill(2)
    )
    return filename


def _json_from_file(filename):
    with open(filename) as f:
        data = f.readline()

    return json.loads(data)


def _download_transactions():
    # from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

    # Download transactions
    driver = webdriver.Chrome()  # Using local chromedriver for testing

    # driver = webdriver.Remote(
    #     command_executor="http://selenium:4444/wd/hub",
    #     desired_capabilities=DesiredCapabilities.CHROME,
    # )

    # driver.implicitly_wait(10)  # seconds

    driver.get("https://mine.spiir.dk/log-ind")

    elem_username = driver.find_element_by_name("Email")
    elem_username.send_keys(spiir_username)

    elem_password = driver.find_element_by_name("Password")
    elem_password.send_keys(spiir_password)

    elem_button = driver.find_element_by_class_name("btn")
    elem_button.click()

    driver.get("https://mine.spiir.dk/Profile/ExportAllPostingsToJson")

    driver.close()


def get_raw_transactions():
    """
    If transactions have already been downloaded for today, return those.
    Otherwise download transactions from Spiir using selenium.
    """
    # TODO: Implement Spiir time filter
    if len(glob.glob(_filename_today())) == 0:
        _download_transactions()
    return _json_from_file(_filename_today())


def get_transactions(id_postfix=""):
    """
    Returns list of Transation objects from raw transactions.
    """
    return [
        Transaction.from_spiir_dict(spiir_dict, id_postfix)
        for spiir_dict in get_raw_transactions()
    ]


def list_all_accounts():
    accounts = []
    for transaction in get_transactions():
        accounts.append(transaction["AccountName"])
    return list(set(accounts))


def list_all_categories():
    categories = []
    for transaction in get_transactions():
        categories.append(transaction["CategoryName"])
    return list(set(categories))
