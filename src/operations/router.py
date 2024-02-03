import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)

@router.get("/long_operation")
@cache(expire=60) #кэшируем ответ с даненой сигнатурой на 60  секунд. Если сигнатура меняется, функция пересчитывается!
def get_long_op():
    time.sleep(2)
    return "qweqweqweqweqweqweqweqweqweqwe"

@router.get("/")
async def get_specific_operations(operation_type : str, session : AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {"status":"success",
                "data":result.all(),
                "details":None
                }
    except:
        raise HTTPException(500, detail={
                "status" : "error",
                "data":None,
                "details":None
                })

@router.post("/")
async def add_specific_operations(new_operation : OperationCreate, session : AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(operation).values(**new_operation.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status" : "success",
                "data" : None,
                "details" : None
                }
    except:
        raise HTTPException(500, detail={
                "status": "error",
                "data": None,
                "details": None
               })

@router.put("/")
async def edit_specific_operation(new_operation : OperationCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = update(operation).where(operation.c.id == new_operation.id).values(**new_operation.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status":"success",
                "data": new_operation,
                "details":None
                }
    except:
        raise HTTPException(500, detail={
             "status": "error",
             "data": None,
             "details": None
         })

@router.delete("/{id}")
async def del_specific_operation(id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = delete(operation).where(operation.c.id == id)
        await session.execute(stmt)
        await session.commit()
        return {"status":"success",
                "data":None,
                "details":None
                }
    except:
        raise HTTPException(status_code=500, detail={
             "status": "error",
             "data": None,
             "details": None
         })
