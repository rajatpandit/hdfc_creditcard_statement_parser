#!/usr/bin/env python3
from ast import IsNot
from datetime import date, datetime
from typing import NamedTuple, List
import csv
import tabula
import sys
import os
import locale
import argparse


locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
_DATE_FORMAT = "%d/%m/%Y %H:%M:%S"
_DATE_FORMAT_ALT = "%d/%m/%Y"
_CREDIT = 'credit'
_DEBIT = 'debit'
_HEADER_DATE = 'date'
_HEADER_TRANSACTION = 'transaction'
_HEADER_AMOUNT = 'amount'
_HEADER_TYPE = 'type'

class Transaction(NamedTuple):
    recv: date
    details: str
    amount: float
    type: str

def main(pdf_path):
    transactions = []
    if os.path.isfile(pdf_path):
        transactions = get_credit_infos(pdf_path)
        write_transactions(transactions)

def isNaN(num):
    return num != num

def get_credit_infos(fname: str):
    res = tabula.read_pdf(fname ,pages='all', stream=True)
    transactions = []
    for page in res:
        for line in page.values:
            out = parse_line(line)
            if out is not None:
                transactions.append(out)
    
    return transactions

def write_transactions(transactions):
    with open('output.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow((_HEADER_DATE, _HEADER_TRANSACTION,_HEADER_AMOUNT, _HEADER_TYPE))
        for transaction in transactions:
            writer.writerow(transaction)

    return None;

def _parse_date(ds: str):
    try:
        if len(ds) == 10:
            return datetime.strptime(ds, _DATE_FORMAT_ALT)
        else:
            return datetime.strptime(ds, _DATE_FORMAT)
    except:
        return None

def _sanitize_amount(amnts):
    if isNaN(amnts):
        return None

    clean_amount = amnts.split()
    try:
        if 'Cr' in amnts:
            transaction_type = _CREDIT
        else:
            transaction_type = _DEBIT
        return locale.atof(clean_amount[0]), transaction_type
    except ValueError:
        return None

def parse_line(line):
    transaction_date                     = _parse_date(line[0])
    transaction_amount, transaction_type = _sanitize_amount(line[-1]) or (None, None)
    transaction_details = line[1]
    if transaction_date is None:
        return
    if transaction_amount is None:
        return

    return Transaction(
        recv=transaction_date,
        amount=transaction_amount,
        details=transaction_details,
        type=transaction_type
    )
    
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', required=True, type=str,
                        help='path to pdf')
    return parser.parse_args()

if __name__ == '__main__':
    arguments = parse_arguments()
    main(arguments.s)