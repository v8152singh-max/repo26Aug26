from flask import Flask, render_template, request, jsonify
from functools import wraps
import time

app = Flask(__name__)


def log(func):
    """Decorator that logs a function call (shows how wraps preserves metadata)."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__} args={args} kwargs={kwargs}")
        return func(*args, **kwargs)
    return wrapper


def timer(func):
    """Decorator that measures elapsed time for a function call."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            print(f"[TIMER] {func.__name__} executed in {elapsed:.4f} sec")
    return wrapper


def require_admin(func):
    """
    Simple decorator that allows the call only if user == 'admin'.
    It checks (in order):
      1. request.args['user'] (query parameter)
      2. X-User header
      3. first positional arg (if provided)
    Returns a 403 JSON response when not allowed.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = None
        # Prefer query param or header when available (for Flask routes)
        try:
            user = request.args.get('user') or request.headers.get('X-User')
        except RuntimeError:
            # No active request context; fall back to positional args
            pass
        if not user and args:
            user = args[0]
        if user != "admin":
            return jsonify({"error": "Access Denied"}), 403
        return func(*args, **kwargs)
    return wrapper


class Employee:
    """Simple Employee class demonstrating a read-only property for salary."""
    def __init__(self, salary: int):
        self._salary = salary

    @property
    def salary(self) -> int:
        return self._salary


# Example function demonstrating @wraps preserving __name__ and __doc__
@log
def greet():
    """This is the greet function (demo of wraps)."""
    return "Hello from greet()"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
@log
@timer
def calculate():
    """
    Simulates some work. Accepts JSON payload: {"sleep": float_seconds}
    The route is decorated with @log and @timer so you'll see both behaviors.
    """
    payload = request.get_json(silent=True) or {}
    sleep_time = float(payload.get("sleep", 0.2))
    # simulate work
    time.sleep(sleep_time)
    return jsonify({"result": "done", "sleep": sleep_time})


@app.route("/dashboard")
@require_admin
def dashboard():
    """Admin-only endpoint (use ?user=admin or header X-User: admin)."""
    return jsonify({"message": "Welcome to Dashboard"})


@app.route("/employee")
def employee_route():
    """
    Returns an Employee salary. Use query param ?salary=50000
    Demonstrates the @property salary access.
    """
    salary = request.args.get("salary", default=50000, type=int)
    e = Employee(salary)
    return jsonify({"salary": e.salary})


@app.route("/greet")
def greet_route():
    """
    Demonstrates that the original metadata is preserved by @wraps.
    Returns the wrapped function's __name__, __doc__, and its return value.
    """
    return jsonify({
        "name": greet.__name__,
        "doc": greet.__doc__,
        "call": greet()
    })


if __name__ == "__main__":
    app.run(debug=True)
