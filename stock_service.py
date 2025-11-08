from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import httpx
import os
import logging

# --- Konfiguracja logów ---
logging.basicConfig(
    level=logging.INFO,
    format='[MAGAZYN] %(asctime)s %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# --- Inicjalizacja aplikacji ---
app = FastAPI(title="Stock Service")

# --- Model stanu magazynowego ---
class Stock(BaseModel):
    productId: int
    quantity: int

# --- Dane "na sztywno" ---
STOCKS: Dict[int, Stock] = {
    1: Stock(productId=1, quantity=15),
    2: Stock(productId=2, quantity=0),
    3: Stock(productId=3, quantity=7),
}

# --- Adres serwisu produktów ---
PRODUCT_SERVICE_URL = os.environ.get("PRODUCT_SERVICE_URL", "http://localhost:8001")

@app.get("/stock/{product_id}", response_model=Stock)
async def get_stock(product_id: int):
    logger.info(f"Otrzymano zapytanie o stan magazynowy produktu ID: {product_id}")
    product_url = f"{PRODUCT_SERVICE_URL}/products/{product_id}"
    logger.info(f"Nawiązywanie połączenia z Serwisem Produktów pod adresem: {product_url}")

    # 1️⃣ Sprawdzenie czy produkt istnieje w serwisie produktów
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            resp = await client.get(product_url)
        except httpx.RequestError as e:
            logger.error(f"Błąd podczas komunikacji z Serwisem Produktów: {e}")
            raise HTTPException(status_code=503, detail=f"Nie można połączyć się z Serwisem Produktów: {e}") from e

    # 2️⃣ Obsługa statusów
    if resp.status_code == 404:
        logger.warning(f"Produkt ID {product_id} nie istnieje w Serwisie Produktów — zwracam 404.")
        detail = resp.json().get("detail") if "application/json" in resp.headers.get("content-type", "") else None
        raise HTTPException(status_code=404, detail=detail or f"Produkt o ID {product_id} nie istnieje.")

    if resp.status_code >= 400:
        logger.error(f"Serwis Produktów zwrócił błąd {resp.status_code}.")
        raise HTTPException(status_code=502, detail=f"Błąd z Serwisu Produktów ({resp.status_code}).")

    logger.info(f"Serwis Produktów potwierdził istnienie produktu ID {product_id}.")

    # 3️⃣ Pobranie stanu magazynowego
    stock = STOCKS.get(product_id)
    if not stock:
        logger.warning(f"Brak wpisu magazynowego dla produktu ID {product_id}. Zwracam quantity=0.")
        return Stock(productId=product_id, quantity=0)

    logger.info(f"Zwracam stan magazynowy: {stock.dict()}")
    return stock

# --- Start logowy ---
@app.on_event("startup")
async def startup_event():
    logger.info("Serwis Magazynowy uruchomiony na http://localhost:8002")
    logger.info(f"Adres Serwisu Produktów: {PRODUCT_SERVICE_URL}")
