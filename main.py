import uvicorn
from fastapi import FastAPI
from routes.students import router as router_student
from routes.schools import router as router_schools


app = FastAPI()

@app.get("/")
def read_root():
    return {
        "Hello": "Students!"
        , "version": "0.1.0"
    }


app.include_router(router_schools)
app.include_router(router_student)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
