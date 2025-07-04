import streamlit as st
import requests
import pandas as pd
from datetime import datetime

API_URL = "http://localhost:5000"

st.title("Users Tablosu (Frontend)")

def get_users():
    resp = requests.get(f"{API_URL}/users")
    return pd.DataFrame(resp.json())

df = get_users()
st.dataframe(df)

# Kullanıcı ekleme
st.subheader("Yeni Kullanıcı Ekle")
with st.form("add_user"):
    role_id = st.number_input("role_id", min_value=0, step=1)
    name = st.text_input("name")
    surname = st.text_input("surname")
    password = st.text_input("password")
    e_mail = st.text_input("e_mail")
    institution_working = st.text_input("institution_working")
    status = st.text_input("status")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    submitted = st.form_submit_button("Ekle")
    if submitted:
        data = {
            "role_id": role_id,
            "name": name,
            "surname": surname,
            "password": password,
            "e_mail": e_mail,
            "institution_working": institution_working,
            "status": status,
            "create_date": now,
            "change_date": now,
            "last_login": now
        }
        requests.post(f"{API_URL}/users", json=data)
        st.success("Kullanıcı eklendi!")
        st.rerun()

# Kullanıcı silme
st.subheader("Kullanıcı Sil")
if not df.empty:
    user_ids = df['id'].tolist()
    user_to_delete = st.selectbox("Silinecek kullanıcı id", user_ids)
    if st.button("Sil"):
        requests.delete(f"{API_URL}/users/{user_to_delete}")
        st.success(f"id {user_to_delete} silindi!")
        st.rerun()
else:
    st.info("Silinecek kullanıcı yok.")

# Kullanıcı güncelleme
st.subheader("Kullanıcı Güncelle")
if not df.empty:
    user_to_update = st.selectbox("Güncellenecek kullanıcı id", user_ids, key="update")
    user_row = df[df['id'] == user_to_update].iloc[0]
    with st.form("update_user"):
        role_id_u = st.number_input("role_id", min_value=0, step=1, value=int(user_row['role_id']) if user_row['role_id'] else 0)
        name_u = st.text_input("name", value=user_row['name'])
        surname_u = st.text_input("surname", value=user_row['surname'])
        password_u = st.text_input("password", value=user_row['password'])
        e_mail_u = st.text_input("e_mail", value=user_row['e_mail'])
        institution_working_u = st.text_input("institution_working", value=user_row['institution_working'])
        status_u = st.text_input("status", value=user_row['status'])
        last_login_u = st.text_input("last_login", value=user_row['last_login'])
        submitted_u = st.form_submit_button("Güncelle")
        if submitted_u:
            data = {
                "role_id": role_id_u,
                "name": name_u,
                "surname": surname_u,
                "password": password_u,
                "e_mail": e_mail_u,
                "institution_working": institution_working_u,
                "status": status_u,
                "change_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_login": last_login_u
            }
            requests.put(f"{API_URL}/users/{user_to_update}", json=data)
            st.success("Kullanıcı güncellendi!")
            st.rerun()
else:
    st.info("Güncellenecek kullanıcı yok.")
