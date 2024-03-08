
DEFAULT_DEBT = 1000.0

DEFAULT_TERM = 12

DEFAULT_PERCENT = 12.0

PAYMENT_FIELDS_SETTINGS = [('date', 'Дата', 12),
                           ('pay_min', 'Мин.платеж', 12),
                           ('pay_debt', 'Осн.долг', 12),
                           ('pay_percent', 'Проценты', 12),
                           ('debt', 'Остаток', 12),
                          ]

CREDIT_FIELDS_SETTINGS = [('debt', 'Сумма кредита(руб)', float),
                          ('term', 'Срок кредита(мес)', int),
                          ('percent', 'Годовой процент(%)', float),
                         ]

