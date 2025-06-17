# NutriAI – Instant Nutritional Information  
*Advancing Nutrition Science Through Gemini AI*

## 🔍 Overview
NutriAI is a Streamlit web-app that delivers calorie & macronutrient data for any comma-separated food list using Google **Gemini 1.5 Flash**.

## 🏗️ Architecture
![image](https://github.com/user-attachments/assets/1d00d11b-51bb-4846-a87b-d26a1077ccdf)


## ⚙️ Tech Stack
* **Frontend** – Streamlit  
* **LLM** – Gemini 1.5 Flash (or any model selectable in sidebar)  
* **Language** – Python 3.11

## 🚀 Quick Start
```bash
git clone https://github.com/nitin200411/NutriAI.git
cd NutriAI
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export GOOGLE_API_KEY="AIzaSyAhUQ1a_HuaZXjTK2MXozz8RVqmzb1XLQo"  
streamlit run app.py
