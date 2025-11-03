from flask import Blueprint, render_template, request
from scanner.crawler import crawl

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
    # logic for scanning
    return render_template("results.html")
