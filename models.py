import config
import services
from mixins import BaseModel

class SheduleModel:
    def __init__(self):
        self.credit = self.Credit()

    def get_annuitet(self):
        return services.get_annuitet(
                *self.credit.get_fields().values())

    def get_difference(self):
        return services.get_difference(
                *self.credit.get_fields().values())
    #----------------
    class Credit(BaseModel):
        def __init__(self,
                     debt: float = config.DEFAULT_DEBT,
                     term: int = config.DEFAULT_TERM,
                     percent: float = config.DEFAULT_PERCENT):
            self.debt = debt
            self.term = term
            self.percent = percent


