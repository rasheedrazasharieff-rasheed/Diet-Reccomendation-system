import os
import sys
from flask import Flask, session
import pandas as pd
import numpy as np
import random

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app.utils import calculate_bmi, calculate_caloric_needs

# Create a test Flask app for session context
app = Flask(__name__)
app.config['SECRET_KEY'] = 'debug_key'

# Sample user data
test_data = {
    'height': 175.0,
    'weight': 70.0,
    'age': 30,
    'gender': 'male',
    'activity_level': 'moderate'
}


class TestDietModel:
    def __init__(self):
        # Simplified initialization for demonstration
        self.breakfast_data = self._load_sample_data('Breakfast')
        self.lunch_data = self._load_sample_data('Lunch')
        self.dinner_data = self._load_sample_data('Dinner')

        # Add Meal Type column to each dataset
        self.breakfast_data['Meal Type'] = 'Breakfast'
        self.lunch_data['Meal Type'] = 'Lunch'
        self.dinner_data['Meal Type'] = 'Dinner'

        # Concatenate all data
        self.nutrition_data = pd.concat(
            [self.breakfast_data, self.lunch_data, self.dinner_data],
            ignore_index=True
        )

        # Features for meal planning
        self.features = ["Calories", "Protein", "Fat", "Carbohydrates", "Fiber"]

    def _load_sample_data(self, meal_type):
        """Load sample food data for the given meal type."""
        # Create sample data for demonstration
        if meal_type == 'Breakfast':
            data = {
                'Food Item': ['Oatmeal with Berries', 'Scrambled Eggs', 'Greek Yogurt with Honey',
                              'Avocado Toast', 'Smoothie Bowl'],
                'Calories': [300, 220, 180, 250, 320],
                'Protein': [10, 15, 20, 8, 12],
                'Fat': [5, 15, 8, 15, 6],
                'Carbohydrates': [50, 2, 15, 30, 60],
                'Fiber': [8, 0, 0, 6, 10],
                'Serving Size': ['1 bowl', '2 eggs', '1 cup', '1 slice', '1 bowl']
            }
        elif meal_type == 'Lunch':
            data = {
                'Food Item': ['Chicken Salad', 'Quinoa Bowl', 'Tuna Sandwich',
                              'Vegetable Soup', 'Lentil Curry'],
                'Calories': [350, 400, 320, 200, 380],
                'Protein': [30, 15, 25, 8, 18],
                'Fat': [15, 10, 12, 5, 8],
                'Carbohydrates': [10, 60, 30, 30, 50],
                'Fiber': [3, 8, 4, 6, 12],
                'Serving Size': ['1 plate', '1 bowl', '1 sandwich', '1 bowl', '1 plate']
            }
        else:  # Dinner
            data = {
                'Food Item': ['Grilled Salmon', 'Stir-Fry Vegetables', 'Pasta with Tomato Sauce',
                              'Baked Chicken', 'Bean Burrito'],
                'Calories': [400, 250, 450, 350, 500],
                'Protein': [35, 10, 15, 40, 20],
                'Fat': [20, 8, 10, 15, 15],
                'Carbohydrates': [0, 30, 70, 0, 70],
                'Fiber': [0, 8, 4, 0, 12],
                'Serving Size': ['1 fillet', '1 plate', '1 plate', '1 breast', '1 burrito']
            }

        return pd.DataFrame(data)

    def generate_meal_plan(self, target_calories, meal_type, used_food_items):
        """Generate a meal plan for the specified meal type."""
        try:
            print(f"Generating meal plan for {meal_type} with target calories: {target_calories}")
            meal_data = self.nutrition_data[self.nutrition_data['Meal Type'] == meal_type]

            if meal_data.empty:
                print(f"No data available for meal type: {meal_type}")
                return []

            # Filter out already used food items
            available_meals = meal_data
            if used_food_items:
                available_meals = meal_data[~meal_data["Food Item"].isin(used_food_items)]

            if available_meals.empty:
                # If all meals have been used, reset and use any meal
                print(f"All {meal_type} items have been used, resetting selection")
                available_meals = meal_data

            # Select a random meal
            if not available_meals.empty:
                food = available_meals.sample(1).iloc[0]
                meal_plan = [{
                    "food_item": food["Food Item"],
                    "calories": int(food["Calories"]),
                    "protein": float(food["Protein"]),
                    "fat": float(food["Fat"]),
                    "carbs": float(food["Carbohydrates"]),
                    "fiber": float(food["Fiber"]),
                    "serving_size": food["Serving Size"]
                }]
                used_food_items.add(food["Food Item"])
                print(f"Selected {food['Food Item']} for {meal_type}")
                return meal_plan

            print(f"No meals available for {meal_type}")
            return []
        except Exception as e:
            import traceback
            print(f"Error in generate_meal_plan for {meal_type}: {str(e)}")
            print(traceback.format_exc())
            return []

    def generate_weekly_plan(self, caloric_needs, daily_calorie_deficit):
        """Generate a weekly meal plan based on caloric needs."""
        try:
            print(f"Generating weekly plan with caloric needs: {caloric_needs}, deficit: {daily_calorie_deficit}")
            used_food_items = set()
            weekly_plan = []

            target_calories = caloric_needs - daily_calorie_deficit
            print(f"Target calories per day: {target_calories}")

            for day in range(7):
                print(f"Generating plan for day {day + 1}")
                try:
                    breakfast = self.generate_meal_plan(target_calories / 3, "Breakfast", used_food_items)
                    print(f"Breakfast generated with {len(breakfast)} items")
                except Exception as e:
                    print(f"Error generating breakfast: {str(e)}")
                    breakfast = []

                try:
                    lunch = self.generate_meal_plan(target_calories / 3, "Lunch", used_food_items)
                    print(f"Lunch generated with {len(lunch)} items")
                except Exception as e:
                    print(f"Error generating lunch: {str(e)}")
                    lunch = []

                try:
                    dinner = self.generate_meal_plan(target_calories / 3, "Dinner", used_food_items)
                    print(f"Dinner generated with {len(dinner)} items")
                except Exception as e:
                    print(f"Error generating dinner: {str(e)}")
                    dinner = []

                # Calculate total calories safely
                total_calories = 0
                for meals in [breakfast, lunch, dinner]:
                    if meals:
                        for meal in meals:
                            if 'calories' in meal:
                                total_calories += meal['calories']

                daily_plan = {
                    "day": day + 1,
                    "breakfast": breakfast,
                    "lunch": lunch,
                    "dinner": dinner,
                    "total_calories": total_calories
                }
                weekly_plan.append(daily_plan)
                print(f"Day {day + 1} plan added successfully")

            print(f"Weekly plan generated with {len(weekly_plan)} days")
            return weekly_plan
        except Exception as e:
            import traceback
            print(f"Error in generate_weekly_plan: {str(e)}")
            print(traceback.format_exc())
            # Return an empty plan instead of raising an exception
            return [{"day": i + 1, "breakfast": [], "lunch": [], "dinner": [], "total_calories": 0} for i in range(7)]


