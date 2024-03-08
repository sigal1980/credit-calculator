#!/usr/bin/python
import unittest
from datetime import date
from itertools import product

import services

class TestServices(unittest.TestCase):
    def test_get_k_throw_exception(self):
        p_list = list(product([-1, 0, 1.1],
                              [-1, 0]))
        for term, month_percent in p_list:
            self.assertRaises(
                    ValueError, services.get_k, term, month_percent)

    def test_get_k_return_value(self):
        k = round(services.get_k(1, 0.01), 2)
        self.assertEqual(k, 1.01)

    def test_get_pay_percent_negative_value(self):
        values = [(-1, 1),
                  (1, -1)]
        for d, p in values:
            self.assertRaises(ValueError, services.get_pay_percent,
                              d, p)

    def test_get_next_date_not_date_value(self):
        ex_date = date(2000, 1, 1).isoformat()
        self.assertRaises(ValueError,services.get_next_date, ex_date)

    def test_get_next_date_return_correct_value(self):
        ex_date = date(2000, 1, 1)
        ret_date = date(2000, 2, 1)
        self.assertEqual(services.get_next_date(ex_date), ret_date)

    def test_get_annuitet_incorrect_args(self):

        data = [(-1, 1, 1),
                (1, -1, 1),
                (1, 1, -1),
                (1, 1.0, 1)
                ]
        for values in data:
            gen = services.get_annuitet(*values)
            self.assertRaises(ValueError, next, gen)
            del(gen)
    def test_get_annuitet_return_value(self):
        credit = (1000, 12, 12)
        pay1 = {'pay_min': 88.85,
               'pay_debt': 78.85,
               'pay_percent': 10.0,
               'debt': 921.15,
               }
        gen = services.get_annuitet(*credit)
        fields = ['pay_min',
                  'pay_debt',
                  'pay_percent',
                  'debt']
        pay_res = next(gen)
        for name, value in pay_res.items():
            if name in fields:
                pay_res[name] = round(value, 2)
                assert pay1[name] == pay_res[name]
        del(gen)

    def test_get_difference_return_value(self):
        credit = (1000, 12, 12)
        pay1 = {'pay_min': 93.33,
               'pay_debt': 83.33,
               'pay_percent': 10.0,
               'debt': 916.67,
               }
        gen = services.get_difference(*credit)
        fields = ['pay_min',
                  'pay_debt',
                  'pay_percent',
                  'debt']
        pay_res = next(gen)
        for name, value in pay_res.items():
            if name in fields:
                pay_res[name] = round(value, 2)
                assert pay1[name] == pay_res[name]
        del(gen)



