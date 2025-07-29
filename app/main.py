from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, auth, database
from app.database import SessionLocal
from datetime import date, timedelta, datetime  # ✅ แก้ตรงนี้
from sqlalchemy import desc  # 👈 นำเข้า

models.Base.metadata.create_all(bind=database.engine)

from fastapi import FastAPI

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Login ---
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = auth.create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Authenticated User Info ---
@app.get("/me")
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return {"username": current_user.username, "role": current_user.role}

# --- Admin Only ---
@app.get("/admin-only")
def read_admin_data(current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only!")
    return {"msg": "Welcome, admin"}

# --- Jobs Endpoint ---
@app.get("/jobs")
def get_jobs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    today_date = date.today()
    start_date = today_date - timedelta(days=7)
    end_date = today_date + timedelta(days=7)

    jobs = db.query(models.Job).filter(
        models.Job.date_plan >= start_date,
        models.Job.date_plan <= end_date,
        models.Job.driver_name == current_user.username
    ).all()

    # ✅ Sort แบบ custom: เอาวันนี้ขึ้นก่อน แล้วตามด้วยวันอื่นเรียงมาก → น้อย
    sorted_jobs = sorted(
        jobs,
        key=lambda job: (
            0 if job.date_plan == today_date else 1,   # วันนี้อยู่บนสุด
            -job.date_plan.toordinal()                # วันอื่นเรียง DESC
        )
    )

    return [job.__dict__ for job in sorted_jobs]
