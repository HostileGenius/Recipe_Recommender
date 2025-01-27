import os
csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/recipes.csv')
recipes_df = pd.read_csv(csv_file_path)
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/data")
def get_csv():
    # Replace 'data.csv' with your actual CSV file path
    return FileResponse("data.csv", media_type="text/csv", filename="https://github.com/HostileGenius/recipes/Recipes.csv")
