"""
Simplified diet plan generator that doesn't rely on complex data structures.
This is a fallback solution when the main DietModel fails.
"""


def generate_simple_meal_plan(height, weight, age, gender, activity_level):
    """Generate a simple meal plan based on user data."""
    # Calculate BMI
    bmi = weight / (height / 100) ** 2

    if bmi < 18.5:
        status = "Underweight"
    elif 18.5 <= bmi <= 24.9:
        status = "Normal weight"
    elif 25 <= bmi <= 29.9:
        status = "Overweight"
    else:
        status = "Obese"

    # Calculate caloric needs
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_multiplier = {
        "sedentary": 1.2,  # Little or no exercise
        "moderate": 1.55,  # Moderate exercise 3-5 days/week
        "active": 1.725  # Hard exercise 6-7 days/week
    }

    caloric_needs = round(bmr * activity_multiplier[activity_level.lower()])
    daily_calorie_deficit = 500
    target_calories = caloric_needs - daily_calorie_deficit

    # Hardcoded meal options
    breakfast_options = [
        {"food_item": "Oatmeal with Berries", "calories": 300, "protein": 10, "fat": 5, "carbs": 50, "fiber": 8,
         "serving_size": "1 bowl"},
        {"food_item": "Scrambled Eggs", "calories": 220, "protein": 15, "fat": 15, "carbs": 2, "fiber": 0,
         "serving_size": "2 eggs"},
        {"food_item": "Greek Yogurt with Honey", "calories": 180, "protein": 20, "fat": 8, "carbs": 15, "fiber": 0,
         "serving_size": "1 cup"},
        {"food_item": "Avocado Toast", "calories": 250, "protein": 8, "fat": 15, "carbs": 30, "fiber": 6,
         "serving_size": "1 slice"},
        {"food_item": "Smoothie Bowl", "calories": 320, "protein": 12, "fat": 6, "carbs": 60, "fiber": 10,
         "serving_size": "1 bowl"}
    ]

    lunch_options = [
        {"food_item": "Chicken Salad", "calories": 350, "protein": 30, "fat": 15, "carbs": 10, "fiber": 3,
         "serving_size": "1 plate"},
        {"food_item": "Quinoa Bowl", "calories": 400, "protein": 15, "fat": 10, "carbs": 60, "fiber": 8,
         "serving_size": "1 bowl"},
        {"food_item": "Tuna Sandwich", "calories": 320, "protein": 25, "fat": 12, "carbs": 30, "fiber": 4,
         "serving_size": "1 sandwich"},
        {"food_item": "Vegetable Soup", "calories": 200, "protein": 8, "fat": 5, "carbs": 30, "fiber": 6,
         "serving_size": "1 bowl"},
        {"food_item": "Lentil Curry", "calories": 380, "protein": 18, "fat": 8, "carbs": 50, "fiber": 12,
         "serving_size": "1 plate"}
    ]

    dinner_options = [
        {"food_item": "Grilled Salmon", "calories": 400, "protein": 35, "fat": 20, "carbs": 0, "fiber": 0,
         "serving_size": "1 fillet"},
        {"food_item": "Stir-Fry Vegetables", "calories": 250, "protein": 10, "fat": 8, "carbs": 30, "fiber": 8,
         "serving_size": "1 plate"},
        {"food_item": "Pasta with Tomato Sauce", "calories": 450, "protein": 15, "fat": 10, "carbs": 70, "fiber": 4,
         "serving_size": "1 plate"},
        {"food_item": "Baked Chicken", "calories": 350, "protein": 40, "fat": 15, "carbs": 0, "fiber": 0,
         "serving_size": "1 breast"},
        {"food_item": "Bean Burrito", "calories": 500, "protein": 20, "fat": 15, "carbs": 70, "fiber": 12,
         "serving_size": "1 burrito"}
    ]

    # Generate weekly plan
    import random
    weekly_plan = []

    for day in range(1, 8):
        # Select random meals for each day
        breakfast = [random.choice(breakfast_options)]
        lunch = [random.choice(lunch_options)]
        dinner = [random.choice(dinner_options)]

        # Calculate total calories
        total_calories = breakfast[0]["calories"] + lunch[0]["calories"] + dinner[0]["calories"]

        daily_plan = {
            "day": day,
            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner,
            "total_calories": total_calories
        }

        weekly_plan.append(daily_plan)

    # Calculate weight loss projection
    calorie_deficit_7_days = daily_calorie_deficit * 7
    weight_loss_kg = calorie_deficit_7_days / 7700
    estimated_weight = weight - weight_loss_kg

    # Prepare final data
    plan_data = {
        'bmi': round(bmi, 2),
        'status': status,
        'caloric_needs': caloric_needs,
        'weekly_plan': weekly_plan,
        'estimated_weight_loss': round(weight_loss_kg, 2),
        'estimated_new_weight': round(estimated_weight, 2)
    }

    return plan_data

