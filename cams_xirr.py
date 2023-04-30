import json
import datetime as dt
from mftool import Mftool
import pyxirr as fin


def get_historical_nav(scheme_code):
    """Returns historical nav data for a particular fund"""
    mf = Mftool()
    scheme_data = mf.get_scheme_historical_nav(scheme_code, as_json=True)
    scheme_data = json.loads(scheme_data)
    return scheme_data["data"]


def get_nav_for_specific_date(date, nav_data):
    """Returns Nav value on a specific date"""
    nav_value = 0
    found = False
    for nav in nav_data:
        nav_date = convert_date(nav["date"])
        if nav_date == date:
            nav_value = nav["nav"]
            found = True
            break
    if not found:
        nav_value = nav_data[0]["nav"]
    return nav_value


def calculate_maturity_amount(unit_balance, nav_price):
    """calcualtes the expected Maturity amount"""
    return float(unit_balance) * float(nav_price)


def calculate_fund_latest_market_valuation(ut, nav_value):
    """Returns dummy trasnaction with corpus's latest value"""
    maturity_amount = calculate_maturity_amount(ut, nav_value)
    txn = {
        "date": dt.datetime.now(),
        "description": "Sell",
        "amount": maturity_amount,
        "price": nav_value
    }
    return txn


def sort_transactions_for_time_period(
    scheme_code,
    from_date,
    fund_transactions,
):
    """Returns sorted transactions for specified time period"""
    filtered_transactions = []
    units_held_previously = openingUnitBalance

    #sorts transactions according to time period and
    #calulcates previously held units for the preciding time
    for txn in fund_transactions:
        date = txn["date"]
        if date > from_date:
            filtered_transactions.append(txn)
        else:
            if txn["description"] != "Sell":
                units_held_previously += txn["units"]
            else:
                units_held_previously -= txn["units"]

    # calcaulates maturity amount for previously held units
    historical_nav = get_historical_nav(scheme_code)
    nav_value = get_nav_for_specific_date(from_date, historical_nav)
    previous_corpus_value = calculate_maturity_amount(
        units_held_previously,
        nav_value,
    )

    txn = {
        "date": from_date,
        "description": "Systematic Investment(1)",
        "amount": previous_corpus_value,
        "price": nav_value,
        "units": previous_corpus_value / float(nav_value)
    }
    filtered_transactions.append(txn)

    #get latest corpus value
    final_transaction = calculate_fund_latest_market_valuation(
        closing_units,
        historical_nav[0]["nav"],
    )
    filtered_transactions.append(final_transaction)

    # sort transactions
    filtered_transactions = sorted(
        filtered_transactions,
        key=lambda transaction: transaction["date"],
    )
    return filtered_transactions


def cal_xirr_for_time_range(fund_transactions):
    """calculates and print xirr for given trasnactions"""
    dates = []
    amounts = []
    for txn in fund_transactions:
        date = txn["date"]
        description = txn["description"]
        dates.append(date)
        if description != "Sell":
            amounts.append(txn["amount"] * -1)
        else:
            amounts.append(txn["amount"])
    print(xirr(dates, amounts))


def xirr(date_list, amount_list):
    """retruns xirr value for the given dataset"""
    result = fin.xirr(dates=date_list, amounts=amount_list) * 100
    return result


def convert_date(date):
    """converts the date into specified format"""
    try:
        format1 = '%d-%b-%Y'
        datetime_str = dt.datetime.strptime(date, format1)
    except:
        format2 = '%d-%m-%Y'
        datetime_str = dt.datetime.strptime(date, format2)
    return datetime_str


# main
jsonFile = open("cams_data.json", encoding="utf-8")

data = json.load(jsonFile)
openingUnitBalance = data["holdings"][0]["openingUnitBalance"]
transactions = data["holdings"][0]["transactions"]
closing_units = openingUnitBalance

for transaction in transactions:
    units = transaction["amount"] / transaction["price"]
    transaction["date"] = convert_date(transaction["date"])
    transaction["units"] = units
    closing_units += units

# filtered transactions

oneYearBefore = dt.datetime.now() - dt.timedelta(days=365)
twoYearBefor = dt.datetime.now() - dt.timedelta(days=730)
threeYearBefore = dt.datetime.now() - dt.timedelta(days=1095)
fiveYearBefore = dt.datetime.now() - dt.timedelta(days=1825)
tenYearBefore = dt.datetime.now() - dt.timedelta(days=3650)

print("For 1 year")
sorted_transactions = sort_transactions_for_time_period(
    "120166",
    oneYearBefore,
    transactions,
)
cal_xirr_for_time_range(sorted_transactions)
print("For 2 year")
sorted_transactions = sort_transactions_for_time_period(
    "120166",
    twoYearBefor,
    transactions,
)
cal_xirr_for_time_range(sorted_transactions)
print("Since inception")
sorted_transactions = sort_transactions_for_time_period(
    "120166",
    fiveYearBefore,
    transactions,
)
cal_xirr_for_time_range(sorted_transactions)
