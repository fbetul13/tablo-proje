import streamlit as st
import requests
import pandas as pd
import json
import re

BACKEND_URL = "http://127.0.0.1:5000"

# --- BAŞARI MESAJI BLOĞU ---
if "success_message" in st.session_state:
    st.success(st.session_state["success_message"])
    del st.session_state["success_message"]

if "role_form_key" not in st.session_state:
    st.session_state["role_form_key"] = 0

if "show_table" not in st.session_state:
    st.session_state["show_table"] = False

# Custom CSS for alert boxes (KALDIRILDI)

def get_users():
    try:
        resp = requests.get(f"{BACKEND_URL}/users")
        if resp.status_code == 200:
            return resp.json()
        return []
    except Exception:
        return []

def get_roles():
    try:
        resp = requests.get(f"{BACKEND_URL}/roles")
        if resp.status_code == 200:
            return resp.json()
        return []
    except Exception:
        return []

def get_assistants():
    try:
        resp = requests.get(f"{BACKEND_URL}/assistants")
        if resp.status_code == 200:
            return resp.json()
        return []
    except Exception:
        return []

def get_database_info():
    try:
        resp = requests.get(f"{BACKEND_URL}/database_info")
        if resp.status_code == 200:
            return resp.json()
        return []
    except Exception:
        return []

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

table_options = {
    "Roles": {
        "endpoint": "roles",
        "fields": [
            {"name": "role_id", "type": "number"},
            {"name": "role_name", "type": "text"},
            {"name": "permissions", "type": "json"},
            {"name": "admin_or_not", "type": "bool"}
        ]
    },
    "Users": {
        "endpoint": "users",
        "fields": [
            {"name": "role_id", "type": "number"},
            {"name": "name", "type": "text"},
            {"name": "surname", "type": "text"},
            {"name": "password", "type": "text"},
            {"name": "e_mail", "type": "text"},
            {"name": "institution_working", "type": "text"}
        ]
    },
    "Database Info": {
        "endpoint": "database_info",
        "fields": [
            {"name": "database_ip", "type": "text"},
            {"name": "database_port", "type": "text"},
            {"name": "database_user", "type": "text"},
            {"name": "database_password", "type": "text"},
            {"name": "database_type", "type": "text"},
            {"name": "database_name", "type": "text"},
            {"name": "user_id", "type": "number"}
        ]
    },
    "Data Prepare Modules": {
        "endpoint": "data_prepare_modules",
        "fields": [
            {"name": "module_id", "type": "number"},
            {"name": "module_name", "type": "text"},
            {"name": "description", "type": "text"},
            {"name": "user_id", "type": "number"},
            {"name": "asistan_id", "type": "number"},
            {"name": "database_id", "type": "number"},
            {"name": "csv_database_id", "type": "number"},
            {"name": "query", "type": "text"},
            {"name": "working_platform", "type": "text"},
            {"name": "query_name", "type": "text"},
            {"name": "db_schema", "type": "text"},
            {"name": "documents_id", "type": "number"},
            {"name": "csv_db_schema", "type": "text"},
            {"name": "data_prep_code", "type": "text"}
        ]
    },
    "Assistants": {
        "endpoint": "assistants",
        "fields": [
            {"name": "title", "type": "text"},
            {"name": "explanation", "type": "text"},
            {"name": "parameters", "type": "json"},
            {"name": "user_id", "type": "number"},
            {"name": "working_place", "type": "text"},
            {"name": "default_instructions", "type": "text"},
            {"name": "data_instructions", "type": "text"},
            {"name": "file_path", "type": "text"},
            {"name": "trigger_time", "type": "json"}
        ]
    },
    "Auto Prompt": {
        "endpoint": "auto_prompt",
        "fields": [
            {"name": "question", "type": "text"},
            {"name": "assistant_title", "type": "text"},
            {"name": "trigger_time", "type": "json"},
            {"name": "python_code", "type": "text"},
            {"name": "mcrisactive", "type": "bool"},
            {"name": "receiver_emails", "type": "text"}
        ]
    }
}

st.title("Tablo Yönetim Paneli")
table_name = st.sidebar.selectbox("Tablo Seçin", list(table_options.keys()))
config = table_options[table_name]
endpoint = config["endpoint"]
fields = config["fields"]

st.header(f"{table_name} Tablosu")

if table_name == "Users":
    roles = get_roles()
    role_name_to_id = {r['role_name']: r['role_id'] for r in roles}
    role_names = list(role_name_to_id.keys())

# Listele
if st.button("Verileri Listele"):
    st.session_state["show_table"] = not st.session_state["show_table"]

