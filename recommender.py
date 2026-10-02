"""
recommender.py - The brain of NutriGuide AI.
This file contains all the logic to score and recommend foods
based on what the user tells us about themselves.

HOW SCORING WORKS (out of 100 points):
  - Diet type match:          30 pts
  - Health goal match:        25 pts
  - Meal type match:          20 pts
  - Ingredients match:        15 pts
  - Cuisine match:            10 pts
"""


def diet_is_compatible(food_diet: str, user_diet: str) -> bool:
    """
    Check if a food's diet type is safe for the user.
    A vegan can eat vegan food.
    A vegetarian can eat vegetarian OR vegan food.
    A Jain can eat Jain OR vegan food (Jain food has stricter rules).
    A non-vegetarian can eat everything.
    """
    compatibility = {
        "vegan":          ["vegan"],
        "vegetarian":     ["vegan", "vegetarian"],
        "jain":           ["vegan", "jain"],
        "non_vegetarian": ["vegan", "vegetarian", "jain", "non_vegetarian"],
    }
    allowed = compatibility.get(user_diet.lower(), [])
    return food_diet.lower() in allowed


def has_allergen(food_allergens: str, user_allergies: str) -> bool:
    """
    Return True if any of the user's allergies appear in the food's allergen list.
    Both inputs are comma-separated strings.
    """
    if not user_allergies or user_allergies.strip().lower() in ("none", ""):
        return False
    if food_allergens.strip().lower() == "none":
        return False

    food_list = [a.strip().lower() for a in food_allergens.split(",")]
    user_list = [a.strip().lower() for a in user_allergies.split(",")]

    for allergen in user_list:
        if allergen and allergen in food_list:
            return True
    return False


def score_food(food: dict, preferences: dict) -> int:
    """
    Score a single food item against the user's preferences.
    Returns a score between 0 and 100.
    """
    score = 0

    # 1. Diet type match (30 points)
    if diet_is_compatible(food["diet_type"], preferences.get("diet_type", "")):
        score += 30

    # 2. Health goal match (25 points)
    food_goals = [g.strip().lower() for g in food["health_goals"].split(",")]
    user_goal = preferences.get("health_goal", "").strip().lower()
    if user_goal and user_goal in food_goals:
        score += 25

    # 3. Meal type match (20 points)
    food_meals = [m.strip().lower() for m in food["meal_type"].split(",")]
    user_meal = preferences.get("meal_type", "").strip().lower()
    if user_meal and user_meal in food_meals:
        score += 20

    # 4. Available ingredients match (15 points)
    # Check how many of the user's available ingredients appear in the food
    food_ingredients = [i.strip().lower() for i in food["ingredients"].split(",")]
    user_ingredients_raw = preferences.get("available_ingredients", "")
    if user_ingredients_raw:
        user_ingredients = [i.strip().lower() for i in user_ingredients_raw.split(",")]
        matches = sum(1 for ui in user_ingredients if any(ui in fi for fi in food_ingredients))
        if matches > 0:
            # Award up to 15 points proportionally
            match_ratio = min(matches / max(len(food_ingredients), 1), 1.0)
            score += int(15 * match_ratio)

    # 5. Cuisine match (10 points)
    user_cuisine = preferences.get("cuisine", "").strip().lower()
    food_cuisine = food["cuisine"].strip().lower()
    if user_cuisine and (user_cuisine == food_cuisine or user_cuisine == "any"):
        score += 10

    return score


def get_recommendations(all_foods: list, preferences: dict) -> list:
    """
    Main recommendation function.
    Takes all foods from the database and the user's preferences.
    Returns a filtered and sorted list of recommended foods.

    Each food dict returned has an extra 'score' and 'score_label' key.
    """
    results = []

    for food in all_foods:
        # Hard filter: skip foods that contain the user's allergens
        if has_allergen(food["allergens"], preferences.get("allergies", "")):
            continue

        # Hard filter: skip foods that don't match the user's diet at all
        if not diet_is_compatible(food["diet_type"], preferences.get("diet_type", "non_vegetarian")):
            continue

        # Calculate the match score
        s = score_food(food, preferences)

        # Attach score info to the food dict (make a copy so we don't modify the original)
        food_copy = dict(food)
        food_copy["score"] = s
        food_copy["score_label"] = score_label(s)
        results.append(food_copy)

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def score_label(score: int) -> str:
    """Convert numeric score to a human-readable label."""
    if score >= 80:
        return "Excellent Match"
    elif score >= 60:
        return "Great Match"
    elif score >= 40:
        return "Good Match"
    elif score >= 20:
        return "Fair Match"
    else:
        return "Low Match"


def get_nutrition_tip(health_goal: str, age: int) -> str:
    """Return a personalised nutrition tip based on goal and age."""
    tips = {
        "weight_loss": "Focus on high-fibre, low-calorie foods. Drink water before meals.",
        "muscle_gain": "Aim for 1.6–2.2g of protein per kg of body weight daily.",
        "heart_health": "Reduce saturated fats. Choose omega-3 rich foods like fish and flaxseeds.",
        "diabetes_control": "Choose complex carbs with low glycaemic index. Avoid sugary drinks.",
        "digestive_health": "Include probiotic foods (yogurt, fermented foods) and fibre-rich vegetables.",
        "weight_management": "Maintain a balanced diet with portion control and regular meals.",
        "energy_boost": "Include complex carbs and B-vitamin foods for sustained energy.",
        "detox": "Focus on hydrating foods, green vegetables, and antioxidant-rich fruits.",
        "bone_health": "Ensure adequate calcium and vitamin D from dairy, seeds, and sunlight.",
        "brain_health": "Include omega-3 fatty acids, antioxidants, and B vitamins.",
    }
    tip = tips.get(health_goal, "Eat a balanced diet with variety across all food groups.")

    # Add age-specific advice
    if age and int(age) < 20:
        tip += " As a teenager, ensure adequate calcium for bone development."
    elif age and int(age) > 50:
        tip += " After 50, prioritise calcium, vitamin D, and fibre intake."

    return tip
