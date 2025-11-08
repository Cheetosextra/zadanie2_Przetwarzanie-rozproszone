# zadanie2_Przetwarzanie-rozproszone
Przetwarzanie rozproszone Zadanie 2 na wsb
# System Rozproszony z REST API

## Opis projektu

Projekt składa się z dwóch niezależnych mikroserwisów komunikujących się między sobą:

1. **Serwis Produktów** (`product_service.py`)  
   - Endpointy:  
     - `GET /products` — lista wszystkich produktów  
     - `GET /products/{id}` — informacje o konkretnym produkcie

2. **Serwis Magazynowy** (`stock_service.py`)  
   - Endpoint: `GET /stock/{productId}` — stan magazynowy produktu  
   - Weryfikuje istnienie produktu w Serwisie Produktów

---

## Wymagania

- Python 3.10+  
- Pakiety:
```bash
pip install -r requirements.txt

## Uruchomienie w katologu systemu

W jednym oknie CMD/PowerShell uruchom 
uvicorn product_service:app --host 127.0.0.1 --port 8001 --reload --log-level info

W drugim oknie CMD/PowerShell urchom 
uvicorn stock_service:app --host 127.0.0.1 --port 8002 --reload --log-level info

W osobnym oknie testowanie endPoitow za pomoca 
np. curl http://127.0.0.1:8002/stock/1
