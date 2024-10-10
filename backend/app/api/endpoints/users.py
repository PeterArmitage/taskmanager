from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
from app.core import security

router = APIRouter()

@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    db_user = crud.user.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.user.create(db=db, obj_in=user)

@router.post("/login", response_model=schemas.Token)
def login_user(user_credentials: schemas.UserLogin, db: Session = Depends(deps.get_db)):
    user = crud.user.authenticate(
        db, email=user_credentials.email, password=user_credentials.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = security.create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout_user():
    # For a simple token-based system, logout is typically handled client-side
    # by removing the token. Here we'll just return a success message.
    return {"detail": "Successfully logged out"}

@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(deps.get_current_user)):
    return current_user