from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/data")
def get_csv():
    # Replace 'data.csv' with your actual CSV file path
    return FileResponse("data.csv", media_type="text/csv", filename="data.csv")
