import streamlit as st
import pandas as pd
import base64

# Set page configuration
st.set_page_config(
    page_title="Dashboard Indikator Dit. Takel PKP",
    page_icon="icon.png",
    layout="wide"
)

# Kemenkes Branding Color identified from v4header.png
KEMENKES_TEAL = "#00A99D"

# CSS for a premium, polished look
st.markdown(f"""
    <style>
    /* Menyembunyikan header (menu titik tiga) dan footer (Made with Streamlit) */
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Memaksa background tetap putih dan teks gelap agar tidak terpengaruh sistem */
    .stApp {{
        background-color: white !important;
        color: #31333f !important;
    }}

    /* Reset padding container utama */
    .block-container {{
        padding-top: 0rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }}
    
    /* v4header Image Container */
    .v4header-container {{
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }}
    
    .v4header-container img {{
        max-width: 100%;
        height: auto;
        object-fit: contain;
    }}

    /* Table Styling */
    .custom-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 0.95em;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border-radius: 12px;
        overflow: hidden;
    }}
    
    .custom-table thead tr {{
        background-color: {KEMENKES_TEAL};
        color: #ffffff;
    }}
    
    .custom-table th {{
        padding: 15px;
        text-align: center !important;
        border: 1px solid #e2e8f0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    .custom-table td {{
        padding: 12px 15px;
        border: 1px solid #e2e8f0;
        vertical-align: middle;
        line-height: 1.5;
    }}
    
    /* Perataan Kolom */
    .custom-table td:nth-child(1) {{ text-align: center; font-weight: 600; width: 10%; background-color: #f8fafc; }}
    .custom-table td:nth-child(2) {{ text-align: left; width: 35%; }}
    .custom-table td:nth-child(n+3), .custom-table th:nth-child(n+3) {{ 
        text-align: center; 
        width: 9%; 
    }}
    
    .custom-table tbody tr:nth-of-type(even) {{ background-color: #f1f5f9; }}
    .custom-table tbody tr:hover {{ background-color: #e2e8f0; transition: 0.2s; }}
    
    @media screen and (max-width: 768px) {{
        .custom-table {{ font-size: 0.8em; }}
        .block-container {{ padding-left: 0.5rem; padding-right: 0.5rem; }}
    }}
    </style>
""", unsafe_allow_html=True)

# Display v4header Image
try:
    st.markdown('<div class="v4header-container"><img src="data:image/png;base64,{}" /></div>'.format(
        base64.b64encode(open("v4header.png", "rb").read()).decode()
    ), unsafe_allow_html=True)
except: pass

# Teks dan Link di atas tabel
st.markdown("""
    <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px;">
        <div style="flex: 1; min-width: 300px; background-color: #eff6ff; padding: 15px; border-radius: 8px; border-left: 5px solid #00A99D;">
            <span style="color: #007D8C; font-weight: 500;">ℹ️ Informasi:</span> 
            Silakan klik tautan berikut untuk melihat detail capaian indikator dan melakukan input data: 
            <a href="https://s.kemkes.go.id/MonevIndikatorTakelPKP" target="_blank" style="color: #00A99D; font-weight: bold; text-decoration: underline;">
                s.kemkes.go.id/MonevIndikatorTakelPKP
            </a>
        </div>
        <div style="background-color: #ffffff; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0; display: flex; align-items: center; gap: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <span style="font-weight: 600; color: #475569;">Keterangan Capaian:</span>
            <div style="display: flex; align-items: center; gap: 5px;">
                <div style="width: 12px; height: 12px; background-color: #ef4444; border-radius: 2px;"></div>
                <span style="font-size: 0.9em; color: #ef4444; font-weight: 600;">Belum Tercapai</span>
            </div>
            <div style="display: flex; align-items: center; gap: 5px;">
                <div style="width: 12px; height: 12px; background-color: #22c55e; border-radius: 2px;"></div>
                <span style="font-size: 0.9em; color: #22c55e; font-weight: 600;">Sudah Tercapai</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Formatting function for display
def format_value(val, col_name=None, row_data=None):
    if pd.isna(val) or val == "": return ""
    if col_name == 'GAP' and row_data is not None:
        target_val = str(row_data.get('TARGET 2026', ''))
        if "Kab/Kota" in target_val:
            try:
                v = float(val)
                return f"{int(v)} Kab/Kota" if v == int(v) else f"{v:g} Kab/Kota"
            except: return f"{val} Kab/Kota"
    if isinstance(val, (int, float)):
        if 0 < val <= 1:
            res = val * 100
            if res == int(res): return f"{int(res)}%"
            return f"{res:.2f}".rstrip('0').rstrip('.') + "%"
        else:
            if val == int(val): return str(int(val))
            return f"{val:g}"
    return str(val)

# Helper to extract numeric value for comparison
def get_numeric_value(val):
    if pd.isna(val) or val == "": return None
    if isinstance(val, (int, float)): return float(val)
    if isinstance(val, str):
        import re
        # Extract first number found in string (handles "90 Kab/Kota" -> 90.0)
        match = re.search(r"([-+]?\d*\.?\d+)", val.replace(',', '.'))
        if match:
            try: return float(match.group(1))
            except: return None
    return None

@st.cache_data
def load_data_v6():
    df = pd.read_excel('v4_data_dashboard_latsar.xlsx')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df

try:
    df = load_data_v6()
    
    # Process for Table Display - Convert to object to avoid dtype conflicts
    display_df = df.copy().astype(object)
    cols_to_format = ['TARGET 2026', 'TW I', 'TW II', 'TW III', 'TW IV', 'GAP']
    
    tw_cols = ['TW I', 'TW II', 'TW III', 'TW IV']
    
    for idx, row in df.iterrows():
        target_raw = row.get('TARGET 2026')
        t_num = get_numeric_value(target_raw)
        
        for col in cols_to_format:
            if col in df.columns:
                val = row[col]
                formatted = format_value(val, col, row)
                
                # Apply conditional coloring for TW columns
                if col in tw_cols and not pd.isna(val) and val != "":
                    v_num = get_numeric_value(val)
                    if v_num is not None and t_num is not None:
                        color = "#ef4444" if v_num < t_num else "#22c55e"
                        formatted = f'<span style="color: {color}; font-weight: bold;">{formatted}</span>'
                
                display_df.at[idx, col] = formatted
    
    # Display Table
    st.markdown(display_df.to_html(classes='custom-table', index=False, escape=False), unsafe_allow_html=True)
    
    # Footer simple
    st.markdown("""
        <br><div style="text-align: center; color: #94a3b8; font-size: 0.85em;">
            Data Update : 15 April 2026 (Capaian TW I)
        </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
