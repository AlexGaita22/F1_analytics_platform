"""
Modul de plotare
================
Creează vizualizări matplotlib pentru analiza tururilor F1.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List, Optional
import streamlit as st


def plot_predictions_vs_actual(
    actual: np.ndarray,
    predicted: np.ndarray,
    lap_numbers: Optional[np.ndarray] = None
) -> plt.Figure:
    """
    Plotează timpii reali versus timpii preziși pe tururi.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if lap_numbers is None:
        lap_numbers = np.arange(1, len(actual) + 1)
    
    ax.plot(lap_numbers, actual, 'o-', label='Actual', alpha=0.7, markersize=6)
    ax.plot(lap_numbers, predicted, 's-', label='Predicted', alpha=0.7, markersize=6)
    ax.set_xlabel('Lap Number')
    ax.set_ylabel('Lap Time (seconds)')
    ax.set_title('Actual vs Predicted Lap Times')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_errors(
    errors: np.ndarray,
    lap_numbers: Optional[np.ndarray] = None
) -> plt.Figure:
    """
    Plotează erorile de predicție pe fiecare tur (linie).
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if lap_numbers is None:
        lap_numbers = np.arange(1, len(errors) + 1)
    
    ax.plot(lap_numbers, errors, 'o-', alpha=0.7, color='coral', markersize=6)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax.set_xlabel('Lap Number')
    ax.set_ylabel('Error (seconds)')
    ax.set_title('Prediction Error per Lap')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_coefficients(
    coefficients: np.ndarray,
    feature_names: List[str]
) -> plt.Figure:
    """
    Afișează magnitudinea coeficienților de regresie (bar chart).
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Folosim valorile absolute (magnitudini)
    abs_coeffs = np.abs(coefficients)
    colors = ['red' if c < 0 else 'blue' for c in coefficients]
    bars = ax.barh(feature_names, abs_coeffs, color=colors, alpha=0.7)
    
    ax.set_xlabel('Coefficient Magnitude')
    ax.set_title('Regression Coefficients Magnitude')
    ax.grid(True, alpha=0.3, axis='x')
    
    # Etichete cu valorile semnate
    for i, (bar, val, orig_val) in enumerate(zip(bars, abs_coeffs, coefficients)):
        ax.text(val, i, f'{orig_val:.4f}', va='center',
                ha='left', fontsize=9)
    
    plt.tight_layout()
    return fig


def plot_track_map(session, driver_code: Optional[str] = None) -> Optional[plt.Figure]:
    """
    Desenează harta circuitului din pozițiile FastF1.
    Folosește cel mai rapid tur al pilotului ales sau turul cel mai rapid din sesiune.
    """
    try:
        # Luăm tururile pilotului sau cădem pe cel mai rapid
        if driver_code:
            try:
                laps = session.laps.pick_driver(driver_code)
                if laps.empty:
                    laps = session.laps.pick_fastest()
            except Exception:
                laps = session.laps.pick_fastest()
        else:
            laps = session.laps.pick_fastest()
        
        if laps.empty:
            return None
        
        # Turul cel mai rapid
        fastest_lap = laps.pick_fastest()
        if fastest_lap is None or fastest_lap.empty:
            return None
        
        # Datele de poziție (X, Y)
        try:
            pos_data = fastest_lap.get_pos_data()
        except Exception as e:
            st.warning(f"Could not load position data: {str(e)}")
            return None
        
        # Căutăm coloanele X și Y (FastF1 folosește 'X' și 'Y')
        x_col = None
        y_col = None
        for col in ['X', 'x', 'XPosition']:
            if col in pos_data.columns:
                x_col = col
                break
        for col in ['Y', 'y', 'YPosition']:
            if col in pos_data.columns:
                y_col = col
                break
        
        if x_col is None or y_col is None:
            st.warning("Position data columns (X, Y) not found.")
            return None
        
        x = pos_data[x_col].values
        y = pos_data[y_col].values
        
        # Recentram coordonatele pentru vizualizare mai clară
        x = x - np.mean(x)
        y = y - np.mean(y)
        
        # Desenăm
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.plot(x, y, 'b-', linewidth=2, alpha=0.8)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Titlu cu nume eveniment și an
        try:
            event_name = session.event.EventName if hasattr(session.event, 'EventName') else "Circuit"
            year = session.event.year if hasattr(session.event, 'year') else ""
            title = f"{event_name}"
            if year:
                title += f" {year}"
            if driver_code:
                title += f" - {driver_code}"
            ax.set_title(title, fontsize=12, pad=20)
        except Exception:
            ax.set_title("Circuit Map", fontsize=12, pad=20)
        
        plt.tight_layout()
        return fig
    except Exception as e:
        st.warning(f"Error plotting track map: {str(e)}")
        return None
