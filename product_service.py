from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import logging

# --- Konfiguracja logów ---
logging.basicConfig(
    level=logging.INFO,
    format='[PRODUKTY] %(asctime)s %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# --- Inicjalizacja aplikacji ---
app = FastAPI(title="Product Service")

# --- Model produktu ---
class Product(BaseModel):
    id: int
    name: str
    price: float

# --- Dane "na sztywno" ---
PRODUCTS: Dict[int, Product] = {
    1: Product(id=1, name="Laptop", price=4500.00),
    2: Product(id=2, name="Smartphone", price=2500.50),
    3: Product(id=3, name="Monitor", price=800.99),
}

# --- Endpoint: pojedynczy produkt ---
@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    logger.info(f"Otrzymano zapytanie o produkt ID: {product_id}")

    product = PRODUCTS.get(product_id)
    if not product:
        logger.warning(f"Produkt ID {product_id} nie został znaleziony — zwracam 404.")
        raise HTTPException(status_code=404, detail=f"Produkt o ID {product_id} nie istnieje.")

    logger.info(f"Zwracam dane produktu: {product.dict()}")
    return product

# --- Endpoint: lista wszystkich produktów ---
@app.get("/products")
async def list_products():
    logger.info("Otrzymano zapytanie o listę wszystkich produktów.")
    logger.info(f"Zwracam {len(PRODUCTS)} produktów.")
    return list(PRODUCTS.values())

# --- Start logowy ---
@app.on_event("startup")
async def startup_event():
    logger.info("Serwis Produktów uruchomiony na http://localhost:8001")
