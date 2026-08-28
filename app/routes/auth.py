from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# from fastapi.security import OAuth2PasswordRequestForm



from ..auth import (
    create_access_token,
    hash_password,
    verify_password
)

from ..schemas import (
    UserCreate,
    UserResponse,
    LoginRequest
)

from ..crud import (
    create_user,
    get_user_by_email,
)

from ..database import get_db

from ..schemas import (
    UserCreate,
    UserResponse
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse
)

def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = get_user_by_email(
        db,
        user.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    password_hash = hash_password(
        user.password
    )

    new_user = create_user(
        db=db,
        username=user.user_id,
        email=user.email,
        password_hash=password_hash
    )

    return new_user



@router.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = get_user_by_email(
        db,
        login_data.email
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.username)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }