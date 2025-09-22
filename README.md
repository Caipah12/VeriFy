# VeriFy
VeriFy is a final-year project that detects fake news in English text using AI and machine learning. The system focuses on text-only news articles, excluding images and multimedia, and provides a simple way to verify the authenticity of online content.

🔑 Key Features

✅ English-language fake news detection (text-based only)
👥 User & Administrator roles:
Users can register, log in, and check news authenticity
Administrators can manage users, oversee predictions, and monitor system activity

📊 Machine learning models with accuracy, precision, recall, and F1 evaluation
🔍 Explainable outputs with confidence scores and highlighted keywords
🌐 Flask web application with a clean purple-themed interface
⚡ JavaScript for interactive frontend features
💾 MySQL database for user accounts, roles, and history storage

🛠 Tech Stack
Python (Flask, scikit-learn, pandas, numpy)
JavaScript (frontend interactivity & client-side scripts)
HTML/CSS (UI design)

📂 Dataset

The dataset used in this project can be accessed here:
👉 [Google Drive – VeriFy Dataset](https://drive.google.com/drive/folders/1Q7QKDCskRJ0EyoqTENN2t8EUdVaOuoZu)


VeriFy/
│── app.py                     # Main Flask application (entry point)  
│── Fake_News_Det.py            # Fake news detection logic / ML model integration  
│── forms.py                    # Form handling (login, registration, input forms)  
│  
├── models/                     # Model-related files  
│   ├── news_model.py           # Machine learning model code  
│   └── news_model.csv          # Dataset or model-related CSV file  
│  
├── templates/                  # HTML templates for Flask  
│   └── *.html                  # All user & admin interface pages  
│  
├── training_output/  
│   └── executed_notebook.ipynb # Jupyter notebook with training results/output  
│  
├── static/                     # Static files (CSS, JS, Images)  
│   ├── css/  
│   │   ├── admin_styles.css    # Styling for admin pages  
│   │   └── styles.css          # Styling for user pages  
│   │  
│   └── js/  
│       ├── *.js                # JavaScript files for interactivity  
│       └── *.jsx               # React/JSX files if applicable  
│
└── requirements.txt            # Python dependencies (recommended to add)  



Demo User - https://youtu.be/9yTGAQpo9Hw
Demo Admin - https://youtu.be/cTUjPpYdHSA
 
