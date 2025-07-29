from sqlalchemy import Column, String, Integer, Date
from app.database import Base

# ── User Model ───────────────────────────────────────
class User(Base):
    __tablename__ = "userdata"
    __table_args__ = {'schema': 'fleetdata'}  # 👈 ระบุ schema ชัดเจน

    username = Column(String, primary_key=True, index=True)
    hashed_password = Column("password", String)  # 👈 map จาก column password จริงใน DB
    role = Column(String)

# ── Job Model ────────────────────────────────────────
class Job(Base):
    __tablename__ = "jobdata"
    __table_args__ = {"schema": "fleetdata"}

    load_id = Column(String, primary_key=True, index=True)
    date_plan = Column(Date)
    h_plate = Column(String)
    t_plate = Column(String)
    fuel_type = Column(String)
    height = Column(String)
    weight = Column(String)
    driver_name = Column(String)
    phone = Column(String)
    status = Column(String)
    remark = Column(String)
    locat_recive = Column(String)
    date_recive = Column(Date)
    locat_deliver = Column(String)
    date_deliver = Column(Date)
    pallet_type = Column(String)
    pallet_plan = Column(Integer)
    unload_cost = Column(String)
