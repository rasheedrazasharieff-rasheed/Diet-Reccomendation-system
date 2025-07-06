def calculate_bmi(height, weight):
    """Calculate BMI and return status."""
    bmi = weight / (height / 100) ** 2

    if bmi < 18.5:
        status = "Underweight"
    elif 18.5 <= bmi <= 24.9:
        status = "Normal weight"
    elif 25 <= bmi <= 29.9:
        status = "Overweight"
    else:
        status = "Obese"

    return bmi, status


def calculate_caloric_needs(height, weight, age, gender, activity_level):
    """Calculate daily caloric needs."""
    # Mifflin-St Jeor Equation
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_multiplier = {
        "sedentary": 1.2,  # Little or no exercise
        "moderate": 1.55,  # Moderate exercise 3-5 days/week
        "active": 1.725  # Hard exercise 6-7 days/week
    }

    return round(bmr * activity_multiplier[activity_level.lower()])

