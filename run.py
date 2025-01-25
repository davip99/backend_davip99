from app import create_app
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

if __name__ == '__main__':
    env = os.environ.get('FLASK_ENV')
    app = create_app(env)

    app.run(host='0.0.0.0', port=5000)