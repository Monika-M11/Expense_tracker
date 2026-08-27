from sqlalchemy.orm import Session

from .models import Expense,User

from .schemas import ExpenseCreate, ExpenseUpdate



#Create User
def get_user_by_email(
    db: Session,
    email: str
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user(
    db: Session,
    username: str,
    email: str,
    password_hash: str
):
    new_user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# CREATE
def create_expense(
    db: Session,
    expense: ExpenseCreate,
    user_id: int
):
    new_expense = Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category,
        expense_date=expense.expense_date,
        description=expense.description,
        user_id=user_id
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


# READ - ALL
def get_expenses(
    db: Session,
    user_id: int
):
    return (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .all()
    )


# READ - ONE
def get_expense_by_id(
    db: Session,
    expense_id: int,
    user_id: int
):
    return (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == user_id
        )
        .first()
    )


# UPDATE
def update_expense(
    db: Session,
    expense_id: int,
    expense_data: ExpenseUpdate,
    user_id: int
):
    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == user_id
        )
        .first()
    )

    if not expense:
        return None

    update_data = expense_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)

    return expense


# DELETE
def delete_expense(
    db: Session,
    expense_id: int,
    user_id: int
):
    expense = (
        db.query(Expense)
        .filter(
            Expense.id == expense_id,
            Expense.user_id == user_id
        )
        .first()
    )

    if not expense:
        return None

    db.delete(expense)
    db.commit()

    return expense