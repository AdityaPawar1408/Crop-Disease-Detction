<p align="center"> <img src="https://img.shields.io/badge/Django-6.0-success?style=for-the-badge&logo=django"> <img src="https://img.shields.io/badge/TensorFlow-VGG16-orange?style=for-the-badge&logo=tensorflow"> <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python"> <img src="https://img.shields.io/badge/Status-Working-brightgreen?style=for-the-badge"> </p> <p align="center"> <b>An AI-powered Django web application to detect crop diseases from leaf images using a pretrained CNN model.</b> </p>
✨ Overview

Crop Disease Detection is a deep learning–based web application that helps farmers and researchers identify plant diseases from leaf images.
The system uses a VGG16-based CNN model to classify diseases and provides confidence scores, severity levels, and treatment recommendations.

🚀 Key Features

✅ Upload image or capture using camera
✅ Deep Learning model (VGG16 – TensorFlow/Keras)
✅ Disease prediction with confidence (%)
✅ Severity level detection (Low / Moderate / High)
✅ Disease-specific recommendations & prevention tips
✅ Scan history stored in database
✅ Clean & responsive UI
✅ Multilingual-ready (Django i18n support)

🧠 Diseases Supported

🟢 Potato – Healthy

🟡 Potato – Early Blight

🔴 Potato – Late Blight

🔧 Model can be extended for more crops and diseases.

🛠️ Tech Stack
Layer	Technology
Backend	Django
Deep Learning	TensorFlow / Keras
CNN Model	VGG16
Image Processing	Pillow, NumPy
Database	SQLite (Development)
Frontend	HTML, CSS, JavaScript
📂 Project Structure
Crop Disease Detection/
│
├── manage.py
├── db.sqlite3                # SQLite DB (ignored)
│
├── crop_detection/           # Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── detector/                 # Main app
│   ├── views.py              # ML + Django logic
│   ├── models.py
│   ├── templates/
│   ├── static/
│   └── migrations/
│
├── media/                    # Uploaded images (ignored)
├── 1/                        # Pretrained models (ignored)
│   └── potato_disease_vgg16.keras
│
├── .gitignore
└── README.md

⚙️ Installation & Setup
1️⃣ Clone Repository
git clone <your-github-repo-url>
cd Crop-Disease-Detection

2️⃣ Create Virtual Environment
python -m venv .venv


Activate:

Windows

.venv\Scripts\activate


Linux / macOS

source .venv/bin/activate

3️⃣ Install Dependencies
pip install django tensorflow pillow numpy


⚠️ TensorFlow works best with Python ≤ 3.12

▶️ Run the Project
python manage.py migrate
python manage.py runserver


Open browser:

http://127.0.0.1:8000/

🔍 How It Works

User uploads or scans a leaf image

Image is resized & normalized

CNN model predicts disease

Confidence (%) & severity calculated

Recommendations shown

Result stored in history

📊 Sample Output
Field	Example
Disease	Potato – Late Blight
Confidence	96.23%
Severity	High
Recommendation	Apply Mancozeb fungicide
🧪 Model Information

Model: VGG16 CNN

Framework: TensorFlow / Keras

Input Size: 224 × 224

Stored in 1/ directory (gitignored)

Update model path in:

detector/views.py

🚀 Deployment Notes

For production:

Set DEBUG = False

Use PostgreSQL

Serve static files using WhiteNoise / S3

Store secrets in environment variables

Use Gunicorn + Nginx

🤝 Contributing

Pull requests are welcome!

Fork the repo

Create feature branch

Commit changes

Open PR

📄 License

This project is intended for educational & academic purposes.
Add a LICENSE file if open-sourcing.

👨‍💻 Author

Aditya Pawar

AI & Data Science

Final Year Project – Crop Disease Detection 🌾
