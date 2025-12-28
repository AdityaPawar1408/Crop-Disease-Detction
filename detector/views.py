from .models import ScanRecord 
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.utils import timezone 
from django.http import HttpResponse, JsonResponse 
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from django.conf import settings
import numpy as np
import os
import uuid
import logging
from django.utils.translation import gettext_lazy as _ # Required for translation

# Set up logging
logger = logging.getLogger(__name__)

# --- Model and Constants Setup ---

IMAGE_SIZE = (224, 224) 

try:
    MODEL_PATH = os.path.join(settings.BASE_DIR, '1/potato_disease_vgg16.keras')
    model = load_model(MODEL_PATH, compile=False)
    logger.info("CNN VGG16 model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model from {MODEL_PATH}: {e}")
    model = None

CLASS_NAMES = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___Healthy']

# Disease info map (All strings wrapped with _() for translation)
DISEASE_INFO = {
    'Potato___Healthy': {
        'description': _('The leaf is healthy. No disease detected. Keep up the good work!'),
        'color': '#28a745', 
        'recommendations': [
            {'text': _('Apply water regularly.'), 'priority': 'low'},
            {'text': _('Monitor plant daily for early signs of disease.'), 'priority': 'low'},
        ],
        'prevention_tips': [
            _('Monitor closely for pests and new disease symptoms.'),
            _('Maintain optimal soil moisture and nutrient levels.'),
            _('Ensure adequate spacing for good air circulation.'),
        ],
    },
    'Potato___Early_blight': {
        'description': _('Caused by fungus Alternaria solani. Symptoms: dark spots, yellowing leaves.'),
        'color': '#ffc107',
        'recommendations': [
            {'text': _('Apply approved copper fungicide (e.g., Chlorothalonil) immediately.'), 'priority': 'high'},
            {'text': _('Ensure good air circulation around the plants.'), 'priority': 'medium'},
            {'text': _('Avoid overhead watering.'), 'priority': 'medium'},
        ],
        'prevention_tips': [
            _('Practice crop rotation every 2-3 years.'),
            _('Destroy infected plant debris immediately after harvest.'),
            _('Avoid working in the garden when leaves are wet.'),
        ],
    },
    'Potato___Late_blight': {
        'description': _('Caused by Phytophthora infestans. Symptoms: brown lesions, rotting. Urgent action required!'),
        'color': '#dc3545',
        'recommendations': [
            {'text': _('Immediately remove and destroy infected plant parts.'), 'priority': 'high'},
            {'text': _('Apply systemic fungicide (e.g., Mancozeb).'), 'priority': 'high'},
            {'text': _('Monitor neighboring plants closely.'), 'priority': 'medium'},
        ],
        'prevention_tips': [
            _('Use certified disease-free potato seed.'),
            _('Apply preventive fungicide sprays during wet or humid weather.'),
            _('Improve drainage and avoid excessive nitrogen fertilizer.'),
        ],
    }
}

# --- Prediction Function ---
def predict_disease(img_path):
    if model is None:
        return "Prediction Error", 0.0, "Model failed to load on server startup."
    
    try:
        img = image.load_img(img_path, target_size=IMAGE_SIZE)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        prediction = model.predict(img_array)[0]
        predicted_class = CLASS_NAMES[np.argmax(prediction)]
        confidence = float(np.max(prediction)) * 100   # ✅ FIX

        return predicted_class, confidence, None

    except Exception as e:
        logger.error(f"Prediction error for image {img_path}: {e}")
        return "Prediction Error", 0.0, str(e)

# --- Index View (Landing Page) ---
def index(request):
    """Renders the main landing page (index.html)."""
    if request.method == 'POST':
        return scan_view(request)
    return render(request, 'detector/index.html')

