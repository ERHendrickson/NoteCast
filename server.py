from flask_app import app
from flask_app.controllers import podcasts
from flask_app.controllers import notes

if __name__ == "__main__":
    app.run(debug = True)
