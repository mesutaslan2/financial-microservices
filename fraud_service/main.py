from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Finans Servisi - Anomali (Fraud) Kontrolü")

# Transaction servisinden gelecek mesajın şablonu
class TransactionEvent(BaseModel):
    transaction_id: int
    sender_id: int
    amount: float

@app.post("/api/v1/fraud/check", summary="Şüpheli İşlem Kontrolü")
def check_fraud(event: TransactionEvent):
    # Basit bir yapay zeka/kural simülasyonu: 10.000 TL üzeri şüphelidir!
    is_suspicious = event.amount > 10000.0
    
    if is_suspicious:
        print(f"🚨 ALARM! Şüpheli İşlem Yakalandı. İşlem ID: {event.transaction_id}, Tutar: {event.amount}")
        return {"status": "fraud_detected", "action": "account_frozen"}
    else:
        print(f"✅ İşlem Güvenli. İşlem ID: {event.transaction_id}, Tutar: {event.amount}")
        return {"status": "safe", "action": "transaction_approved"}