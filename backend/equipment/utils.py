import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import tempfile




def analyze_csv(file):
    df = pd.read_csv(file)

    summary = {
        "total": int(len(df)),
        "avg_flowrate": float(df["Flowrate"].mean()),
        "avg_pressure": float(df["Pressure"].mean()),
        "avg_temperature": float(df["Temperature"].mean()),
        "type_distribution": df["Type"].value_counts().to_dict()
    }

    return summary


def generate_pdf_report(dataset, history):
    import json
    import tempfile
    from io import BytesIO
    from datetime import datetime
    import matplotlib.pyplot as plt
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # ================= PAGE 1 =================
    y = height - 50

    # ----- Title -----
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Chemical Equipment Analysis Report")
    y -= 25

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
    y -= 40

    # ----- Summary -----
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Summary")
    y -= 20

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Total Equipment: {dataset.total_equipment}")
    y -= 15
    c.drawString(50, y, f"Average Flowrate: {dataset.avg_flowrate:.2f}")
    y -= 15
    c.drawString(50, y, f"Average Pressure: {dataset.avg_pressure:.2f}")
    y -= 15
    c.drawString(50, y, f"Average Temperature: {dataset.avg_temperature:.2f}")
    y -= 30

    # ----- Charts -----
    type_dist = (
    json.loads(dataset.type_distribution)
    if isinstance(dataset.type_distribution, str)
    else dataset.type_distribution
)
    labels = list(type_dist.keys())
    values = list(type_dist.values())

    # Bar chart
    bar_img = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    plt.figure(figsize=(5, 3))
    plt.bar(labels, values)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(bar_img.name)
    plt.close()

    # Pie chart
    pie_img = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    plt.figure(figsize=(4, 4))
    plt.pie(values, labels=labels, autopct="51.1f%%")
    plt.tight_layout()
    plt.savefig(pie_img.name)
    plt.close()

    # Draw charts side-by-side
    c.drawImage(bar_img.name, 40, y - 180, width=240, height=160)
    c.drawImage(pie_img.name, 320, y - 180, width=200, height=160)

    # ================= PAGE 2 =================
    c.showPage()

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Last 5 Uploads")
    y -= 25

    c.setFont("Helvetica", 10)

    for h in history:
        line = (
            f"{h.name} | "
            f"Total: {h.total_equipment} | "
            f"Flow: {h.avg_flowrate:.2f} | "
            f"Pressure: {h.avg_pressure:.2f} | "
            f"Temp: {h.avg_temperature:.2f}"
        )
        c.drawString(50, y, line)
        y -= 15

        # Safety: move to new page if needed
        if y < 60:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)

    c.save()
    buffer.seek(0)
    return buffer

