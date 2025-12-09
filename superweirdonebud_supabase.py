import streamlit as st
import pandas as pd
import numpy as np
import datetime
from supabase import create_client, Client
from typing import Optional

st.set_page_config(page_title="Rottnest Island Conditions Tracker", layout="wide", initial_sidebar_state="collapsed")

# ============================================================
# SUPABASE INITIALIZATION
# ============================================================
@st.cache_resource
def init_supabase() -> Client:
    """Initialize and return Supabase client using secrets."""
    try:
        supabase_url = st.secrets["SUPABASE_URL"]
        supabase_key = st.secrets["SUPABASE_KEY"]
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        st.error(f"❌ Failed to connect to Supabase: {str(e)}")
        st.error("**Configuration needed:** Add SUPABASE_URL and SUPABASE_KEY to .streamlit/secrets.toml")
        st.stop()

supabase: Client = init_supabase()

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if 'user' not in st.session_state:
    st.session_state.user = None
if 'session' not in st.session_state:
    st.session_state.session = None

# ============================================================
# AUTHENTICATION FUNCTIONS
# ============================================================
def sign_up(email: str, password: str, full_name: str = "") -> bool:
    """Sign up a new user."""
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "full_name": full_name
                }
            }
        })
        
        if response.user:
            st.session_state.user = response.user
            st.session_state.session = response.session
            return True
        return False
    except Exception as e:
        st.error(f"Sign up failed: {str(e)}")
        return False

def sign_in(email: str, password: str) -> bool:
    """Sign in an existing user."""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.user:
            st.session_state.user = response.user
            st.session_state.session = response.session
            return True
        return False
    except Exception as e:
        st.error(f"Sign in failed: {str(e)}")
        return False

def sign_out():
    """Sign out the current user."""
    try:
        supabase.auth.sign_out()
        st.session_state.user = None
        st.session_state.session = None
    except Exception as e:
        st.error(f"Sign out failed: {str(e)}")

# ============================================================
# DATABASE FUNCTIONS
# ============================================================
def load_user_records(publicity_filter: Optional[str] = None) -> pd.DataFrame:
    """Load records for the current user from Supabase."""
    if not st.session_state.user:
        return pd.DataFrame()
    
    try:
        query = supabase.table('records').select('*').eq('user_id', st.session_state.user.id)
        
        if publicity_filter:
            query = query.eq('publicity', publicity_filter)
        
        response = query.order('date', desc=True).execute()
        
        if response.data:
            df = pd.DataFrame(response.data)
            # Convert column names from snake_case to match original format
            column_mapping = {
                'surfline_primary_swell_size_m': 'Surfline Primary Swell Size (m)',
                'seabreeze_swell_m': 'Seabreeze Swell (m)',
                'swell_period_s': 'Swell Period (s)',
                'swell_direction': 'Swell Direction',
                'suitable_swell': 'Suitable Swell?',
                'swell_score': 'Swell Score',
                'final_swell_score': 'Final Swell Score',
                'swell_comments': 'Swell Comments',
                'wind_bearing': 'Wind Bearing',
                'wind_speed_kn': 'Wind Speed (kn)',
                'suitable_wind': 'Suitable Wind?',
                'wind_score': 'Wind Score',
                'wind_final_score': 'Wind Final Score',
                'wind_comments': 'Wind Comments',
                'tide_reading_m': 'Tide Reading (m)',
                'tide_direction': 'Tide Direction',
                'tide_suitable': 'Tide Suitable?',
                'tide_score': 'Tide Score',
                'tide_final_score': 'Tide Final Score',
                'tide_comments': 'Tide Comments',
                'full_commentary': 'Full Commentary',
                'total_score': 'TOTAL SCORE',
                'date': 'Date',
                'time': 'Time',
                'break': 'Break',
                'zone': 'Zone'
            }
            df = df.rename(columns=column_mapping)
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Failed to load records: {str(e)}")
        return pd.DataFrame()

