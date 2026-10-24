from fastapi import FastAPI

app = FastAPI(
    title="Expense Intelligence API",
    description="Track expenses and get spending insights.",
    version="0.1.0",
)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
