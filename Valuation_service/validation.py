import csv
from decimal import Decimal


def main():
    with open('data.csv', newline='') as csvfile:
        data = list(csv.DictReader(csvfile))
    with open('currencies.csv', newline='') as csvfile:
        currencies = list(csv.DictReader(csvfile))
    with open('matchings.csv', newline='') as csvfile:
        matchings = list(csv.DictReader(csvfile))

    result = valuate(data, currencies, matchings)

    with open('top_products.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            'matching_id',
            'total_price',
            'avg_price',
            'currency',
            'ignored_products_count',
        ])
        writer.writeheader()
        for record in result:
            writer.writerow(record)


def valuate(data, currencies, matchings):
    currencies_map = {row['currency']: Decimal(row['ratio']) for row in currencies}

    data_grouped = {}
    for row in data:
        matching_id = row.pop('matching_id')
        price_PLN = Decimal(row['price']) * currencies_map[row['currency']]
        row['total_price_PLN'] = price_PLN * Decimal(row['quantity'])
        if matching_id not in data_grouped:
            data_grouped[matching_id] = []
        data_grouped[matching_id].append(row)

    for group in data_grouped.values():
        group.sort(key=lambda row: row['total_price_PLN'], reverse=True)

    result = []
    for matching in matchings:
        matching_id = matching['matching_id']
        group = data_grouped[matching['matching_id']]
        top_priced_count = int(matching['top_priced_count'])
        group_length = len(group)
        # in case of top_priced_count > length of group
        top_length = min(group_length, top_priced_count)
        top_products = group[:top_length]
        total_price = sum(row['total_price_PLN'] for row in top_products)
        result.append({
            'matching_id': matching_id,
            'total_price': total_price,
            'avg_price': total_price / top_length,
            'currency': 'PLN',
            'ignored_products_count': group_length - top_length,
        })

    return result


TEST_CASES = [
    {
        'currencies': [
            {'currency': 'EU', 'ratio': '10'},
            {'currency': 'PLN', 'ratio': '1'},
        ],
        'matchings': [
            {'matching_id': '1', 'top_priced_count': '1'},
            {'matching_id': '2', 'top_priced_count': '2'},
        ],
        'data': [
            {'id': '1', 'price': '10', 'currency': 'PLN', 'quantity': '1', 'matching_id': '1'},
            {'id': '2', 'price': '20', 'currency': 'EU', 'quantity': '10', 'matching_id': '1'},
            {'id': '3', 'price': '30', 'currency': 'PLN', 'quantity': '1', 'matching_id': '2'},
            {'id': '4', 'price': '40', 'currency': 'PLN', 'quantity': '10', 'matching_id': '2'},
        ],
        'expected_output': [
            {'matching_id': '1', 'total_price': Decimal('2000'), 'avg_price': Decimal('2000'), 'currency': 'PLN',
             'ignored_products_count': 1},
            {'matching_id': '2', 'total_price': Decimal('430'), 'avg_price': Decimal('215'), 'currency': 'PLN',
             'ignored_products_count': 0},
        ],
    },
    {
        'currencies': [
            {'currency': 'GBP', 'ratio': '2.4'},
            {'currency': 'EU', 'ratio': '2.1'},
            {'currency': 'PLN', 'ratio': '1'},
        ],
        'matchings': [
            {'matching_id': '1', 'top_priced_count': '2'},
            {'matching_id': '2', 'top_priced_count': '2'},
            {'matching_id': '3', 'top_priced_count': '3'},
        ],
        'data': [
            {'id': '1', 'price': '1000', 'currency': 'GBP', 'quantity': '2', 'matching_id': '3'},
            {'id': '2', 'price': '1050', 'currency': 'EU', 'quantity': '1', 'matching_id': '1'},
            {'id': '3', 'price': '2000', 'currency': 'PLN', 'quantity': '1', 'matching_id': '1'},
            {'id': '4', 'price': '1750', 'currency': 'EU', 'quantity': '2', 'matching_id': '2'},
            {'id': '5', 'price': '1400', 'currency': 'EU', 'quantity': '4', 'matching_id': '3'},
            {'id': '6', 'price': '7000', 'currency': 'PLN', 'quantity': '3', 'matching_id': '2'},
            {'id': '7', 'price': '630', 'currency': 'GBP', 'quantity': '5', 'matching_id': '3'},
            {'id': '8', 'price': '4000', 'currency': 'EU', 'quantity': '1', 'matching_id': '3'},
            {'id': '9', 'price': '1400', 'currency': 'GBP', 'quantity': '3', 'matching_id': '1'}
        ],
        'expected_output': [
            {'matching_id': '1', 'total_price': Decimal('12285.0'), 'avg_price': Decimal('6142.5'), 'currency': 'PLN',
             'ignored_products_count': 1},
            {'matching_id': '2', 'total_price': Decimal('28350.0'), 'avg_price': Decimal('14175.0'), 'currency': 'PLN',
             'ignored_products_count': 0},
            {'matching_id': '3', 'total_price': Decimal('27720.0'), 'avg_price': Decimal('9240.0'), 'currency': 'PLN',
             'ignored_products_count': 1}
        ]
    }
]


def test():
    for test_case in TEST_CASES:
        result = valuate(
            data=test_case['data'],
            currencies=test_case['currencies'],
            matchings=test_case['matchings'],
        )
        assert result == test_case['expected_output'], 'expected:\n' + str(
            test_case['expected_output']) + '\ngot:\n' + str(result)


# to run tests
test()

# to read/write files
main()
