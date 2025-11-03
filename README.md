A lightweight Flask-based Web Application Security Scanner that automatically tests websites for common vulnerabilities like SQL Injection (SQLi) and Cross-Site Scripting (XSS), and checks essential security headers.

Built by Obasan Joseph, this tool provides a modern dashboard powered by TailwindCSS with optional Chart.js visualizations and a persistent scan history using SQLite.

🚀 Features

✅ Crawl target websites and collect internal links

✅ Detect common SQL Injection (SQLi) and Cross-Site Scripting (XSS) vulnerabilities

✅ Check for missing security headers (CSP, HSTS, X-Frame-Options, etc.)

✅ Store scan history with timestamp in SQLite

✅ View scan results in a clean TailwindCSS dashboard

✅ Extendable architecture — add new vulnerability modules easily


IC_CS_01/
│
├── web/
│   ├── app.py                 # Flask app (main entry)
│   ├── models.py              # Database models (SQLAlchemy)
│   ├── templates/
│   │   ├── results.html       # Main scan results page
│   │   ├── history.html       # Scan history view
│   │   └── base.html          # Shared layout
│   ├── static/
│   │   └── charts.js          # Chart.js visualization
│   └── scanner_history.db     # SQLite database (auto-created)
│
├── scanner/
│   ├── crawler.py             # Link crawler logic
│   ├── vulns.py               # SQLi & XSS test logic
│   └── headers_chek.py        # Header security checker
│
├── requirements.txt
└── README.md


pip install -r requirements.txt


2️⃣ Set up a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On Mac/Linux


⚠️ Disclaimer

⚡ This tool is for educational and authorized security testing only.
Do not use it to scan websites without proper permission.

🧑‍💻 Author

Obasan Joseph
Frontend Developer | Aspiring Fullstack & Cybersecurity Engineer
🌍 Based in Nigeria
💼 LinkedIn
 | 🖥️ Portfolio : https://obasanjosephportfolio.netlify.app/
# IC_CS_01
