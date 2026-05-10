import os
import pandas as pd
from fastapi import APIRouter
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

DATABASE_URL = os.getenv("DATABASE_URL")

TABLES_AND_FILES = {
    "user": "user.csv",
    "activity_tracker_dataset": "activity_tracker_dataset_cleaned.csv",
    "leave_dataset": "leave_dataset_cleaned.csv",
    "onboarding_dataset": "onboarding_dataset.csv",
    "performance_dataset": "performance_dataset.csv",
    "rewards_dataset": "rewards_dataset.csv",
    "vibemeter_dataset": "vibemeter_dataset.csv",
}

@router.get("/run")
async def seed_database():
    try:
        data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data")
        engine = create_engine(DATABASE_URL)
        results = []
        with engine.connect() as conn:
            for table_name, file_path in TABLES_AND_FILES.items():
                full_path = os.path.join(data_dir, file_path)
                if not os.path.exists(full_path):
                    results.append(f"SKIP: {file_path} not found")
                    continue
                df = pd.read_csv(full_path)
                df.columns = map(str.lower, df.columns)
                df.to_sql(table_name, con=conn, if_exists='append', index=False)
                conn.commit()
                results.append(f"OK: {table_name} - {len(df)} rows")
        return {"status": "success", "results": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}