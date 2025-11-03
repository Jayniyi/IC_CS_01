// static/js/charts.js
// A reusable Chart.js configuration for your security scanner dashboard

document.addEventListener("DOMContentLoaded", () => {
  const ctx = document.getElementById("vulnChart");
  if (!ctx) return; // If no chart element, skip

  // You can pass data dynamically from Flask as data attributes
  const sqlCount = parseInt(ctx.dataset.sql || "0");
  const xssCount = parseInt(ctx.dataset.xss || "0");
  const totalScans = parseInt(ctx.dataset.total || "0");

  const data = {
    labels: ["SQL Injection", "XSS"],
    datasets: [
      {
        label: "Vulnerabilities Detected",
        data: [sqlCount, xssCount],
        backgroundColor: [
          "rgba(239, 68, 68, 0.8)", // red
          "rgba(250, 204, 21, 0.8)" // yellow
        ],
        borderColor: [
          "rgba(185, 28, 28, 1)", // dark red
          "rgba(202, 138, 4, 1)"  // dark yellow
        ],
        borderWidth: 1,
        borderRadius: 8
      }
    ]
  };

  const config = {
    type: "bar",
    data,
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: `Vulnerability Summary (${totalScans} Scans Total)`,
          color: "#1e293b",
          font: { size: 18, weight: "bold" }
        },
        legend: { display: false },
        tooltip: {
          backgroundColor: "#1e293b",
          titleColor: "#f1f5f9",
          bodyColor: "#f1f5f9",
          padding: 12
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: "#334155", font: { weight: "600" } }
        },
        y: {
          beginAtZero: true,
          grid: { color: "rgba(203, 213, 225, 0.3)" },
          ticks: { color: "#475569" }
        }
      }
    }
  };

  new Chart(ctx, config);
});
