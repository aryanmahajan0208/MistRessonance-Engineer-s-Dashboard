"""
    Alert Engine: MistRessonance Dashboard
    Date: 2026-10-28

    Description:
        Delivers the instanteneous running status between optimal, warning, and critical
        Also delivers predicitve alerts for the future 25 frames, returning whether the efficiency is on an
        upward or downward trend and expected to drop to suboptimal levels
"""

from collections import deque

OPTIMAL_EFFICIENCY = 60     # %, at or above this is healthy
CRITICAL_EFFICIENCY = 35    # %, below this is critical (35 to 60 is warning)
WINDOW = 25                 # readings kept
MIN_POINTS = 8              # minimum readings required before estimating slope

smoothed_efficiency = deque(maxlen=WINDOW)

def smooth_stream(raw_efficiency: float) -> float:
    """Appends raw efficiency to the rolling window and returns moving average."""
    smoothed_efficiency.append(raw_efficiency)
    return sum(smoothed_efficiency) / len(smoothed_efficiency)

def instant_status(smoothed_value: float) -> str:
    """Classifies current state based on smoothed efficiency."""
    if smoothed_value <= CRITICAL_EFFICIENCY:
        return "critical"
    elif smoothed_value < OPTIMAL_EFFICIENCY:
        return "warning"
    return "normal"

def get_slope() -> float:
    """Calculates linear slope across the current smoothed history."""
    n = len(smoothed_efficiency)
    if n < MIN_POINTS:
        return 0.0
    # Change over window length
    return (smoothed_efficiency[-1] - smoothed_efficiency[0]) / n

def predict_status(slope: float) -> str:
    """Predicts trajectory based on calculated slope."""
    if len(smoothed_efficiency) < MIN_POINTS:
        return "calibrating..."
    if slope > 0.5:
        return "increase in efficiency"
    elif slope < -0.5:
        return "decrease in efficiency"
    return "stable at current state"

if __name__ == "__main__":
    import cooling_tower_sim as cts
    cts.sim_values()