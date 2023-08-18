from fastapi import APIRouter, Depends
from dependencies import get_current_user

router = APIRouter(prefix="/user",
                   dependencies=[Depends(get_current_user)],
                   tags=["Users"])


@router.get("/")
def users():
    return "You must login to see me"
