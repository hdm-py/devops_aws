import logging
import sys
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, status

from db import (
    create_review_db,
    create_user_db,
    delete_user_db,
    get_movie_db,
    get_user_with_reviews_db,
    list_movies_db,
    list_users_db,
    update_user_db,
)
from exceptions import MovieNotFoundError, UserNotFoundError
from schemas import ReviewBase, ReviewOut, UserIn, UserWithReviews
from setup import get_connection

app = FastAPI()

error_logger = logging.getLogger("uvicorn.error")
error_logger.setLevel(logging.DEBUG)

log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(log_formatter)
error_logger.addHandler(stream_handler)

file_handler = logging.FileHandler("app.log", mode="a")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_formatter)
error_logger.addHandler(file_handler)

# -------------------------
# 2) Configure uvicorn.access (for request logs)
# -------------------------
access_logger = logging.getLogger("uvicorn.access")
access_logger.setLevel(logging.INFO)

# reuse the same handlers so logs go to both console & file
access_logger.addHandler(stream_handler)
access_logger.addHandler(file_handler)

# You can also log an info to see if it's working:
access_logger.info("Configured uvicorn.access logger")

error_logger.info("API is starting up")


# This is an endpoint, it doesn't do anything special, but it's an endpoint
@app.get("/status")
def get_status():
    return {"message": "Hello world"}


# list endpoints
@app.get("/movies", status_code=200)
def get_movies():
    """
    Returns a list of movies
    Unfortunately, no limit supported. sry.
    """
    con = get_connection()
    return list_movies_db(con)


@app.get("/movie/{movie_id}")
def get_movie(movie_id: int):
    con = get_connection()
    try:
        movie = get_movie_db(con, movie_id)
        return movie
    except MovieNotFoundError:
        raise HTTPException(detail="Movie not found", status_code=404)


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserIn, con: Any = Depends(get_connection)):
    result = create_user_db(con, user.username)
    if result:
        return {"message": f"User created successfully with id: {result['id']}"}
    raise HTTPException(detail="User not created properly")


@app.get("/users", status_code=200)
def get_users():
    """
    Returns a list of_users
    Unfortunately, no limit supported. sry.
    """
    con = get_connection()
    return list_users_db(con)


@app.delete("/user/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, con: Any = Depends(get_connection)):
    try:
        delete_user_db(con, user_id)
        return {"message": "User deleted"}
    except UserNotFoundError:
        raise HTTPException(
            detail="User not found", status_code=status.HTTP_404_NOT_FOUND
        )


@app.put("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_user(user_id: int, user: UserIn, con: Any = Depends(get_connection)):
    try:
        update_user_db(con, user_id, username=user.username)
        return {"message": "User deleted"}
    except UserNotFoundError:
        raise HTTPException(
            detail="User not found", status_code=status.HTTP_404_NOT_FOUND
        )


@app.post("/reviews", status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewBase, con: Any = Depends(get_connection)):
    result = create_review_db(con, review)
    if result:
        return {"message": "Review created successfully", "id": result["id"]}
    raise HTTPException(detail="Review not created", status_code=400)
