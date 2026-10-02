"""
database.py - Sets up the SQLite database and seeds it with 35 food items.
This file creates the database tables and fills them with sample data.
Run this file once before starting the app: python database.py
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'nutriguide.db')

# -------------------------------------------------------------------
# All 35 sample food items
# -------------------------------------------------------------------
FOOD_DATA = [
    # id, name, category, diet_type, meal_type, cuisine,
    # calories, protein, carbs, fats,
    # ingredients (comma-separated), benefits, allergens,
    # health_goals (comma-separated), image_emoji
    (1, "Masoor Dal", "legume", "vegan", "lunch,dinner", "Indian",
     180, 12, 30, 2,
     "red lentils,tomato,onion,garlic,cumin,turmeric",
     "High protein plant food, great for heart health and digestion",
     "none",
     "weight_loss,muscle_gain,heart_health", "🍲"),

    (2, "Paneer Tikka", "dairy", "vegetarian", "snack,dinner", "Indian",
     290, 18, 8, 20,
     "paneer,yogurt,capsicum,onion,tomato,spices",
     "Rich in calcium and protein, supports bone and muscle health",
     "dairy",
     "muscle_gain,weight_management", "🧀"),

    (3, "Quinoa Salad", "grain", "vegan", "lunch,dinner", "Continental",
     220, 8, 35, 5,
     "quinoa,cucumber,tomato,olive oil,lemon,herbs",
     "Complete protein source, gluten-free, high in fibre",
     "none",
     "weight_loss,diabetes_control,heart_health", "🥗"),

    (4, "Chicken Breast Grilled", "meat", "non_vegetarian", "lunch,dinner", "Continental",
     165, 31, 0, 4,
     "chicken breast,olive oil,garlic,herbs,lemon",
     "Lean protein, very low fat, excellent for muscle building",
     "none",
     "muscle_gain,weight_loss", "🍗"),

    (5, "Oatmeal with Fruits", "grain", "vegan", "breakfast", "Continental",
     250, 7, 45, 4,
     "oats,banana,strawberry,almond milk,honey,chia seeds",
     "High fibre, reduces cholesterol, sustained energy release",
     "gluten",
     "weight_loss,heart_health,diabetes_control", "🥣"),

    (6, "Idli Sambar", "grain", "vegan", "breakfast,lunch", "South Indian",
     200, 6, 38, 2,
     "rice,urad dal,sambar,vegetables,mustard seeds",
     "Fermented food, probiotic benefits, easy to digest",
     "none",
     "weight_loss,digestive_health", "🍚"),

    (7, "Egg Omelette", "egg", "non_vegetarian", "breakfast,snack", "Continental",
     180, 14, 2, 13,
     "eggs,onion,capsicum,tomato,butter,salt,pepper",
     "Complete protein, rich in vitamins B12 and D",
     "eggs",
     "muscle_gain,weight_management", "🍳"),

    (8, "Palak Paneer", "dairy", "vegetarian", "lunch,dinner", "Indian",
     240, 14, 10, 16,
     "spinach,paneer,onion,tomato,cream,spices",
     "Rich in iron, calcium, and protein; great for anaemia prevention",
     "dairy",
     "muscle_gain,weight_management,bone_health", "🥬"),

    (9, "Brown Rice Bowl", "grain", "vegan", "lunch,dinner", "Asian",
     215, 5, 45, 2,
     "brown rice,mixed vegetables,soy sauce,sesame oil",
     "Complex carbs, high fibre, better blood sugar control than white rice",
     "gluten",
     "diabetes_control,weight_loss,heart_health", "🍱"),

    (10, "Moong Dal Soup", "legume", "vegan", "lunch,dinner", "Indian",
     150, 10, 25, 1,
     "moong dal,ginger,garlic,cumin,turmeric,lemon",
     "Easy to digest, high protein, detoxifying",
     "none",
     "weight_loss,digestive_health,detox", "🍵"),

    (11, "Greek Yogurt Parfait", "dairy", "vegetarian", "breakfast,snack", "Continental",
     180, 15, 20, 3,
     "greek yogurt,granola,berries,honey,nuts",
     "Probiotic rich, high protein, good for gut and bone health",
     "dairy,gluten,nuts",
     "weight_management,digestive_health,muscle_gain", "🍓"),

    (12, "Tofu Stir Fry", "soy", "vegan", "lunch,dinner", "Asian",
     190, 14, 12, 9,
     "tofu,broccoli,bell pepper,soy sauce,ginger,garlic,sesame oil",
     "Plant protein, anti-inflammatory, supports heart health",
     "soy,gluten",
     "muscle_gain,heart_health,weight_loss", "🥦"),

    (13, "Samosa (Baked)", "snack", "vegan", "snack", "Indian",
     180, 4, 28, 6,
     "potato,peas,flour,spices,coriander",
     "Energy-dense snack, good for quick energy",
     "gluten",
     "weight_management", "🥟"),

    (14, "Fish Curry", "seafood", "non_vegetarian", "lunch,dinner", "Indian",
     210, 22, 8, 9,
     "fish,coconut milk,tomato,onion,spices,curry leaves",
     "Omega-3 fatty acids, brain health, heart health",
     "fish,shellfish",
     "heart_health,brain_health,muscle_gain", "🐟"),

    (15, "Avocado Toast", "grain", "vegan", "breakfast,snack", "Continental",
     250, 6, 28, 14,
     "whole grain bread,avocado,lemon,salt,chilli flakes",
     "Healthy fats, fibre, potassium — great for heart health",
     "gluten",
     "heart_health,weight_management", "🥑"),

    (16, "Rajma Chawal", "legume", "vegan", "lunch,dinner", "Indian",
     320, 14, 58, 4,
     "kidney beans,rice,onion,tomato,spices,bay leaf",
     "High fibre, plant protein, iron-rich",
     "none",
     "muscle_gain,weight_management,heart_health", "🫘"),

    (17, "Banana Smoothie", "fruit", "vegetarian", "breakfast,snack", "Continental",
     200, 5, 42, 2,
     "banana,milk,yogurt,honey,cinnamon",
     "Quick energy, potassium, calcium, mood booster",
     "dairy",
     "muscle_gain,weight_management,energy_boost", "🍌"),

    (18, "Chole Bhature", "legume", "vegan", "breakfast,lunch", "Indian",
     480, 16, 72, 14,
     "chickpeas,flour,yogurt,onion,tomato,spices",
     "High protein meal, iron-rich chickpeas — enjoy in moderation",
     "gluten",
     "muscle_gain,weight_management", "🥙"),

    (19, "Sprouts Salad", "legume", "jain", "breakfast,snack", "Indian",
     120, 8, 20, 1,
     "mixed sprouts,cucumber,tomato,lemon,chaat masala,coriander",
     "Enzyme-rich, high protein, aids metabolism and immunity",
     "none",
     "weight_loss,detox,digestive_health", "🌱"),

    (20, "Salmon with Vegetables", "seafood", "non_vegetarian", "lunch,dinner", "Continental",
     320, 35, 10, 16,
     "salmon,asparagus,lemon,olive oil,garlic,dill",
     "Excellent omega-3 source, high protein, reduces inflammation",
     "fish",
     "heart_health,brain_health,muscle_gain", "🐠"),

    (21, "Dal Makhani", "legume", "vegetarian", "lunch,dinner", "Indian",
     280, 12, 35, 10,
     "black lentils,kidney beans,butter,cream,tomato,spices",
     "Rich protein and fibre meal, iron and folate source",
     "dairy",
     "muscle_gain,weight_management", "🫕"),

    (22, "Vegetable Upma", "grain", "vegan", "breakfast,snack", "South Indian",
     200, 5, 38, 4,
     "semolina,mixed vegetables,mustard seeds,curry leaves,oil",
     "Quick energy, B vitamins, filling breakfast",
     "gluten",
     "weight_management,energy_boost", "🍜"),

    (23, "Mango Lassi", "dairy", "vegetarian", "snack", "Indian",
     220, 6, 40, 4,
     "mango,yogurt,milk,sugar,cardamom",
     "Probiotic drink, vitamin C and A, cooling effect",
     "dairy",
     "digestive_health,energy_boost", "🥭"),

    (24, "Grilled Paneer Salad", "dairy", "jain", "lunch,snack", "Indian",
     210, 15, 10, 14,
     "paneer,lettuce,cucumber,olive oil,lemon,pepper",
     "High calcium, protein-rich, suitable for Jain diet",
     "dairy",
     "muscle_gain,weight_loss,bone_health", "🥗"),

    (25, "Mutton Biryani", "meat", "non_vegetarian", "lunch,dinner", "Indian",
     520, 28, 55, 18,
     "mutton,basmati rice,onion,yogurt,saffron,whole spices",
     "Protein and iron-rich, celebration meal",
     "dairy",
     "muscle_gain", "🍛"),

    (26, "Poha", "grain", "vegan", "breakfast", "Indian",
     190, 4, 38, 4,
     "flattened rice,onion,peas,mustard seeds,curry leaves,lemon",
     "Light and easy to digest, iron-fortified, quick energy",
     "none",
     "weight_loss,digestive_health,energy_boost", "🍚"),

    (27, "Egg Bhurji", "egg", "non_vegetarian", "breakfast,snack", "Indian",
     210, 16, 6, 14,
     "eggs,onion,tomato,capsicum,spices,oil",
     "High protein Indian style scrambled eggs, vitamin-rich",
     "eggs",
     "muscle_gain,weight_management", "🍳"),

    (28, "Lemon Rice", "grain", "vegan", "lunch,dinner", "South Indian",
     220, 4, 45, 5,
     "rice,lemon,peanuts,mustard seeds,curry leaves,turmeric",
     "Anti-inflammatory turmeric, quick to make, good for digestion",
     "peanuts",
     "digestive_health,weight_management", "🍋"),

    (29, "Bean and Veggie Soup", "legume", "vegan", "lunch,dinner", "Continental",
     160, 9, 28, 2,
     "mixed beans,carrot,celery,tomato,garlic,herbs",
     "High fibre, plant protein, low calorie, heart healthy",
     "none",
     "weight_loss,heart_health,diabetes_control", "🥣"),

    (30, "Jain Thali", "mixed", "jain", "lunch,dinner", "Indian",
     350, 12, 55, 8,
     "dal,roti,rice,sabzi,papad,pickle",
     "Balanced Jain meal without root vegetables, diverse nutrients",
     "gluten,dairy",
     "weight_management,digestive_health", "🍽️"),

    (31, "Almond Butter Toast", "grain", "vegan", "breakfast,snack", "Continental",
     280, 9, 30, 16,
     "whole grain bread,almond butter,banana,honey",
     "Healthy fats, vitamin E, magnesium — great pre-workout snack",
     "gluten,nuts",
     "muscle_gain,energy_boost,heart_health", "🍞"),

    (32, "Pav Bhaji", "mixed", "vegan", "snack,dinner", "Indian",
     380, 10, 58, 12,
     "mixed vegetables,pav,butter,tomato,onion,spices",
     "Vegetable-rich street food, vitamin C, iron",
     "gluten,dairy",
     "weight_management,energy_boost", "🥖"),

    (33, "Fruit Bowl", "fruit", "jain", "breakfast,snack", "Continental",
     150, 2, 35, 1,
     "apple,banana,orange,pomegranate,grapes,kiwi",
     "Antioxidants, vitamins, natural sugars for energy",
     "none",
     "weight_loss,detox,heart_health,digestive_health", "🍎"),

    (34, "Stuffed Capsicum", "vegetable", "jain", "lunch,dinner", "Indian",
     190, 8, 22, 8,
     "capsicum,paneer,spices,herbs,tomato sauce",
     "Low calorie, vitamin C rich, good for immunity and eye health",
     "dairy",
     "weight_loss,heart_health,digestive_health", "🫑"),

    (35, "Chana Chaat", "legume", "vegan", "snack", "Indian",
     180, 9, 30, 3,
     "chickpeas,onion,tomato,cucumber,lemon,chaat masala,coriander",
     "High protein snack, fibre-rich, aids digestion",
     "none",
     "weight_loss,muscle_gain,digestive_health", "🥘"),
]


def create_database():
    """Create the SQLite database and populate it with food data."""
    # Make sure the data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ---- Create the foods table ----
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            diet_type TEXT,         -- vegan, vegetarian, jain, non_vegetarian
            meal_type TEXT,         -- breakfast, lunch, dinner, snack
            cuisine TEXT,
            calories INTEGER,
            protein REAL,
            carbs REAL,
            fats REAL,
            ingredients TEXT,       -- comma-separated
            benefits TEXT,
            allergens TEXT,         -- comma-separated (none if no allergens)
            health_goals TEXT,      -- comma-separated
            image_emoji TEXT
        )
    ''')

    # ---- Create user_sessions table to save user preferences ----
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            diet_type TEXT,
            health_goal TEXT,
            allergies TEXT,
            available_ingredients TEXT,
            cuisine TEXT,
            meal_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Clear existing food data and re-insert (so re-running is safe)
    cursor.execute('DELETE FROM foods')

    cursor.executemany('''
        INSERT INTO foods (id, name, category, diet_type, meal_type, cuisine,
                           calories, protein, carbs, fats,
                           ingredients, benefits, allergens, health_goals, image_emoji)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', FOOD_DATA)

    conn.commit()
    conn.close()
    print(f"[OK] Database created at: {DB_PATH}")
    print(f"[OK] {len(FOOD_DATA)} food items inserted successfully!")


if __name__ == '__main__':
    create_database()
