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
    eligible_housing = get("elgible_housing", 0)
    ineligible_housing = get("inelgible_housing", 0)
    sua_expense = get("sua_expense", 0)
    lua_expense = get("lua_expense", 0)
    tua_expense = get("tua_expense", 0)
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

    prorated_housing = eligible_housing * (
        household_size / total_persons
    ) + ineligible_housing * (ineligible_count / total_persons)

    if sua_expense > 0:
        util_expense = SUA_DEFAULT
    elif lua_expense > 0:
        util_expense = LUA_DEFAULT
    elif tua_expense > 0:
        util_expense = TUA_DEFAULT
    else:
        util_expense = 0

    return maximum_benefit


for i in range(1, 6):
    print("-" * 40)
    print("Household size: ", i)
    print(benefit(household_size=i))
    print
