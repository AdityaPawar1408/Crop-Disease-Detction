from django.db import models
from django.utils import timezone

class ScanRecord(models.Model):
    """Stores the result of each successful crop disease scan."""
    image_url = models.CharField(max_length=255)
    crop_detected = models.CharField(max_length=50)
    disease_name = models.CharField(max_length=100)
    confidence = models.FloatField()
    severity = models.CharField(max_length=20)
    analysis_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.crop_detected}: {self.disease_name} ({self.analysis_date.strftime('%Y-%m-%d')})"

    class Meta:
        # Order history from newest to oldest
        ordering = ['-analysis_date']