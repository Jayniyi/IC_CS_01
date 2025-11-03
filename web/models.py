from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ScanResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(255))
    sql_vuln = db.Column(db.Boolean)
    xss_vuln = db.Column(db.Boolean)
    total_links = db.Column(db.Integer)
    date_scanned = db.Column(db.DateTime, default=db.func.now())
