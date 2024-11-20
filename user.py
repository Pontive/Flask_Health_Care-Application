import csv
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["survey_db"]
collection = db["survey_data"]

class User:
    def save_to_csv(self, filepath):
        """
        Save MongoDB data to a CSV file at the specified location.
        
        Args:
            filepath (str): The full path where the CSV file will be saved.
        """
        # Fetch data from MongoDB collection
        data = list(collection.find())
        
        # Define the CSV fields
        fieldnames = ["age", "gender", "total_income", "utilities", "entertainment", "school_fees", "shopping", "healthcare"]
        
        # Write to CSV
        with open(filepath, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for entry in data:
                row = {
                    "age": entry.get("age", "Not provided"),
                    "gender": entry.get("gender", "Not provided"),
                    "total_income": entry.get("total_income", 0),
                    "utilities": entry["expenses"].get("utilities", 0),
                    "entertainment": entry["expenses"].get("entertainment", 0),
                    "school_fees": entry["expenses"].get("school_fees", 0),
                    "shopping": entry["expenses"].get("shopping", 0),
                    "healthcare": entry["expenses"].get("healthcare", 0),
                }
                writer.writerow(row)

# Specify the file path for the CSV
file_path = r"C:\Users\YD\survey_results.csv"

# Create a User instance and save data to the specified location
user = User()
try:
    user.save_to_csv(file_path)
    print(f"CSV file saved successfully at: {file_path}")
except Exception as e:
    print(f"An error occurred while saving the file: {e}")
