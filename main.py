import calfresh as cf

debug = True
print(
    cf.benefit(
        household_size=2,
        unearned_income=1200,
        disabled=1,
        eligible_housing=500,
        sua_expense=1,
        target_date="2023-10-01"
    )
)
# for i in range(1, 6):
#    print("-" * 40)
#    print("Household size: ", i)
#    print(benefit(household_size=i, unearned_income=1000))
#    print