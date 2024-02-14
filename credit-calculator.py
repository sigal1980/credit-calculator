#/usr/bin/python
#python 3.11
'''


Author: sigal1980
Date: 2024-02-07
'''

from collections import namedtuple

#-----------------------------------------------------
'''Настройки'''
_Shedule_keys = namedtuple('Shedule_keys', [
                                        'NUMBER',
                                        'DATE',
                                        'PAY_MIN',
                                        'PAY_DEBT',
                                        'PAY_PERCENT',
                                        'EARLY_PAY',
                                        'DEBT'])

# теперь для измменения имени ключа в графике...
# ... меняем 0-ое значение в кортеже. 1-й и 2-й элементы
# кортежа это заголовок шапки при печати и ширина столбца
_SHEDULE_KEYS = _Shedule_keys(
            ('Number', '№', 4),
            ('Date', 'Дата', 12),
            ('Pay_min', 'Мин.платеж', 12),
            ('Pay_debt', 'Осн.долг', 10),
            ('Pay_percent', 'Проценты', 12),
            ('Early_pay', 'Дос.погашение', 14),
            ('Debt', 'Долг', 12))

#-----------------------------------------

class MixinOverpay:
    '''Миксин расчитывает переплату по кредиту'''
    _overpay: float = 0.0

    @property
    def overpay(self) -> float:
        return MixinOverpay._overpay

    def _get_pay_percent(self) -> float:
        '''Переопределяем метод для добавления расчета переплаты'''
        super()._get_pay_percent()
        MixinOverpay._overpay += self._pay_percent
        return self._pay_percent

#-----------------------------------------

class MixinSheduleToDisplay:
    #import tabulate
    '''Интерфейс для вывода информации по кредиту на экран
    в виде простой таблицы.'''

    def shedule_to_display(self) -> list:
        str_out = ''
        # собираем шапку таблицы
        for value in _SHEDULE_KEYS:
            str_out += f'{value[1]: <{value[2]}}'
        str_out += '\n'
        # выводим данные о платежах
        for pay in self._shedule:
            for value in _SHEDULE_KEYS:
                if type(pay[value[0]]) in (str, int):
                    flt = ''
                else:
                    flt = '.2f'
                str_out += f'{pay[value[0]]: <{value[2]}{flt}}'
            str_out += '\n'
        print(str_out)

#-----------------------------------------

class CreditCalcMeta:
    '''Класс-родитель для кредитного калькулятора.
    Описывает методы и свойства совпадающие для обоих
    типов платежей.'''

    def __init__(self,
                 debt: float = 0,
                 term: int = 0,
                 percent:float = 0) -> None:
        # Основной долг
        self._debt = debt
        # Срок кредита
        self._term = term
        # Процент, под который взят кредит
        self._percent = percent
        # Минимальный месячный платеж
        self._pay_min:float
        # Сумма погашения основного долга в платеже
        self._pay_debt: float
        # Сумма процентов в платеже
        self._pay_percent:float
        # График платежей
        self._shedule: list = []

    @property
    def debt(self) -> float:
        '''Свойство для чтения/записи размера кредита.'''
        debt = round(self._debt, 2)
        return debt
    @debt.setter
    def debt(self, value: float) -> None:
        self._debt = float(value)

    @property
    def term(self) -> int:
        '''Свойство для чтения/записи срока кредита.'''
        return self._term
    @term.setter
    def term(self, value: int) -> None:
        self._term = value

    @property
    def percent(self) -> float:
        '''Свойство для чтения/записи процента по кредиту.'''
        return self._percent
    @percent.setter
    def percent(self, value: float) -> None:
        self._percent = value

    @property
    def shedule(self) -> list:
        '''Свойство для ЧТЕНИЯ графика платежей.'''
        return self._shedule

    def _get_pay_debt(self) -> float:
        '''Высчитывает сумму погашения основного долга в
        месячном платеже. Так как этот параметр меняется
        в ануеттетном типе платежей, а в дифференцированном нет,
        необходимо переопределить данный метод в потомке'''
        ...

    def _get_pay_min(self) -> float:
        '''Высчитывает минимальный месячный платеж.
        Так как этот параметр меняется в дифференцированном типе
        платежей, а в ануеттетном нет, необходимо переопределить
        данный метод в потомке.'''
        ...

    def get_pay_shedule(self) -> list:
        '''Формирует график платежей, который представляет из себя
        список из словарей.
        Ключи словаря:
            Number      - номер платежа. Начинается с 1;
            Date        - дата платежа (str);
            Pay_min     - минимальный платеж;
            Pay_debt    - сумма погашения долга в платеже;
            Pay_percent - сумма процентов в платеже;
            Early_pay   - остаток долга для досрочного погашения;
            Debt        - остаток долга после платежа.'''
        from calendar import monthrange
        from datetime import date, timedelta
        pay_date = date.today()
        for i in range(1, self._term + 1):
            payment = {}
            days_in_month = monthrange(pay_date.year,
                                       pay_date.month)[1]
            pay_date += timedelta(days = days_in_month)
            payment[_SHEDULE_KEYS.NUMBER[0]] = i
            payment[_SHEDULE_KEYS.DATE[0]] = \
                    pay_date.isoformat()
            payment[_SHEDULE_KEYS.PAY_MIN[0]] = 0.0
            payment[_SHEDULE_KEYS.PAY_DEBT[0]] = 0.0
            payment[_SHEDULE_KEYS.PAY_PERCENT[0]] = 0.0
            payment[_SHEDULE_KEYS.EARLY_PAY[0]] = 0.0
            payment[_SHEDULE_KEYS.DEBT[0]] = 0.0
            self._shedule.append(payment)
        return self._shedule

    def _get_pay_percent(self) -> float:
        '''Высчитывает проценты в месячном платеже.'''
        self._pay_percent = self._debt * self._percent / 12 / 100
        return self._pay_percent

    def __repr__(self) -> str:
        repr_str = f'{self.__class__.__name__}:\n'
        repr_str += f'  Debt: {self._debt}\n'
        repr_str += f'  Term: {self._term}\n'
        repr_str += f'  Percent: {self._percent}\n'
        return repr_str

