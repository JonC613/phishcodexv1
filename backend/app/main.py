import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.db import init_db
from app.routes import search, shows, comments


def create_app() -> FastAPI:
    app = FastAPI(title="Phish Show Finder")

    origins = [
        os.getenv("CORS_ORIGIN", "http://localhost:5173"),
        "http://localhost",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(search.router)
    app.include_router(shows.router)
    app.include_router(comments.router)

    @app.on_event("startup")
    def on_startup():
        init_db()

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        if isinstance(exc, HTTPException):
            raise exc
        return JSONResponse(status_code=500, content={"detail": str(exc)})

    return app


app = create_app()
