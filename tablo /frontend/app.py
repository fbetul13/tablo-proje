import streamlit as st
import requests
import pandas as pd
import json

BACKEND_URL = "http://127.0.0.1:5000"

def get_users():
    try:
        resp = requests.get(f"{BACKEND_URL}/users")
        if resp.status_code == 200:
            return resp.json()
        return []
    except:
        return []

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
            {"name": "prompt_text", "type": "text"},
            {"name": "assistants_id", "type": "number"},
            {"name": "trigger_time", "type": "json"},
            {"name": "mcrisactive", "type": "bool"}
        ]
    }
}

st.title("Tablo Yönetim Paneli")
table_name = st.sidebar.selectbox("Tablo Seçin", list(table_options.keys()))
config = table_options[table_name]
endpoint = config["endpoint"]
fields = config["fields"]

st.header(f"{table_name} Tablosu")

# Listele
if st.button("Verileri Listele"):
    try:
        resp = requests.get(f"{BACKEND_URL}/{endpoint}")
        data = resp.json()
        if isinstance(data, list) and data:
            st.dataframe(pd.DataFrame(data))
        elif isinstance(data, list):
            st.info("Tabloda veri yok.")
        else:
            st.error(str(data))
    except Exception as e:
        st.error(f"Veri alınamadı: {e}")

# Ekle
with st.expander("Yeni Kayıt Ekle"):
    add_data = {}
    add_result = None
    for field in fields:
        fname = field["name"]
        ftype = field["type"]
        if ftype == "bool":
            add_data[fname] = st.selectbox(fname, ["Evet", "Hayır"]) == "Evet"
        elif ftype == "json":
            add_data[fname] = st.text_area(fname + " (JSON)", value="{}")
        elif ftype == "number":
            add_data[fname] = st.number_input(fname, step=1, format="%d")
        else:
            add_data[fname] = st.text_input(fname)
    if st.button("Ekle"):
        for field in fields:
            if field["type"] == "json":
                try:
                    add_data[field["name"]] = json.loads(add_data[field["name"]]) if add_data[field["name"]] else {}
                except:
                    add_data[field["name"]] = {}
        try:
            resp = requests.post(f"{BACKEND_URL}/{endpoint}", json=add_data)
            if table_name == "Users":
                if resp.status_code == 200:
                    add_result = ("Kişi eklendi!", "success")
                else:
                    add_result = ("Kişi eklenemedi!", "error")
            else:
                st.success("Kayıt eklendi!" if resp.status_code == 200 else resp.text)
        except Exception as e:
            if table_name == "Users":
                add_result = ("Kişi eklenemedi!", "error")
            else:
                st.error(f"Kayıt eklenemedi: {e}")
    if table_name == "Users" and add_result:
        if add_result[1] == "success":
            st.success(add_result[0])
        else:
            st.error(add_result[0])

# Sil
with st.expander("Kayıt Sil"):
    if table_name == "Users":
        users = get_users()
        if users:
            user_options = {f"{u['id']} - {u['name']} {u['surname']} ({u['e_mail']})": u['id'] for u in users}
            selected = st.selectbox("Silinecek Kişi", list(user_options.keys()), key="delete_user_select")
            delete_id = user_options[selected]
        else:
            st.warning("Silinecek kullanıcı yok.")
            delete_id = None
    else:
        delete_id = st.text_input("Silinecek ID (veya anahtar)", key="delete_id")
    if st.button("Sil"):
        if delete_id:
            try:
                resp = requests.delete(f"{BACKEND_URL}/{endpoint}/{delete_id}")
                st.success("Kayıt silindi!" if resp.status_code == 200 else resp.text)
            except Exception as e:
                st.error(f"Kayıt silinemedi: {e}")
        else:
            st.warning("Lütfen silinecek ID girin.")

# Güncelle
with st.expander("Kayıt Güncelle"):
    if table_name == "Users":
        users = get_users()
        if users:
            user_options = {f"{u['id']} - {u['name']} {u['surname']} ({u['e_mail']})": u['id'] for u in users}
            selected = st.selectbox("Güncellenecek Kişi", list(user_options.keys()), key="update_user_select")
            update_id = user_options[selected]
        else:
            st.warning("Güncellenecek kullanıcı yok.")
            update_id = None
    else:
        update_id = st.text_input("Güncellenecek ID (veya anahtar)", key="update_id")
    update_data = {}
    for field in fields:
        fname = field["name"]
        ftype = field["type"]
        if ftype == "bool":
            update_data[fname] = st.selectbox("Yeni " + fname, ["Evet", "Hayır"]) == "Evet"
        elif ftype == "json":
            update_data[fname] = st.text_area("Yeni " + fname + " (JSON)", value="{}", key="update_json"+fname)
        elif ftype == "number":
            update_data[fname] = st.number_input("Yeni " + fname, step=1, format="%d", key="update_num"+fname)
        else:
            update_data[fname] = st.text_input("Yeni " + fname, key=f"update_{fname}")
    if st.button("Güncelle"):
        for field in fields:
            if field["type"] == "json":
                try:
                    update_data[field["name"]] = json.loads(update_data[field["name"]]) if update_data[field["name"]] else {}
                except:
                    update_data[field["name"]] = {}
        if update_id:
            try:
                resp = requests.put(f"{BACKEND_URL}/{endpoint}/{update_id}", json=update_data)
                st.success("Kayıt güncellendi!" if resp.status_code == 200 else resp.text)
            except Exception as e:
                st.error(f"Kayıt güncellenemedi: {e}")
        else:
            st.warning("Lütfen güncellenecek ID girin.")