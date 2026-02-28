"""
Loader date F1
==============
Încarcă sesiuni FastF1 cu suport de cache.
"""

import fastf1
import streamlit as st
from typing import Optional
import pandas as pd
import os
from pathlib import Path


def get_cache_dir() -> str:
    """
    Returnează (sau creează) directorul de cache FastF1.
    """
    # Verificăm dacă există variabilă de mediu personalizată
    env_cache = os.getenv("FASTF1_CACHE")
    if env_cache:
        cache_dir = Path(env_cache)
    else:
        # Folosim rădăcina proiectului / cache
        # Directorul curent (f1/)
        current_file = Path(__file__).resolve()
        # Urcăm un nivel la rădăcina proiectului
        project_root = current_file.parents[1]
        cache_dir = project_root / "cache"
    
    # Creăm directorul de cache dacă nu există
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    return str(cache_dir)


# Inițializăm cache-ul la import
_cache_initialized = False

def _init_cache():
    """Initializează cache-ul FastF1."""
    global _cache_initialized
    if not _cache_initialized:
        cache_path = get_cache_dir()
        fastf1.Cache.enable_cache(cache_path)
        _cache_initialized = True

# Pornim cache-ul
_init_cache()


@st.cache_data(ttl=3600)  # Cache o oră
def load_session(year: int, event_name: str, session_type: str) -> Optional[fastf1.core.Session]:
    """
    Încarcă o sesiune F1 cu cache.
    """
    try:
        session = fastf1.get_session(year, event_name, session_type)
        session.load()
        return session
    except Exception as e:
        st.error(f"Error loading session: {str(e)}")
        return None


def get_laps_data(session: fastf1.core.Session, driver_code: str) -> Optional[pd.DataFrame]:
    """
    Extrage datele pe tur pentru un pilot.
    """
    if session is None:
        return None
    
    try:
        laps = session.laps.pick_driver(driver_code).copy()
        if laps.empty:
            st.warning(f"Driver {driver_code} not found in this session.")
            return None
        
        # Filtrăm tururile valide: LapTime nenul și IsAccurate dacă există
        valid_mask = laps['LapTime'].notna()
        if 'IsAccurate' in laps.columns:
            valid_mask = valid_mask & (laps['IsAccurate'] == True)
        
        laps_valid = laps[valid_mask].copy()
        
        if laps_valid.empty:
            st.warning(f"No valid laps found for driver {driver_code}.")
            return None
        
        return laps_valid
    except Exception as e:
        st.error(f"Error extracting lap data: {str(e)}")
        return None


def get_telemetry_data(session: fastf1.core.Session, driver_code: str) -> Optional[pd.DataFrame]:
    """
    Extrage telemetria pentru un pilot.
    """
    if session is None:
        return None
    
    try:
        telemetry = session.laps.pick_driver(driver_code).get_telemetry()
        return telemetry
    except Exception as e:
        st.warning(f"Could not load telemetry for {driver_code}: {str(e)}")
        return None
