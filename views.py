import config

def input_credit_data():
    fields = dict()
    for name, value, func in config.CREDIT_FIELDS_SETTINGS:
        while True:
            try:
                value = func(input(f'{value}:'))
                fields[name] = value
            except:
                continue
            break
    return fields

def display_shedule(**fields):
    col_end = ''
    row_len = 0
    if fields:
        for name, _, col_width in config.PAYMENT_FIELDS_SETTINGS:
            value = fields[name]
            if type(value) in (int, float):
                value = round(value, 2)
            column = f'{value: ^{col_width}}'
            print(column, end = col_end)
            row_len += len(column) + len(col_end)
        print()
        print('-' * row_len)
    else:
        for _, verbose, col_width in config.PAYMENT_FIELDS_SETTINGS:
            column = f'{verbose: ^{col_width}}'
            print(column, end = col_end)
            row_len += len(column) + len(col_end)
        print()
        print('=' * row_len)


