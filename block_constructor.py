import csv


def read_mempool(file_path):
    transactions = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
                
            if len(row) >= 3: 
                txid, fee, weight = row[:3]
                parents = row[3] if len(row) > 3 else ''
                transactions[txid] = {
                    'fee': int(fee),
                    'weight': int(weight),
                    'parents': set(parents.split(';')) if parents else set()
                }
            # else:
            #     print(f"Skipping row: {row}. Insufficient values.")
    return transactions

def calculate_total_fee(selected_transactions, transactions):
    total_fee = 0
    for txid in selected_transactions:
        total_fee += transactions[txid]['fee']
    return total_fee

def select_transactions(transactions, max_weight):
    selected_transactions = set()
    total_weight = 0
    
    sorted_transactions = sorted(transactions.keys(), key=lambda x: transactions[x]['fee'], reverse=True)
    
    for txid in sorted_transactions:
        if total_weight + transactions[txid]['weight'] <= max_weight:
            if all(parent in selected_transactions for parent in transactions[txid]['parents']):
                selected_transactions.add(txid)
                total_weight += transactions[txid]['weight']
    
    return selected_transactions

def main():
    mempool_file = 'mempool.csv'
    max_block_weight = 4000000
    
    transactions = read_mempool(mempool_file)
    selected_transactions = select_transactions(transactions, max_block_weight)
    total_fee = calculate_total_fee(selected_transactions, transactions)
    
    with open('block.txt', 'w') as blockfile:
        for txid in selected_transactions:
            blockfile.write(txid + '\n')
    
    print(f'Total fee collected: {total_fee}')

if __name__ == '__main__':
    main()
