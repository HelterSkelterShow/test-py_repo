from fastapi import FastAPI, Body, Path
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.operations.router import router as router_operation
from src.tasks.router import router as router_tasks
from src.pages.router import router as router_pages
from src.chat.router import router as router_chat
from src.items.router import router as router_items


app = FastAPI(
    title="Trading App"
)

app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)

app.include_router(router_tasks)

app.include_router(router_pages)

app.include_router(router_chat)

app.include_router(router_items)

@app.on_event("startup")    #настройки для редиса при запуске приложения
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")




# fake_users = [
#     {"id" : 1, "role" : "admin", "name" : "Bob"},
#     {"id" : 2, "role" : "investor", "name" : "John"},
#     {"id" : 3, "role" : "trader", "name" : "Nick", "degree": [
#         {"id" : 1, "created_at" : "2020-01-01T00:00:00", "type_degree" : "newbie"}
#     ]}
# ]

# class DegreeType(Enum):
#     newbie = "newbie"
#     expert = "expert"
#
# class Degree(BaseModel):
#     id : int
#     created_at : datetime
#     type_degree : DegreeType
#
# class User(BaseModel):
#     id : int
#     role : str
#     name : str
#     degree : Optional[List[Degree]] = []
#
#
# @app.get("/users/{userId}", response_model=List[User])
# def hello(userId : int):
#     return [user for user in fake_users if userId == user.get("id")]
#
# fake_trades = [
#     {"id" : 1, "user_id" : 2, "price" : 125, "side" : "buy"},
#     {"id" : 2, "user_id" : 3, "price" : 123, "side" : "sell"}
# ]
#
# class Trade(BaseModel):
#     id: int
#     user_id: int
#     currency: str = Field(ge=5)
#     side: str
#     price: float = Field(ge=0)
#     amount: float
#
#
# @app.post("/trades")
# def add_trades(trades : List[Trade]):
#     fake_trades.extend(trades)
#     return {"state" : 200, "data" : fake_trades}
