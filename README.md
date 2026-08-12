# Threat Collector

> **Status: 🔵 Completed / Portfolio Project**

A lightweight web-based **threat intelligence dashboard** for managing and searching Indicators of Compromise (IOCs). Built with **Python, Flask, SQLite, HTML/CSS, and bcrypt-based authentication**.

## Overview

Threat Collector explores the workflow behind a small threat-intelligence system: authenticated users interact with a central IOC repository while administrators can manage indicators and users.

The project is intentionally lightweight and suitable for local security-analysis experimentation rather than production threat intelligence operations.

## Key Features

- User registration and authentication
- Password hashing with bcrypt
- Admin and User roles
- IOC creation, removal and search
- Central SQLite-backed IOC storage
- Admin dashboard
- User-facing IOC lookup
- Server-rendered Flask interface

## Architecture

```text
Browser
   │
   ▼
Flask Web Application
   │
   ├── Authentication / RBAC
   │
   ├── IOC Management
   │
   └── Search
   │
   ▼
SQLite Database
```

## Technology Stack

- Python
- Flask
- SQLite
- HTML / CSS
- bcrypt

## Roles

| Role | Capabilities |
|---|---|
| Admin | Manage users and IOCs, search indicators |
| User | Search and view available IOCs |

## Running Locally

```bash
git clone https://github.com/Balu-Annapureddy/ti-collector.git
cd ti-collector

python -m venv .venv

# Windows
.venv\\Scripts\\activate

# Linux/macOS
# source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Then open the local Flask development server shown in the terminal.

## Security Notes

The project demonstrates authentication and password hashing, but it should **not** be deployed directly to the public internet without additional hardening.

Production improvements would include:

- CSRF protection
- secure session configuration
- stronger authorization boundaries
- input validation and IOC normalization
- audit logging
- secrets/configuration management
- production WSGI deployment
- automated security testing

## Project Status

🔵 **Completed / Portfolio Project**

The current implementation provides the core authenticated IOC-management workflow. Future iterations could add external threat feeds, IOC-type normalization, enrichment providers, API endpoints, analytics, and more advanced analyst workflows.

## Why I Built It

This project was built to explore the practical intersection of **web application development and cybersecurity**, particularly authentication, role-based access, structured threat data, and analyst-facing workflows.

## License

This project is for educational and portfolio purposes.