#----------------------------------------

class CreditCalcDiff(MixinOverpay,
                     MixinSheduleToDisplay,
                     CreditCalcMeta):
    '''Кредитный калькулятор. Расчитывает дифференцированный
    тип платежа. Т. е. ежемесячный платеж уменьшается по мере
    выплаты основного долга.'''
    def _get_pay_min(self) -> float:
        self._pay_min = self._pay_debt + self._pay_percent
        return self._pay_min

    def _get_pay_debt(self) -> float:
        self._pay_debt = self._debt / self._term
        return self._pay_debt

    def get_pay_shedule(self) -> list:
        super().get_pay_shedule()
        self._get_pay_debt()
        for payment in self._shedule:
            self._get_pay_percent()
            self._get_pay_min()
            payment[_SHEDULE_KEYS.PAY_DEBT[0]] = \
                    self._pay_debt
            payment[_SHEDULE_KEYS.PAY_MIN[0]] = \
                    self._pay_min
            payment[_SHEDULE_KEYS.PAY_PERCENT[0]] = \
                    self._pay_percent
            payment[_SHEDULE_KEYS.EARLY_PAY[0]] = self._debt
            self._debt -= self._pay_debt
            payment[_SHEDULE_KEYS.DEBT[0]] = self._debt
        return self._shedule

#---------------------------------------------------------

class CreditCalcAnnuitet(MixinOverpay,
                         MixinSheduleToDisplay,
                         CreditCalcMeta):
    '''Кредитный калькулятор. Расчитывает аннуитетный
    тип платежа. Т. е. ежемесячный платеж всегда одинаковый'''
    def _get_annuitet(self) -> float:
        monht_percent = self._percent / 100 / 12
        k = (monht_percent * (1 + monht_percent) ** self._term) / \
                ((1 + monht_percent) ** self._term - 1)
        return k

    def _get_pay_min(self) -> float:
        self._pay_min = self._debt * self._get_annuitet()
        return self._pay_min

    def _get_pay_debt(self) -> float:
        self._pay_debt = self._pay_min - self._pay_percent
        return self._pay_debt

    def get_pay_shedule(self) -> list:
        super().get_pay_shedule()
        self._get_pay_min()
        for payment in self._shedule:
            self._get_pay_percent()
            self._get_pay_debt()
            payment[_SHEDULE_KEYS.PAY_DEBT[0]] = \
                    self._pay_debt
            payment[_SHEDULE_KEYS.PAY_PERCENT[0]] = \
                    self._pay_percent
            payment[_SHEDULE_KEYS.PAY_MIN[0]] = \
                    self._pay_min
            payment[_SHEDULE_KEYS.EARLY_PAY[0]] = self._debt
            self._debt -= self._pay_debt
            payment[_SHEDULE_KEYS.DEBT[0]] = self._debt
        return self._shedule


if __name__ == '__main__':
    #cc = CreditCalcDiff()
    cc = CreditCalcAnnuitet()
    cc.debt = 300000
    cc.term = 60
    cc.percent = 22
    shedule = cc.get_pay_shedule()
    print('График платежей:\n')
    cc.shedule_to_display()
    print(f'Переплата по кредиту: {cc.overpay:.2f}')