if st.session_state["show_table"]:
    try:
        resp = requests.get(f"{BACKEND_URL}/{endpoint}")
        data = resp.json()
        if isinstance(data, list) and data:
            if table_name == "Users":
                for user in data:
                    user['role_name'] = next((r['role_name'] for r in roles if r['role_id'] == user['role_id']), "")
                df = pd.DataFrame(data)
                show_cols = ['id', 'role_name', 'name', 'surname', 'e_mail', 'institution_working']
                show_cols = [c for c in show_cols if c in df.columns]
                st.dataframe(df[show_cols])
            elif table_name == "Assistants":
                df = pd.DataFrame(data)
                show_cols = ['asistan_id', 'title', 'explanation', 'parameters', 'user_id', 'working_place', 'default_instructions', 'data_instructions', 'file_path', 'trigger_time']
                show_cols = [c for c in show_cols if c in df.columns]
                st.dataframe(df[show_cols])
            elif table_name == "Auto Prompt":
                df = pd.DataFrame(data)
                show_cols = ['prompt_id', 'question', 'assistant_title', 'trigger_time', 'python_code', 'mcrisactive', 'receiver_emails']
                show_cols = [c for c in show_cols if c in df.columns]
                st.dataframe(df[show_cols])
            elif table_name == "Data Prepare Modules":
                df = pd.DataFrame(data)
                show_cols = ['module_id', 'module_name', 'description', 'user_id', 'asistan_id', 'database_id', 'csv_database_id', 'query', 'working_platform', 'query_name', 'db_schema', 'documents_id', 'csv_db_schema', 'data_prep_code']
                show_cols = [c for c in show_cols if c in df.columns]
                for idx, row in df.iterrows():
                    st.write(f"**Module ID:** {row.get('module_id','')}")
                    st.write(f"**Module Name:** {row.get('module_name','')}")
                    st.write(f"**Description:** {row.get('description','')}")
                    st.write(f"**User ID:** {row.get('user_id','')}")
                    st.write(f"**Asistan ID:** {row.get('asistan_id','')}")
                    st.write(f"**Database ID:** {row.get('database_id','')}")
                    st.write(f"**CSV Database ID:** {row.get('csv_database_id','')}")
                    st.write(f"**Query:** {row.get('query','')}")
                    st.write(f"**Working Platform:** {row.get('working_platform','')}")
                    st.write(f"**Query Name:** {row.get('query_name','')}")
                    st.write(f"**DB Schema:** {row.get('db_schema','')}")
                    st.write(f"**Documents ID:** {row.get('documents_id','')}")
                    st.write(f"**CSV DB Schema:** {row.get('csv_db_schema','')}")
                    st.code(row.get('data_prep_code',''), language='python')
                    st.markdown('---')
            else:
                df = pd.DataFrame(data)
                st.dataframe(df)
        elif isinstance(data, list):
            st.info("Tabloda veri yok.")
        else:
            st.error(str(data))
    except Exception as e:
        st.error(f"Veri alınamadı: {e}")

