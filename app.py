import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks

st.title("Harmonic Analyzer using FFT")

# -------------------------------
# INPUT MODE
# -------------------------------
mode = st.radio("Select Input Mode:", ["Simulated Signal", "Upload CSV"])

# -------------------------------
# SIMULATED SIGNAL
# -------------------------------
st.markdown("""
###  Simulated Signal Description

The generated signal is composed of:

- **Fundamental Component**: Base sinusoidal waveform (e.g., 50 Hz)
- **Harmonics**: Integer multiples of the base frequency (3rd, 5th, etc.)
- **Noise**: Random Gaussian noise to simulate real-world disturbances

This allows analysis of how distortion affects the frequency spectrum and Total Harmonic Distortion (THD).
""")
if mode == "Simulated Signal":
    fs = 12000
    t = np.linspace(0, 1, fs, endpoint=False)

    frequency = st.sidebar.number_input("Base Frequency (Hz)",min_value=50,max_value=1000,value=50)
    noise_level = st.sidebar.slider("Noise Level", 0.0, 1.0, 0.2)

    signal = (
        np.sin(2*np.pi*frequency*t)
        + 0.3*np.sin(2*np.pi*3*frequency*t)
        + 0.6*np.sin(2*np.pi*5*frequency*t)
        + noise_level*np.random.randn(len(t))
    )

# -------------------------------
# CSV INPUT
# -------------------------------
else:
    st.info("Upload CSV with columns: time, voltage")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is None:
        st.stop()

    data = pd.read_csv(uploaded_file)

    if 'time' in data.columns and 'voltage' in data.columns:
        t = data['time'].values
        signal = data['voltage'].values
    else:
        signal = data.iloc[:, 0].values
        fs = st.number_input("Sampling Frequency (Hz)", value=1000)
        t = np.linspace(0, len(signal)/fs, len(signal), endpoint=False)

# -------------------------------
# FFT
# -------------------------------
N = len(signal)
if N < 2:
    st.error("Need at least 2 samples to calculate FFT.")
    st.stop()

dt = t[1] - t[0]

yf = fft(signal)
xf = fftfreq(N, dt)

positive_freqs = xf[:N//2]
magnitude = 2.0/N * np.abs(yf[:N//2])

# -------------------------------
# PEAK DETECTION
# -------------------------------
threshold = st.sidebar.slider("Peak Sensitivity", 0.01, 0.5, 0.1)

peaks, properties = find_peaks(magnitude, height=threshold)

peak_freqs = positive_freqs[peaks]
peak_mags = magnitude[peaks]

# -------------------------------
# FUNDAMENTAL
# -------------------------------
valid = peak_freqs > 1
valid_peak_freqs = peak_freqs[valid]
valid_peak_mags = peak_mags[valid]

if len(valid_peak_freqs) == 0:
    st.error("No valid frequency peak found. Try lowering the peak detection threshold.")
    st.stop()

fundamental_index = np.argmin(valid_peak_freqs)
f1 = valid_peak_freqs[fundamental_index]
V1 = valid_peak_mags[fundamental_index]

# -------------------------------
# HARMONICS
# -------------------------------
harmonics = []

for f, mag in zip(peak_freqs, peak_mags):
    ratio = f / f1

    if abs(ratio - round(ratio)) < 0.1:
        harmonics.append((f, mag))

# -------------------------------
# THD
# -------------------------------
harmonic_power = []

for f, mag in harmonics:
    if abs(f - f1) > 1:
        harmonic_power.append(mag**2)

THD = np.sqrt(sum(harmonic_power)) / V1

# -------------------------------
# TIME DOMAIN PLOT
# -------------------------------
st.markdown("---")
st.header("📈 Time Domain")
fig_time = go.Figure()
fig_time.add_trace(go.Scatter(x=t[:2000], y=signal[:2000], mode='lines'))

fig_time.update_layout(
    title="Time Domain (Zoomed)",
    xaxis_title="Time (s)",
    yaxis_title="Amplitude"
)

st.plotly_chart(fig_time)

# -------------------------------
# FFT PLOT
# -------------------------------
st.markdown("---")
st.header("📊 Frequency Domain")
fig_fft = go.Figure()

fig_fft.add_trace(go.Scatter(
    x=positive_freqs,
    y=magnitude,
    mode='lines',
    name='Spectrum'
))

# Mark peaks
fig_fft.add_trace(go.Scatter(
    x=peak_freqs,
    y=peak_mags,
    mode='markers',
    marker=dict(size=10,color='red'),
    name='Peaks'
))

fig_fft.update_layout(
    title="Frequency Spectrum",
    xaxis_title="Frequency (Hz)",
    yaxis_title="Magnitude"
)

st.plotly_chart(fig_fft)

# -------------------------------
# RESULTS
# -------------------------------
st.markdown("---")
st.header("📊 Results")

col1, col2 = st.columns(2)

with col1:
    st.metric("THD (%)", f"{THD*100:.2f}")

with col2:
    st.metric("Fundamental (Hz)", f"{f1:.2f}")

st.subheader("Detected Harmonics")
for f, mag in harmonics:
    st.write(f"{f:.2f} Hz → {mag:.3f}")
