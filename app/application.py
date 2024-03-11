from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.user import router as user_router
from .routers.deal import router as deal_router


fastapi_app = FastAPI()

fastapi_app.include_router(user_router, prefix="/api")
fastapi_app.include_router(deal_router, prefix="/api")

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
