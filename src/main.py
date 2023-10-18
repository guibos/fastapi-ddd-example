from fastapi import FastAPI

from application.use_case.accounts.views import accounts_router

app = FastAPI()
app.include_router(accounts_router)
