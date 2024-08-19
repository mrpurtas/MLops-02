from fastapi import FastAPI, Depends, status, HTTPException
from mall.models import Customer, CreateUpdateCustomer
from mall.database import get_db, engine
from sqlmodel import Session, SQLModel, select

app = FastAPI()

# Create Database and Tables on startup
@app.on_event("startup")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/customers", status_code=status.HTTP_201_CREATED)
async def create_customer(request: CreateUpdateCustomer, session: Session = Depends(get_db)):
    new_customer = Customer(
        Gender=request.Gender,
        Age=request.Age,
        AnnualIncome=request.AnnualIncome,
        SpendingScore=request.SpendingScore
    )
    with session:
        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)
        return new_customer

# Get all customers
@app.get("/customers",  status_code=status.HTTP_200_OK)
async def get_all(session: Session = Depends(get_db)):
    customers = session.exec(
        select(Customer)).all()
    return customers

# Get customer by id
@app.get("/customers/{id}")
async def get_by_id(id: int, session: Session = Depends(get_db)):
    statement = select(Customer).where(Customer.CustomerID == id)
    results = session.exec(statement)
    try:
        one_customer = results.one()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Customer {id} has not found.")
    return one_customer