from django.urls import path
from . import views

app_name = 'detector' 

urlpatterns = [
    # Main Landing Page (Index)
    path('', views.index, name='index'), 
    
    # NEW: Dedicated Scan/Upload Page
    path('scan/', views.scan_view, name='scan'),

    path('result/', views.result_view, name='result'), # Re-added URL path


     path('result/download/', views.download_report, name='download'),
    path('result/share/', views.share_results, name='share'),
    path('history/', views.view_history, name='history'), # Often linked directly from root
    path('chat-api/', views.chat_api, name='chat_api'),
]