print("Hello,FastF1")
"""
Tyre Strategy Chart — Project 1
Shows which tyre compound each driver used and for how long,
across a real F1 race, using the FastF1 library.
"""

import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt

# --- 1. Set up caching so we don't re-download data every run ---
import os
os.makedirs('cache', exist_ok=True)
fastf1.Cache.enable_cache('cache')  # creates a "cache" folder in this project

# --- 2. Load a race session ---
# Pick any year/race you like. Format: get_session(year, 'Race Name', session_type)
# session_type: 'R' = Race, 'Q' = Qualifying, 'FP1'/'FP2'/'FP3' = Practice
session = fastf1.get_session(2024, 'Monza', 'R')
session.load()

# --- 3. Get lap data for every driver ---
laps = session.laps

# --- 4. Group laps into "stints" (a stint = laps on one tyre compound before a pit stop)

stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
stints = stints.groupby(["Driver", "Stint", "Compound"]).count().reset_index()
stints = stints.rename(columns={"LapNumber": "StintLength"})
print(stints)

# --- 5. Set up colors for each tyre compound ---
compound_colors = {
    "SOFT": "#DA291C",
    "MEDIUM": "#FFD12E",
    "HARD": "#F0F0F0",
    "INTERMEDIATE": "#43B02A",
    "WET": "#0067AD",
}

# --- 6. Build the chart ---
drivers = session.drivers
driver_names = [session.get_driver(d)["Abbreviation"] for d in drivers]

fig, ax = plt.subplots(figsize=(10, 10))

for driver in driver_names:
    driver_stints = stints[stints["Driver"] == driver]
    previous_stint_end = 0

    for _, row in driver_stints.iterrows():
        compound_color = compound_colors.get(row["Compound"], "#999999")
        ax.barh(
            y=driver,
            width=row["StintLength"],
            left=previous_stint_end,
            color=compound_color,
            edgecolor="black",
            linewidth=0.5,
        )
        previous_stint_end += row["StintLength"]

ax.set_xlabel("Lap Number")
ax.set_ylabel("Driver")
ax.set_title(f"Tyre Strategy — {session.event['EventName']} {session.event.year}")
ax.invert_yaxis()  # so the first driver in the list appears at the top

plt.tight_layout()
plt.savefig("tyre_strategy.png", dpi=200)
plt.show()

print("Chart saved as tyre_strategy.png")