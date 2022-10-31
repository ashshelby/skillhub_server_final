from a2wsgi import ASGIMiddleware
from src.routes import app  # Import your FastAPI app.

application = ASGIMiddleware(app)
