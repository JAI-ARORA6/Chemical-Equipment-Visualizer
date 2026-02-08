import React, { useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";

import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  ArcElement,
} from "chart.js";
import { Pie } from "react-chartjs-2";

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  Tooltip,
  Legend
);


function Upload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);


  const fetchHistory = async () => {
  try {
    const res = await axios.get(
      "http://127.0.0.1:8000/api/history/",
      {
        auth: {
          username: "jai",
          password: "jai#24arora",
        },
      }
    );
    setHistory(res.data);
  } catch (err) {
    console.error(err);
  }
};

const SummaryCard = ({ title, value }) => (
  <div style={{
    background: "white",
    padding: "20px",
    borderRadius: "10px",
    textAlign: "center",
    boxShadow: "0 2px 6px rgba(0,0,0,0.1)"
  }}>
    <div style={{ color: "#6b7280", marginBottom: "8px" }}>{title}</div>
    <div style={{ fontSize: "26px", fontWeight: "bold" }}>{value}</div>
  </div>
);

const chartCard = {
  background: "white",
  padding: "20px",
  borderRadius: "10px",
  boxShadow: "0 2px 6px rgba(0,0,0,0.1)"
};

const downloadReport = async () => {
  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/api/download-report/",
      {
        auth: {
          username: "jai",
          password: "jai#24arora",
        },
        responseType: "blob",
      }
    );

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "equipment_report.pdf");
    document.body.appendChild(link);
    link.click();
  } catch (err) {
    alert("Download failed");
    console.error(err);
  }
};


const uploadFile = async () => {
  if (!file) return alert("Select a file");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/api/upload/",
      formData,
      {
        auth: {
          username: "jai",
          password: "jai#24arora",
        },
      }
    );

    setResult(response.data);
    fetchHistory();
  } catch (err) {
    alert("Upload failed");
    console.error(err);
  }
};




      

  const pieData = result && {
  labels: Object.keys(result.type_distribution),
  datasets: [
    {
      data: Object.values(result.type_distribution),
      backgroundColor: [
        "#60a5fa",
        "#f87171",
        "#34d399",
        "#fbbf24",
        "#a78bfa",
        "#fb7185",
      ],
    },
  ],
};





  const chartData = result && {
  labels: Object.keys(result.type_distribution),
  datasets: [
    {
      label: "Equipment Count",
      data: Object.values(result.type_distribution),
      backgroundColor: "#4ade80",
    },
  ],
};

  return (
  <div style={{
    maxWidth: "1200px",
    margin: "auto",
    padding: "30px",
    fontFamily: "Arial, sans-serif",
    background: "#f9fafb"
  }}>

    <h1 style={{ textAlign: "center", marginBottom: "30px" }}>
      Chemical Equipment Visualizer
    </h1>

    {/* Upload Card */}
    <div style={{
      background: "white",
      padding: "25px",
      borderRadius: "10px",
      boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
      marginBottom: "40px"
    }}>
      <h2>Upload Equipment CSV</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <br /><br />
      <button
        onClick={uploadFile}
        style={{
          padding: "10px 24px",
          background: "#2563eb",
          color: "white",
          border: "none",
          borderRadius: "6px",
          fontSize: "16px",
          cursor: "pointer"
        }}
      >
        Upload CSV
      </button>
    </div>

    {result && (
      <>
        {/* Summary Cards */}
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gap: "20px",
          marginBottom: "40px"
        }}>
          <SummaryCard title="Total Equipment" value={result.total} />
          <SummaryCard title="Avg Flowrate" value={result.avg_flowrate.toFixed(2)} />
          <SummaryCard title="Avg Pressure" value={result.avg_pressure.toFixed(2)} />
          <SummaryCard title="Avg Temperature" value={result.avg_temperature.toFixed(2)} />
        </div>

        <button
  onClick={downloadReport}
  style={{
    padding: "10px 20px",
    background: "#16a34a",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    marginBottom: "30px"
  }}
>
  Download PDF Report
</button>
  

        {/* Charts */}
        <div style={{
          display: "grid",
          gridTemplateColumns: "2fr 1fr",
          gap: "30px",
          marginBottom: "40px"
        }}>
          <div style={chartCard}>
            <h3>Equipment Type Distribution</h3>
            <Bar data={chartData} />
          </div>

          <div style={chartCard}>
            <h3>Composition</h3>
            <Pie data={pieData} />
          </div>
        </div>
      </>
    )}

    {/* History Table */}
    {history.length > 0 && (
      <div style={{
        background: "white",
        padding: "25px",
        borderRadius: "10px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)"
      }}>
        <h2>Last 5 Uploads</h2>
        <table width="100%" cellPadding="12" style={{ borderCollapse: "collapse" }}>
          <thead style={{ background: "#e5e7eb" }}>
            <tr>
              <th>Name</th>
              <th>Total</th>
              <th>Flow</th>
              <th>Pressure</th>
              <th>Temp</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item, i) => (
              <tr key={i} style={{ textAlign: "center", borderBottom: "1px solid #eee" }}>
                <td>{item.name}</td>
                <td>{item.total_equipment}</td>
                <td>{item.avg_flowrate.toFixed(2)}</td>
                <td>{item.avg_pressure.toFixed(2)}</td>
                <td>{item.avg_temperature.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )}
  </div>
);

}

export default Upload;
