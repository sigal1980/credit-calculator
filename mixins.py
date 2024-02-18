#/usr/bin/python
#python 3.11
'''


Author: sigal1980
Date: 2024-02-10
'''

#-----------------------------------------

class MixinOverpay:
    '''Миксин расчитывает переплату по кредиту'''
    _overpay: float = 0.0

    @property
    def overpay(self) -> float:
        return MixinOverpay._overpay

    def _get_pay_percent(self) -> float:
        '''Переопределяем метод для добавления расчета переплаты'''
        pay_percent = super()._get_pay_percent()
        MixinOverpay._overpay += pay_percent
        return pay_percent

#-----------------------------------------

class MixinSheduleToDisplay:
    #import tabulate
    '''Интерфейс для вывода информации по кредиту на экран
    в виде простой таблицы.'''

    def table_from_shedule(self,
                           shedule: list,
                           headers: list,
                           columns: list) -> list:
        '''Входящие параметры:
            shedule: график платежей;
            headers: шапка таблицы;
            columns: ширина столбцов'''
        str_out = ''
        # собираем шапку таблицы
        for header, col_width in zip(headers, columns):
            str_out += f'{header: <{col_width}}'
        # Собираем таблицу
        for payment in shedule:
            str_out += '\n'
            for pay, col_width in zip(payment, columns):
                fmt = '' if type(payment[pay]) in (str, int) else '.2f'
                str_out += f'{payment[pay]: <{col_width}{fmt}}'

        return str_out

