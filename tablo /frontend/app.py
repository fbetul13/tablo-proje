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
            {"name": "module_name", "type": "text"},
            {"name": "description", "type": "text"},
            {"name": "user_id", "type": "number"},
            {"name": "asistan_id", "type": "number"},
            {"name": "database_id", "type": "number"},
            {"name": "csv_database_id", "type": "number"}
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
            {"name": "option_code", "type": "text"},
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
                show_cols = ['prompt_id', 'question', 'assistant_title', 'trigger_time', 'option_code', 'mcrisactive', 'receiver_emails']
                show_cols = [c for c in show_cols if c in df.columns]
                st.dataframe(df[show_cols])
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
    if table_name == "Roles":
        form = st.form(key=f"role_form_{st.session_state['role_form_key']}")
        role_id = form.number_input("role_id", step=1, format="%d")
        role_name = form.text_input("role_name")
        permissions = form.text_area("permissions (JSON)", value="{}")
        admin_or_not = form.selectbox("admin_or_not", ["Evet", "Hayır"]) == "Evet"
        submitted = form.form_submit_button("Ekle")
        if submitted:
            try:
                add_data = {
                    "role_id": role_id,
                    "role_name": role_name,
                    "permissions": json.loads(permissions) if permissions else {},
                    "admin_or_not": admin_or_not
                }
                resp = requests.post(f"{BACKEND_URL}/roles", json=add_data)
                if resp.status_code == 200:
                    st.session_state["success_message"] = "Kayıt eklendi!"
                    st.session_state["role_form_key"] += 1  # Formu sıfırla
                    st.rerun()
                else:
                    form.error(resp.text)
            except Exception as e:
                form.error(f"Kayıt eklenemedi: {e}")
    elif table_name == "Assistants":
        users = get_users()
        user_options = {f"{u['name']} {u['surname']}": u['id'] for u in users} if users else {}
        form = st.form(key=f"assistant_form_{st.session_state.get('assistant_form_key', 0)}")
        title = form.text_input("title")
        explanation = form.text_input("explanation")
        parameters = form.text_area("parameters (JSON)", value="{}")
        if user_options:
            user_display = form.selectbox("Kişi (Users tablosundan)", list(user_options.keys()))
            user_id = user_options[user_display]
        else:
            user_id = None
        working_place = form.text_input("working_place")
        default_instructions = form.text_input("default_instructions")
        data_instructions = form.text_input("data_instructions")
        file_path = form.text_input("file_path")
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
                    form.error(resp.text)
            except Exception as e:
                form.error(f"Kayıt eklenemedi: {e}")
    elif table_name == "Auto Prompt":
        # Assistants tablosundan başlıkları çek
        try:
            assistants = requests.get(f"{BACKEND_URL}/assistants").json()
            assistant_titles = [a['title'] for a in assistants] if assistants else []
        except Exception:
            assistant_titles = []
        form = st.form(key=f"auto_prompt_form_{st.session_state.get('auto_prompt_form_key', 0)}")
        question = form.text_input("question")
        if assistant_titles:
            assistant_title = form.selectbox("assistant_title (Assistants tablosundan)", assistant_titles)
        else:
            assistant_title = form.text_input("assistant_title")
        trigger_time = form.text_area("trigger_time (JSON)", value="{}")
        option_code = form.text_input("option_code")
        mcrisactive = form.selectbox("mcrisactive", ["Evet", "Hayır"]) == "Evet"
        receiver_emails = form.text_area("receiver_emails")
        submitted = form.form_submit_button("Ekle")
        if submitted:
            try:
                add_data = {
                    "question": question,
                    "assistant_title": assistant_title,
                    "trigger_time": json.loads(trigger_time) if trigger_time else {},
                    "option_code": option_code,
                    "mcrisactive": mcrisactive,
                    "receiver_emails": receiver_emails
                }
                resp = requests.post(f"{BACKEND_URL}/auto_prompt", json=add_data)
                if resp.status_code == 200:
                    st.session_state["success_message"] = "Kayıt eklendi!"
                    st.session_state["auto_prompt_form_key"] = st.session_state.get('auto_prompt_form_key', 0) + 1
                    st.rerun()
                else:
                    form.error(resp.text)
            except Exception as e:
                form.error(f"Kayıt eklenemedi: {e}")
    elif table_name == "Data Prepare Modules":
        users = get_users()
        assistants = get_assistants()
        user_options = {f"{u['id']} - {u['name']} {u['surname']} ({u['e_mail']})": u['id'] for u in users} if users else {}
        assistant_options = {f"{a['asistan_id']} - {a['title']}": a['asistan_id'] for a in assistants} if assistants else {}
        form = st.form(key=f"dpm_form_{st.session_state.get('dpm_form_key', 0)}")
        module_name = form.text_input("module_name")
        description = form.text_input("description")
        user_id = form.selectbox("user_id (Users tablosundan)", list(user_options.keys())) if user_options else form.text_input("user_id")
        asistan_id = form.selectbox("asistan_id (Assistants tablosundan)", list(assistant_options.keys())) if assistant_options else form.text_input("asistan_id")
        database_id = form.text_input("database_id")
        csv_database_id = form.text_input("csv_database_id")
        submitted = form.form_submit_button("Ekle")
        if submitted:
            try:
                add_data = {
                    "module_name": module_name,
                    "description": description,
                    "user_id": user_options[user_id] if user_options else user_id,
                    "asistan_id": assistant_options[asistan_id] if assistant_options else asistan_id,
                    "database_id": database_id,
                    "csv_database_id": csv_database_id
                }
                resp = requests.post(f"{BACKEND_URL}/data_prepare_modules", json=add_data)
                if resp.status_code == 200:
                    st.session_state["success_message"] = "Kayıt eklendi!"
                    st.session_state["dpm_form_key"] = st.session_state.get('dpm_form_key', 0) + 1
                    st.rerun()
                else:
                    form.error(resp.text)
            except Exception as e:
                form.error(f"Kayıt eklenemedi: {e}")
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
                add_data[fname] = st.text_input(fname)
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
                            st.error(resp.text)
                    except Exception as e:
                        st.error(f"Kayıt eklenemedi: {e}")
            else:
                try:
                    resp = requests.post(f"{BACKEND_URL}/{endpoint}", json=add_data)
                    if resp.status_code == 200:
                        st.session_state["success_message"] = "Kayıt eklendi!"
                        st.rerun()
                    else:
                        st.error(resp.text)
                except Exception as e:
                    st.error(f"Kayıt eklenemedi: {e}")

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
            st.warning("Silinecek kullanıcı yok.")
            delete_id = None
    elif table_name == "Roles":
        roles = get_roles()
        if roles:
            role_options = {f"{r['role_id']} - {r['role_name']}": r['role_id'] for r in roles}
            selected = st.selectbox("Silinecek Rol", list(role_options.keys()), key="delete_role_select")
            delete_id = role_options[selected]
        else:
            st.warning("Silinecek rol yok.")
            delete_id = None
    else:
        delete_id = st.text_input("Silinecek ID (veya anahtar)", key="delete_id")
    if st.button("Sil"):
        if delete_id:
            try:
                resp = requests.delete(f"{BACKEND_URL}/{endpoint}/{delete_id}")
                st.success("Kayıt silindi!" if resp.status_code == 200 else resp.text)
                if resp.status_code == 200:
                    st.rerun()
            except Exception as e:
                st.error(f"Kayıt silinemedi: {e}")
        else:
            st.warning("Lütfen silinecek ID girin.")

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
            st.warning("Güncellenecek kullanıcı yok.")
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
            st.warning("Güncellenecek rol yok.")
            update_id = None
            role_row = None
    else:
        update_id = st.text_input("Güncellenecek ID (veya anahtar)", key="update_id")
        user_row = None
        role_row = None
    update_data = {}
    for field in fields:
        fname = field["name"]
        ftype = field["type"]
        if fname in ["create_date", "change_date"]:
            continue  # Bu alanları atla
        if table_name == "Users" and fname == "role_id":
            if user_row:
                default_role = next((r for r in roles if r['role_id'] == user_row['role_id']), None)
                default_role_name = default_role['role_name'] if default_role else role_names[0]
            else:
                default_role_name = role_names[0]
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
                st.success("Kayıt güncellendi!" if resp.status_code == 200 else resp.text)
                if resp.status_code == 200:
                    st.rerun()
            except Exception as e:
                st.error(f"Kayıt güncellenemedi: {e}")
        else:
            st.warning("Lütfen güncellenecek ID girin.") 