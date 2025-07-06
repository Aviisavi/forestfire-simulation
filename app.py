
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# ---- Sidebar Input ----
st.sidebar.title("Environment Inputs")
temp = st.sidebar.slider("Temperature (°C)", 20, 45, 30)
humidity = st.sidebar.slider("Humidity (%)", 10, 90, 40)
wind_speed = st.sidebar.slider("Wind Speed (0-5)", 0, 5, 2)
veg_density = st.sidebar.slider("Vegetation Density (1-5)", 1, 5, 3)

# ---- Predict Fire Spread Speed ----
data = pd.DataFrame({
    "Temperature": [temp],
    "Humidity": [humidity],
    "WindSpeed": [wind_speed],
    "VegetationDensity": [veg_density]
})

# Dummy model (pretend-trained for simplicity)
def get_spread_speed(temp, humidity, wind_speed, veg):
    if temp > 35 and humidity < 30 and wind_speed > 2 and veg > 3:
        return 2  # Fast
    elif temp > 28 and humidity < 50:
        return 1  # Medium
    else:
        return 0  # Slow

spread_speed = get_spread_speed(temp, humidity, wind_speed, veg_density)
spread_probs = [0.2, 0.4, 0.6]
spread_prob = spread_probs[spread_speed]

# ---- Fire Spread Simulation ----
n = 50
forest = np.zeros((n, n))
forest[n//2, n//2] = 1
wind = (0, 1)

@st.cache_data(show_spinner=False)
def run_simulation(spread_prob):
    frames = []
    current_forest = forest.copy()
    for _ in range(30):
        frames.append(current_forest.copy())
        new_forest = current_forest.copy()
        for i in range(1, n-1):
            for j in range(1, n-1):
                if current_forest[i, j] == 1:
                    new_forest[i, j] = 2
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            ni, nj = i + dx, j + dy
                            if current_forest[ni, nj] == 0:
                                wind_boost = 0.3 if (dx, dy) == wind else 0
                                if np.random.rand() < spread_prob + wind_boost:
                                    new_forest[ni, nj] = 1
        current_forest = new_forest
    return frames

frames = run_simulation(spread_prob)

# ---- Display Results ----
st.title("🔥 Forest Fire Spread Simulation")
labels = ["Slow", "Medium", "Fast"]
st.subheader(f"Predicted Spread Speed: {labels[spread_speed]}")

# Animation Display
fig, ax = plt.subplots()
ims = []
for f in frames:
    im = ax.imshow(f, animated=True, cmap="hot", vmin=0, vmax=2)
    ims.append([im])
ani = animation.ArtistAnimation(fig, ims, interval=300, blit=True, repeat=False)
st.pyplot(fig)

st.caption("Note: Simulation is based on simplified environmental rules.")
