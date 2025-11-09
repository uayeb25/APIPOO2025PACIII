from fastapi import FastAPI
from routes.students import router as router_student

app = FastAPI()

app.include_router(router_student)

@app.get("/")
def read_root():
    return {"Hello": "Students!"}



