
from src.routes import app
import uvicorn
if __name__ =="__main__":
    uvicorn.run("routes:app",reload=True)

