# Contributing to Billing Engine

Thanks for your interest in contributing!  
This project is a backend‑only usage‑based billing engine built with FastAPI, SQLAlchemy, Redis, and RQ.  
Contributions of all kinds are welcome — bug fixes, improvements, documentation, or new features.

---

## 🚀 Getting Started

### Fork the repository  
Click “Fork” at the top of the GitHub page.

### Clone your fork
```
git clone https://github.com/<your-username>/billing-engine.git
cd billing-engine
```

### Create a virtual environment
```
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 4. Install dependencies
```
pip install -r requirements.txt
```

### 5. Start the development server 
``` 
uvicorn main:app --reload
```

### 6. Start Redis + RQ worker
```
redis-server
rq worker
```

---

## 🧪 Running Tests (if tests are added later)
```
pytest
```

---

## 📦 Submitting a Pull Request

### Create a new branch
``` 
git checkout -b feature/my-new-feature
```

### Make your changes  
- Keep code clean and modular  
- Follow existing patterns (routers → services → models)

### Commit with a clear message 
```
git commit -m "Add invoice filtering endpoint"
```

### Push your branch 
```
git push origin feature/my-new-feature
```

### Open a Pull Request  
- Describe what you changed  
- Reference any related issues  
- Include screenshots or examples if relevant  

---

## 🧹 Code Style

- Use **Black** for formatting  
- Keep functions small and focused  
- Follow FastAPI best practices  
- Keep routers thin — business logic belongs in `services/`

---

## ❤️ Thank You

Your contributions help improve the project and make it more useful for others.  
Whether it's a typo fix or a new feature — it’s appreciated!