import os
import sys
import traceback
from flask import Blueprint, render_template, request, jsonify, g, redirect, url_for, session, render_template_string
from app.auth import login_required
from app.simple_diet import generate_simple_meal_plan

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if g.user:
        return redirect(url_for('main.diet_form'))
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@main.route('/diet-form')
@login_required
def diet_form():
    return render_template('diet/form.html')


@main.route('/process-diet', methods=['POST'])
@login_required
def process_diet():
    try:
        # Store form data in session
        diet_data = {
            'height': float(request.form.get('height', 0)),
            'weight': float(request.form.get('weight', 0)),
            'age': int(request.form.get('age', 0)),
            'gender': request.form.get('gender', ''),
            'activity_level': request.form.get('activity_level', '')
        }

        # Validate data
        if diet_data['height'] <= 0 or diet_data['weight'] <= 0 or diet_data['age'] <= 0:
            return render_template('diet/form.html', error="Please enter valid height, weight, and age values.")

        if not diet_data['gender'] or not diet_data['activity_level']:
            return render_template('diet/form.html', error="Please select gender and activity level.")

        # Print debug information
        print(f"Storing diet data in session: {diet_data}")

        # Store in session
        session['diet_data'] = diet_data
        session.modified = True  # Ensure session is saved

        # Redirect to the processing page
        return redirect(url_for('main.processing'))
    except Exception as e:
        print(f"Error processing diet form: {str(e)}")
        print(traceback.format_exc())
        return render_template('diet/form.html', error=str(e))


@main.route('/processing')
@login_required
def processing():
    # Check if we have diet data in the session
    if 'diet_data' not in session:
        return redirect(url_for('main.diet_form'))

    return render_template('diet/processing.html')


@main.route('/meal-plan')
@login_required
def meal_plan():
    try:
        # Check if we have diet data in the session
        if 'diet_data' not in session:
            print("No diet data found in session")
            return redirect(url_for('main.diet_form'))

        # Get diet data from session
        data = session.get('diet_data')

        if not data:
            print("Diet data is empty")
            return render_template('diet/form.html', error="Please fill out the form again.")

        print(f"Diet data from session: {data}")

        # Use the simplified meal plan generator
        try:
            plan_data = generate_simple_meal_plan(
                data['height'],
                data['weight'],
                data['age'],
                data['gender'],
                data['activity_level']
            )
            print("Successfully generated simple meal plan")
        except Exception as e:
            print(f"Error generating simple meal plan: {str(e)}")
            print(traceback.format_exc())
            return render_template('diet/error.html', error=f"Error generating meal plan: {str(e)}")

        # Try to render the template
        try:
            return render_template('diet/meal_plan.html', data=plan_data)
        except Exception as template_error:
            print(f"Error rendering meal_plan.html template: {str(template_error)}")
            print(traceback.format_exc())

            # Use a fallback template string if the template file can't be found
            fallback_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Your Meal Plan</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; background-color: #121212; color: white; }
                    h1, h2, h3 { color: #39ff14; }
                    .metric { margin-bottom: 20px; background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px; }
                    .day { margin-bottom: 30px; border-bottom: 1px solid #ccc; padding-bottom: 20px; }
                    .meal { margin-bottom: 15px; background: rgba(255, 255, 255, 0.05); padding: 10px; border-radius: 5px; }
                    .btn { display: inline-block; background: linear-gradient(45deg, #00ffff, #bf00ff); color: white; 
                           padding: 10px 20px; text-decoration: none; border-radius: 20px; margin-top: 20px; }
                </style>
            </head>
            <body>
                <h1>Your Personalized Meal Plan</h1>

                <div class="metric">
                    <h2>BMI: {{ data.bmi }} ({{ data.status }})</h2>
                    <h2>Daily Calories: {{ data.caloric_needs }} kcal/day</h2>
                    <h2>Expected Weight Loss: {{ data.estimated_weight_loss }} kg</h2>
                </div>

                {% for day in data.weekly_plan %}
                <div class="day">
                    <h2>Day {{ day.day }}</h2>

                    <div class="meal">
                        <h3>Breakfast</h3>
                        {% for meal in day.breakfast %}
                        <p>{{ meal.food_item }} ({{ meal.calories }} kcal)</p>
                        <p>Protein: {{ meal.protein }}g | Fat: {{ meal.fat }}g | Carbs: {{ meal.carbs }}g | Fiber: {{ meal.fiber }}g</p>
                        {% endfor %}
                    </div>

                    <div class="meal">
                        <h3>Lunch</h3>
                        {% for meal in day.lunch %}
                        <p>{{ meal.food_item }} ({{ meal.calories }} kcal)</p>
                        <p>Protein: {{ meal.protein }}g | Fat: {{ meal.fat }}g | Carbs: {{ meal.carbs }}g | Fiber: {{ meal.fiber }}g</p>
                        {% endfor %}
                    </div>

                    <div class="meal">
                        <h3>Dinner</h3>
                        {% for meal in day.dinner %}
                        <p>{{ meal.food_item }} ({{ meal.calories }} kcal)</p>
                        <p>Protein: {{ meal.protein }}g | Fat: {{ meal.fat }}g | Carbs: {{ meal.carbs }}g | Fiber: {{ meal.fiber }}g</p>
                        {% endfor %}
                    </div>

                    <p>Total calories: {{ day.total_calories }} kcal</p>
                </div>
                {% endfor %}

                <a href="{{ url_for('main.diet_form') }}" class="btn">Create New Plan</a>
            </body>
            </html>
            """
            return render_template_string(fallback_html, data=plan_data)
    except Exception as e:
        print(f"Error generating meal plan: {str(e)}")
        print(traceback.format_exc())
        return render_template('diet/error.html', error=f"Error generating meal plan: {str(e)}")


@main.route('/debug-meal-plan')
@login_required
def debug_meal_plan():
    """A debug endpoint to test meal plan generation directly."""
    try:
        # Use sample data
        sample_data = {
            'height': 175.0,
            'weight': 70.0,
            'age': 30,
            'gender': 'male',
            'activity_level': 'moderate'
        }

        # Generate a meal plan using the simplified generator
        plan_data = generate_simple_meal_plan(
            sample_data['height'],
            sample_data['weight'],
            sample_data['age'],
            sample_data['gender'],
            sample_data['activity_level']
        )

        # Return the plan as JSON for debugging
        return jsonify({
            'success': True,
            'message': 'Debug meal plan generated successfully',
            'data': plan_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        })


@main.route('/api/check-session')
@login_required
def check_session():
    """Debug endpoint to check session data."""
    try:
        return jsonify({
            'success': True,
            'has_diet_data': 'diet_data' in session,
            'diet_data': session.get('diet_data'),
            'user_id': session.get('user_id'),
            'all_keys': list(session.keys())
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@main.route('/api/clear-session')
@login_required
def clear_session():
    """Debug endpoint to clear session data."""
    try:
        if 'diet_data' in session:
            del session['diet_data']
            session.modified = True

        return jsonify({
            'success': True,
            'message': 'Diet data cleared from session',
            'remaining_keys': list(session.keys())
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@main.route('/debug')
@login_required
def debug_page():
    """Debug page to test meal plan generation."""
    return render_template('diet/debug.html')

