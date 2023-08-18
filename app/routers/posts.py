from fastapi import APIRouter, Depends
from dependencies import get_current_user

router = APIRouter(prefix="/posts",
                   dependencies=[Depends(get_current_user)],
                   tags=["Posts"])

@router.get("/")
def posts():
    return "You need to log in to see me"
