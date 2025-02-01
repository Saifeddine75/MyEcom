import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
import models.models
from routers import user, auth
from fastapi.openapi.utils import get_openapi

app = FastAPI()

# Include the routers
app.include_router(user.router)
app.include_router(auth.router)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


app.openapi_schema = app.openapi()
app.openapi_schema["components"]["securitySchemes"] = {
    "OAuth2PasswordBearer": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }
}

models.models.Base.metadata.create_all(bind=engine)

memory_db = {"products": []}

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"🧐 Requête reçue: {request.method} {request.url}")
    print(f"🛑 Headers: {request.headers}")
    response = await call_next(request)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)