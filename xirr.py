from datetime import date
import pyxirr as fin


def xirr(dates, amounts):
    """calculates xirr value for the given dataset"""
    xirr = fin.xirr(dates=dates, amounts=amounts) * 100
    return xirr


def calc_xirr():
    """provides xirr function required parameters and prints the returned value"""
    # sample data 1
    dates = [
        date(2000, 1, 1),
        date(2001, 1, 1),
        date(2002, 1, 1),
        date(2003, 1, 1),
        date(2004, 1, 1),
        date(2005, 1, 1),
        date(2006, 1, 1),
        date(2007, 1, 1),
        date(2008, 1, 1),
        date(2009, 1, 1),
        date(2010, 1, 1),
        date(2011, 1, 1),
        date(2012, 1, 1),
        date(2013, 1, 1),
        date(2014, 1, 1),
        date(2015, 1, 1),
        date(2016, 1, 1),
        date(2017, 1, 1),
        date(2018, 1, 1),
        date(2019, 1, 1),
        date(2020, 1, 1),
    ]
    amounts = [
        -10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000,
        -10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000,
        -10000, -10000, 800000
    ]
    print(f'\n\nSample data 1: {xirr(dates=dates, amounts=amounts)}\n')

    #sample data 2
    dates = [
        date(2000, 1, 1),
        date(2000, 2, 1),
        date(2000, 3, 1),
        date(2000, 4, 1),
        date(2000, 5, 1),
        date(2000, 6, 1),
        date(2000, 7, 1),
        date(2000, 8, 1),
        date(2000, 9, 1),
        date(2000, 10, 1),
        date(2000, 11, 1),
        date(2000, 12, 1),
        date(2001, 1, 1),
        date(2001, 2, 1),
        date(2001, 3, 1),
        date(2001, 4, 1),
        date(2001, 5, 1),
        date(2001, 6, 1),
        date(2001, 7, 1),
        date(2001, 8, 1),
        date(2001, 9, 1),
    ]
    amounts = [
        -10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000,
        -10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000, -10000,
        -10000, -10000, 250000
    ]
    print(f'Sample data 2: {xirr(dates=dates, amounts=amounts)}\n')

    #sample data 2
    dates = [
        date(2000, 1, 1),
        date(2001, 1, 1),
        date(2002, 1, 1),
        date(2003, 1, 1),
        date(2004, 1, 1),
        date(2005, 1, 1),
        date(2006, 1, 1),
        date(2007, 1, 1),
        date(2008, 1, 1),
        date(2009, 1, 1),
        date(2010, 1, 1),
        date(2011, 1, 1),
        date(2012, 1, 1),
        date(2013, 1, 1),
    ]
    amounts = [
        -10000, -10000, -10000, 10000, -10000, -10000, -10000, -10000, 5000,
        30000, -10000, -10000, -10000, 200000
    ]
    print(f'Sample data 3: {xirr(dates=dates, amounts=amounts)}\n')
    #sample data 4
    dates = [
        date(2000, 1, 1),
        date(2000, 11, 1),
        date(2000, 12, 2),
        date(2001, 5, 1),
        date(2001, 9, 1),
        date(2002, 3, 5),
        date(2002, 10, 10),
        date(2003, 2, 2),
        date(2003, 12, 4),
        date(2005, 1, 1),
        date(2005, 6, 1)
    ]
    amounts = [
        -5000, -8000, -12000, 4000, 2000, -10000, -6000, -11000, -3000, 10000,
        80000
    ]
    print(f'Sample data 4: {xirr(dates=dates, amounts=amounts)}\n')


calc_xirr()
