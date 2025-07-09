from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import json
from datetime import datetime
import pandas as pd
def prepare(df):
    df['total'] = df['price'] * df['quantity']
    return df

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="tablo_db",
        user="postgres",
        password="Betul1103"
    )

# 1. Roles CRUD
@app.route('/roles', methods=['GET'])
def get_roles():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM llm_platform.roles')
    roles = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(roles)

@app.route('/roles', methods=['POST'])
def add_role():
    data = request.get_json(force=True) or {}
    conn = get_db_connection()
    cur = conn.cursor()
    permissions = data.get('permissions')
    if isinstance(permissions, dict):
        permissions = json.dumps(permissions)
    cur.execute(
        'INSERT INTO llm_platform.roles (role_id, role_name, permissions, admin_or_not) VALUES (%s, %s, %s, %s)',
        (
            data.get('role_id'),
            data.get('role_name'),
            permissions,
            data.get('admin_or_not')
        )
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM llm_platform.roles WHERE role_id = %s', (role_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'deleted'})

@app.route('/roles/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    data = request.get_json(force=True) or {}
    conn = get_db_connection()
    cur = conn.cursor()
    permissions = data.get('permissions')
    if isinstance(permissions, dict):
        permissions = json.dumps(permissions)
    cur.execute(
        'UPDATE llm_platform.roles SET role_name=%s, permissions=%s, admin_or_not=%s WHERE role_id=%s',
        (
            data.get('role_name'),
            permissions,
            data.get('admin_or_not'),
            role_id
        )
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'updated'})

# 2. Users CRUD
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM llm_platform.users')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json(force=True) or {}
    conn = get_db_connection()
    cur = conn.cursor()
    fields = ['role_id', 'name', 'surname', 'password', 'e_mail', 'institution_working']
    values = [data.get(f) for f in fields]
    sql_fields = ', '.join(fields)
    sql_placeholders = ', '.join(['%s'] * len(fields))
    if data.get('create_date'):
        sql_fields += ', create_date'
        sql_placeholders += ', %s'
        values.append(data.get('create_date'))
    if data.get('change_date'):
        sql_fields += ', change_date'
        sql_placeholders += ', %s'
        values.append(data.get('change_date'))
    cur.execute(f'INSERT INTO llm_platform.users ({sql_fields}) VALUES ({sql_placeholders})', values)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM llm_platform.users WHERE id = %s', (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'deleted'})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json(force=True) or {}
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'UPDATE llm_platform.users SET role_id=%s, name=%s, surname=%s, password=%s, e_mail=%s, institution_working=%s, status=%s, change_date=%s, last_login=%s WHERE id=%s',
        (
            data.get('role_id'),
            data.get('name'),
            data.get('surname'),
            data.get('password'),
            data.get('e_mail'),
            data.get('institution_working'),
            data.get('status'),
            data.get('change_date'),
            data.get('last_login'),
            user_id
        )
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'updated'})

# 3. database_info CRUD
@app.route('/database_info', methods=['GET'])
def get_database_info():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM llm_platform.database_info')
    records = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(records)

@app.route('/database_info', methods=['POST'])
def add_database_info():
    data = request.get_json(force=True) or {}
    conn = get_db_connection()
    cur = conn.cursor()
    fields = ['database_ip', 'database_port', 'database_user', 'database_password', 'database_type', 'database_name', 'user_id']
    values = [data.get(f) for f in fields]
    sql_fields = ', '.join(fields)
    sql_placeholders = ', '.join(['%s'] * len(fields))
    if data.get('create_date'):
        sql_fields += ', create_date'
        sql_placeholders += ', %s'
        values.append(data.get('create_date'))
    if data.get('change_date'):
        sql_fields += ', change_date'
        sql_placeholders += ', %s'
        values.append(data.get('change_date'))
    cur.execute(f'INSERT INTO llm_platform.database_info ({sql_fields}) VALUES ({sql_placeholders})', values)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/database_info/<int:database_id>', methods=['DELETE'])
