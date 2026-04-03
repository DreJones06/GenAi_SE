# 🎮 Advanced Tetris Web App

A full-stack Tetris game built using **Flask (Python)** for the backend and **React (JavaScript)** for the frontend.
This project demonstrates real-time game logic, REST API integration, and interactive UI design.

---

## 🚀 Features

* 🎮 Classic Tetris gameplay
* 🔄 Piece rotation
* ⬅️➡️ Movement controls
* ⬇️ Soft drop
* 🎯 Score tracking system
* 🚨 Game Over detection
* 🔄 Restart functionality
* 🎨 Colorful block palette
* 🌙 Clean dark-themed UI

---

## 🧱 Tech Stack

### Backend

* Python
* Flask
* Flask-CORS

### Frontend

* React
* JavaScript (ES6)
* CSS Grid / Flexbox

---

## 🧠 Architecture

React frontend communicates with Flask backend via REST APIs:

```
React UI  <--->  Flask API  <--->  Game Logic Engine
```

* Flask handles:

  * Game state
  * Collision detection
  * Scoring
* React handles:

  * Rendering UI
  * User input (keyboard)
  * Game updates

---

## ⚙️ Setup Instructions

### 🔹 1. Clone Repository

```
git clone <your-repo-url>
cd project-folder
```

---

### 🔹 2. Backend Setup (Flask)

```
cd backend
python -m venv venv
venv\\Scripts\\activate   # Windows
pip install flask flask-cors
python app.py
```

Backend runs on:

```
http://127.0.0.1:5000
```

---

### 🔹 3. Frontend Setup (React)

> Make sure Node.js is installed

```
cd frontend/tetris-ui
npm install
npm start
```

Frontend runs on:

```
http://localhost:3000
```

---

## 🎮 Controls

| Key      | Action       |
| -------- | ------------ |
| ⬅️ Left  | Move Left    |
| ➡️ Right | Move Right   |
| ⬇️ Down  | Soft Drop    |
| ⬆️ Up    | Rotate Piece |

---

## 🔄 Restart Game

Click the **Restart Button** to reset:

* Score
* Grid
* Game state

---

## 📸 Screenshots (Optional)

*Add screenshots here for better presentation*

---

## 🚀 Future Enhancements

* 👻 Ghost piece preview
* ⏬ Hard drop (spacebar)
* 📦 Next piece preview
* 🏆 Leaderboard (DB integration)
* 🔊 Sound effects
* 🤖 AI-based move suggestions

---

## 💡 Learning Outcomes

* Full-stack development (Flask + React)
* REST API integration
* Game logic implementation
* State management
* UI/UX design fundamentals

---

## 👨‍💻 Author

**Andre Jones**

---

## 📜 License

This project is open-source and available under the MIT License.
