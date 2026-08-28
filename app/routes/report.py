from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user_id
from ..crud import get_expense_report
from ..schemas import ReportResponse


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get(
    "/summary",
    response_model=ReportResponse
)
def expense_report(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    report = get_expense_report(
        db=db,
        user_id=user_id
    )

    return report