# Ekle
with st.expander("Yeni Kayıt Ekle"):
    def check_required_fields(field_defs, values_dict):
        missing = []
        for f in field_defs:
            fname = f["name"]
            if fname in ["create_date", "change_date"]:
                continue
            if f["type"] == "bool":
                continue
            if not values_dict.get(fname) and values_dict.get(fname) != False:
                missing.append((fname, f"{fname} alanı zorunludur."))
        return missing

    if table_name == "Roles":
        form = st.form(key=f"role_form_{st.session_state['role_form_key']}")
        role_id = form.number_input("role_id", min_value=0, step=1, format="%d")
        role_name = form.text_input("role_name", max_chars=100)
        # Karakter sayacı kaldırıldı
        permissions = form.text_area("permissions (JSON)", value="{}")
        admin_or_not = form.selectbox("admin_or_not", ["Evet", "Hayır"]) == "Evet"
        submitted = form.form_submit_button("Ekle")
        add_data = {
            "role_id": role_id,
            "role_name": role_name,
            "permissions": permissions,
            "admin_or_not": admin_or_not
        }
        missing_fields = check_required_fields(table_options["Roles"]["fields"], add_data)
        if submitted:
            if role_id == 0:
                form.error("Role ID 0 olamaz.")
            elif missing_fields:
                for mf, reason in missing_fields:
                    form.markdown(f'<div style="color:red; font-size:12px;">{reason}</div>', unsafe_allow_html=True)
                form.error("Eksik alan(lar): " + ", ".join([mf for mf, _ in missing_fields]))
            else:
                try:
                    add_data["permissions"] = json.loads(permissions) if permissions else {}
                    resp = requests.post(f"{BACKEND_URL}/roles", json=add_data)
                    if resp.status_code == 200:
                        st.session_state["success_message"] = "Kayıt eklendi!"
                        st.session_state["role_form_key"] += 1  # Formu sıfırla
                        st.rerun()
                    else:
                        try:
                            error_msg = resp.json().get('error') if resp.headers.get('Content-Type','').startswith('application/json') else resp.text
                            if isinstance(error_msg, str) and (error_msg.strip().lower().startswith('<html') or error_msg.strip().lower().startswith('<!doctype')):
                                form.error('Geçersiz giriş, lütfen alanları kontrol edin.')
                            elif isinstance(error_msg, str) and (
                                'already exists' in error_msg.lower() or
                                'duplicate' in error_msg.lower() or
                                'unique constraint' in error_msg.lower() or
                                'not unique' in error_msg.lower()
                            ):
                                if 'e_mail' in error_msg.lower() or 'email' in error_msg.lower():
                                    form.error('Bu e-posta adresiyle zaten bir kullanıcı var.')
                                elif 'id' in error_msg.lower():
                                    form.error('Bu ID ile zaten bir kayıt mevcut.')
                                elif 'name' in error_msg.lower():
                                    form.error('Bu isimle bir kayıt zaten eklenmiş.')
                                else:
                                    form.error('Bu kayıt zaten mevcut.')
                            else:
                                form.error(error_msg)
                        except Exception:
                            form.error('Geçersiz giriş, lütfen alanları kontrol edin.')
                except Exception as e:
                    form.error(str(e))
    elif table_name == "Assistants":
        users = get_users()
        user_options = {f"{u['name']} {u['surname']}": u['id'] for u in users} if users else {}
        form = st.form(key=f"assistant_form_{st.session_state.get('assistant_form_key', 0)}")
        title = form.text_area("title", max_chars=255)
        # Karakter sayacı kaldırıldı
        explanation = form.text_area("explanation")
        parameters = form.text_area("parameters (JSON)", value="{}")
        if user_options:
            user_display = form.selectbox("Kişi (Users tablosundan)", list(user_options.keys()))
            user_id = user_options[user_display]
        else:
            user_id = None
        working_place = form.text_area("working_place", max_chars=255)
        # Karakter sayacı kaldırıldı
        default_instructions = form.text_area("default_instructions")
        data_instructions = form.text_area("data_instructions")
        file_path = form.text_area("file_path", max_chars=255)
        # Karakter sayacı kaldırıldı
        trigger_time = form.text_area("trigger_time (JSON)", value="{}")
        submitted = form.form_submit_button("Ekle")
        if submitted:
            try:
                add_data = {
                    "title": title,
                    "explanation": explanation,
                    "parameters": json.loads(parameters) if parameters else {},
                    "user_id": user_id,
                    "working_place": working_place,
                    "default_instructions": default_instructions,
                    "data_instructions": data_instructions,
                    "file_path": file_path,
                    "trigger_time": json.loads(trigger_time) if trigger_time else {}
                }
                resp = requests.post(f"{BACKEND_URL}/assistants", json=add_data)
                if resp.status_code == 200:
                    st.session_state["success_message"] = "Kayıt eklendi!"
                    st.session_state["assistant_form_key"] = st.session_state.get('assistant_form_key', 0) + 1
                    st.rerun()
                else:
                    try:
                        error_msg = resp.json().get('error') if resp.headers.get('Content-Type','').startswith('application/json') else resp.text
                        if isinstance(error_msg, str) and (error_msg.strip().lower().startswith('<html') or error_msg.strip().lower().startswith('<!doctype')):
                            form.error('Geçersiz giriş, lütfen alanları kontrol edin.')
                        elif isinstance(error_msg, str) and (
                            'already exists' in error_msg.lower() or
                            'duplicate' in error_msg.lower() or
                            'unique constraint' in error_msg.lower() or
                            'not unique' in error_msg.lower()
                        ):
                            if 'e_mail' in error_msg.lower() or 'email' in error_msg.lower():
                                form.error('Bu e-posta adresiyle zaten bir kullanıcı var.')
                            elif 'id' in error_msg.lower():
                                form.error('Bu ID ile zaten bir kayıt mevcut.')
                            elif 'name' in error_msg.lower():
                                form.error('Bu isimle bir kayıt zaten eklenmiş.')
                            else:
                                form.error('Bu kayıt zaten mevcut.')
                        else:
                            form.error(error_msg)
                    except Exception:
                        form.error('Geçersiz giriş, lütfen alanları kontrol edin.')
            except Exception as e:
                form.error(str(e))
    elif table_name == "Auto Prompt":
        # Assistants tablosundan başlıkları çek
        try:
            assistants = requests.get(f"{BACKEND_URL}/assistants").json()
            assistant_titles = [a['title'] for a in assistants] if assistants else []
        except Exception:
            assistant_titles = []
        form = st.form(key=f"auto_prompt_form_{st.session_state.get('auto_prompt_form_key', 0)}")
        question = form.text_area("question", max_chars=255)
        if len(question) > 100:
            form.markdown('<div style="color:red; font-size:12px;">En fazla 100 karakter girebilirsiniz.</div>', unsafe_allow_html=True)
        if assistant_titles:
            assistant_title = form.selectbox("assistant_title (Assistants tablosundan)", assistant_titles)
        else:
            assistant_title = form.text_area("assistant_title", max_chars=100)
            if len(assistant_title) > 100:
                form.markdown('<div style="color:red; font-size:12px;">En fazla 100 karakter girebilirsiniz.</div>', unsafe_allow_html=True)
        trigger_time = form.text_area("trigger_time (JSON)", value="{}")
        python_code = form.text_area("python_code", height=200, help="Buraya Python kodunuzu yazabilirsiniz.")
        mcrisactive = form.selectbox("mcrisactive", ["Evet", "Hayır"]) == "Evet"
        receiver_emails = form.text_area("receiver_emails")
        email_warning = False
        if receiver_emails:
            emails = [e.strip() for e in receiver_emails.split(",")]
            for e in emails:
                if not is_valid_email(e):
                    form.markdown('<div style="color:red; font-size:12px;">Lütfen geçerli e-posta adres(ler)i girin. (Virgülle ayırabilirsiniz)</div>', unsafe_allow_html=True)
                    email_warning = True
                    break
        submitted = form.form_submit_button("Ekle")
        if submitted:
            if len(question) > 100 or (not assistant_title or len(assistant_title) > 100) or email_warning:
                form.error("Lütfen alanları doğru ve limitlere uygun doldurun.")
            else:
                try:
                    add_data = {
                        "question": question,
                        "assistant_title": assistant_title,
                        "trigger_time": json.loads(trigger_time) if trigger_time else {},
                        "python_code": python_code,
                        "mcrisactive": mcrisactive,
                        "receiver_emails": receiver_emails
                    }
                    resp = requests.post(f"{BACKEND_URL}/auto_prompt", json=add_data)
                    if resp.status_code == 200:
                        st.session_state["success_message"] = "Kayıt eklendi!"
                        st.session_state["auto_prompt_form_key"] = st.session_state.get('auto_prompt_form_key', 0) + 1
                        st.rerun()
                    else:
                        try:
                            error_msg = resp.json().get('error') if resp.headers.get('Content-Type','').startswith('application/json') else resp.text
                            if isinstance(error_msg, str) and (error_msg.strip().lower().startswith('<html') or error_msg.strip().lower().startswith('<!doctype')):
                                form.error('Geçersiz giriş, lütfen alanları kontrol edin.')
                            elif isinstance(error_msg, str) and (
                                'already exists' in error_msg.lower() or
                                'duplicate' in error_msg.lower() or
                                'unique constraint' in error_msg.lower() or
                                'not unique' in error_msg.lower()
                            ):
                                if 'e_mail' in error_msg.lower() or 'email' in error_msg.lower():
                                    form.error('Bu e-posta adresiyle zaten bir kullanıcı var.')
                                elif 'id' in error_msg.lower():
                                    form.error('Bu ID ile zaten bir kayıt mevcut.')
                                elif 'name' in error_msg.lower():
                                    form.error('Bu isimle bir kayıt zaten eklenmiş.')
                                else:
                                    form.error('Bu kayıt zaten mevcut.')
                            else:
                                form.error(error_msg)
                        except Exception:
                            form.error('Geçersiz giriş, lütfen alanları kontrol edin.')
                except Exception as e:
                    form.error(str(e))
    elif table_name == "Data Prepare Modules":
        users = get_users()
        assistants = get_assistants()
        databases = get_database_info()
        user_options = {f"{u['id']} - {u['name']} {u['surname']} ({u['e_mail']})": u['id'] for u in users} if users else {}
        assistant_options = {f"{a['asistan_id']} - {a['title']}": a['asistan_id'] for a in assistants} if assistants else {}
        database_options = {f"{d['database_id']} - {d['database_name']} ({d['database_ip']}:{d['database_port']})": d['database_id'] for d in databases} if databases else {}
        form = st.form(key=f"dpm_form_{st.session_state.get('dpm_form_key', 0)}")
        module_name = form.text_area("module_name")
        description = form.text_area("description")
        user_id = form.selectbox("user_id (Users tablosundan)", list(user_options.keys())) if user_options else form.text_input("user_id")
        asistan_id = form.selectbox("asistan_id (Assistants tablosundan)", list(assistant_options.keys())) if assistant_options else form.text_input("asistan_id")
        database_id = form.selectbox("database_id (Database Info tablosundan)", list(database_options.keys())) if database_options else form.text_input("database_id")
        csv_database_id = form.text_input("csv_database_id")
        query_name = form.text_area("query_name", max_chars=255)
        working_platform = form.text_area("working_platform", max_chars=100)
        db_schema = form.text_area("db_schema")
        documents_id = form.text_area("documents_id")
        csv_db_schema = form.text_area("csv_db_schema")
        data_prep_code = form.text_area("data_prep_code", height=200, max_chars=1000, help="Buraya Python kodunuzu yazabilirsiniz.")
        # Karakter sayacı kaldırıldı
        submitted = form.form_submit_button("Ekle")
        if submitted:
            if (working_platform and len(working_platform) > 100) or (query_name and len(query_name) > 100):
                form.error("Lütfen alanları doğru ve limitlere uygun doldurun.")
            else:
                try:
                    add_data = {
                        "module_name": module_name,
                        "description": description,
                        "user_id": user_options[user_id] if user_options else user_id,
                        "asistan_id": assistant_options[asistan_id] if assistant_options else asistan_id,
                        "database_id": database_options[database_id] if database_options else database_id,
                        "csv_database_id": csv_database_id,
                        "query_name": query_name,
                        "working_platform": working_platform,
                        "db_schema": db_schema,
                        "documents_id": documents_id,
                        "csv_db_schema": csv_db_schema,
                        "data_prep_code": data_prep_code
                    }
                    resp = requests.post(f"{BACKEND_URL}/data_prepare_modules", json=add_data)
                    if resp.status_code == 200:
                        st.session_state["success_message"] = "Kayıt eklendi!"
                        st.session_state["dpm_form_key"] = st.session_state.get('dpm_form_key', 0) + 1
                        st.rerun()
                    else:
                        try:
                            error_msg = resp.json().get('error') if resp.headers.get('Content-Type','').startswith('application/json') else resp.text
                            if isinstance(error_msg, str) and (error_msg.strip().lower().startswith('<html') or error_msg.strip().lower().startswith('<!doctype')):
                                form.error('Geçersiz giriş, lütfen alanları kontrol edin.')
                            elif isinstance(error_msg, str) and (
                                'already exists' in error_msg.lower() or
                                'duplicate' in error_msg.lower() or
                                'unique constraint' in error_msg.lower() or
                                'not unique' in error_msg.lower()
                            ):
                                form.error('Bu kayıt zaten mevcut.')
                            else:
                                form.error(error_msg)
                        except Exception:
                            form.error('Geçersiz giriş, lütfen alanları kontrol edin.')
                except Exception as e:
                    form.error(str(e))
    elif table_name == "Database Info":
        users = get_users()
        user_options = {f"{u['id']} - {u['name']} {u['surname']} ({u['e_mail']})": u['id'] for u in users} if users else {}
        form = st.form(key=f"dbinfo_form_{st.session_state.get('dbinfo_form_key', 0)}")
        database_ip = form.text_area("database_ip", max_chars=100)
        database_port = form.text_area("database_port")
        database_user = form.text_area("database_user", max_chars=100)
        database_password = form.text_area("database_password", max_chars=100)
        database_type = form.text_area("database_type", max_chars=50)
        database_name = form.text_area("database_name", max_chars=100)
        user_id = form.selectbox("user_id (Users tablosundan)", list(user_options.keys())) if user_options else form.text_input("user_id")
        submitted = form.form_submit_button("Ekle")
        if submitted:
            try:
                add_data = {
                    "database_ip": database_ip,
                    "database_port": database_port,
                    "database_user": database_user,
                    "database_password": database_password,
                    "database_type": database_type,
                    "database_name": database_name,
                    "user_id": user_options[user_id] if user_options else user_id
                }
                resp = requests.post(f"{BACKEND_URL}/database_info", json=add_data)
                if resp.status_code == 200:
                    st.session_state["success_message"] = "Kayıt eklendi!"
                    st.session_state["dbinfo_form_key"] = st.session_state.get('dbinfo_form_key', 0) + 1
                    st.rerun()
                else:
                    try:
                        error_msg = resp.json().get('error') if resp.headers.get('Content-Type','').startswith('application/json') else resp.text
                        if isinstance(error_msg, str) and (error_msg.strip().lower().startswith('<html') or error_msg.strip().lower().startswith('<!doctype')):
                            form.error('Geçersiz giriş, lütfen alanları kontrol edin.')
                        elif isinstance(error_msg, str) and (
                            'already exists' in error_msg.lower() or
                            'duplicate' in error_msg.lower() or
                            'unique constraint' in error_msg.lower() or
                            'not unique' in error_msg.lower()
                        ):
                            form.error('Bu kayıt zaten mevcut.')
                        else:
                            form.error(error_msg)
                    except Exception:
                        form.error('Geçersiz giriş, lütfen alanları kontrol edin.')
            except Exception as e:
                form.error(str(e))
    else:
        add_data = {}
        for field in fields:
            fname = field["name"]
            ftype = field["type"]
            if fname in ["create_date", "change_date"]:
                continue  # Bu alanları atla
            if table_name == "Users" and fname == "role_id":
                add_data['role_name'] = st.selectbox("Rol", role_names)
            elif ftype == "bool":
                add_data[fname] = st.selectbox(fname, ["Evet", "Hayır"]) == "Evet"
            elif ftype == "json":
                add_data[fname] = st.text_area(fname + " (JSON)", value="{}")
            elif ftype == "number":
                if not (table_name == "Users" and fname == "role_id"):
                    add_data[fname] = st.number_input(fname, step=1, format="%d")
            else:
                max_chars = 100 if fname in ["name", "surname"] else None
                add_data[fname] = st.text_input(fname, max_chars=max_chars)
                if max_chars and add_data[fname] and len(add_data[fname]) > max_chars:
                    st.markdown(f'<div style="color:red; font-size:12px;">En fazla {max_chars} karakter girebilirsiniz.</div>', unsafe_allow_html=True)
                if fname == "e_mail" and add_data[fname] and not is_valid_email(add_data[fname]):
                    st.markdown('<div style="color:red; font-size:12px;">Lütfen geçerli bir e-posta adresi girin (ör: kisi@site.com)</div>', unsafe_allow_html=True)
        if st.button("Ekle"):
            for field in fields:
                if field["name"] in ["create_date", "change_date"]:
                    continue
                if field["type"] == "json":
                    try:
                        add_data[field["name"]] = json.loads(add_data[field["name"]]) if add_data[field["name"]] else {}
                    except Exception:
                        add_data[field["name"]] = {}
            if table_name == "Users":
                add_data['role_id'] = role_name_to_id.get(add_data.pop('role_name'), None)
                email = add_data.get("e_mail", "")
                if not is_valid_email(email):
                    st.error("Lütfen geçerli bir e-posta adresi girin (ör: kisi@site.com)")
                else:
                    try:
                        resp = requests.post(f"{BACKEND_URL}/{endpoint}", json=add_data)
                        if resp.status_code == 200:
                            st.session_state["success_message"] = "Kişi eklendi!"
                            st.rerun()
                        else:
                            try:
                                error_msg = resp.json().get('error') if resp.headers.get('Content-Type','').startswith('application/json') else resp.text
                                if isinstance(error_msg, str) and (error_msg.strip().lower().startswith('<html') or error_msg.strip().lower().startswith('<!doctype')):
                                    st.error('Geçersiz giriş, lütfen alanları kontrol edin.')
                                elif isinstance(error_msg, str) and (
                                    'already exists' in error_msg.lower() or
                                    'duplicate' in error_msg.lower() or
                                    'unique constraint' in error_msg.lower() or
                                    'not unique' in error_msg.lower()
                                ):
                                    st.error('Bu kayıt zaten mevcut.')
                                else:
                                    st.error(error_msg)
                            except Exception:
                                st.error('Geçersiz giriş, lütfen alanları kontrol edin.')
                    except Exception as e:
                        st.error(str(e))
            else:
                try:
                    resp = requests.post(f"{BACKEND_URL}/{endpoint}", json=add_data)
                    if resp.status_code == 200:
                        st.session_state["success_message"] = "Kayıt eklendi!"
                        st.rerun()
                    else:
                        try:
                            error_msg = resp.json().get('error') if resp.headers.get('Content-Type','').startswith('application/json') else resp.text
                            if isinstance(error_msg, str) and (error_msg.strip().lower().startswith('<html') or error_msg.strip().lower().startswith('<!doctype')):
                                st.error('Geçersiz giriş, lütfen alanları kontrol edin.')
                            elif isinstance(error_msg, str) and (
                                'already exists' in error_msg.lower() or
                                'duplicate' in error_msg.lower() or
                                'unique constraint' in error_msg.lower() or
                                'not unique' in error_msg.lower()
                            ):
                                st.error('Bu kayıt zaten mevcut.')
                            else:
                                st.error(error_msg)
                        except Exception:
                            st.error(resp.text)
                except Exception as e:
                    st.error(str(e))

