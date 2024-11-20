from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import pandas as pd
import os

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["survey_db"]
collection = db["survey_data"]
print("Databases:", client.list_database_names())  # Lists all databases
print("Collections in survey_db:", db.list_collection_names())

# Define the User class
class User:
    def __init__(self, data):
        self.data = data

    def save_to_csv(self, filename):
        # Convert data to DataFrame and save to CSV
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)

# Survey route
@app.route("/", methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        # Collect form data
        age = request.form.get("age")
        gender = request.form.get("gender")
        total_income = request.form.get("total_income")
        expenses = {
            "utilities": request.form.get("utilities"),
            "entertainment": request.form.get("entertainment"),
            "school_fees": request.form.get("school_fees"),
            "shopping": request.form.get("shopping"),
            "healthcare": request.form.get("healthcare"),
        }

        # Store data in MongoDB
        collection.insert_one({
            "age": age,
            "gender": gender,
            "total_income": total_income,
            "expenses": expenses,
        })
        return redirect("/")
    return render_template("form.html")

# Process route
@app.route("/process")
def process_data():
    try:
        # Fetch data from MongoDB collection
        data = list(collection.find())
        print("Data retrieved from MongoDB:", data)  # Debugging line
        
        # Create User instance with the data
        user = User(data)
        
        # Save data to CSV
        csv_path = "survey_results.csv"
        user.save_to_csv(csv_path)
        print("CSV file saved at:", os.path.abspath(csv_path))  # Debugging line
        return "Data processed and saved to survey_results.csv"
    
    except Exception as e:
        print(f"Error occurred while saving CSV: {e}")
        return f"Error occurred while saving CSV: {e}"

if __name__ == "__main__":
    app.run(debug=True)
