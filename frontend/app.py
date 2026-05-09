import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.title("📝 Todo App")

# Session state
if "token" not in st.session_state:
    st.session_state.token = None
if "uid" not in st.session_state:
    st.session_state.uid = None

# ---------- CHƯA ĐĂNG NHẬP ----------
if not st.session_state.token:
    tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Mật khẩu", type="password", key="login_pass")
        if st.button("Đăng nhập"):
            res = requests.post(f"{API}/auth/login", json={"email": email, "password": password})
            if res.status_code == 200:
                data = res.json()
                st.session_state.token = data["idToken"]
                st.session_state.uid = data["uid"]
                st.rerun()
            else:
                st.error(res.json().get("detail", "Lỗi đăng nhập"))

    with tab2:
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Mật khẩu", type="password", key="reg_pass")
        if st.button("Đăng ký"):
            res = requests.post(f"{API}/auth/register", json={"email": email, "password": password})
            if res.status_code == 200:
                st.success("Đăng ký thành công! Hãy đăng nhập.")
            else:
                st.error(res.json().get("detail", "Lỗi đăng ký"))

# ---------- ĐÃ ĐĂNG NHẬP ----------
else:
    st.success(f"Đã đăng nhập: {st.session_state.uid}")
    if st.button("Đăng xuất"):
        st.session_state.token = None
        st.session_state.uid = None
        st.rerun()

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    # Thêm todo
    st.subheader("➕ Thêm công việc")
    new_title = st.text_input("Tên công việc")
    if st.button("Thêm"):
        res = requests.post(f"{API}/todos", json={"title": new_title, "done": False}, headers=headers)
        if res.status_code == 200:
            st.success("Đã thêm!")
            st.rerun()
        else:
            st.error("Lỗi thêm todo")

    # Danh sách todo
    st.subheader("📋 Danh sách công việc")
    res = requests.get(f"{API}/todos", headers=headers)
    if res.status_code == 200:
        todos = res.json()
        for todo in todos:
            col1, col2, col3 = st.columns([5, 2, 1])
            with col1:
                st.write(f"{'✅' if todo['done'] else '⬜'} {todo['title']}")
            with col2:
                if st.button("Hoàn thành" if not todo["done"] else "Bỏ hoàn thành", key=f"done_{todo['id']}"):
                    requests.put(f"{API}/todos/{todo['id']}", 
                                json={"title": todo["title"], "done": not todo["done"]}, 
                                headers=headers)
                    st.rerun()
            with col3:
                if st.button("🗑️", key=f"del_{todo['id']}"):
                    requests.delete(f"{API}/todos/{todo['id']}", headers=headers)
                    st.rerun()
    else:
        st.error("Không thể tải danh sách")