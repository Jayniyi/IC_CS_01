# web/app.py
from flask import Flask, render_template, request, flash
from urllib.parse import urlparse
from scanner.crawler import crawl
from scanner.vulns import test_sql_injection, test_xss
from scanner.headers_chek import check_headers   # fixed import name
import traceback
import logging

# --- APP SETUP ---
app = Flask(__name__)
app.secret_key = "dev-secret"  # replace with an environment variable in production

# Simple logger for debug output
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("web.app")


# --- HELPERS ---
def is_vulnerable(result):
    """
    Normalizes different return shapes from test functions:
    - If function returns a dict with 'vulnerable' key, use that.
    - If it returns a bool, use it.
    - Otherwise treat truthy values as vulnerable.
    """
    if isinstance(result, dict):
        if "vulnerable" in result:
            return bool(result.get("vulnerable"))
        # if dict has any content we treat as a positive finding (heuristic)
        return bool(result)
    return bool(result)


@app.after_request
def add_security_headers(response):
    """Add a set of helpful security headers to responses (adjust for your needs)."""
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), camera=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';"
    )
    return response


# --- ROUTES ---
@app.route("/", methods=["GET", "POST"])
def index():
    # Provide an empty dict so the template can reference keys safely
    result = {}
    if request.method == "POST":
        target = request.form.get("url", "").strip()

        # Basic normalization: add scheme if user omitted it
        parsed = urlparse(target)
        if not parsed.scheme:
            target = "http://" + target
            parsed = urlparse(target)

        if parsed.scheme not in ("http", "https"):
            flash("Please enter a valid http or https URL.", "error")
            return render_template("results.html", result={})

        try:
            # --- Crawl safely and ensure we have a concrete list ---
            try:
                raw_links = crawl(target)
                # Convert generator / set / other iterable -> list, handle None
                links = list(raw_links) if raw_links is not None else []
            except Exception as e:
                logger.exception("Crawler error")
                links = []

            logger.info("[DEBUG] Crawled %d links for target %s", len(links), target)
            if len(links) > 0:
                for u in links[:10]:
                    logger.info(" - %s", u)

            # --- Run lightweight checks per URL ---
            url_reports = []
            sql_found = False
            xss_found = False

            for u in links:
                try:
                    sqli_res = test_sql_injection(u)
                    xss_res = test_xss(u)

                    url_report = {
                        "url": u,
                        "sqli": sqli_res,
                        "xss": xss_res,
                        "sqli_bool": is_vulnerable(sqli_res),
                        "xss_bool": is_vulnerable(xss_res),
                    }

                    if url_report["sqli_bool"]:
                        sql_found = True
                    if url_report["xss_bool"]:
                        xss_found = True

                    url_reports.append(url_report)
                except Exception:
                    logger.exception("Error scanning URL: %s", u)
                    url_reports.append({"url": u, "error": "scan_error"})

            # --- Headers check for the target root URL ---
            try:
                headers_report = check_headers(target)
            except Exception:
                logger.exception("Header check error")
                headers_report = {"error": "headers_check_failed"}

            # --- Build final result object for template ---
            result = {
                "target": target,
                "total_links": len(links),
                "sql_vuln": sql_found,
                "xss_vuln": xss_found,
                "headers": headers_report,
                "details": url_reports[:50],  # limit UI rendering
            }

        except Exception as e:
            traceback.print_exc()
            logger.exception("Unhandled error during scan")
            flash(f"An error occurred during scan: {e}", "error")
            result = {}

    # Render the results page (results.html expected in web/templates/)
    return render_template("results.html", result=result)


# --- ENTRYPOINT ---
if __name__ == "__main__":
    # Run from project root with: `py -m web.app`
    app.run(debug=True)
