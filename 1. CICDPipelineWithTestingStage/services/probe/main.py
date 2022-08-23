from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="CICD Testing",
    description="CICD Testing",
    version="1.0.0.0",
    servers=[
        {"url": "http://localhost:8000", "description": "Local environment"},
    ],
    # No custom exception handlers are used as of now
    # exception_handlers={
    #     # GISUpdateBaseError: gisupdate_exception_handler,
    #     # RequestValidationError: request_validation_exception_handler,
    # }
)

# # Add custom middlewares that apply to all APIRouter instances
# app.middleware("http")(add_security_headers)

@app.get("/status")
async def status():
    return {"status": "OK", "service": app.title, "version": app.version}




### enable this for testing via swagger-api
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload="0",
        port="8000",
    )
