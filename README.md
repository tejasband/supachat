# 🚀 SupaChat – AI-Powered Analytics Platform

SupaChat is a full-stack conversational analytics application that converts natural language queries into structured insights and visualizes them using charts.

This project demonstrates a complete **DevOps lifecycle** including containerization, CI/CD automation, monitoring, and logging.

---

## 🔥 Features
- Natural language → analytics queries
- Dynamic chart generation (line, bar, table)
- Full-stack architecture (FastAPI + Next.js)
- Dockerized microservices
- CI/CD pipeline using GitHub Actions
- Monitoring with Prometheus & Grafana
- Centralized logging with Loki

---

## 🏗️ Architecture

### 🔹 Tech Stack
- **Frontend**: Next.js
- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Reverse Proxy**: Nginx
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Cloud**: AWS EC2

---

### 🔹 Monitoring Stack
- Prometheus → metrics collection  
- Grafana → dashboards & visualization  
- Node Exporter → system metrics  

---

### 🔹 Logging Stack
- Loki → log aggregation  
- Promtail → log collection  

---

## 🌐 Live Application
👉 http://13.126.242.36

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/<your-username>/supachat.git
cd supachat
docker-compose up --build