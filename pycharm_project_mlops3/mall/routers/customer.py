from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from mall.models import Customer, CreateUpdateCustomer, ShowCustomer
from mall.database import get_db
from mall.routers.auth import AuthHandler

router = APIRouter()
auth_handler = AuthHandler()
@router.post("/customers", status_code=status.HTTP_201_CREATED, response_model=ShowCustomer)
async def create_customer(request: CreateUpdateCustomer, username=Depends(auth_handler.auth_wrapper),  session: Session = Depends(get_db)):
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
@router.get("/customers",  status_code=status.HTTP_200_OK, response_model=List[ShowCustomer])
async def get_all(username=Depends(auth_handler.auth_wrapper), session: Session = Depends(get_db)):
    customers = session.exec(
        select(Customer)).all()
    return customers

# Get customer by id
@router.get("/customers/{id}")
async def get_by_id(id: int, username=Depends(auth_handler.auth_wrapper), session: Session = Depends(get_db)):
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
async def delete_customer(id: int, username=Depends(auth_handler.auth_wrapper), session: Session = Depends(get_db)):
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
async def update_customer(id: int, request: CreateUpdateCustomer, username=Depends(auth_handler.auth_wrapper), session: Session = Depends(get_db)):
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