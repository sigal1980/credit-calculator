import models
import views

def main():
    model = models.SheduleModel()
#    fields = views.input_credit_data()
#    model.credit.set_fields(**fields)
    shedule_gen = model.get_annuitet()
#    shedule_gen = model.get_difference()
    views.display_shedule()
    for payment in shedule_gen:
        views.display_shedule(**payment)


if __name__ == '__main__':
    main()
