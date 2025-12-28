Crop Disease Detection Web Application

A Django-based AI web application that detects crop diseases from leaf images using a pretrained deep learning model (VGG16).
Users can upload or capture plant images, get instant disease predictions with confidence scores, view recommendations, and access scan history.

🚀 Project Highlights

✅ AI-powered crop disease detection (Potato leaf diseases)

✅ Image upload and camera scan support

✅ Confidence score & severity level analysis

✅ Disease-specific treatment & prevention tips

✅ Scan history stored in database

✅ Clean UI with result visualization

✅ Multilingual-ready (Django i18n support)

🧠 Diseases Supported

Potato – Early Blight

Potato – Late Blight

Potato – Healthy

(Model can be extended to other crops & diseases)

🛠️ Tech Stack
Layer	Technology
Backend	Django
ML Model	TensorFlow / Keras (VGG16)
Image Processing	Pillow, NumPy
Database	SQLite (dev)
Frontend	HTML, CSS, JavaScript
Server	Django Development Server
📂 Project Structure
Crop Disease Detection/
│
├── manage.py
├── db.sqlite3                  # Local database (ignored in git)
│
├── crop_detection/             # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── detector/                   # Main Django app
│   ├── views.py                # Core logic (ML + Django)
│   ├── models.py               # ScanRecord model
│   ├── templates/
│   ├── static/
│   └── migrations/
│
├── media/                      # Uploaded images (gitignored)
│
├── 1/                          # Pretrained ML models (gitignored)
│   └── potato_disease_vgg16.keras
│
├── .gitignore
├── README.md

⚙️ Installation & Setup
1️⃣ Clone the repository
git clone <your-repo-url>
cd Crop-Disease-Detection

2️⃣ Create virtual environment
python -m venv .venv


Activate it:

Windows (PowerShell)

.venv\Scripts\activate


Linux / macOS

source .venv/bin/activate

3️⃣ Install dependencies

If requirements.txt exists:

pip install -r requirements.txt


Otherwise install manually:

pip install django tensorflow pillow numpy


⚠️ TensorFlow requires Python ≤ 3.12

▶️ Running the Project Locally
Apply migrations
python manage.py migrate

(Optional) Create admin user
python manage.py createsuperuser

Start development server
python manage.py runserver

Open in browser
http://127.0.0.1:8000/

📸 How It Works

User uploads or captures a leaf image

Image is preprocessed (resize + normalization)

VGG16-based CNN predicts disease class

Confidence (%) and severity are calculated

Result page shows:

Disease name

Confidence score

Severity level

Treatment recommendations

Prevention tips

Scan result is stored in database

📊 Output Example

Disease: Potato – Late Blight

Confidence: 96.23%

Severity: High

Recommendation: Apply Mancozeb fungicide immediately

🧪 Model & Large Files

Pretrained model files are stored in the 1/ directory

These files are ignored by .gitignore due to large size

Update model path in:

detector/views.py

MODEL_PATH = os.path.join(settings.BASE_DIR, '1/potato_disease_vgg16.keras')

🧾 Notes

media/ folder stores uploaded images (do NOT commit)

SQLite is used only for development

Internationalization (gettext_lazy) is already integrated

Designed for college projects, demos & hackathons

🚀 Deployment (Production)

For production:

Set DEBUG = False

Use PostgreSQL instead of SQLite

Serve static files using WhiteNoise or AWS S3

Store secrets in environment variables

Use Gunicorn + Nginx

🤝 Contributing

Contributions are welcome!

Fork the repo

Create a feature branch

Commit with clear messages

Open a pull request

📄 License

This project is intended for educational and academic use.
Add a LICENSE file if you plan to open-source it.

👨‍💻 Author

Aditya Pawar
AI & Data Science Enthusiast
Final Year Project – Crop Disease Detection 🌾