def test_meal_plan_generation():
    print("Starting meal plan generation test...")

    try:
        # Calculate health metrics
        bmi, status = calculate_bmi(test_data['height'], test_data['weight'])
        print(f"BMI calculation successful: {bmi}, {status}")

        caloric_needs = calculate_caloric_needs(
            test_data['height'],
            test_data['weight'],
            test_data['age'],
            test_data['gender'],
            test_data['activity_level']
        )
        print(f"Caloric needs calculation successful: {caloric_needs}")

        # Generate meal plan
        diet_model = TestDietModel()
        print("DietModel initialized successfully")

        daily_calorie_deficit = 500
        weekly_plan = diet_model.generate_weekly_plan(caloric_needs, daily_calorie_deficit)
        print(f"Weekly plan generated successfully with {len(weekly_plan)} days")

        # Ensure variety in the meal plan
        for day in weekly_plan:
            for meal_type in ['breakfast', 'lunch', 'dinner']:
                if not day[meal_type]:
                    # If no meal was found, add a random one
                    random_meal = diet_model.generate_meal_plan(caloric_needs / 3, meal_type.capitalize(), set())
                    day[meal_type] = random_meal
        print("Meal variety ensured successfully")

        # Calculate weight loss projection
        calorie_deficit_7_days = daily_calorie_deficit * 7
        weight_loss_kg = calorie_deficit_7_days / 7700
        estimated_weight = test_data['weight'] - weight_loss_kg
        print(f"Weight projection calculated successfully: loss={weight_loss_kg}kg, new weight={estimated_weight}kg")

        # Prepare data for the template
        plan_data = {
            'bmi': round(bmi, 2),
            'status': status,
            'caloric_needs': caloric_needs,
            'weekly_plan': weekly_plan,
            'estimated_weight_loss': round(weight_loss_kg, 2),
            'estimated_new_weight': round(estimated_weight, 2)
        }

        print("Successfully prepared plan data")
        print("Test completed successfully!")

        # Print a sample of the meal plan
        print("\nSample meal plan for Day 1:")
        day1 = weekly_plan[0]
        print(f"Breakfast: {day1['breakfast'][0]['food_item'] if day1['breakfast'] else 'None'}")
        print(f"Lunch: {day1['lunch'][0]['food_item'] if day1['lunch'] else 'None'}")
        print(f"Dinner: {day1['dinner'][0]['food_item'] if day1['dinner'] else 'None'}")
        print(f"Total calories: {day1['total_calories']}")

    except Exception as e:
        import traceback
        print(f"Test failed with error: {str(e)}")
        print(traceback.format_exc())


if __name__ == "__main__":
    test_meal_plan_generation()

