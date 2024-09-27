"""Calculates the total reimbursement and returns it."""


def calculate_reimbursement(country_data, departure, return_date, meal_data, expenses):
    """Calculates the total reimbursement using the chosen country, the given
    date of departure and return, the provided meals and expenses."""


    def sum_expenses(expenses_list):
        """Calculates the sum of expenses. 'expenses' is a list with the following structure:
        [{'description': STRING, 'cost': FLOAT}, {'description': STRING, 'cost': FLOAT}]"""
        ans = 0

        for item in expenses_list:
            ans += item['cost']

        return ans


    def sum_allowance(allowance_list):
        """Calculates the sum of allowance. 'allowance' is a list with the following structure:
        {'08/07/2024': {'duration': FLOAT, 'euros': FLOAT}}"""
        ans = 0

        for date, val in allowance_list.items():
            ans += val['euros']

        return ans


    def reduction_allowance(date):
        """Calculates the reduction of allowance in % due to
        breakfast, lunch or dinner being provided for free."""
        reduction = 0

        if meal_data[date]['breakfast']:
            reduction += 20
        if meal_data[date]['lunch']:
            reduction += 40
        if meal_data[date]['dinner']:
            reduction += 40

        return reduction


    reimbursement = 0

    ### Create a dictionary for every day with duration and money to be filled.
    allowance = {}
    for date in meal_data:
        allowance[date] = {
            'duration': None,
            'euros': None,
        }

    for date, val in allowance.items():

        ### Enter the duration the user was on the business trip for the day in the dict.
        if date == departure.date().strftime("%d/%m/%Y"):
            val['duration'] = 24 - departure.time().hour + departure.time().minute / 60
        elif date == return_date.date().strftime("%d/%m/%Y"):
            val['duration'] = departure.time().hour
        else:
            val['duration'] = 24

        ### Calculate the reduction of allowance due to
        ### having breakfast, lunch or dinner provided for free.
        reduction = reduction_allowance(date)

        ### Enter the daily allowance for each day in the dict.
        if val['duration'] == 24:
            val['euros'] = country_data[1] * (1 - reduction / 100)
        if 11 < val['duration'] < 24:
            val['euros'] = country_data[2] * (1 - reduction / 100)
        if 8 < val['duration'] <= 11:
            val['euros'] = country_data[3] * (1 - reduction / 100)
        if val['duration'] <= 8:
            val['euros'] = 0

    ### Calculate total reimbursement.
    reimbursement += sum_expenses(expenses)
    reimbursement += sum_allowance(allowance)
    
    return reimbursement