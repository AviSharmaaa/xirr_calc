import json
import datetime as dt
import pyxirr as fin

def calc_xirr(date_range, fund_transactions):
    """filters the transactions by date range provided and then calculates the XIRR"""
    transactions_object = filter_transactions_by_time_range(
        date_range,
        fund_transactions,
    )
    maturity_amount = calculate_maturity_amount(
        transactions_object["unitsHeld"],
        data["holdings"][0]["nav"],
    )
    transactions_object["transactions"].append({
        "date": data["holdings"][0]["navDate"],
        "description": "Sell",
        "amount": round(maturity_amount, 4),
        "price": data["holdings"][0]["nav"]
    })
    cal_xirr_for_time_range(transactions_object["transactions"])

def calculate_maturity_amount(unit_balance, nav_price):
    """calcualtes the expected Maturity amount"""
    return unit_balance * nav_price


def filter_transaction(unit_balance, transactions_to_filter):
    """filters the transactions, removes all the items that deal with the older holdings data"""
    filtered_transactions = []
    units_held = 0
    for transaction in transactions_to_filter:
        units = round(transaction["amount"] / transaction["price"], 4)
        if transaction["description"] != "Sell":
            units_held += units
            transaction["units"] = units
            filtered_transactions.append(transaction)
        else:
            unit_balance -= units

        if unit_balance < 0 and transaction["description"] == "Sell":
            units_held += unit_balance
            transaction["amount"] = abs(unit_balance) * transaction["price"]
            transaction["units"] = abs(unit_balance)
            filtered_transactions.append(transaction)
            unit_balance = 0
    return filtered_transactions


def cal_xirr_for_time_range(fund_transactions):
    """makes 2 list of amounts and dates resp, and feeds them to xirr calc function"""
    dates = []
    amounts = []
    for transaction in fund_transactions:
        date = convert_date(transaction["date"])
        description = transaction["description"]
        dates.append(date)
        if description != "Sell":
            amounts.append(transaction["amount"] * -1)
        else:
            amounts.append(transaction["amount"])
    print(xirr(dates, amounts))


def filter_transactions_by_time_range(date, fund_transactions):
    """filter transactions by given time range, also calculates units held at present"""
    temp_dict = {}
    transactions_list = []
    # if there are backdate transactions available, then we store the value of their units
    # in unitsHeld variable
    units_held_previously = 0

    units_held_now = 0
    for transaction in fund_transactions:
        transaction_date = convert_date(transaction["date"])
        if transaction_date > date:
            transactions_list.append(transaction)
        else:
            units_held_previously += transaction["units"]

    transactions_list = filter_transaction(units_held_previously,
                                           transactions_list)
    for transaction in transactions_list:
        if transaction["description"] == "Sell":
            units_held_now -= transaction["units"]
        else:
            units_held_now += transaction["units"]
    temp_dict["unitsHeld"] = units_held_now
    temp_dict["transactions"] = transactions_list
    return temp_dict


def xirr(date_list, amount_list):
    """calculates xirr value for the given dataset"""
    result = fin.xirr(dates=date_list, amounts=amount_list) * 100
    return result


def convert_date(date):
    """converts the date into specified format"""
    format = '%d-%b-%Y'
    datetime_str = dt.datetime.strptime(date, format)
    return datetime_str


jsonFile = open("cams_data.json", encoding="utf-8")

data = json.load(jsonFile)
openingUnitBalance = data["holdings"][0]["openingUnitBalance"]

# filtered transactions
transactions = filter_transaction(
    openingUnitBalance,
    data["holdings"][0]["transactions"],
)

oneYearBefore = dt.datetime.now() - dt.timedelta(days=365)
twoYearBefor = dt.datetime.now() - dt.timedelta(days=730)
threeYearBefore = dt.datetime.now() - dt.timedelta(days=1095)
fiveYearBefore = dt.datetime.now() - dt.timedelta(days=1825)
tenYearBefore = dt.datetime.now() - dt.timedelta(days=3650)

print("For 1 Year")
calc_xirr(oneYearBefore, transactions)
print("For 2 Year")
calc_xirr(twoYearBefor, transactions)
print("Since Inception")
calc_xirr(fiveYearBefore, transactions)
