from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db

from .crud import (
    create_expense,
    get_expenses,
    get_expense_by_id,
    update_expense,
    delete_expense
)

from .schemas import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse
)

from .logging_config import setup_logging

from .routes.auth import router as auth_router
from .routes.report import router as report_router
from .auth import get_current_user_id


# Logging


logger = setup_logging()


# FastAPI Application



app = FastAPI(
    title="Expense Tracker API",
    description="Expense Tracker built using FastAPI and PostgreSQL",
    version="1.0.0"
)



# Routers


app.include_router(auth_router)
app.include_router(report_router)




@app.get("/")
def root():
    return {
        "message": "Expense Tracker API is running"
    }

# CREATE EXPENSE


@app.post(
    "/expenses",
    response_model=ExpenseResponse
)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):

    logger.info(
        f"Creating expense for user_id={user_id}, "
        f"title={expense.title}, amount={expense.amount}"
    )

    try:

        result = create_expense(
            db=db,
            expense=expense,
            user_id=user_id
        )

        logger.info(
            f"Expense created successfully. "
            f"expense_id={result.id}, user_id={user_id}"
        )

        return result

    except Exception as e:

        logger.error(
            f"Error creating expense for user_id={user_id}: {str(e)}"
        )

        raise

# GET ALL EXPENSES


@app.get(
    "/expenses",
    response_model=list[ExpenseResponse]
)
def read_expenses(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):

    logger.info(
        f"Fetching expenses for user_id={user_id}"
    )

    try:

        expenses = get_expenses(
            db=db,
            user_id=user_id
        )

        logger.info(
            f"Fetched {len(expenses)} expenses "
            f"for user_id={user_id}"
        )

        return expenses

    except Exception as e:

        logger.error(
            f"Error fetching expenses for user_id={user_id}: {str(e)}"
        )

        raise


# GET EXPENSE BY ID


@app.get(
    "/expenses/{expense_id}",
    response_model=ExpenseResponse
)
def read_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):

    logger.info(
        f"Fetching expense_id={expense_id} "
        f"for user_id={user_id}"
    )

    expense = get_expense_by_id(
        db=db,
        expense_id=expense_id,
        user_id=user_id
    )

    if not expense:

        logger.warning(
            f"Expense not found. "
            f"expense_id={expense_id}, user_id={user_id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense


# UPDATE EXPENSE


@app.put(
    "/expenses/{expense_id}",
    response_model=ExpenseResponse
)
def edit_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):

    logger.info(
        f"Updating expense_id={expense_id} "
        f"for user_id={user_id}"
    )

    expense = update_expense(
        db=db,
        expense_id=expense_id,
        expense_data=expense_data,
        user_id=user_id
    )

    if not expense:

        logger.warning(
            f"Cannot update expense. "
            f"Expense not found. "
            f"expense_id={expense_id}, user_id={user_id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    logger.info(
        f"Expense updated successfully. "
        f"expense_id={expense_id}, user_id={user_id}"
    )

    return expense



# DELETE EXPENSE


@app.delete("/expenses/{expense_id}")
def remove_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):

    logger.info(
        f"Deleting expense_id={expense_id} "
        f"for user_id={user_id}"
    )

    expense = delete_expense(
        db=db,
        expense_id=expense_id,
        user_id=user_id
    )

    if not expense:

        logger.warning(
            f"Cannot delete expense. "
            f"Expense not found. "
            f"expense_id={expense_id}, user_id={user_id}"
        )

        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    logger.info(
        f"Expense deleted successfully. "
        f"expense_id={expense_id}, user_id={user_id}"
    )

    return {
        "message": "Expense deleted successfully"
    }