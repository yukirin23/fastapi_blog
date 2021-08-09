from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# decorator get--> operation, ('/') --> path
@app.get('/blog')
# function
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    # only get 10 published blogs
    if published:
        return {'data': f'{limit} published blog list from database'}
    else:
        return {'data': f'{limit} blog list from database'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}


@app.get('/blog/{id}')
def show(id: int):
    # fetch blog with id = id
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id, limit=10):
    # fetch comment of blog with id = id
    return {'data': {'1', '2'}}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
def create_blog(blog: Blog):
    return {'data': f'blog is created with title as {blog.title}'}
