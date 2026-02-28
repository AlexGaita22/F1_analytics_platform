"""
Modul de feature engineering
============================
Construiește matricea de feature-uri și vectorul țintă din datele F1.
Suportă doar: TyreLife, TrackTemp, WindSpeed, AirTemp, LapNumber.
"""

import pandas as pd
import numpy as np
from typing import List, Tuple, Optional
import streamlit as st


# Feature-uri permise (doar aceste 5)
ALLOWED_FEATURES = ["TyreLife", "TrackTemp", "WindSpeed", "AirTemp", "LapNumber"]


def build_feature_matrix(
    laps: pd.DataFrame,
    telemetry: Optional[pd.DataFrame],
    selected_features: List[str]
) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """
    Construiește matricea A și vectorul țintă b din datele pe tur.
    Suportă doar: TyreLife, TrackTemp, WindSpeed, AirTemp, LapNumber.
    """
    warnings_list = []
    
    # Ținta: LapTime în secunde
    if 'LapTime' not in laps.columns:
        st.error("LapTime column not found in lap data.")
        return None, None, []
    
    # Convertim LapTime în secunde dacă este timedelta
    if pd.api.types.is_timedelta64_dtype(laps['LapTime']):
        b = laps['LapTime'].dt.total_seconds().values
    else:
        b = laps['LapTime'].values
    
    # Eliminăm tururile cu NaN
    valid_mask = ~np.isnan(b)
    laps_clean = laps[valid_mask].copy()
    b = b[valid_mask]
    
    if len(b) == 0:
        st.error("No valid lap times found.")
        return None, None, []
    
    # Construim matricea de feature-uri
    feature_list = []
    feature_names = []
    
    # Mapare feature-uri (doar cele 5 permise)
    basic_features = {
        'TyreLife': 'TyreLife',
        'TrackTemp': 'TrackTemp',
        'WindSpeed': 'WindSpeed',
        'AirTemp': 'AirTemp',
        'LapNumber': 'LapNumber'
    }
    
    # Păstrăm doar feature-urile permise
    valid_selected = [f for f in selected_features if f in ALLOWED_FEATURES]
    
    for feature_key, col_name in basic_features.items():
        if feature_key in valid_selected:
            if col_name in laps_clean.columns:
                feature_list.append(laps_clean[col_name].fillna(0).values)
                feature_names.append(feature_key)
            else:
                warnings_list.append(f"Feature {feature_key} (column {col_name}) not available, skipping.")
    
    # Semnalăm selecțiile invalide
    invalid_features = [f for f in selected_features if f not in ALLOWED_FEATURES]
    if invalid_features:
        warnings_list.append(f"Invalid features ignored: {', '.join(invalid_features)}")
    
    if len(feature_list) == 0:
        st.error("No features could be extracted. Please select different features.")
        return None, None, []
    
    # Adăugăm termenul de intercept
    feature_list.insert(0, np.ones(len(b)))
    feature_names.insert(0, 'Intercept')
    
    # Formăm matricea
    A = np.column_stack(feature_list)
    
    # Înlocuim NaN / Inf cu 0
    A = np.nan_to_num(A, nan=0.0, posinf=0.0, neginf=0.0)
    
    # Afișăm eventualele avertismente
    for warning in warnings_list:
        st.warning(warning)
    
    return A, b, feature_names
