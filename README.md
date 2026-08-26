# Decorators + Employee Demo (Flask)

This is a minimal Flask app demonstrating:
- decorators with `functools.wraps` (log, timer),
- an authorization decorator `require_admin`,
- a simple `Employee` class using `@property`,
- a small HTML/CSS/JS front end to interact with the API.

Structure
- app.py
- templates/index.html
- static/style.css
- static/script.js
- requirements.txt

Quick start
1. Create a virtual environment (recommended):
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\\Scripts\\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Run the app:
   flask --app app.py run
   or
   python app.py

4. Open http://127.0.0.1:5000 in your browser and try the buttons.

Notes
- /calculate is decorated with both @log and @timer; server console will show logs and timing.
- /dashboard requires `?user=admin` (or header `X-User: admin`) to return the welcome message.
- /employee shows use of the Employee class and property access.
- /greet demonstrates that wraps preserved the original function's `__name__` and `__doc__`.

Example cURL
- Calculate:
  curl -X POST -H "Content-Type: application/json" -d '{"sleep":0.3}' http://127.0.0.1:5000/calculate

- Dashboard (allowed):
  curl "http://127.0.0.1:5000/dashboard?user=admin"

- Dashboard (denied):
  curl "http://127.0.0.1:5000/dashboard?user=guest"

- Employee:
  curl "http://127.0.0.1:5000/employee?salary=75000"
