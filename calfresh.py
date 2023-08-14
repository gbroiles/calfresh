import datetime
import sys

def gross_income_max(household_size):
    income_limit = [2266, 3052, 3840, 4626, 5412, 6200, 6986, 7772]
    income_increment = 758
    try: household_size
    except NameError: household_size = 1
    if household_size < 1:
        print("Household size cannot be less than 1.")
        sys.exit(1)
    maxsize = len(income_limit)
    if household_size <= maxsize:
        max = income_limit[household_size-1]
    else:
        max = income_limit[maxsize -1] + (income_increment * (household_size - maxsize))
    return(max)

def benefit(**args):
    application_date = args.get('application_date', datetime.date.today())
    household_size = args.get('household_size', 1)
    ineligible_count = args.get('ineligible_count', 0)
    earned_income = args.gen('earned_imcome', 0)
    unearned_income = args.get('unearned_income', 0)
    child_support_paid = args.get('child_support_paid', 0)


    print("Application date: ", application_date)
    print("HH Sizei: ", household_size)
    print("Ineligible count: ", ineligible_count)
    print("Earned inocme: ", earned_income)
    print("Unearned income: ", unearned_income)

for i in range(20):
    print(gross_income_max(i+1))
