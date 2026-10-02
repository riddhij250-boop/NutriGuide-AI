"""
app.py - The Flask web server (backend).
This file handles all HTTP requests from the browser and sends back responses.

Routes:
  GET  /              → Home page
  GET  /preferences   → Preferences form page
  GET  /recommendations → Recommendations page
  GET  /food/<id>     → Food detail page
  GET  /dashboard     → Dashboard page
  GET  /about         → About page
  POST /api/recommend → JSON API: get recommendations
  GET  /api/food/<id> → JSON API: get single food details
  GET  /api/foods     → JSON API: get all foods
"""

from flask import Flask, render_template, request, jsonify, session
import sqlite3
import os
from recommender import get_recommendations, get_nutrition_tip
from database import create_database, DB_PATH

app = Flask(__name__)
# Secret key is needed for session (storing user data between requests)
app.secret_key = "nutriguide_secret_key_2024"

# -------------------------------------------------------
# Helper: Get a database connection
# -------------------------------------------------------
def get_db():
    """Open a connection to the SQLite database and return rows as dicts."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # Lets us access columns by name
    return conn


def food_row_to_dict(row) -> dict:
    """Convert a sqlite3.Row object to a plain Python dictionary."""
    return {
        "id": row["id"],
        "name": row["name"],
        "category": row["category"],
        "diet_type": row["diet_type"],
        "meal_type": row["meal_type"],
        "cuisine": row["cuisine"],
        "calories": row["calories"],
        "protein": row["protein"],
        "carbs": row["carbs"],
        "fats": row["fats"],
        "ingredients": row["ingredients"],
        "benefits": row["benefits"],
        "allergens": row["allergens"],
        "health_goals": row["health_goals"],
        "image_emoji": row["image_emoji"],
    }


# -------------------------------------------------------
# Page routes (serve HTML pages)
# -------------------------------------------------------

@app.route("/")
def home():
    """Home page."""
    return render_template("index.html")


@app.route("/preferences")
def preferences():
    """User preferences form page."""
    return render_template("preferences.html")


@app.route("/recommendations")
def recommendations():
    """Recommendations results page."""
    return render_template("recommendations.html")


@app.route("/food/<int:food_id>")
def food_detail(food_id):
    """Single food detail page."""
    return render_template("food_detail.html", food_id=food_id)


@app.route("/dashboard")
def dashboard():
    """Dashboard page showing stats and charts."""
    return render_template("dashboard.html")


@app.route("/about")
def about():
    """About page."""
    return render_template("about.html")


# -------------------------------------------------------
# API routes (return JSON data to the frontend JavaScript)
# -------------------------------------------------------

@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    """
    Receive user preferences as JSON, run the recommendation algorithm,
    and return a list of scored food items.
    """
    try:
        data = request.get_json()

        # Save to session so other pages can access user preferences
        session["user_prefs"] = data

        # Load all foods from the database
        conn = get_db()
        rows = conn.execute("SELECT * FROM foods").fetchall()
        conn.close()

        all_foods = [food_row_to_dict(r) for r in rows]

        # Run recommendation logic
        recommended = get_recommendations(all_foods, data)

        # Get a personalised tip
        tip = get_nutrition_tip(
            data.get("health_goal", ""),
            data.get("age", 0)
        )

        return jsonify({
            "success": True,
            "recommendations": recommended,
            "tip": tip,
            "total": len(recommended),
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/food/<int:food_id>")
def api_food_detail(food_id):
    """Return details for a single food item."""
    try:
        conn = get_db()
        row = conn.execute("SELECT * FROM foods WHERE id = ?", (food_id,)).fetchone()
        conn.close()

        if row is None:
            return jsonify({"success": False, "error": "Food not found"}), 404

        return jsonify({"success": True, "food": food_row_to_dict(row)})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/foods")
def api_all_foods():
    """Return all foods, with optional filtering by diet_type or meal_type."""
    try:
        diet = request.args.get("diet", "")
        meal = request.args.get("meal", "")
        cuisine = request.args.get("cuisine", "")

        query = "SELECT * FROM foods WHERE 1=1"
        params = []

        if diet:
            query += " AND diet_type = ?"
            params.append(diet)
        if meal:
            query += " AND meal_type LIKE ?"
            params.append(f"%{meal}%")
        if cuisine:
            query += " AND cuisine = ?"
            params.append(cuisine)

        conn = get_db()
        rows = conn.execute(query, params).fetchall()
        conn.close()

        foods = [food_row_to_dict(r) for r in rows]
        return jsonify({"success": True, "foods": foods, "total": len(foods)})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/stats")
def api_stats():
    """Return summary statistics for the dashboard."""
    try:
        conn = get_db()
        cursor = conn.cursor()

        total = cursor.execute("SELECT COUNT(*) FROM foods").fetchone()[0]
        vegan = cursor.execute("SELECT COUNT(*) FROM foods WHERE diet_type='vegan'").fetchone()[0]
        vegetarian = cursor.execute("SELECT COUNT(*) FROM foods WHERE diet_type='vegetarian'").fetchone()[0]
        jain = cursor.execute("SELECT COUNT(*) FROM foods WHERE diet_type='jain'").fetchone()[0]
        non_veg = cursor.execute("SELECT COUNT(*) FROM foods WHERE diet_type='non_vegetarian'").fetchone()[0]

        # Average macros
        avg = cursor.execute(
            "SELECT AVG(calories), AVG(protein), AVG(carbs), AVG(fats) FROM foods"
        ).fetchone()

        # Foods by cuisine
        cuisines = cursor.execute(
            "SELECT cuisine, COUNT(*) as count FROM foods GROUP BY cuisine"
        ).fetchall()

        # Foods by category
        categories = cursor.execute(
            "SELECT category, COUNT(*) as count FROM foods GROUP BY category"
        ).fetchall()

        conn.close()

        return jsonify({
            "success": True,
            "total_foods": total,
            "diet_breakdown": {
                "vegan": vegan,
                "vegetarian": vegetarian,
                "jain": jain,
                "non_vegetarian": non_veg,
            },
            "avg_macros": {
                "calories": round(avg[0], 1),
                "protein": round(avg[1], 1),
                "carbs": round(avg[2], 1),
                "fats": round(avg[3], 1),
            },
            "by_cuisine": [{"cuisine": r[0], "count": r[1]} for r in cuisines],
            "by_category": [{"category": r[0], "count": r[1]} for r in categories],
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -------------------------------------------------------
# Start the app
# -------------------------------------------------------
if __name__ == "__main__":
    # Create (or verify) the database before starting
    if not os.path.exists(DB_PATH):
        print("Database not found. Creating it now...")
        create_database()
    print("NutriGuide AI is starting...")
    print("Open your browser and go to: http://127.0.0.1:5000")
    app.run(debug=True)
