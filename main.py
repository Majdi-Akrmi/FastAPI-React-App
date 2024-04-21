from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import supplier_pydantic, supplier_pydanticIn, Supplier

app = FastAPI(title="FastAPI-React")

@app.get('/')
def get_msg():
    return {"msg" : "Go to /docs for the API Documentation"}

# Create a supplier
@app.post('/supplier')
async def add_supplier(supplier_info: supplier_pydanticIn): # type: ignore
    supplier_obj = await Supplier.create(**supplier_info.dict(exclude_unset=True))
    res = await supplier_pydantic.from_tortoise_orm(supplier_obj)
    return {"status": "OK", "data": res}

# Get all supplier
@app.get('/supplier')
async def get_all_suppliers():
    res = await supplier_pydantic.from_queryset(Supplier.all())
    return {"status": "OK", "data": res}

# Get a specific supplier
@app.get('/supplier/{supplier_id}')
async def get_specific_supplier(supplier_id: int):
    res = await supplier_pydantic.from_queryset_single(Supplier.get(id=supplier_id))
    return {"status": "OK", "data": res}

# Update a supplier
@app.put('/supplier/{supplier_id}')
async def update_supplier(supplier_id: int, update_info: supplier_pydanticIn): # type: ignore
    supplier = await Supplier.get(id=supplier_id)
    update_info = update_info.dict(exclude_unset=True)
    supplier.name = update_info['name']
    supplier.company = update_info['company']
    supplier.phone = update_info['phone']
    supplier.email = update_info['email']
    await supplier.save()
    res = await supplier_pydantic.from_tortoise_orm(supplier)
    return {"status": "OK", "data": res}
    

register_tortoise(
    app,
    db_url= "sqlite://database.sqlite3",
    modules= {"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)