def delete_database_info(database_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM llm_platform.database_info WHERE database_id = %s', (database_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'deleted'})

@app.route('/database_info/<int:database_id>', methods=['PUT'])
def update_database_info(database_id):
    data = request.get_json(force=True) or {}
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'UPDATE llm_platform.database_info SET database_ip=%s, database_port=%s, database_user=%s, database_password=%s, database_type=%s, database_name=%s, user_id=%s WHERE database_id=%s',
        (
            data.get('database_ip'),
            data.get('database_port'),
            data.get('database_user'),
            data.get('database_password'),
            data.get('database_type'),
            data.get('database_name'),
            data.get('user_id'),
            database_id
        )
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'updated'})

# 4. data_prepare_modules CRUD
@app.route('/data_prepare_modules', methods=['GET'])
def get_data_prepare_modules():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM llm_platform.data_prepare_modules')
    records = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(records)

@app.route('/data_prepare_modules', methods=['POST'])
def add_data_prepare_module():
    data = request.get_json(force=True) or {}
    conn = get_db_connection()
    cur = conn.cursor()
    # JSON alanları stringe çevir
    trigger_time = data.get('trigger_time')
    if isinstance(trigger_time, dict):
        trigger_time = json.dumps(trigger_time)
    fields = ['module_name', 'description', 'user_id']
    values = [data.get(f) for f in fields]
    sql_fields = ', '.join(fields)
    sql_placeholders = ', '.join(['%s'] * len(fields))
    if data.get('create_date'):
        sql_fields += ', create_date'
        sql_placeholders += ', %s'
        values.append(data.get('create_date'))
    if data.get('change_date'):
        sql_fields += ', change_date'
        sql_placeholders += ', %s'
        values.append(data.get('change_date'))
    cur.execute(f'INSERT INTO llm_platform.data_prepare_modules ({sql_fields}) VALUES ({sql_placeholders})', values)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/data_prepare_modules/<int:module_id>', methods=['DELETE'])
def delete_data_prepare_module(module_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM llm_platform.data_prepare_modules WHERE module_id = %s', (module_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'deleted'})

@app.route('/data_prepare_modules/<int:module_id>', methods=['PUT'])
def update_data_prepare_module(module_id):
    data = request.get_json(force=True) or {}
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'UPDATE llm_platform.data_prepare_modules SET module_name=%s, description=%s, user_id=%s, create_date=%s, change_date=%s WHERE module_id=%s',
        (
            data.get('module_name'),
            data.get('description'),
            data.get('user_id'),
            data.get('create_date'),
            data.get('change_date'),
            module_id
        )
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'updated'})

# 5. assistants CRUD
@app.route('/assistants', methods=['GET'])
def get_assistants():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM llm_platform.assistants')
    records = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(records)

@app.route('/assistants', methods=['POST'])
def add_assistant():
    data = request.get_json(force=True) or {}
    conn = get_db_connection()
    cur = conn.cursor()
    # JSON alanları stringe çevir
    parameters = data.get('parameters')
    if isinstance(parameters, dict):
        parameters = json.dumps(parameters)
    trigger_time = data.get('trigger_time')
    if isinstance(trigger_time, dict):
        trigger_time = json.dumps(trigger_time)
    fields = ['title', 'explanation', 'parameters', 'user_id', 'working_place', 'default_instructions', 'data_instructions', 'file_path', 'trigger_time']
    values = [
        data.get('title'),
        data.get('explanation'),
        parameters,
        data.get('user_id'),
        data.get('working_place'),
        data.get('default_instructions'),
        data.get('data_instructions'),
        data.get('file_path'),
        trigger_time
    ]
    sql_fields = ', '.join(fields)
    sql_placeholders = ', '.join(['%s'] * len(fields))
    if data.get('create_date'):
        sql_fields += ', create_date'
        sql_placeholders += ', %s'
        values.append(data.get('create_date'))
    if data.get('change_date'):
        sql_fields += ', change_date'
        sql_placeholders += ', %s'
        values.append(data.get('change_date'))
    cur.execute(f'INSERT INTO llm_platform.assistants ({sql_fields}) VALUES ({sql_placeholders})', values)
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/assistants/<int:asistan_id>', methods=['DELETE'])
def delete_assistant(asistan_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM llm_platform.assistants WHERE asistan_id = %s', (asistan_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'deleted'})

@app.route('/assistants/<int:asistan_id>', methods=['PUT'])
def update_assistant(asistan_id):
    data = request.get_json(force=True) or {}
    conn = get_db_connection()
    cur = conn.cursor()
    parameters = data.get('parameters')
    trigger_time = data.get('trigger_time')
    if isinstance(parameters, dict):
        parameters = json.dumps(parameters)
    if isinstance(trigger_time, dict):
        trigger_time = json.dumps(trigger_time)
    cur.execute(
        'UPDATE llm_platform.assistants SET title=%s, explanation=%s, parameters=%s, user_id=%s, create_date=%s, change_date=%s, working_place=%s, default_instructions=%s, data_instructions=%s, file_path=%s, trigger_time=%s WHERE asistan_id=%s',
        (
            data.get('title'),
            data.get('explanation'),
            parameters,
            data.get('user_id'),
            data.get('create_date'),
            data.get('change_date'),
            data.get('working_place'),
            data.get('default_instructions'),
            data.get('data_instructions'),
            data.get('file_path'),
            trigger_time,
            asistan_id
        )
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'updated'})

