from routers.users import user_router
from utils import config
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise


app = FastAPI(title="ADA 2022 - Assignment 1 - Users MicroService", docs_url="/docs")
app.include_router(user_router)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex="^https?:\/\/.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


register_tortoise(
    app, db_url=config.DB_URL,
    modules={"models": ["models"]},
    generate_schemas=True, add_exception_handlers=True)
