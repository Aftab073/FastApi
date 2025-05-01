from fastapi import FastAPI, Depends
from . import schemas, models
from .database import engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext
app = FastAPI()

models.Base.metadata.create_all(engine)

@app.post('/blog')
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog/{id}')
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        return {"error": "Blog not found"}
    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}


    
@app.get('/blog')
def get_blogs(id, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blogs

@app.put('/blog/{id}')
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        return {"error": "Blog not found"}
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return blog

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated= 'auto')

@app.post('/user')
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashedPassword = pwd_cxt.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashedPassword )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user