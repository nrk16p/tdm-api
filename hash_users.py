from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import SessionLocal
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db: Session = SessionLocal()
users = db.query(User).all()

for user in users:
    if not user.hashed_password.startswith("$2b$"):
        user.hashed_password = pwd_context.hash(user.hashed_password)

db.commit()
db.close()
print("✅ All user passwords hashed.")
