import os
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

# Construct the absolute file path for the CSV
csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'recipes.csv')

# Check if the file exists (for debugging)
if not os.path.exists(csv_file_path):
    print(f"CSV file not found at {csv_file_path}")
else:
    recipes_df = pd.read_csv(csv_file_path)  # Read the CSV file using pandas

@app.get("/data")
def get_csv():
    # Return the local CSV file using FastAPI's FileResponse
    if os.path.exists(csv_file_path):
        return FileResponse(csv_file_path, media_type="text/csv", filename="recipes.csv")
    else:
        return {"error": "CSV file not found"}
