"""
Lap-Time Consistency Comparison — Project 2
Compares race pace and consistency between two drivers across a full race.
"""

import fastf1
import matplotlib.pyplot as plt

fastf1.Cache.enable_cache('cache')

# --- 1. Load the race(R) or quali(Q) ---
session = fastf1.get_session(2021, 'Brazil', 'R')
session.load()

# --- 2. Pick two drivers to compare (use their 3-letter codes) ---
driver_1 = 'VER'
driver_2 = 'HAM'

laps = session.laps

# --- 3. Get clean race laps for each driver ---
# pick_quicklaps() filters out in/out laps, safety car laps, and other outliers
# so we're comparing genuine racing pace, not distorted laps.
laps_1 = laps.pick_drivers(driver_1).pick_quicklaps()
laps_2 = laps.pick_drivers(driver_2).pick_quicklaps()


# Convert lap times from a time format into plain seconds, easier to plot
laps_1 = laps_1.copy()
laps_2 = laps_2.copy()
laps_1['LapTimeSeconds'] = laps_1['LapTime'].dt.total_seconds()
laps_2['LapTimeSeconds'] = laps_2['LapTime'].dt.total_seconds()

print(laps_1[['LapNumber', 'LapTimeSeconds']])
print(laps_2[['LapNumber', 'LapTimeSeconds']])


# --- 4. Plot both drivers' lap times across the race ---
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(laps_1['LapNumber'], laps_1['LapTimeSeconds'], label=driver_1, marker='x', markersize=8, color = 'blue')
ax.plot(laps_2['LapNumber'], laps_2['LapTimeSeconds'], label=driver_2, marker='x', markersize=8, color = 'red')

ax.set_xlabel('Lap Number')
ax.set_ylabel('Lap Time (seconds)')
ax.set_title(f'Lap Time Consistency — {driver_1} vs {driver_2} — {session.event["EventName"]} {session.event.year}')
ax.legend()

plt.tight_layout()
plt.savefig('lap_time_consistency.png', dpi=200)
plt.show()

# --- 5. Print quick stats — use these numbers to write your interpretation ---
print(f"{driver_1}: average lap {laps_1['LapTimeSeconds'].mean():.3f}s, consistency (std dev) {laps_1['LapTimeSeconds'].std():.3f}s")
print(f"{driver_2}: average lap {laps_2['LapTimeSeconds'].mean():.3f}s, consistency (std dev) {laps_2['LapTimeSeconds'].std():.3f}s")
print("Lower std dev = more consistent lap-to-lap pace.")