# --- Scan View (Upload Form Handler) ---
def scan_view(request):
    """
    Handles image upload (POST) from traditional file OR camera Base64 data, 
    and renders the scan page (GET).
    """
    
    if request.method == 'POST':
        file = request.FILES.get('image_file') 
        image_data_b64 = request.POST.get('image_data')
        
        save_path = None
        image_url = None

        if file or image_data_b64:
            try:
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                
                if file:
                    ext = file.name.split('.')[-1]
                    filename = f"{uuid.uuid4()}.{ext}"
                    save_name = fs.save(filename, file)
                elif image_data_b64:
                    import io
                    import base64
                    from PIL import Image
                    if ',' in image_data_b64:
                        header, base64_data = image_data_b64.split(',', 1)
                    else:
                        base64_data = image_data_b64
                    image_bytes = base64.b64decode(base64_data)
                    image_obj = Image.open(io.BytesIO(image_bytes))
                    filename = f"{uuid.uuid4()}.jpeg"
                    save_name = fs.get_available_name(filename)
                    temp_path = os.path.join(settings.MEDIA_ROOT, save_name)
                    image_obj.save(temp_path, format="JPEG")
                    save_name = os.path.basename(temp_path) 
                
                save_path = os.path.join(settings.MEDIA_ROOT, save_name)
                image_url = settings.MEDIA_URL + save_name
                
                predicted_class, confidence, error = predict_disease(save_path)
                
                if not error:
                    if confidence >= 90:
                        severity_level = 'High'
                    elif confidence >= 60:
                        severity_level = 'Moderate'
                    else:
                        severity_level = 'Low'

                    info = DISEASE_INFO.get(predicted_class, {})
                    
                    # --- CRITICAL FIX: Serialize lazy strings before session save ---
                    safe_recommendations = [
                        {'text': str(rec['text']), 'priority': rec['priority']} 
                        for rec in info.get('recommendations', [])
                    ]
                    safe_prevention_tips = [
                        str(tip) for tip in info.get('prevention_tips', [])
                    ]
                    
                    analysis_data = {
                        'image_url': image_url,
                        'crop_detected': "Potato",
                        'disease_name': predicted_class,
                        'confidence': round(confidence, 2),
                        'color': info.get('color', '#dc3545'),
                        'severity': severity_level, 
                        'analysis_date': timezone.now().strftime('%m/%d/%Y'),
                        'recommendations': safe_recommendations, # Use safe list
                        'prevention_tips': safe_prevention_tips, # Use safe list
                        'probability_data': [
                            {'label': predicted_class.split('___')[-1], 'value': round(confidence)},
                            {'label': 'Healthy', 'value': max(0, 100 - round(confidence) - 5)},
                            {'label': 'Other', 'value': 5},
                        ],
                    }
                    
                    ScanRecord.objects.create(
                        image_url=analysis_data['image_url'],
                        crop_detected=analysis_data['crop_detected'],
                        disease_name=analysis_data['disease_name'],
                        confidence=analysis_data['confidence'],
                        severity=analysis_data['severity'],
                    )
                    
                    request.session['analysis_data'] = analysis_data
                else:
                    request.session['analysis_data'] = {'error': error, 'image_url': image_url}
                    
                return redirect('detector:result')

            except Exception as e:
                logger.error(f"Unhandled critical error in scan_view: {e}")
                error_context = {
                    'error': f"A critical server error occurred: {e}",
                    'image_url': image_url 
                }
                request.session['analysis_data'] = error_context
                return redirect('detector:result')

    return render(request, 'detector/scan.html')

