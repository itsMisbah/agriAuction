# 🌾 AgriAuction — Direct Farmer-to-Buyer Auction Platform

## 📖 Problem Statement

In Pakistan, farmers receive only **30–40%** of the final market price for their crops because of multiple middlemen (Aarhti system). AgriAuction removes this layer entirely — farmers list their crops with a base price, buyers bid competitively, and the highest bidder wins directly.

---

## ✨ Key Features

- **Role-based registration** — users select Farmer or Buyer role before signing up
- **Role Base Access Management** Only farmer can list Crops and edit and only buyer can bit crops and check marketplace
- **Google OAuth2 & JWT** social login via `django-allauth` and implement JWT Authentication
- **Automation expiry logic for crop** — apply automation for winner announce and expire the crop
- **Validation in bidding** — validat bid to ensure it must be greater then current highest bid


## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Django 4.2 |
| API | Django REST Framework, SimpleJWT |
| Auth | django-allauth (Google OAuth2), Custom Signals |
| Database | PostgreSQL (production), SQLite (development) |
| Frontend | HTML, Bootstrap 5, Bootstrap Icons |
| Deployment | Render |
| API Docs | drf-spectacular (Swagger UI) |


## ⚙️ Local Setup

### Prerequisites
- Python 3.11+
- PostgreSQL
- Git

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/itsMisbah/agriAuction.git
cd agri-auction

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env
# Fill in your values (see Environment Variables section)

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

**Live Demo**: [https://https://agrifarma.up.railway.app](https://https://agrifarma.up.railway.app)

## 👩‍💻 Author

Built by **[Misbah Shahzadi]**
- GitHub: [@itsMisbah](https://github.com/itsMisbah)
- LinkedIn: [linkedin.com/in/misbah-shahzadi](https://linkedin.com/in/misbah-shahzadi)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
