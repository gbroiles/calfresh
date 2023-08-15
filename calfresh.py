import datetime
import math
import sys


# rounding functions borrowed from https://realpython.com/python-rounding
def round_down(n, decimals=0):
    multiplier = 10**decimals
    return math.floor(n * multiplier) / multiplier


def round_half_up(n, decimals=0):
    multiplier = 10**decimals
    return math.floor(n * multiplier + 0.5) / multiplier


def table_lookups(household_size):
    global debug

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

    if household_size < 1:
        print("Household size cannot be less than 1.")
        sys.exit(1)

    if household_size <= lookup_max:
        gross_income_max = gross_income_limit[household_size - 1]
        net_income_max = net_income_limit[household_size - 1]
        standard_deduction = std_deduct[household_size - 1]
        maximum_benefit = max_benefit[household_size - 1]
        hh_irt = irt[household_size - 1]

    else:
        gross_income_max = gross_income_limit[lookup_max - 1] + (
            gross_income_increment * (household_size - lookup_max)
        )
        net_income_max = net_income_limit[lookup_max - 1] + (
            net_income_increment * (household_size - lookup_max)
        )
        standard_deduction = std_deduct[lookup_max - 1] + (
            std_deduct_increment * (household_size - lookup_max)
        )
        maximum_benefit = max_benefit[lookup_max - 1] + (
            max_benefit_increment * (household_size - lookup_max)
        )
        hh_irt = irt[lookup_max - 1] + (irt_increment * (household_size - lookup_max))

    if debug:
        print("Gross income max:", gross_income_max)
        print("Net income max:", net_income_max)
        print("Standard deduction:", standard_deduction)
        print("Maximum benefit:", max_benefit)
        print("IRT:", hh_irt)

    return (
        gross_income_max,
        net_income_max,
        standard_deduction,
        maximum_benefit,
        hh_irt,
    )


def calculate_medical(total_medical_spend):
    if total_medical_spend < 35:
        return 0
    elif total_medical_spend < 155:
        return 120
    else:
        return total_medical_spend


def benefit(**args):
    global debug

    SUA_DEFAULT = 560
    LUA_DEFAULT = 150
    TUA_DEFAULT = 18
    application_date = args.get("application_date", datetime.date.today())
    household_size = args.get("household_size", 1)
    ineligible_count = args.get("ineligible_count", 0)
    earned_income = args.get("earned_imcome", 0)
    ineligible_earned_income = args.get("ineligible_earned_income", 0)
    unearned_income = args.get("unearned_income", 0)
    ineligible_unearned_income = args.get("ineligible_unearned_income", 0)
    child_support_paid = args.get("child_support_paid", 0)
    dependent_care_cost = args.get("dependent_care_cost", 0)
    gross_medical_expense = args.get("gross_medical_expense", 0)
    disabled = args.get("disabled", False)
    homeless = args.get("homeless", False)
    eligible_housing = args.get("eligible_housing", 0)
    ineligible_housing = args.get("inelgible_housing", 0)
    sua_expense = args.get("sua_expense", 0)
    lua_expense = args.get("lua_expense", 0)
    tua_expense = args.get("tua_expense", 0)
    total_persons = household_size + ineligible_count
    (
        gross_income_max,
        net_income_max,
        standard_deduction,
        maximum_benefit,
        hh_irt,
    ) = table_lookups(household_size)
    prorate_gross_max_income = earned_income + (
        ineligible_earned_income * household_size / total_persons
    )
    earned_income_deduct = prorate_gross_max_income * 0.2
    net_earned_income = prorate_gross_max_income - earned_income_deduct
    net_income = unearned_income + net_earned_income - child_support_paid

    if debug:
        print("Earned income deduct:", earned_income_deduct)
        print("Net earned income", net_earned_income)
        print("Net income", net_income)

    if disabled:
        allowed_medical = calculate_medical(gross_medical_expense)
    else:
        allowed_medical = 0

    if homeless:
        homeless_shelter = 157.20
    else:
        homeless_shelter = 0

    adjusted_income = (
        net_income
        - standard_deduction
        - dependent_care_cost
        - allowed_medical
        - homeless_shelter
    )
    if debug:
        print("Adjusted income:", adjusted_income)

    prorated_housing = eligible_housing * (
        household_size / total_persons
    ) + ineligible_housing * (ineligible_count / total_persons)

    if debug:
        print("Prorated housing", prorated_housing)
        print("Eligible housing", eligible_housing)
        print("Household size:", household_size)
        print("Ineligible housing:", ineligible_housing)
        print("Ineligibile count:", ineligible_count)
        print("Total persons:", total_persons)

    if sua_expense > 0:
        util_expense = SUA_DEFAULT
    elif lua_expense > 0:
        util_expense = LUA_DEFAULT
    elif tua_expense > 0:
        util_expense = TUA_DEFAULT
    else:
        util_expense = 0

    adjusted_shelter = prorated_housing + util_expense
    excluded_shelter = adjusted_income / 2
    allowed_shelter = max(0, adjusted_shelter - excluded_shelter)
    if disabled:
        shelter_cost = allowed_shelter  # disabled HH has no shelter limit
    else:
        shelter_cost = min(560, allowed_shelter)  # nondisabled HH shelter max is 560

    if debug:
        print("Prorated housing:", prorated_housing)
        print("Utility expense", util_expense)
        print("Allowed shelter", allowed_shelter)

    final_income = max(
        adjusted_income - shelter_cost, 0
    )  # make sure it is not negative

    gross_income_pass = net_income < gross_income_max
    net_income_pass = final_income < net_income_max

    food_budget = final_income * 0.3
    if final_income == 0:
        benefit = maximum_benefit
    else:
        benefit = maximum_benefit - food_budget
    if (benefit == 1 or benefit == 3 or benefit == 5) and household_size >= 3:
        benefit += 1
    if household_size <= 2:
        benefit = max(benefit, 20)

    return (round_down(benefit), gross_income_pass, net_income_pass)


debug = True
print(
    benefit(
        household_size=2,
        unearned_income=1200,
        disabled=1,
        eligible_housing=500,
        sua_expense=1,
    )
)
# for i in range(1, 6):
#    print("-" * 40)
#    print("Household size: ", i)
#    print(benefit(household_size=i, unearned_income=1000))
#    print
