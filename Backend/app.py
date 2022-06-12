from . import app, db
from .routes.auth import auth_controller
from .routes.pharmacy import pharmacy_controller
from .routes.order import order_controller
from .routes.manuelExceptions import manuelExceptions_controller

app.register_blueprint(pharmacy_controller)
app.register_blueprint(auth_controller)
app.register_blueprint(order_controller)
app.register_blueprint(manuelExceptions_controller)

db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
