# Marketplace API Backend 🚀

This is the standalone backend API engine for our marketplace application, built using Python and Django REST Framework (DRF). It handles user accounts, handles shopping cart updates, and registers order to serve clean data to a decoupled frontend application.

---

## 🛠️ Built With
* **Language:** Python 
* **Framework:** Django
* **API Toolkit:** Django REST Framework (DRF)
* **Security:** SimpleJWT (JSON Web Tokens)
* **Cross-Origin Bridge:** django-cors-headers
* **Image Processor:** Pillow

---

## 📦 Main Features Completed
- **Secure Authentication:** User signup and login routes using secure JWT tokens.
- **Cart Management:** Saves and tracks shopping cart items and updates quantities for logged-in users.
- **Address Book:** Stores customer delivery profiles with dynamic regional checks.
- **Order Placement:** Receives checkout options (UPI, Card, COD), saves order history records, and automatically clears the user's cart on success.

---

## ⚡ Local Setup Instructions

### 1. Set Up Virtual Environment
Clone this project to your computer, open your terminal inside the root backend folder, and run:
```bash
# Create a fresh virtual environment
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on Mac / Linux:
source venv/bin/activate
```

### 2. Install Packages
Once your virtual environment is active, run this command to download all requirements:
```bash
pip install -r requirements.txt
```

### . Run the Server
Build your database tables and start up your development server:
```bash
python manage.py runserver
```
Your backend API is now running locally!
