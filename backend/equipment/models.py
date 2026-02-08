from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    total_equipment = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()

    # ✅ ADD THIS FIELD
    type_distribution = models.JSONField(null=True, blank=True)

    # optional but good
    csv_file = models.FileField(upload_to="csvs/", null=True, blank=True)

    def __str__(self):
        return self.name