def save_record(record_data: dict) -> bool:
    """Save a new surf session record to Supabase."""
    if not st.session_state.user:
        st.error("You must be logged in to save records")
        return False
    
    try:
        # Convert from display format to database snake_case format
        db_record = {
            'user_id': st.session_state.user.id,
            'publicity': record_data.get('publicity', 'Private'),
            'date': str(record_data.get('Date')),
            'time': str(record_data.get('Time')),
            'break': record_data.get('Break'),
            'zone': record_data.get('Zone'),
            'total_score': float(record_data.get('TOTAL SCORE', 0)),
            'surfline_primary_swell_size_m': float(record_data.get('Surfline Primary Swell Size (m)', 0)),
            'seabreeze_swell_m': float(record_data.get('Seabreeze Swell (m)', 0)),
            'swell_period_s': int(record_data.get('Swell Period (s)', 0)),
            'swell_direction': float(record_data.get('Swell Direction', 0)) if record_data.get('Swell Direction') else None,
            'suitable_swell': record_data.get('Suitable Swell?'),
            'swell_score': int(record_data.get('Swell Score', 0)),
            'final_swell_score': int(record_data.get('Final Swell Score', 0)),
            'swell_comments': record_data.get('Swell Comments'),
            'wind_bearing': record_data.get('Wind Bearing'),
            'wind_speed_kn': int(record_data.get('Wind Speed (kn)', 0)),
            'suitable_wind': record_data.get('Suitable Wind?'),
            'wind_score': int(record_data.get('Wind Score', 0)),
            'wind_final_score': int(record_data.get('Wind Final Score', 0)),
            'wind_comments': record_data.get('Wind Comments'),
            'tide_reading_m': float(record_data.get('Tide Reading (m)', 0)),
            'tide_direction': record_data.get('Tide Direction'),
            'tide_suitable': record_data.get('Tide Suitable?'),
            'tide_score': int(record_data.get('Tide Score', 0)),
            'tide_final_score': float(record_data.get('Tide Final Score', 0)),
            'tide_comments': record_data.get('Tide Comments'),
            'full_commentary': record_data.get('Full Commentary')
        }
        
        response = supabase.table('records').insert(db_record).execute()
        
        if response.data:
            return True
        return False
    except Exception as e:
        st.error(f"Failed to save record: {str(e)}")
        return False

def update_record(record_id: str, record_data: dict) -> bool:
    """Update an existing record in Supabase."""
    if not st.session_state.user:
        return False
    
    try:
        # Convert from display format to database format (similar to save_record)
        db_record = {
            'date': str(record_data.get('Date')),
            'time': str(record_data.get('Time')),
            'break': record_data.get('Break'),
            'zone': record_data.get('Zone'),
            'total_score': float(record_data.get('TOTAL SCORE', 0)),
            'surfline_primary_swell_size_m': float(record_data.get('Surfline Primary Swell Size (m)', 0)),
            'seabreeze_swell_m': float(record_data.get('Seabreeze Swell (m)', 0)),
            'swell_period_s': int(record_data.get('Swell Period (s)', 0)),
            'swell_direction': float(record_data.get('Swell Direction', 0)) if record_data.get('Swell Direction') else None,
            'suitable_swell': record_data.get('Suitable Swell?'),
            'swell_score': int(record_data.get('Swell Score', 0)),
            'final_swell_score': int(record_data.get('Final Swell Score', 0)),
            'swell_comments': record_data.get('Swell Comments'),
            'wind_bearing': record_data.get('Wind Bearing'),
            'wind_speed_kn': int(record_data.get('Wind Speed (kn)', 0)),
            'suitable_wind': record_data.get('Suitable Wind?'),
            'wind_score': int(record_data.get('Wind Score', 0)),
            'wind_final_score': int(record_data.get('Wind Final Score', 0)),
            'wind_comments': record_data.get('Wind Comments'),
            'tide_reading_m': float(record_data.get('Tide Reading (m)', 0)),
            'tide_direction': record_data.get('Tide Direction'),
            'tide_suitable': record_data.get('Tide Suitable?'),
            'tide_score': int(record_data.get('Tide Score', 0)),
            'tide_final_score': float(record_data.get('Tide Final Score', 0)),
            'tide_comments': record_data.get('Tide Comments'),
            'full_commentary': record_data.get('Full Commentary')
        }
        
        response = supabase.table('records').update(db_record).eq('id', record_id).eq('user_id', st.session_state.user.id).execute()
        
        return True if response.data else False
    except Exception as e:
        st.error(f"Failed to update record: {str(e)}")
        return False

def delete_record(record_id: str) -> bool:
    """Delete a record from Supabase."""
    if not st.session_state.user:
        return False
    
    try:
        response = supabase.table('records').delete().eq('id', record_id).eq('user_id', st.session_state.user.id).execute()
        return True
    except Exception as e:
        st.error(f"Failed to delete record: {str(e)}")
        return False

