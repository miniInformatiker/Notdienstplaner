from . import app
from .routes.auth import auth_controller
from .routes.pharmacy import pharmacy_controller

app.register_blueprint(pharmacy_controller)
app.register_blueprint(auth_controller)


if __name__ == '__main__':
    app.run(debug=True)
