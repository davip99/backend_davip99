import re
from app.models import get_db

def validate_dni(dni):
    if not re.match(r"\d{8}[A-Z]", dni):
        return False
    
    if not dni[-1] == "TRWAGMYFPDXBNJZSQVHLCKE"[int(dni[:-1]) % 23]:
        return False
    else:
        return True
    
def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    else:
        return True
    
def validate_tae(tae):
    if not re.match(r"\d+(\.\d+)?", tae):
        return False
    else:
        return True
    
def validate_plazo(plazo):
    if not re.match(r"\d+", plazo):
        return False
    else:
        return True
    
def calculate_cuota(dni, tae, plazo):
    db = get_db()
    capital = db.execute('SELECT capital FROM clients WHERE dni = ?', (dni,)).fetchone()
    i = tae / 100 / 12
    n = plazo * 12
    cuota = capital['capital'] * i / (1 - (1 + i) ** -n)
    return cuota

def calculate_importe_total(dni, tae, plazo):
    cuota = calculate_cuota(dni, tae, plazo)
    n = plazo * 12
    importe_total = cuota * n
    return importe_total