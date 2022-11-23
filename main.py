import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from db import models
from db.database import engine
from exceptions import StoryException
from router import article, blog_get, blog_post, product, user

app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)


@app.get("/hello")
def index():
    return "Hello World!"


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(status_code=418, content={"detail": exc.name})


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers["duration"] = str(duration)

    return response


# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: StoryException):
#    return PlainTextResponse(str(exc), status_code=400)


models.Base.metadata.create_all(engine)
