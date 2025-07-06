# This file contains the DietModel class that was imported in routes.py
import pandas as pd
import numpy as np
import os
import random


class DietModel:
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
        meal_data = self.nutrition_data[self.nutrition_data['Meal Type'] == meal_type]

        # Filter out already used food items
        available_meals = meal_data[~meal_data["Food Item"].isin(used_food_items)]

        if available_meals.empty:
            # If all meals have been used, reset and use any meal
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
            return meal_plan

        return []

    def generate_weekly_plan(self, caloric_needs, daily_calorie_deficit):
        """Generate a weekly meal plan based on caloric needs."""
        used_food_items = set()
        weekly_plan = []

        target_calories = caloric_needs - daily_calorie_deficit

        for day in range(7):
            breakfast = self.generate_meal_plan(target_calories / 3, "Breakfast", used_food_items)
            lunch = self.generate_meal_plan(target_calories / 3, "Lunch", used_food_items)
            dinner = self.generate_meal_plan(target_calories / 3, "Dinner", used_food_items)

            daily_plan = {
                "day": day + 1,
                "breakfast": breakfast,
                "lunch": lunch,
                "dinner": dinner,
                "total_calories": sum(
                    sum(meal["calories"] for meal in meals)
                    for meals in [breakfast, lunch, dinner] if meals
                )
            }
            weekly_plan.append(daily_plan)

        return weekly_plan

