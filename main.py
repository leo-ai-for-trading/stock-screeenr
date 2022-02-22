import imp
from pyexpat import model
import re
from urllib import request
import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel 
from models import Stock
#/.run

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")
class StockRequest(BaseModel):
    symbol: str

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def home(request: Request):
    '''
    display the stock screener homepage
    '''
    return templates.TemplateResponse("home.html",{
        "request": request
    })
@app.post("/stock")
#add stock to a db
def create_stock(stock_request: StockRequest, db: Session = Depends(get_db)):
    '''
    created a stock and store it in the databases
    '''
    stock = Stock
    stock.symbol = stock_request.symbol
    db.add(stock)
    return {
        "code": "success",
        "message": "stock created"
    }