# Sil
with st.expander("Kayıt Sil"):
    if table_name == "Users":
        users = get_users()
        if users:
            for user in users:
                user['role_name'] = next((r['role_name'] for r in roles if r['role_id'] == user['role_id']), "")
            user_options = {f"{u['id']} - {u['name']} {u['surname']} ({u['e_mail']}) [{u['role_name']}]": u['id'] for u in users}
            selected = st.selectbox("Silinecek Kişi", list(user_options.keys()), key="delete_user_select")
            delete_id = user_options[selected]
        else:
            st.success("Silinecek kullanıcı yok.")
            delete_id = None
    elif table_name == "Roles":
        roles = get_roles()
        delete_id = None
        if roles:
            # role_name selectbox
            role_names = [r['role_name'] for r in roles]
            selected_role_name = st.selectbox("Silinecek Rol (role_name)", role_names, key="delete_role_name_select")
            # Seçilen role_name'e sahip ilk kaydın id'sini bul
            selected_role_by_name = next((r for r in roles if r['role_name'] == selected_role_name), None)
        else:
            st.success("Silinecek rol yok.")
            selected_role_by_name = None
        # Manuel ID girişi
        manual_delete_id = st.text_input("Silinecek ID (veya anahtar)", key="delete_role_id_manual")
        if manual_delete_id:
            try:
                delete_id = int(manual_delete_id)
            except Exception:
                st.warning("Geçerli bir ID girin.")
                delete_id = None
        elif selected_role_by_name:
            delete_id = selected_role_by_name['role_id']
    elif table_name == "Assistants":
        assistants = get_assistants()
        if assistants:
            assistant_options = {f"{a['asistan_id']} - {a['title']}": a['asistan_id'] for a in assistants}
            selected = st.selectbox("Silinecek Asistan", list(assistant_options.keys()), key="delete_assistant_select")
            delete_id = assistant_options[selected]
        else:
            st.success("Silinecek asistan yok.")
            delete_id = None
    elif table_name == "Auto Prompt":
        auto_prompts = requests.get(f"{BACKEND_URL}/auto_prompt").json()
        if auto_prompts:
            auto_prompt_options = {f"{ap['prompt_id']} - {ap['question']}": ap['prompt_id'] for ap in auto_prompts}
            selected = st.selectbox("Silinecek Auto Prompt", list(auto_prompt_options.keys()), key="delete_auto_prompt_select")
            delete_id = auto_prompt_options[selected]
        else:
            st.success("Silinecek auto prompt yok.")
            delete_id = None
    elif table_name == "Data Prepare Modules":
        dpm_modules = requests.get(f"{BACKEND_URL}/data_prepare_modules").json()
        if dpm_modules:
            dpm_options = {f"{dpm['module_id']} - {dpm['module_name']}": dpm['module_id'] for dpm in dpm_modules}
            selected = st.selectbox("Silinecek Data Prepare Module", list(dpm_options.keys()), key="delete_dpm_select")
            delete_id = dpm_options[selected]
        else:
            st.success("Silinecek data prepare module yok.")
            delete_id = None
    elif table_name == "Database Info":
        dbinfo_entries = requests.get(f"{BACKEND_URL}/database_info").json()
        if dbinfo_entries:
            dbinfo_options = {f"{dbinfo['database_id']} - {dbinfo['database_name']}": dbinfo['database_id'] for dbinfo in dbinfo_entries}
            selected = st.selectbox("Silinecek Database Info", list(dbinfo_options.keys()), key="delete_dbinfo_select")
            delete_id = dbinfo_options[selected]
        else:
            st.success("Silinecek database info yok.")
            delete_id = None
    else:
        delete_id = st.text_input("Silinecek ID (veya anahtar)", key="delete_id")
    if st.button("Sil"):
        if delete_id:
            try:
                resp = requests.delete(f"{BACKEND_URL}/{endpoint}/{delete_id}")
                if resp.status_code == 200:
                    st.success("Kayıt silindi!")
                    if table_name == "Roles":
                        st.markdown('<span style="color:green; font-size:16px;">Kayıt silindi.</span>', unsafe_allow_html=True)
                    st.rerun()
                else:
                    try:
                        error_msg = resp.json().get('error') if resp.headers.get('Content-Type','').startswith('application/json') else resp.text
                        if isinstance(error_msg, str) and (error_msg.strip().lower().startswith('<html') or error_msg.strip().lower().startswith('<!doctype')):
                            st.error('Kayıt silinemedi.')
                        else:
                            st.error(error_msg)
                    except Exception:
                        st.error('Kayıt silinemedi.')
            except Exception as e:
                st.error('Kayıt silinemedi.')
        else:
            st.error("Lütfen silinecek ID girin.")

