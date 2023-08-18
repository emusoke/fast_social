from fastapi import HTTPException, Depends
from starlette.requests import Request

async def get_current_user(request: Request):
    user = request.session.get('user')
    if user is None:
        raise HTTPException(status_code=403, detail="Unauthenticated")
