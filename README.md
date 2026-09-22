# 🚀 Distributed Event-Driven Financial Transaction & Anomaly Detection Platform

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Dashboard-F46800?style=for-the-badge&logo=grafana&logoColor=white)

Dağıtık mikroservis mimarisi standartlarına uygun olarak geliştirilmiş; kullanıcı kimlik doğrulama, finansal transfer yönetimi ve gerçek zamanlı anomali (fraud) tespiti yapan olay güdümlü (event-driven) finans platformu.

---

## 📐 Sistem Mimarisi
+-----------------------+
                             |   Auth Service        |
                             |   (Port 8001)         |
                             +-----------------------+
+-----------------------+        Asenkron Event         +-----------------------+
|  Transaction Service  | ----------------------------> |    Fraud Service      |
|  (Port 8002)          |   (Background Tasks / PubSub) |    (Port 8003)        |
+-----------------------+                               +-----------------------+
|
v
+-----------------------+
|   Grafana Dashboard   |
|   (Port 3000)         |
+-----------------------+
## ✨ Öne Çıkan Özellikler

* **Auth Service (Port 8001):** JWT (JSON Web Token) ve Bcrypt parola hashleme ile güvenli kimlik doğrulama.
* **Transaction Service (Port 8002):** Bakiye ve transfer işlemlerinin yönetimi, asenkron olay fırlatma (event dispatching) altyapısı.
* **Fraud Service (Port 8003):** Transferleri anlık analiz eden kural tabanlı anomali tespit motoru.
* **Konteynerleştirme:** Tüm servislerin `Docker` ve `Docker Compose` ile tek komutla orkestre edilmesi.
* **Sözleşmeli API Dokümantasyonu:** Her mikroservis için bağımsız Swagger UI entegrasyonu.

---

## 🛠️ Teknolojiler ve Araçlar

| Bileşen | Teknoloji / Kütüphane |
| :--- | :--- |
| **Backend Framework** | Python 3.10, FastAPI |
| **ORM & Veritabanı** | SQLAlchemy, SQLite |
| **Güvenlik** | PyJWT, Passlib (Bcrypt) |
| **Konteynerizasyon** | Docker, Docker Compose |
| **İzleme Panel** | Grafana |

---

## 🚀 Hızlı Başlangıç

Sistemi yerel ortamınızda Docker ile çalıştırmak için:

```bash
# Depoyu klonlayın
git clone [https://github.com/mesutaslan2/financial-microservices.git](https://github.com/mesutaslan2/financial-microservices.git)
cd financial-microservices

# Tüm mikroservisleri ve Grafana'yı başlatın
docker-compose up --build
Servis Erişim Adresleri
🔑 Auth Service: http://localhost:8001/docs

💳 Transaction Service: http://localhost:8002/docs

🚨 Fraud Service: http://localhost:8003/docs

📊 Grafana Dashboard: http://localhost:3000 (Kullanıcı: admin / Şifre: admin)