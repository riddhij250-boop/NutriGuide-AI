# NutriGuide AI – Smart Food Recommendation System
### BCA AI/ML College Project

A complete web application that recommends personalised foods based on
dietary preferences, health goals, allergies, and available ingredients.

---

## Project Structure

```
nutriguide/
├── app.py              ← Flask web server (main entry point)
├── recommender.py      ← AI recommendation logic
├── database.py         ← Creates the SQLite database + 35 food items
├── requirements.txt    ← Python packages needed
├── data/
│   └── nutriguide.db   ← SQLite database (created when you run database.py)
├── templates/
│   ├── index.html      ← Home page
│   ├── preferences.html← 3-step preference form
│   ├── recommendations.html ← Food cards with scores
│   ├── food_detail.html← Full details for one food
│   ├── dashboard.html  ← Stats + charts + browse all foods
│   └── about.html      ← About the project
└── static/
    ├── css/
    │   └── style.css   ← All styles (responsive, modern design)
    └── js/
        ├── main.js         ← Shared JS (navbar, utilities)
        ├── preferences.js  ← Form handling + API call
        ├── recommendations.js ← Render food cards
        ├── food_detail.js  ← Single food page
        └── dashboard.js    ← Charts + food table
```

---

## How to Run

### Step 1 – Make sure Python is installed
```
python --version
```
You need Python 3.8 or newer.

### Step 2 – Install Flask
```
pip install flask
```

### Step 3 – Create the database
Run this once to create the SQLite database with 35 foods:
```
python database.py
```
You should see:
```
[OK] Database created at: ...nutriguide.db
[OK] 35 food items inserted successfully!
```

### Step 4 – Start the server
```
python app.py
```
You should see Flask output like:
```
 * Running on http://127.0.0.1:5000
```

### Step 5 – Open the app in your browser
Go to: **http://127.0.0.1:5000**

---

## Pages

| URL | Page |
|-----|------|
| `/` | Home – introduction and overview |
| `/preferences` | Fill in your preferences (3-step form) |
| `/recommendations` | View your AI food recommendations |
| `/food/<id>` | Full details of a single food item |
| `/dashboard` | Statistics, charts, and browse all 35 foods |
| `/about` | About the project and how the AI works |

---

## How the Recommendation Algorithm Works

Each food gets a score out of **100 points**:

| Criteria | Points |
|----------|--------|
| Diet type matches (vegan/vegetarian/jain/non-veg) | 30 |
| Health goal matches (weight loss, muscle gain, etc.) | 25 |
| Meal type matches (breakfast/lunch/dinner/snack) | 20 |
| Available ingredients match food ingredients | 15 |
| Cuisine preference matches | 10 |

Foods containing your **allergens are completely removed** before scoring.

---

## Technology Stack

- **Python 3** – Main language
- **Flask** – Web framework
- **SQLite** – Database (no setup, just a file)
- **HTML/CSS/JavaScript** – Frontend UI
- **No paid APIs** – Everything runs locally

---

## Important Files Explained

### `app.py`
The main web server. When you open `http://127.0.0.1:5000`, Flask reads this file.
It has URL routes (like `/`, `/preferences`) that send HTML pages to your browser.
It also has API routes (like `/api/recommend`) that return JSON data to JavaScript.

### `recommender.py`
This is the "AI brain". It contains:
- `score_food()` – Scores one food against user preferences
- `get_recommendations()` – Filters allergens + scores all 35 foods + sorts them
- `get_nutrition_tip()` – Returns a personalised tip based on goal and age

### `database.py`
Sets up the SQLite database file and inserts all 35 food items.
Run this once with `python database.py` before starting the app.

### `templates/preferences.html` + `static/js/preferences.js`
The 3-step form where the user enters their details.
When submitted, `preferences.js` sends the data to `/api/recommend` and
saves the results in `localStorage` (browser storage).

### `templates/recommendations.html` + `static/js/recommendations.js`
Reads the results from `localStorage` and displays food cards with scores,
badges, macros, and a "View Details" link.

### `static/css/style.css`
All the visual styling – colours, layout, animations, responsive design.
Uses CSS variables (`:root`) to keep colours consistent.