# 6. auto_prompt CRUD
@app.route('/auto_prompt', methods=['GET'])
def get_auto_prompt():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('''
        SELECT ap.*, a.title as assistant_title
        FROM llm_platform.auto_prompt ap
        LEFT JOIN llm_platform.assistants a ON ap.asistan_id = a.asistan_id
    ''')
    records = cur.fetchall()
    for rec in records:
        if 'asistan_id' in rec:
            rec['assistant_title'] = rec.pop('assistant_title')
    cur.close()
    conn.close()
    return jsonify(records)

@app.route('/auto_prompt', methods=['POST'])
def add_auto_prompt():
    data = request.get_json(force=True) or {}
    conn = get_db_connection()
    cur = conn.cursor()
    trigger_time = data.get('trigger_time')
    if isinstance(trigger_time, dict):
        trigger_time = json.dumps(trigger_time)
    assistant_title = data.get('assistant_title')
    if not assistant_title:
        cur.close()
        conn.close()
        return jsonify({'error': 'assistant_title gerekli'}), 400
    cur.execute('SELECT asistan_id FROM llm_platform.assistants WHERE title = %s', (assistant_title,))
    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        return jsonify({'error': 'assistant_title bulunamadı'}), 400
    asistan_id = row[0]
    cur.execute(
        'INSERT INTO llm_platform.auto_prompt (asistan_id, question, trigger_time, option_code, mcrisactive, receiver_emails) VALUES (%s, %s, %s, %s, %s, %s)',
        (
            asistan_id,
            data.get('question'),
            trigger_time,
            data.get('option_code'),
            data.get('mcrisactive'),
            data.get('receiver_emails')
        )
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/auto_prompt/<int:prompt_id>', methods=['DELETE'])
def delete_auto_prompt(prompt_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM llm_platform.auto_prompt WHERE prompt_id = %s', (prompt_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'deleted'})

@app.route('/auto_prompt/<int:prompt_id>', methods=['PUT'])
def update_auto_prompt(prompt_id):
    data = request.get_json(force=True) or {}
    conn = get_db_connection()
    cur = conn.cursor()
    trigger_time = data.get('trigger_time')
    if isinstance(trigger_time, dict):
        trigger_time = json.dumps(trigger_time)
    cur.execute(
        'UPDATE llm_platform.auto_prompt SET prompt_text=%s, assistants_id=%s, trigger_time=%s, mcrisactive=%s WHERE prompt_id=%s',
        (
            data.get('prompt_text'),
            data.get('assistants_id'),
            trigger_time,
            data.get('mcrisactive'),
            prompt_id
        )
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'updated'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True) or {}
    email = data.get('e_mail')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'E-posta ve şifre gerekli'}), 400
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM llm_platform.users WHERE e_mail = %s AND password = %s', (email, password))
    user = cur.fetchone()
    if user:
        cur.execute('UPDATE llm_platform.users SET last_login = CURRENT_TIMESTAMP WHERE id = %s', (user['id'],))
        conn.commit()
        # Kullanıcıyı tekrar çek, güncel last_login ile
        cur.execute('SELECT * FROM llm_platform.users WHERE id = %s', (user['id'],))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify(user)
    else:
        cur.close()
        conn.close()
        return jsonify({'error': 'Geçersiz e-posta veya şifre'}), 401

@app.route('/test')
def test():
    return "Backend çalışıyor!"

if __name__ == '__main__':
    app.run(debug=True)

      