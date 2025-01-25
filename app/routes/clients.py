from flask import Blueprint, request, jsonify
from app.models import get_db
import app.utils as utils
import sqlite3
import datetime

clients_bp = Blueprint('api', __name__)

@clients_bp.route('/clients/', methods=['GET'])
def get_clients():
    db = get_db()
    clients = db.execute('SELECT c.dni, c.name, c.email, c.capital, s.id as simulacion_id, s.tae, s.plazo, s.cuota, s.importe_total, s.created_at, s.updated_at FROM clients c LEFT JOIN simulaciones s ON c.dni = s.dni').fetchall()
    
    clients_dict = {}
    for row in clients:
        dni = row['dni']
        if dni not in clients_dict:
            clients_dict[dni] = {
                'nombre': row['name'],
                'dni': row['dni'],
                'email': row['email'],
                'capital_solicitado': row['capital'],
                'simulaciones': []
            }
        if row['simulacion_id'] is not None:
            simulacion = {
                'id': row['simulacion_id'],
                'dni': row['dni'],
                'tae': row['tae'],
                'plazo': row['plazo'],
                'cuota': row['cuota'],
                'importe_total': row['importe_total'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            clients_dict[dni]['simulaciones'].append(simulacion)
    
    return jsonify(list(clients_dict.values()))

@clients_bp.route('/clients/', methods=['POST'])
def create_client():
    data = request.json
    name = data.get('name')
    dni = data.get('dni')
    email = data.get('email')
    
    if not name or not dni or not email:
        return jsonify({'message': 'Missing name, dni or email'}), 400
    
    if not utils.validate_dni(dni):
        return jsonify({'message': 'Invalid DNI'}), 400
    
    if not utils.validate_email(email):
        return jsonify({'message': 'Invalid email'}), 400
    
    db = get_db()
    try:
        db.execute('INSERT INTO clients (name, dni, email, capital) VALUES (?, ?, ?, ?)', (data['name'], data['dni'], data['email'], data['capital']))
        db.commit()
        return jsonify({'message': 'Client created successfully'}), 200
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Client with this DNI already exists'}), 409
    
@clients_bp.route('/clients/<dni>', methods=['GET'])
def get_clients_by_dni(dni):
    db = get_db()
    
    if not utils.validate_dni(dni):
        return jsonify({'message': 'Invalid DNI'}), 400
    
    try:
        clients = db.execute('SELECT c.dni, c.name, c.email, c.capital, s.id as simulacion_id, s.tae, s.plazo, s.cuota, s.importe_total, s.created_at, s.updated_at FROM clients c LEFT JOIN simulaciones s ON c.dni = s.dni WHERE c.dni = ?', (dni,)).fetchall()
    
        clients_dict = {}
        for row in clients:
            dni = row['dni']
            if dni not in clients_dict:
                clients_dict[dni] = {
                    'nombre': row['name'],
                    'dni': row['dni'],
                    'email': row['email'],
                    'capital_solicitado': row['capital'],
                    'simulaciones': []
                }
            if row['simulacion_id'] is not None:
                simulacion = {
                    'id': row['simulacion_id'],
                    'dni': row['dni'],
                    'tae': row['tae'],
                    'plazo': row['plazo'],
                    'cuota': row['cuota'],
                    'importe_total': row['importe_total'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
                clients_dict[dni]['simulaciones'].append(simulacion)
        
        return jsonify(list(clients_dict.values()))
    except TypeError:
        return jsonify({'message': 'Client not found'})
    

@clients_bp.route('/clients/<dni>', methods=['PUT'])
def update_client(dni):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    capital = data.get('capital')
    
    if not name or not email:
        return jsonify({'message': 'Missing name or email'}), 400
    
    if not utils.validate_dni(dni):
        return jsonify({'message': 'Invalid DNI'}), 400
    
    if not utils.validate_email(email):
        return jsonify({'message': 'Invalid email'}), 400
    
    db = get_db()
    try:
        cursor = db.execute('UPDATE clients SET name = ?, email = ?, capital = ? WHERE dni = ?', (name, email, capital, dni))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({'message': 'Client not found'})
        
        return get_clients_by_dni(dni)
    
    except sqlite3.Error as e:
        return jsonify({'message': str(e)}), 500

@clients_bp.route('/clients/<dni>', methods=['DELETE'])
def delete_client(dni):
    db = get_db()

    if not utils.validate_dni(dni):
        return jsonify({'message': 'Invalid DNI'}), 400
    
    try: 
        db.execute('DELETE FROM clients WHERE dni = ?', (dni,))
        db.commit()

        return jsonify({'message': 'Client deleted successfully'}), 200
    
    except sqlite3.Error as e:
        return jsonify({'message': str(e)}), 500
    
@clients_bp.route('/clients/<dni>/simulation/', methods=['POST'])
def simulate_loan(dni):
    data = request.json
    tae = data.get('tae')
    plazo = data.get('plazo')
    
    if not tae or not plazo:
        return jsonify({'message': 'Missing tae or plazo'}), 400
    
    if not utils.validate_dni(dni):
        return jsonify({'message': 'Invalid DNI'}), 400
    
    try:
        tae = float(tae)
    except ValueError:
        return jsonify({'message': 'TAE has to be a number'}), 400
    
    try:
        plazo = int(plazo)
    except ValueError:
        return jsonify({'message': 'Plazo has to be a number'}), 400
    
    cuota = utils.calculate_cuota(dni, tae, plazo)
    importe_total = utils.calculate_importe_total(dni, tae, plazo)
    current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    db = get_db()
    try:
        db.execute('INSERT INTO simulaciones (dni, tae, plazo, cuota, importe_total, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)', (dni, tae, plazo, cuota, importe_total, current_timestamp, current_timestamp))
        db.commit()
    
        return get_clients_by_dni(dni)
    
    except sqlite3.Error as e:
        return jsonify({'message': str(e)}), 500