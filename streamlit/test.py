  
"""
This is where the user interface is made using the streamlit package.
"""
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; color: indigo;'>Machine Learning for Quantum Dots Synthesis  - Cossairt Laboratory</h1>", unsafe_allow_html=True)

if "InP" not in st.session_state:
    st.session_state.InP = False

if st.button("InP") or st.session_state.InP:
    st.session_state.InP = True
    st.radio('a',('a','b','c'))

    if st.button("Download"):
        st.session_state.submitted = False
        st.write("Download clicked!")