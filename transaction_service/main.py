from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
import urllib.request
import json
from .database import SessionLocal, engine, Base, Transaction

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finans Servisi - İşlemler", description="Para Transferi Yönetimi")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TransactionCreate(BaseModel):
    sender_id: int
    receiver_id: int
    amount: float

# Asenkron Mesaj İletimi (Event-Driven Simülasyonu)
def notify_fraud_service(transaction_id: int, sender_id: int, amount: float):
    url = "http://localhost:8003/api/v1/fraud/check"
    data = json.dumps({
        "transaction_id": transaction_id,
        "sender_id": sender_id,
        "amount": amount
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"Uyarı: Fraud servisine ulaşılamadı - {e}")

@app.post("/api/v1/transactions/send", summary="Para Gönder")
def send_money(transaction: TransactionCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Transfer tutarı 0'dan büyük olmalıdır.")
    
    # İşlem veritabanına "beklemede" (pending) olarak kaydedilir
    new_tx = Transaction(
        sender_id=transaction.sender_id,
        receiver_id=transaction.receiver_id,
        amount=transaction.amount,
        status="pending" 
    )
    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)
    
    # Olayı (Event) arka planda asenkron olarak Fraud servisine ilet
    background_tasks.add_task(notify_fraud_service, new_tx.id, new_tx.sender_id, new_tx.amount)
    
    return {
        "message": "İşlem alındı ve anomali kontrol kuyruğuna gönderildi", 
        "transaction_id": new_tx.id, 
        "status": new_tx.status
    }