# ============================================================
# STYLING
# ============================================================
st.markdown("""
<style>
body {background:#0e1117;}
.block-container {
  max-width:100% !important;
  width:100%;
  margin:0 auto 2.5rem;
  padding:clamp(0.75rem,1.2vw,1.5rem) clamp(1rem,2vw,2.25rem) 3rem clamp(1rem,2vw,2.25rem);
  border:2px solid #2e6f75;
  border-radius:18px;
  box-shadow:0 4px 18px -4px rgba(0,0,0,0.55), 0 0 0 1px rgba(255,255,255,0.04) inset;
  background:linear-gradient(145deg,#162127 0%,#121b20 60%,#10181c 100%);
  position:relative;
  box-sizing:border-box;
}

.auth-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  background: linear-gradient(145deg, #162127 0%, #121b20 100%);
  border: 2px solid #2e6f75;
  border-radius: 18px;
  box-shadow: 0 4px 18px -4px rgba(0,0,0,0.55);
}

.stButton>button {
  width: 100%;
  background: #0f3d3d;
  border: 2px solid #2e6f75;
  color: #2eecb5;
  font-weight: 600;
  padding: 0.75rem;
  border-radius: 10px;
}

.stButton>button:hover {
  background: #145252;
  border-color: #33a9b3;
  color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# AUTHENTICATION UI
# ============================================================
if not st.session_state.user:
    st.title("🏄 Super Weird One Bud")
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
    
    with tab1:
        st.subheader("Sign In")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Sign In", key="signin_btn"):
            if login_email and login_password:
                if sign_in(login_email, login_password):
                    st.success("✅ Signed in successfully!")
                    st.rerun()
            else:
                st.warning("Please enter both email and password")
    
    with tab2:
        st.subheader("Create Account")
        signup_name = st.text_input("Full Name (optional)", key="signup_name")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        signup_password_confirm = st.text_input("Confirm Password", type="password", key="signup_password_confirm")
        
        if st.button("Sign Up", key="signup_btn"):
            if signup_email and signup_password:
                if signup_password == signup_password_confirm:
                    if len(signup_password) >= 6:
                        if sign_up(signup_email, signup_password, signup_name):
                            st.success("✅ Account created! Please check your email to verify your account.")
                            st.info("After verification, you can sign in.")
                    else:
                        st.warning("Password must be at least 6 characters long")
                else:
                    st.warning("Passwords do not match")
            else:
                st.warning("Please enter email and password")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ============================================================
# MAIN APPLICATION (Only visible when logged in)
# ============================================================

# User info and logout button in sidebar
with st.sidebar:
    st.write(f"👤 **{st.session_state.user.email}**")
    if st.button("Sign Out"):
        sign_out()
        st.rerun()

# Import the rest of the application logic from the original file
# This section will contain all the surf tracking functionality
# For now, let's create a simple version:

st.title("Super Weird One Bud - Surf Tracker")
st.write("Welcome! You're now logged in and can start tracking surf sessions.")

# Show simple create/view toggle
if 'creating' not in st.session_state:
    st.session_state.creating = False

if not st.session_state.creating:
    if st.button("➕ Create New Session"):
        st.session_state.creating = True
        st.rerun()
    
    # Load and display user's records
    st.subheader("Your Surf Sessions")
    records_df = load_user_records()
    
    if not records_df.empty:
        # Display simplified view
        display_cols = ['Date', 'Break', 'Zone', 'TOTAL SCORE']
        available_cols = [col for col in display_cols if col in records_df.columns]
        st.dataframe(records_df[available_cols])
    else:
        st.info("No sessions recorded yet. Click 'Create New Session' to add your first one!")

else:
    st.subheader("Create New Session")
    
    if st.button("← Back to List"):
        st.session_state.creating = False
        st.rerun()
    
    # Simple form for now
    with st.form("new_session"):
        col1, col2 = st.columns(2)
        
        with col1:
            session_date = st.date_input("Date", datetime.date.today())
            session_time = st.time_input("Time", datetime.time(8, 0))
            break_name = st.text_input("Break")
            zone_name = st.text_input("Zone")
        
        with col2:
            publicity = st.selectbox("Visibility", ["Private", "Public", "Community"])
            total_score = st.number_input("Total Score", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        
        swell_comments = st.text_area("Swell Comments")
        wind_comments = st.text_area("Wind Comments")
        tide_comments = st.text_area("Tide Comments")
        
        submitted = st.form_submit_button("Save Session")
        
        if submitted:
            if break_name:
                full_commentary = f"{swell_comments} {wind_comments} {tide_comments}".strip()
                
                record = {
                    'Date': session_date,
                    'Time': session_time,
                    'Break': break_name,
                    'Zone': zone_name,
                    'TOTAL SCORE': total_score,
                    'publicity': publicity,
                    'Surfline Primary Swell Size (m)': 0,
                    'Seabreeze Swell (m)': 0,
                    'Swell Period (s)': 0,
                    'Swell Direction': 0,
                    'Suitable Swell?': 'Yes',
                    'Swell Score': 0,
                    'Final Swell Score': 0,
                    'Swell Comments': swell_comments,
                    'Wind Bearing': 'N',
                    'Wind Speed (kn)': 0,
                    'Suitable Wind?': 'Yes',
                    'Wind Score': 0,
                    'Wind Final Score': 0,
                    'Wind Comments': wind_comments,
                    'Tide Reading (m)': 0,
                    'Tide Direction': 'High',
                    'Tide Suitable?': 'Yes',
                    'Tide Score': 0,
                    'Tide Final Score': 0,
                    'Tide Comments': tide_comments,
                    'Full Commentary': full_commentary
                }
                
                if save_record(record):
                    st.success("✅ Session saved successfully!")
                    st.session_state.creating = False
                    st.rerun()
            else:
                st.error("Please enter a break name")
