from app.main import app  # 👈 นำเข้า FastAPI app
from mangum import Mangum

handler = Mangum(app)  # 👈 แปลง FastAPI → AWS Lambda-compatible
