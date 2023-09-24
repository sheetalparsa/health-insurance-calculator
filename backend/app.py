from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# rate_card_data = pd.read_csv('sample--rates.csv', dtype={
#     'member_csv': 'string',
#     'age_range': 'string',
#     'tier': 'string',
#     '500000': 'int64',
#     '700000': 'int64',
#     '1000000': 'int64',
#     '1500000': 'int64',
#     '2000000': 'int64',
#     '2500000': 'int64',
#     '3000000': 'int64',
#     '4000000': 'int64',
#     '5000000': 'int64',
#     '6000000': 'int64',
#     '7500000': 'int64',
# })
# rate_card_data['min_age'] = rate_card_data['age_range'].str[:2].astype('int64')
# rate_card_data['max_age'] = rate_card_data['age_range'].str[3:].astype('int64')

# print(rate_card_data.dtypes)

# Sample rate card data (you should load this from your CSV file)
# rate_card_data = {
#     "1a": 14676,
#     "2a": 9441,
#     "1a,1c": 7073,
#     # Add more rate card data for other combinations
# }

# floater discount logic
def calculate_floater_discount(members):
    if len(members) > 1:
        return 0.5
    return 0

def calculate_health_insurance_premium(member_ages, sum_insured, city_tier, tenure):
    # Define base rate for insurance
    base_rate = 1000 

    # Define age-based factors (adjust these based on your rate card)
    age_factors = {
        18: 1.2,  # Example: 20% increase for age 18
        30: 1.0,  # Example: No age factor for age 30
        40: 1.5,  # Example: 50% increase for age 40
        60: 1.7,  # Example: 70% increase for age 60
        99: 2.0   # Example: 100% increase for age 99
        # Add more age factors as needed
    }

    # Apply city tier-based premium adjustments
    city_premium_adjustment = {
        'tier-1': 1.2,  # Example: 20% premium increase for tier-1 city
        'tier-2': 1.0,  # Example: No premium adjustment for tier-2 city
    }

    # Apply tenure-based discounts
    tenure_discount = {
        '1yr': 1.0,  # No discount for 1-year insurance
        '2yr': 0.9,  # 10% discount for 2-year insurance
    }

    # Calculate premium for each insured member based on their age
    total_premium = 0
    for age in member_ages:
        age_factor = 1.0 # Default to 1.0
        for (key, value) in age_factors.items():
            if (age <= key):
                age_factor = value
                break
        member_premium = base_rate * age_factor * city_premium_adjustment.get(city_tier, 1.0) * tenure_discount.get(tenure, 1.0)
        total_premium += member_premium

    # Multiply total premium by the sum insured
    total_premium *= sum_insured/100000

    return total_premium


@app.route('/calculate_premium', methods=['POST'])
def calculate_premium():
    data = request.json

    sum_insured = data['sum_insured']
    city_tier = data['city_tier']
    tenure = data['tenure']
    member_ages = data['member_ages']

    total_premium = calculate_health_insurance_premium(member_ages, sum_insured, city_tier, tenure)

    return jsonify({"premium": total_premium})

if __name__ == '__main__':
    app.run(port=8080, debug=True)
