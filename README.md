# 🕵️‍♂️ TI Collector

**TI Collector** is a Threat Intelligence Dashboard built using Flask and SQLite.  
It allows users to manage Indicators of Compromise (IOCs) like malicious URLs, with login-based access for both Admins and Users.

---

## 🚀 Features

- User Authentication (Login/Register)
- Admin Dashboard for managing IOCs
- SQLite Database Integration
- IOC Search and Display
- Secure Password Hashing

---

## 🧩 Tech Stack

- Python (Flask)
- SQLite
- HTML, CSS (Flask Templates)
- bcrypt for secure passwords

---

## ⚙️ Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/ti-collector.git
   Navigate into the folder:
   ```

bash
Copy code
cd ti-collector
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the app:

bash
Copy code
python app.py
🧑‍💻 Roles
Admin: Can view/add/remove IOCs and manage users.

User: Can search and view IOCs.

📦 Future Enhancements
API Integration with VirusTotal

Real-time IOC Feed

Role-based dashboards

pgsql
Copy code

---

### 📋 `requirements.txt`

Run this command from your virtual environment (where your project runs fine):

```bash
pip freeze > requirements.txt
```
