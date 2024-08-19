## Create routers package

## routers/customer.py
- Move customer paths to routers/customer.py
```commandline
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from mall.models import Customer, CreateUpdateCustomer, ShowCustomer
from database import get_db

router = APIRouter()


# Create new customer
@router.post("/customers", status_code=status.HTTP_201_CREATED)
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


@router.get("/customers", status_code=status.HTTP_200_OK, response_model=List[ShowCustomer])
async def get_all(session: Session = Depends(get_db)):
    customers = session.exec(
        select(Customer)).all()
    return customers


# Get customer by id
@router.get("/customers/{id}", status_code=status.HTTP_200_OK, response_model=ShowCustomer)
async def get_by_id(id: int, session: Session = Depends(get_db)):
    with session:
        statement = select(Customer).where(Customer.CustomerID == id)
        results = session.exec(statement)
        try:
            one_customer = results.one()
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Customer {id} has not found.")
        return one_customer


# Delete a customer by id
@router.delete("/customer/{id}", status_code=status.HTTP_200_OK)
async def delete_customer(id: int, session: Session = Depends(get_db)):
    with session:
        one_customer = session.get(Customer, id)
        if not one_customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Customer with {id} has not found.")
        session.delete(one_customer)
        session.commit()
        return {"ok": True}


# Update customer
@router.put("/customer/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_customer(id: int, request: CreateUpdateCustomer, session: Session = Depends(get_db)):
    with session:
        one_customer = session.get(Customer, id)
        if not one_customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Customer with {id} has not found.")
        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(one_customer, key, value)
        session.add(one_customer)
        session.commit()
        session.refresh(one_customer)
        return one_customer
```

## main.py
```
from fastapi import FastAPI
from database import create_db_and_tables
from mall.routers import customer, user

app = FastAPI()

app.include_router(customer.router)

# Create Database and Tables on startup
@app.on_event("startup")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```

## Restart uvicorn 
` ... mall.main:app ...`
