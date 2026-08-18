from fastapi import FastAPI

from parking_system.api.routes import router


app = FastAPI(
    title="Smart Parking Management System",
    description="Backend API for managing vehicles, parking slots, fees, and parking history.",
    version="1.0.0",
)


app.include_router(router)