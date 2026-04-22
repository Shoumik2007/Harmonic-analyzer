# Harmonic-analyzer
Harmonic Analyzer using FFT and THD (Streamlit App)
# ⚡ Harmonic Analyzer

A Streamlit-based application to analyze electrical signals using **Fast Fourier Transform (FFT)** and compute **Total Harmonic Distortion (THD)**.

---

##  Features

* 📈 Time-domain signal visualization
* 📊 Frequency spectrum using FFT
* 🔍 Automatic harmonic detection
* ⚡ THD (Total Harmonic Distortion) calculation
* 📂 Supports CSV input (time, voltage)
* 🎛 Adjustable noise and frequency (simulated mode)

---

##  Concepts Used

* Fast Fourier Transform (FFT)
* Signal Processing
* Harmonics in Power Systems
* THD Calculation

---

##  Implementation Tools

* Python
* NumPy
* SciPy
* Pandas
* Plotly
* Streamlit

---

##  How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📂 Input Format (CSV)

```text
time, voltage
0.000, 0.12
0.001, 0.45
...
```

---

## 📌 Future Improvements

* Multi-phase signal analysis (V1, V2, V3)
* Noise filtering
* Harmonic classification
* Better UI and charts

---

## 👨‍💻 Author

Shoumik
