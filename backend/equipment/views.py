from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import FileResponse

from .models import Dataset
from .utils import analyze_csv, generate_pdf_report


# ---------- Upload CSV ----------
import json   # add this at top of file if not present

@api_view(['POST'])
def upload_csv(request):
    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return Response({"error": "No file uploaded"}, status=400)

    summary = analyze_csv(uploaded_file)

    Dataset.objects.create(
        name=uploaded_file.name,
        csv_file=uploaded_file,   # ✅ THIS LINE
        total_equipment=summary["total"],
        avg_flowrate=summary["avg_flowrate"],
        avg_pressure=summary["avg_pressure"],
        avg_temperature=summary["avg_temperature"],
        type_distribution=summary["type_distribution"]
 # ✅ THIS LINE
    )

    return Response(summary, status=200)



# ---------- History ----------
@api_view(['GET'])
def history(request):
    datasets = Dataset.objects.order_by('-uploaded_at')[:5]

    data = []
    for ds in datasets:
        data.append({
            "name": ds.name,
            "uploaded_at": ds.uploaded_at,
            "total_equipment": ds.total_equipment,
            "avg_flowrate": ds.avg_flowrate,
            "avg_pressure": ds.avg_pressure,
            "avg_temperature": ds.avg_temperature,
        })

    return Response(data, status=200)


# ---------- Download PDF ----------
@api_view(['GET'])
def download_report(request):
    dataset = Dataset.objects.order_by('-uploaded_at').first()

    if not dataset:
        return Response({"error": "No data available"}, status=404)

    pdf_buffer = generate_pdf_report(dataset, Dataset.objects.order_by('-uploaded_at')[:5])

    return FileResponse(
        pdf_buffer,
        as_attachment=True,
        filename="equipment_report.pdf"
    )
