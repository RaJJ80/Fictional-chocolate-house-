from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# --------- Routes ---------

# Home Page
@app.route("/")
def home():
    return render_template("home.html")

# --------- Seasonal Flavors ---------
@app.route("/seasonal_flavors")
def seasonal_flavors():
    conn = sqlite3.connect("chocolate_house.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Seasonal_Flavors WHERE availability = 1;")
    flavors = cursor.fetchall()
    conn.close()
    return render_template("seasonal_flavors.html", flavors=flavors)

@app.route("/add_flavor", methods=["POST"])
def add_flavor():
    flavor_name = request.form["flavor_name"]
    conn = sqlite3.connect("chocolate_house.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Seasonal_Flavors (flavor_name) VALUES (?);", (flavor_name,))
    conn.commit()
    conn.close()
    return redirect("/seasonal_flavors")

# --------- Ingredient Inventory ---------
@app.route("/inventory")
def inventory():
    conn = sqlite3.connect("chocolate_house.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Ingredient_Inventory;")
    ingredients = cursor.fetchall()
    conn.close()
    return render_template("inventory.html", ingredients=ingredients)

@app.route("/add_ingredient", methods=["POST"])
def add_ingredient():
    ingredient_name = request.form["ingredient_name"]
    stock_quantity = request.form["stock_quantity"]
    conn = sqlite3.connect("chocolate_house.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Ingredient_Inventory (ingredient_name, stock_quantity) VALUES (?, ?);", (ingredient_name, stock_quantity))
    conn.commit()
    conn.close()
    return redirect("/inventory")

@app.route("/update_stock", methods=["POST"])
def update_stock():
    ingredient_id = request.form["ingredient_id"]
    stock_quantity = request.form["stock_quantity"]
    conn = sqlite3.connect("chocolate_house.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Ingredient_Inventory SET stock_quantity = ? WHERE id = ?;", (stock_quantity, ingredient_id))
    conn.commit()
    conn.close()
    return redirect("/inventory")

# --------- Customer Feedback ---------
@app.route("/customer_feedback", methods=["GET", "POST"])
def customer_feedback():
    if request.method == "POST":
        name = request.form["name"]
        flavor = request.form["flavor"]
        allergy = request.form["allergy"]
        conn = sqlite3.connect("chocolate_house.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Customer_Feedback (customer_name, flavor_suggestion, allergy_concern) VALUES (?, ?, ?);", (name, flavor, allergy))
        conn.commit()
        conn.close()
        return redirect("/customer_feedback")
    return render_template("customer_feedback.html")

# --------- Admin View for Customer Feedback ---------
@app.route("/admin_feedback")
def admin_feedback():
    conn = sqlite3.connect("chocolate_house.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customer_Feedback;")
    feedbacks = cursor.fetchall()
    conn.close()
    return render_template("admin_feedback.html", feedbacks=feedbacks)

# --------- Run the App ---------
if __name__ == "__main__":
    app.run(debug=True)