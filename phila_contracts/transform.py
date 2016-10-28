import csv
from collections import defaultdict

def get_contract_key(data):
    """
    Create a key that identifies a contract.

    If there is a bid number, uses that with the last 5 characters of the
    contract number (the first character may differ for ammendments to the same
    contract -- e.g., 123456 may become A23456, B23456, etc.).

    If there is no bid number, or the bid number is a non-identifying special
    case, just use the whole contract number.

    Arguments:
    * data -- A row of contract data as a dict

    """

    special_bids = ('E-ORDER', 'UTILITY')
    bid = data['Bid_Number'].strip() if data['Bid_Number'] else None
    contract = data['Contract_Number'].strip() if data['Contract_Number'] else None

    if bid and bid not in special_bids:
        return (bid, contract[2:]) if contract else (bid, None)
    else:
        return (None, contract)

def summarize_contracts_data(source_rows, contract_type):
    """
    Aggregate the raw contract data into groups with the total transaction
    amount.
    """

    # 1. Group rows by the contract key

    grouped_rows = defaultdict(list)
    for row in source_rows:
        contract_key = get_contract_key(row)
        grouped_rows[contract_key].append(row)

    # 2. Aggregate rows and annotate with the sum of transaction amounts

    if contract_type == 'pw':
        trans_amount_field = 'Total_Transactions'
    elif contract_type == 'sse':
        trans_amount_field = 'SumOfTransactionAmt'

    for group in grouped_rows.values():
        # i. copy an arbitrary row in the group
        summed_row = group[0].copy()

        # ii. get rid of the original amount column on the copied row
        del summed_row[trans_amount_field]

        # iii. standarze the name of the Max_Value column to Contract_Amount
        if 'Max_Value' in summed_row:
            summed_row['Contract_Amount'] = summed_row.pop('Max_Value')

        # iii. sum over the transaction amounts in the group's rows
        summed_row['Total_Transactions'] = sum(float(row[trans_amount_field] or 0)
                                               for row in group)

        yield summed_row

def write_contracts_data(infile, outfile, contract_type):
    """
    Read contracts data from a stream, transform it, and write it out to a
    stream.
    """

    fields = (
      'Bid_Number',
      'Contract_Number',
      'Contract_Description',
      'Start_Date',
      'End_Date',
      'Contract_Type',
      'Vendor_Name',
      'Department_Name',
      'Contract_Amount',
      'Total_Contract_Months',
      'Remaining_Contract_Months',
      'Total_Transactions',
    )

    reader = csv.DictReader(infile)

    writer = csv.DictWriter(outfile, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()

    for row in summarize_contracts_data(reader, contract_type):
        writer.writerow(row)