# --- Result View (Handles Session AND History Lookup) ---
def result_view(request):
    record_id = request.GET.get('record_id')
    analysis_data = None
    
    if record_id:
        try:
            record = get_object_or_404(ScanRecord, pk=record_id)
            info = DISEASE_INFO.get(record.disease_name, {})
            
            # --- CRITICAL FIX: Serialize lazy strings from DB load ---
            safe_recommendations = [
                {'text': str(rec['text']), 'priority': rec['priority']} 
                for rec in info.get('recommendations', [])
            ]
            safe_prevention_tips = [
                str(tip) for tip in info.get('prevention_tips', [])
            ]

            analysis_data = {
                'image_url': record.image_url,
                'crop_detected': record.crop_detected,
                'disease_name': record.disease_name,
                'confidence': record.confidence, 
                'color': info.get('color', '#dc3545'),
                'severity': record.severity, 
                'analysis_date': record.analysis_date.strftime('%m/%d/%Y'),
                'recommendations': safe_recommendations, # Use safe list
                'prevention_tips': safe_prevention_tips, # Use safe list
                'probability_data': [{'label': 'Loaded from DB', 'value': 100}] 
            }
            request.session.pop('analysis_data', None) 
        except Exception:
            pass

    if analysis_data is None:
        analysis_data = request.session.get('analysis_data')
    
    if not analysis_data:
        return redirect('detector:index')

    if isinstance(analysis_data.get('confidence'), (float, int)):
        analysis_data['confidence'] = f"{analysis_data['confidence']:.2f}"
    
    return render(request, 'detector/result.html', analysis_data)

# --- Quick Action Views ---
def download_report(request):
    """Simulates generating a report for download."""
    analysis_data = request.session.get('analysis_data', {})
    
    # --- CRITICAL FIX: Serialize lazy strings for report text ---
    # Note: This report will be in the language active *at the time of download*
    safe_recommendations = [
        {'text': str(rec['text']), 'priority': rec['priority']} 
        for rec in analysis_data.get('recommendations', [])
    ]

    report_content = f"""
    --- {_('CropCare Disease Report')} ---
    {_('Analysis Date')}: {analysis_data.get('analysis_date', 'N/A')}
    {_('Crop Detected')}: {analysis_data.get('crop_detected', 'N/A')}
    {_('Disease')}: {analysis_data.get('disease_name', 'N/A')}| {_('Confidence')}: {analysis_data.get('confidence', 'N/A')}%
    {_('Severity')}: {analysis_data.get('severity', 'N/A')}
    
    {_('Treatment Recommendations')}:
    --------------------------
    """
    for rec in safe_recommendations:
        report_content += f"- [{str(_(rec['priority'])).upper()}] {rec['text']}\n"
        
    response = HttpResponse(report_content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="cropcare_report.txt"'
    
    return response

def share_results(request):
    """Simulates generating a shareable URL."""
    shareable_url = request.build_absolute_uri(request.path_info)
    return JsonResponse({
        'status': 'success',
        'message': 'Shareable link generated!',
        'link': shareable_url,
    })

def view_history(request):
    """Retrieves all past scan records from the database and renders history.html."""
    history_records = ScanRecord.objects.all()[:50] 
    return render(request, 'detector/history.html', {'history_records': history_records})


def chat_api(request):
    if request.method == 'POST':
        message = request.POST.get('message', '').lower()
        
        # We must use str() to compare the translated string to the user's message
        # Or, even better, check against the plain English string directly
        
        # --- SIMPLEST FIX: Check for English keywords ---
        # This assumes the user types keywords in English even if the UI is Marathi
        
        if 'hello' in message or 'hi' in message:
            response_text = str(_("Hi there! How can I help you today?"))
        
        elif 'healthy' in message:
            response_text = str(_("For healthy plants: Apply water regularly and monitor daily for early signs of disease."))
        
        elif 'late blight' in message:
            response_text = str(_("Late Blight: This is a serious disease. Immediately remove and destroy infected plant parts. Apply systemic fungicide (e.g., Mancozeb)."))
        
        elif 'early blight' in message:
            response_text = str(_("Early Blight: Apply an approved copper fungicide immediately and ensure good air circulation."))
        
        elif 'prevention' in message:
            response_text = str(_("Prevention: Use certified disease-free seeds, practice crop rotation, and apply preventive sprays during wet weather."))
        
        else:
            response_text = str(_("I'm sorry, I don't understand. Please ask about potato diseases or prevention."))

        return JsonResponse({'reply': response_text})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)