# Güncelle
with st.expander("Kayıt Güncelle"):
    if table_name == "Users":
        users = get_users()
        if users:
            for user in users:
                user['role_name'] = next((r['role_name'] for r in roles if r['role_id'] == user['role_id']), "")
            user_options = {f"{u['id']} - {u['name']} {u['surname']} ({u['e_mail']}) [{u['role_name']}]": u['id'] for u in users}
            selected = st.selectbox("Güncellenecek Kişi", list(user_options.keys()), key="update_user_select")
            update_id = user_options[selected]
            user_row = next((u for u in users if u['id'] == update_id), None)
        else:
            st.success("Güncellenecek kullanıcı yok.")
            update_id = None
            user_row = None
    elif table_name == "Roles":
        roles = get_roles()
        if roles:
            role_options = {f"{r['role_id']} - {r['role_name']}": r['role_id'] for r in roles}
            selected = st.selectbox("Güncellenecek Rol", list(role_options.keys()), key="update_role_select")
            update_id = role_options[selected]
            role_row = next((r for r in roles if r['role_id'] == update_id), None)
        else:
            st.success("Güncellenecek rol yok.")
            update_id = None
            role_row = None
    elif table_name == "Assistants":
        assistants = get_assistants()
        if assistants:
            assistant_options = {f"{a['asistan_id']} - {a['title']}": a['asistan_id'] for a in assistants}
            selected = st.selectbox("Güncellenecek Asistan", list(assistant_options.keys()), key="update_assistant_select")
            update_id = assistant_options[selected]
            assistant_row = next((a for a in assistants if a['asistan_id'] == update_id), None)
        else:
            st.success("Güncellenecek asistan yok.")
            update_id = None
            assistant_row = None
    elif table_name == "Auto Prompt":
        auto_prompts = requests.get(f"{BACKEND_URL}/auto_prompt").json()
        if auto_prompts:
            auto_prompt_options = {f"{ap['prompt_id']} - {ap['question']}": ap['prompt_id'] for ap in auto_prompts}
            selected = st.selectbox("Güncellenecek Auto Prompt", list(auto_prompt_options.keys()), key="update_auto_prompt_select")
            update_id = auto_prompt_options[selected]
            auto_prompt_row = next((ap for ap in auto_prompts if ap['prompt_id'] == update_id), None)
        else:
            st.success("Güncellenecek auto prompt yok.")
            update_id = None
            auto_prompt_row = None
    elif table_name == "Data Prepare Modules":
        dpm_modules = requests.get(f"{BACKEND_URL}/data_prepare_modules").json()
        if dpm_modules:
            dpm_options = {f"{dpm['module_id']} - {dpm['module_name']}": dpm['module_id'] for dpm in dpm_modules}
            selected = st.selectbox("Güncellenecek Data Prepare Module", list(dpm_options.keys()), key="update_dpm_select")
            update_id = dpm_options[selected]
            dpm_row = next((dpm for dpm in dpm_modules if dpm['module_id'] == update_id), None)
        else:
            st.success("Güncellenecek data prepare module yok.")
            update_id = None
            dpm_row = None
    elif table_name == "Database Info":
        dbinfo_entries = requests.get(f"{BACKEND_URL}/database_info").json()
        if dbinfo_entries:
            dbinfo_options = {f"{dbinfo['database_id']} - {dbinfo['database_name']}": dbinfo['database_id'] for dbinfo in dbinfo_entries}
            selected = st.selectbox("Güncellenecek Database Info", list(dbinfo_options.keys()), key="update_dbinfo_select")
            update_id = dbinfo_options[selected]
            dbinfo_row = next((dbinfo for dbinfo in dbinfo_entries if dbinfo['database_id'] == update_id), None)
        else:
            st.success("Güncellenecek database info yok.")
            update_id = None
            dbinfo_row = None
    else:
        update_id = st.text_input("Güncellenecek ID (veya anahtar)", key="update_id")
        user_row = None
        role_row = None
        assistant_row = None
        auto_prompt_row = None
        dbinfo_row = None
    update_data = {}
    for field in fields:
        fname = field["name"]
        ftype = field["type"]
        if fname in ["create_date", "change_date"]:
            continue  # Bu alanları atla
        if table_name == "Users" and fname == "role_id":
            if user_row:
                default_role = next((r for r in roles if r['role_id'] == user_row['role_id']), None)
                if role_names:
                    default_role_name = default_role['role_name'] if default_role else role_names[0]
                else:
                    default_role_name = ""
            else:
                default_role_name = role_names[0] if role_names else ""
            update_data['role_name'] = st.selectbox("Yeni Rol", role_names, index=role_names.index(default_role_name) if default_role_name in role_names else 0)
        elif table_name == "Roles" and fname == "role_id":
            continue  # role_id güncellenemez
        elif ftype == "bool":
            update_data[fname] = st.selectbox("Yeni " + fname, ["Evet", "Hayır"]) == "Evet"
        elif ftype == "json":
            update_data[fname] = st.text_area("Yeni " + fname + " (JSON)", value="{}", key="update_json"+fname)
        elif ftype == "number":
            if not (table_name == "Users" and fname == "role_id") and not (table_name == "Roles" and fname == "role_id"):
                update_data[fname] = st.number_input("Yeni " + fname, step=1, format="%d", key="update_num"+fname)
        else:
            if (table_name == "Users" and user_row and fname in user_row):
                update_data[fname] = st.text_input("Yeni " + fname, value=user_row[fname], key=f"update_{fname}")
            elif (table_name == "Roles" and role_row and fname in role_row):
                update_data[fname] = st.text_input("Yeni " + fname, value=role_row[fname], key=f"update_{fname}")
            elif (table_name == "Assistants" and assistant_row and fname in assistant_row):
                update_data[fname] = st.text_area("Yeni " + fname, value=assistant_row[fname], key=f"update_{fname}")
            elif (table_name == "Auto Prompt" and auto_prompt_row and fname in auto_prompt_row):
                update_data[fname] = st.text_area("Yeni " + fname, value=auto_prompt_row[fname], key=f"update_{fname}")
            elif (table_name == "Data Prepare Modules" and dpm_row and fname in dpm_row):
                update_data[fname] = st.text_area("Yeni " + fname, value=dpm_row[fname], key=f"update_{fname}")
            elif (table_name == "Database Info" and dbinfo_row and fname in dbinfo_row):
                update_data[fname] = st.text_area("Yeni " + fname, value=dbinfo_row[fname], key=f"update_{fname}")
            else:
                update_data[fname] = st.text_input("Yeni " + fname, key=f"update_{fname}")
    if st.button("Güncelle"):
        for field in fields:
            if field["name"] in ["create_date", "change_date"]:
                continue
            if field["type"] == "json":
                try:
                    update_data[field["name"]] = json.loads(update_data[field["name"]]) if update_data[field["name"]] else {}
                except Exception:
                    update_data[field["name"]] = {}
        if table_name == "Users":
            update_data['role_id'] = role_name_to_id.get(update_data.pop('role_name'), None)
        if update_id:
            try:
                resp = requests.put(f"{BACKEND_URL}/{endpoint}/{update_id}", json=update_data)
                if resp.status_code == 200:
                    st.success("Kayıt güncellendi!")
                    st.rerun()
                else:
                    st.error("Kayıt güncellenemedi: " + resp.text)
            except Exception as e:
                st.error(f"Kayıt güncellenemedi: {e}")
        else:
            st.error("Lütfen güncellenecek ID girin.") 

# Auto Prompt'taki python_code alanı için Courier fontu
st.markdown(
    """
    <style>
    textarea[data-testid="stTextArea-input"] {
        font-family: Courier, monospace !important;
        font-size: 16px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
) 