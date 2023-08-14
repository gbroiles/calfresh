import datetime
import sys

def table_lookups(household_size):
    gross_income_limit = [2266, 3052, 3840, 4626, 5412, 6200, 6986, 7772]
    net_income_limit = [1133, 1526, 1920, 2313, 2706, 3100, 3493, 3886]
    gross_income_increment = 758
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


def standard_deduction(household_size):
    if household_size < 0:
        print("Error - household size below zero.")
        sys.exit(1)
    if household_size < 5:
        standard_deduction = 193
    elif household_size < 6:
        standard_deduction = 225
    else:
        standard_deduction = 258
    return(standard_deduction) 

def benefit(**args):
    application_date = args.get('application_date', datetime.date.today())
    household_size = args.get('household_size', 1)
    ineligible_count = args.get('ineligible_count', 0)
    earned_income = args.get('earned_imcome', 0)
    unearned_income = args.get('unearned_income', 0)
    child_support_paid = args.get('child_support_paid', 0)

    print("Application date: ", application_date)
    print("HH Size: ", household_size)
    print("Ineligible count: ", ineligible_count)
    print("Earned inocme: ", earned_income)
    print("Unearned income: ", unearned_income)
    print("Gross income limit: ", gross_income_max(household_size))
    print("Standard deduction: ", standard_deduction(household_size))
    print("Net income limit: ", net_income_max(household_size))

for i in range(1,21,3):
    print(benefit(household_size=i))
    print
    
