from datetime import date, timedelta
import calendar

import config

def get_k(term, month_percent):
    '''функция для расчета коэффициента аннуитета'''
    if term <= 0 and type(term != int):
        raise ValueError(
                'Кол-во месяцев должно быть целым числом больше 0!')
    elif month_percent <= 0:
        raise ValueError('Месячный процент должен быть больше 0!')
    k = (month_percent * (1 + month_percent) ** term) / \
        ((1 + month_percent) ** term - 1)
    return k

def get_pay_percent(debt, month_percent):
    '''Фукнкция для расчета месячного процента в платеже.'''
    if debt < 0 or month_percent < 0:
        raise ValueError
    pay_percent = debt * month_percent
    return pay_percent

def get_month_percent(percent):
    return percent / 100 / 12

def get_next_date(current_date):
    '''Функция добавляет к полученной дате календарный месяц.
    То есть:
    1 января -> 1 февраля -> 1 марта.'''
    if not type(current_date) is date:
        raise ValueError
    count_days = calendar.monthrange(current_date.year,
                                     current_date.month)[1]
    next_date = current_date + timedelta(days = count_days)
    return next_date

def validate_args(*kwargs):
    debt, term, percent = kwargs
    if debt < 0:
        raise ValueError
    if term <= 0 or not isinstance(term, int):
        raise ValueError
    if percent < 0:
        raise ValueError


def get_annuitet(debt, term, percent):
    '''Расчет и заполнение графика аннуитетных платежей.'''
    validate_args(debt, term, percent)
    month_percent = get_month_percent(percent)
    k = get_k(term, month_percent)
    pay_min = debt * k
    current_date = date.today()
    for i in range(term):
        payment = dict(
                [(name, '') for name, _, _ in
                 config.PAYMENT_FIELDS_SETTINGS])
        payment['pay_min'] = pay_min
        payment['pay_percent'] = get_pay_percent(debt, month_percent)
        payment['pay_debt'] = pay_min - payment['pay_percent']
        debt -= payment['pay_debt']
        payment['debt'] = debt
        current_date = get_next_date(current_date)
        payment['date'] = current_date.isoformat()
        yield payment

def get_difference(debt, term, percent):
    '''Расчет и заполнение графика дифференцированных платежей.'''
    validate_args(debt, term, percent)
    month_percent = get_month_percent(percent)
    pay_debt = debt / term
    current_date = date.today()
    for i in range(term):
        payment = dict(
                [(name, '') for name, _, _ in
                 config.PAYMENT_FIELDS_SETTINGS])
        payment = dict()
        payment['pay_debt'] = pay_debt
        payment['pay_percent'] = get_pay_percent(debt, month_percent)
        payment['pay_min'] = pay_debt + payment['pay_percent']
        debt -= pay_debt
        payment['debt'] = debt
        current_date = get_next_date(current_date)
        payment['date'] = current_date.isoformat()
        yield payment


#def shedule(func):
#    '''Декоратор для расчета аннуитет. и дифф. платежей.
#    Но что-то мне подсказывает, что лучше оставить две 
#    функции с полным расчетом: они понятнее, декоратор 
#    получился сильно запутанным.'''
#    def wrapper(debt, term, percent):
#        percent = get_month_percent(percent)
#        pay_date = date.today()
#        if func.__name__ == 'get_annuitet':
#            k = get_k(term, percent)
#            pay_min = debt * k
#            # необходима для вызова основной функции
#            pay_debt = ''
#        else:
#            pay_debt = debt / term
#            # необходима для вызова основной функции
#            pay_min = ''
#        for i in range(term):
#            # определяем набор полей в платеже. нужны во views.py
#            # если здесь будет меньше полей, чем требует views, то...
#            # views выкинет ошибку.
#            payment = dict([(name, '') for name, _, _ in
#                            config.PAYMENT_FIELDS_SETTINGS])
#            payment['pay_percent'] = get_pay_percent(debt, percent)
#            payment.update(func(debt,
#                                term,
#                                percent,
#                                # формируем payment для основной
#                                # фукнции.
#                                pay_min = pay_min,
#                                pay_debt = pay_debt,
#                                pay_percent = payment['pay_percent']
#                                )
#                           )
#            debt -= payment['pay_debt']
#            payment['debt'] = debt
#            pay_date = get_next_date(pay_date)
#            payment['date'] = pay_date.isoformat()
#            # используется генератор. Для возврата полного списка
#            # платежей добавить переменную-сборщик и проверить 
#            # controller на отсутствие next()
#            yield payment
#    return wrapper
#
#@shedule
#def get_annuitet(debt, term, percent, **payment):
#    '''Расчет графика аннуитетных платежей.
#    Аргумент payment передается ТОЛЬКО из декоратора.'''
#    payment['pay_debt'] = payment['pay_min'] - payment['pay_percent']
#    return payment
#
#@shedule
#def get_difference(debt, term, percent, **payment):
#    '''Расчет графика дифф. платежей.
#    Аргумент payment передается ТОЛЬКО из декоратора.'''
#    payment['pay_min'] = payment['pay_debt'] + payment['pay_percent']
#    return payment
