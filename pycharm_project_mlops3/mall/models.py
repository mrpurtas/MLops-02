from sqlmodel import SQLModel, Field
from typing import Optional


class Customer(SQLModel, table=True):
    CustomerID: Optional[int] = Field(default=None, primary_key=True)
    Gender: str
    Age: Optional[int]
    AnnualIncome: float
    SpendingScore: int

class CreateUpdateCustomer(SQLModel):
    Gender: Optional[str]
    Age: Optional[int]
    AnnualIncome: Optional[float]
    SpendingScore: Optional[int]