from .clients import clients_bp

def register_routes(app):
    app.register_blueprint(clients_bp, url_prefix='/api')
