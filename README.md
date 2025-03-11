# Simple FastAPI and Firebase Firestore 🐍

## 📖 Table of Content

- [About The Project](#about-the-project)
- [Setup & Installation](#setup-&-installation)
- [Project Usage](#project-usage)
   - [Manual Run](#manual-run)
   - [Run with Docker](#run-with-docker)
- [Demo & Documentations](#demo-&-documentations)
   - [Architecture & Folder Structure](#architecture-&-folder-structure)
   - [How It Works](#how-it-works)
- [Important Notes](#important-notes)

---

## 1️⃣ About The Project

A simple FastAPI and Firebase Firestore back-end project. This task was accomplished with these key requirements and additional features: 

- ✅ CRUD (Create, Read, Update, and Delete) API for user data.
- ✅ Database integration with Firebase Firestore.
- ✅ Data Validation and Documentation with pydantic library.
- ✅ Automatic API Documentation with Swagger UI and Redoc (FastAPI Built In).
- ⭐ User Authentication (Register, Login, and Logout) with JWT (Json Web Token).
- ⭐ API Authorization Middleware (Access Token and Refresh Token).
- ⭐ API Testing using pytest library.
- ⭐ Layered Architecture.
- ⭐ Docker Containerization.

---

##  2️⃣ Setup & Installation

### 1. Clone Repository
```sh
git clone <repo-url>
cd simple-api-challenge
```

### 2. Create Virtual Environments

```sh
python -m venv .venv
```

### 3. Activate Virtual Environments


```sh
source .venv/Scripts/activate (bash) || .venv\Scripts\Activate.ps1 (powershell)
```

### 4. Install Package/Dependencies/Libraries

```sh
pip install -r requirements.txt
```


### 5. Environment Variables

Create a `.env` file and configure:

```env
FIREBASE_CREDENTIALS=./app/assets/yourServiceAccountKeyName.json
FIREBASE_PROJECT=your_firebase_project_name

JWT_SECRET_KEY=your_secret_key
KEY=your_secret_key
```

or just copy the `.env.example` to `.env`

```sh
cp .env.example .env (bash) || Copy-Item .env.example .env (powershell)
```


## Setup Firebase Firestore

### 1. Create a Project in the Firebase

- Buka [Firebase Console](https://console.firebase.google.com/) dan buat proyek baru.

### 2. Activate Cloud Firestore

- Go to **Firestore Database** and select **Test Mode** for development.

### 3. Download the Service Account Key

- Go to **Project Overview** > **Project Settings > Service accounts**, and the download **Generate New Private Key**.

### 4. Save or Copy the Service Account Key to the Project

- Save your service account key .json to the `assets` folder.
- Or you can just copy the value of your service account key .json and paste it on the file name `yourServiceAccountKey.json` in the `assets` folder.

---

## 3️⃣ Project Usage

### Manual Run

### 1. Open Terminal and Start the Server

```sh
fastapi dev app/main.py (dev mode)

fastapi run --workers 2 app/main.py (production mode)
```

### 2. Check the API in Your Browser

- **Base URL:** 
  [http://localhost:8000/](http://localhost:8000/)
- **Swagger UI (Dokumentasi API):**
  [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc UI:**
  [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 3. Test the API using PyTest

Open Terminal and type:
```sh
pytest
```

### Run With Docker

### 1. Install Docker Engine (Install Docker Desktop for Easy UI)
- **Docker Installation Guide:** 
[How to Install Docker](https://docs.docker.com/desktop/)
- If you run with docker you just need to set up the **.env** file
- Continue to the next step

### 2. Run with Docker Compose

```sh
docker-compose up --build -d
```

### 3. Check the API in Your Browser

- **Base URL:** 
  [http://localhost:8000/](http://localhost:8000/)
- **Swagger UI (Dokumentasi API):**
  [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc UI:**
  [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 4. Test the API using PyTest

Open Terminal and type:
```sh
pytest
```

## 4️⃣ Demo & Documenatations

### Demo Video URL
[Demo Video URL Google Drive](http://localhost:8000/redoc)

### Architecture & Folder Structure
Explained inside demo video on the minute 

### How It Works
Explained inside demo video on the minute 

---