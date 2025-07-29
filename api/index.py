# ✅ api/index.py
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def root():
    return {"msg": "Deployed via Vercel works!"}

handler = Mangum(app)