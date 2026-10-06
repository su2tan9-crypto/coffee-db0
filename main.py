from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from db import Base, engine, get_db
from models import Drink

Base.metadata.create_all(bind=engine)
app = FastAPI() 
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home(request: Request, search: str = "", db: Session = Depends(get_db)):
    search = (search or "").strip()

    if search:
        drinks = db.query(Drink).filter(Drink.name.ilike(f"%{search}%")).all()
    else:
        drinks = db.query(Drink).all()    

    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={"drinks": drinks, "search": search}
)
 


@app.get("/drink/{drink_id}")
def item(request: Request, drink_id: int, db: Session = Depends(get_db)):
    drink = db.query(Drink).filter(Drink.id == drink_id).first()
    if not drink:
        raise HTTPException(status_code=404, detail="not found")
    return templates.TemplateResponse(
    request=request,
    name="buy.html",
    context={"drink": drink}
)


@app.post("/drink")
def create(name: str = Form(...), image: str = Form(...), price: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    new_c = Drink(name=name, image=image, price=price, description=description)
    db.add(new_c)
    db.commit()
    db.refresh(new_c)
    return RedirectResponse("/", status_code=303)


@app.delete("/drink/{drink_id}")
def delete(drink_id: int, db: Session = Depends(get_db)):
    drink = db.query(Drink).filter(Drink.id == drink_id).first()
    if not drink:
        raise HTTPException(status_code=404, detail="not found")
    
    db.delete(drink)
    db.commit()
    return {"message": "delete"}
