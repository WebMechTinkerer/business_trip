"""Backend of website"""
from flask import Flask, render_template, request
from data import DATA
from reimbursement import calculate_reimbursement
from datetime import datetime, timedelta
import json  # Import json to handle JSON data

app = Flask(__name__)

# Extract and sort country names from DATA
countries = sorted([item[0] for item in DATA])

@app.route('/', methods=['GET', 'POST'])
def home():
    reimbursement = 0
    expenses = []  # Initialize the expenses list here

    if request.method == 'POST':
        # Retrieve form data
        country = request.form['country']
        departure_str = request.form['departure']
        return_date_str = request.form['return']

        # Convert strings to datetime objects
        departure = datetime.strptime(departure_str, '%Y-%m-%dT%H:%M')
        return_date = datetime.strptime(return_date_str, '%Y-%m-%dT%H:%M')

        # Retrieve meal data from form
        meal_data = {}
        current_date = departure
        while current_date <= return_date:
            date_str = current_date.strftime('%d/%m/%Y')
            meal_data[date_str] = {
                'breakfast': request.form.get(f'meal_{date_str}_breakfast') is not None,
                'lunch': request.form.get(f'meal_{date_str}_lunch') is not None,
                'dinner': request.form.get(f'meal_{date_str}_dinner') is not None,
            }
            current_date = current_date + timedelta(days=1)

        # Retrieve country data from DATA
        country_data = next((item for item in DATA if item[0] == country), None)

        # Retrieve and parse expense data
        expenses_json = request.form.get('expenses', '[]')
        if expenses_json:  # Check if there is any data in the 'expenses' field
            try:
                expenses = json.loads(expenses_json)  # Convert the JSON string back to a list of expenses
            except json.JSONDecodeError:
                expenses = []  # If JSON decoding fails, set expenses to an empty list

        # Call the reimbursement calculation function
        reimbursement = calculate_reimbursement(country_data, departure, return_date, meal_data, expenses)

    return render_template('index.html', countries=countries, reimbursement=reimbursement, expenses=expenses)

if __name__ == '__main__':
    app.run(debug=True)
