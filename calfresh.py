import datetime
import sys

def table_lookups(household_size):
    gross_income_limit = [2266, 3052, 3840, 4626, 5412, 6200, 6986, 7772]
    net_income_limit = [1133, 1526, 1920, 2313, 2706, 3100, 3493, 3886]
    std_deduct = [193, 193, 193, 193, 225, 258, 258, 258]
    max_benefit = [281, 516, 740, 939, 1116, 1339, 1480, 1691]
    irt = [1473, 1984, 2496, 3007, 3518, 4030, 4541, 5052]
    gross_income_increment = 758
    net_income_increment = 394
    std_deduct_increment = 0
    max_benefit_increment = 211
    irt_increment = 512
    lookup_max = 8
    
    try: household_size
    except NameError: household_size = 1
    if household_size < 1:
        print("Household size cannot be less than 1.")
        sys.exit(1)
    
    if household_size <= lookup_max:
        gross_income_max = gross_income_limit[household_size-1]
        net_income_max = net_income_limit[household_size-1]
        standard_deduction = std_deduct[household_size-1]
        maximum_benefit = max_benefit[household_size-1]
        hh_irt = irt[household_size-1]
        
    else:
        gross_income_max = gross_income_limit[lookup_max -1] + (gross_income_increment * (household_size - lookup_max))
        net_income_max = net_income_limit[lookup_max -1] + (net_income_increment * (household_size - lookup_max))
        standard_deduction = std_deduct[lookup_max -1] + (std_deduct_increment * (household_size - lookup_max))
        maximum_benefit = max_benefit[lookup_max - 1] + (max_benefit_increment * (household_size - lookup_max))
        hh_irt = irt[lookup_max -1] + (irt_increment * (household_size - lookup_max))
    return(gross_income_max, net_income_max, standard_deduction, hh_irt)


def gross_income_max(household_size):
    income_limit = [2266, 3052, 3840, 4626, 5412, 6200, 6986, 7772]
    income_increment = 758
    try: household_size
    except NameError: household_size = 1
    if household_size < 1:
        print("Household size cannot be less than 1.")
        sys.exit(1)
    lookup_max = len(income_limit)
    if household_size <= lookup_max:
        max = income_limit[household_size-1]
    else:
        max = income_limit[lookup_max -1] + (income_increment * (household_size - lookup_max))
    return(max)

def net_income_max(household_size):
    income_limit = [1133, 1526, 1920, 2313, 2706, 3100, 3493, 3886]
    income_increment = 394
    try: household_size
    except NameError: household_size = 1
    if household_size < 1:
        print("Household size cannot be less than 1.")
        sys.exit(1)
    lookup_max = len(income_limit)
    if household_size <= lookup_max:
        max = income_limit[household_size-1]
    else:
        max = income_limit[lookup_max -1] + (income_increment * (household_size - lookup_max))
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
    
