import sys
import requests

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout,
    QLabel, QPushButton, QFileDialog, QMessageBox,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QSizePolicy
)
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# ---------- CONFIG ----------
BASE_URL = "https://chemical-equipment-visualizer-4-rn0v.onrender.com"

API_UPLOAD_URL = f"{BASE_URL}/api/upload/"
API_HISTORY_URL = f"{BASE_URL}/api/history/"
API_PDF_URL = f"{BASE_URL}/api/download-report/"

USERNAME = "jai"
PASSWORD = "jai#24arora"



class ResponsiveCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()


class EquipmentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.resize(1200, 800)

        self.data = None
        main_layout = QVBoxLayout(self)

        # ---------- Title ----------
        title = QLabel("Chemical Equipment Visualizer (Desktop)")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        main_layout.addWidget(title)

        # ---------- Buttons ----------
        btn_layout = QHBoxLayout()
        upload_btn = QPushButton("Upload CSV")
        upload_btn.clicked.connect(self.upload_csv)

        pdf_btn = QPushButton("Download PDF Report")
        pdf_btn.clicked.connect(self.download_pdf)

        btn_layout.addWidget(upload_btn)
        btn_layout.addWidget(pdf_btn)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)

        # ---------- Summary ----------
        summary_grid = QGridLayout()

        self.total_lbl = QLabel()
        self.flow_lbl = QLabel()
        self.pressure_lbl = QLabel()
        self.temp_lbl = QLabel()

        for lbl in [self.total_lbl, self.flow_lbl, self.pressure_lbl, self.temp_lbl]:
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("""
                QLabel {
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    padding: 15px;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)

        summary_grid.addWidget(self.total_lbl, 0, 0)
        summary_grid.addWidget(self.flow_lbl, 0, 1)
        summary_grid.addWidget(self.pressure_lbl, 1, 0)
        summary_grid.addWidget(self.temp_lbl, 1, 1)

        main_layout.addLayout(summary_grid)

        # ---------- Charts ----------
        charts_layout = QHBoxLayout()

        self.bar_canvas = ResponsiveCanvas()
        self.bar_ax = self.bar_canvas.fig.add_subplot(111)

        self.pie_canvas = ResponsiveCanvas()
        self.pie_ax = self.pie_canvas.fig.add_subplot(111)

        charts_layout.addWidget(self.bar_canvas, 2)
        charts_layout.addWidget(self.pie_canvas, 1)

        main_layout.addLayout(charts_layout)

        # ---------- History ----------
        history_label = QLabel("Last 5 Uploads")
        history_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(history_label)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["Name", "Total", "Avg Flow", "Avg Pressure", "Avg Temp"]
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(
            self.table.horizontalHeader().ResizeToContents
        )
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout.addWidget(self.table)

        self.fetch_history()

    # ---------- Upload CSV ----------
    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        with open(file_path, "rb") as f:
            response = requests.post(
                API_UPLOAD_URL,
                files={"file": f},
                auth=(USERNAME, PASSWORD)
            )

        if response.status_code != 200:
            QMessageBox.critical(self, "Error", "Upload failed")
            return

        self.data = response.json()
        self.update_summary()
        self.update_charts()
        self.fetch_history()

    # ---------- Summary ----------
    def update_summary(self):
        self.total_lbl.setText(f"Total Equipment\n{self.data['total']}")
        self.flow_lbl.setText(f"Avg Flowrate\n{self.data['avg_flowrate']:.2f}")
        self.pressure_lbl.setText(f"Avg Pressure\n{self.data['avg_pressure']:.2f}")
        self.temp_lbl.setText(f"Avg Temperature\n{self.data['avg_temperature']:.2f}")

    # ---------- Charts ----------
    def update_charts(self):
        types = list(self.data["type_distribution"].keys())
        counts = list(self.data["type_distribution"].values())

        # Bar chart
        self.bar_ax.clear()
        self.bar_ax.bar(types, counts, color="skyblue")
        self.bar_ax.set_title("Equipment Type Distribution")
        self.bar_ax.tick_params(axis='x', rotation=30)
        self.bar_canvas.fig.tight_layout()
        self.bar_canvas.draw()

        # Pie chart
        self.pie_ax.clear()
        self.pie_ax.pie(
            counts,
            labels=types,
            autopct="%1.1f%%",
            startangle=90
        )
        self.pie_ax.set_title("Composition")
        self.pie_canvas.fig.tight_layout()
        self.pie_canvas.draw()

    # ---------- History ----------
    def fetch_history(self):
        response = requests.get(API_HISTORY_URL, auth=(USERNAME, PASSWORD))
        if response.status_code != 200:
            return

        data = response.json()
        self.table.setRowCount(len(data))

        for row, item in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(item["total_equipment"])))
            self.table.setItem(row, 2, QTableWidgetItem(f"{item['avg_flowrate']:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{item['avg_pressure']:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{item['avg_temperature']:.2f}"))

    # ---------- PDF ----------
    def download_pdf(self):
        response = requests.get(API_PDF_URL, auth=(USERNAME, PASSWORD))
        if response.status_code != 200:
            QMessageBox.critical(self, "Error", "PDF download failed")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", "equipment_report.pdf", "PDF Files (*.pdf)"
        )
        if path:
            with open(path, "wb") as f:
                f.write(response.content)

            QMessageBox.information(self, "Success", "PDF downloaded")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EquipmentApp()
    window.show()
    sys.exit(app.exec_())
