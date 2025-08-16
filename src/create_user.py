import sys
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import User, Base
from .auth import get_password_hash

def create_user(db: Session, username: str, password: str):
    db_user = User(username=username, hashed_password=get_password_hash(password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f"User '{username}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m src.create_user <username> <password>")
        sys.exit(1)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    create_user(db=db, username=sys.argv[1], password=sys.argv[2])
    db.close()
