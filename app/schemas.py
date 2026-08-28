from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field



#User creation
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: str
    password: str = Field(..., min_length=6)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str


class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    amount: Decimal = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=100)
    expense_date: date
    description: str | None = None


class ExpenseUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=150)
    amount: Decimal | None = Field(None, gt=0)
    category: str | None = Field(None, min_length=1, max_length=100)
    expense_date: date | None = None
    description: str | None = None


class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: Decimal
    category: str
    expense_date: date
    description: str | None = None
    user_id: int

    class Config:
        from_attributes = True


class ReportResponse(BaseModel):
    user_id: int
    total_expense: Decimal
    expense_count: int