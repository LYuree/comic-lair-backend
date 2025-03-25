from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import router

# Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["mail.ru",
                   "http://localhost:3000",
                   "http://localhost",
                   "https://98vxpncx-3000.euw.devtunnels.ms",
                   "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем маршруты
app.include_router(router)
