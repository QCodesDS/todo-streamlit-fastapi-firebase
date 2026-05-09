# 📝 Todo App — Streamlit + FastAPI + Firebase

Ứng dụng quản lý công việc (Todo) xây dựng với kiến trúc 3 tầng hiện đại.

**Môn học:** Tư duy Tính toán 
**Sinh viên:** Lê Văn Quốc — MSSV: 24120421  
**Trường:** Đại học Khoa học Tự nhiên TP.HCM (HCMUS)

---

## 🏗️ Kiến trúc

```
Streamlit (Frontend) ──► FastAPI + Uvicorn (Backend) ──► Firebase Emulator
     :8501                        :8000                  Auth :9099 | Firestore :8080
```

| Tầng     | Công nghệ               | Vai trò                  |
| -------- | ----------------------- | ------------------------ |
| Frontend | Streamlit               | Giao diện người dùng     |
| Backend  | FastAPI + Uvicorn       | REST API, xác thực token |
| Auth     | Firebase Authentication | Đăng ký / Đăng nhập      |
| Database | Cloud Firestore         | Lưu trữ dữ liệu Todo     |

---

## ✨ Tính năng

- 🔐 Đăng ký và đăng nhập bằng email/password
- ✅ Thêm, xem, hoàn thành, xóa công việc Todo
- 👤 Mỗi user chỉ thấy Todo của chính mình (phân quyền theo uid)
- 📄 Tài liệu API tự động tại `/docs` (Swagger UI)

---

## 📁 Cấu trúc thư mục

```
todo-streamlit-fastapi-firebase/
├── backend/
│   ├── venv/
│   └── main.py          # FastAPI app
├── frontend/
│   ├── venv/
│   └── app.py           # Streamlit app
├── notebook/
│   └── todo_app_notebook.ipynb  # Báo cáo + kiểm thử
├── firebase.json
├── .firebaserc
└── README.md
```

---

## 🚀 Hướng dẫn chạy

### Yêu cầu

- Python 3.10+
- Node.js 18+
- Java 11+ (cho Firebase Emulator)
- Firebase CLI (`npm install -g firebase-tools`)

### Bước 1: Clone project

```bash
git clone https://github.com/QCodesDS/todo-streamlit-fastapi-firebase.git
cd todo-streamlit-fastapi-firebase
```

### Bước 2: Khởi động Firebase Emulator

```bash
firebase emulators:start
```

- Emulator UI: http://127.0.0.1:4000
- Auth: http://127.0.0.1:9099
- Firestore: http://127.0.0.1:8080

### Bước 3: Chạy Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install fastapi uvicorn firebase-admin google-cloud-firestore python-jose[cryptography] requests
uvicorn main:app --reload --port 8000
```

- API Docs: http://127.0.0.1:8000/docs

### Bước 4: Chạy Frontend

```bash
cd frontend
python -m venv venv
venv\Scripts\activate        # Windows
pip install streamlit requests
streamlit run app.py
```

- App: http://localhost:8501

---

## 🔌 API Endpoints

| Method | Endpoint         | Mô tả                      | Auth         |
| ------ | ---------------- | -------------------------- | ------------ |
| POST   | `/auth/register` | Đăng ký user mới           | Không        |
| POST   | `/auth/login`    | Đăng nhập, trả về ID Token | Không        |
| GET    | `/todos`         | Lấy danh sách todo         | Bearer Token |
| POST   | `/todos`         | Tạo todo mới               | Bearer Token |
| PUT    | `/todos/{id}`    | Cập nhật todo              | Bearer Token |
| DELETE | `/todos/{id}`    | Xóa todo                   | Bearer Token |

---

## 🔒 Luồng xác thực

```
1. User đăng nhập → Frontend gọi POST /auth/login
2. Backend gọi Firebase Auth Emulator → nhận ID Token (JWT)
3. Frontend lưu token vào st.session_state
4. Mỗi request gửi header: Authorization: Bearer <idToken>
5. Backend verify token → lấy uid → query Firestore theo uid
```

---

## 🗃️ Mô hình dữ liệu Firestore

Collection: `todos`

```json
{
  "uid": "string",
  "title": "string",
  "done": false
}
```

---

## 📦 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — Backend framework
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- [Streamlit](https://streamlit.io/) — Frontend framework
- [Firebase Authentication](https://firebase.google.com/docs/auth) — Xác thực người dùng
- [Cloud Firestore](https://firebase.google.com/docs/firestore) — NoSQL database
- [Firebase Emulator Suite](https://firebase.google.com/docs/emulator-suite) — Local development
