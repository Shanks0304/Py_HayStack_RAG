from .core.app_factory import FastAPIApp
import logging

my_app = FastAPIApp()
app = my_app.get_app()
logging.basicConfig(level=logging.INFO, format='%(levelname)s:\t  %(message)s [%(name)s]')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000, reload=True)
