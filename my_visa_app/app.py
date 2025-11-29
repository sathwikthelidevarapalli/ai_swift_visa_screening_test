import streamlit as st
import subprocess
import os
import threading
import time

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="Global Visa Navigator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="auto",
)

# Define a palette inspired by 'English colors' - sophisticated blues, greys, and warm accents
PRIMARY_COLOR = "#34495E"
ACCENT_COLOR = "#8E44AD"
BACKGROUND_COLOR = "#ECF0F1"
SECONDARY_BACKGROUND_COLOR = "#BDC3C7"
TEXT_COLOR = "#2C3E50"
SUCCESS_COLOR = "#2ECC71"
ERROR_COLOR = "#E74C3C"


# Inject custom CSS for a more refined Streamlit look and 'English colors'
st.markdown(f"""
<style>
    /* General body styling */
    .stApp {{
        background-color: {BACKGROUND_COLOR};
        color: {TEXT_COLOR};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    /* Header styling */
    .st-emotion-cache-gq02mv {{
        padding-top: 3rem;
        padding-bottom: 1rem;
    }}
    h1 {{
        color: {PRIMARY_COLOR};
        text-align: center;
        font-size: 3.5em;
        margin-bottom: 0.5em;
        font-weight: 700;
    }}
    h2 {{
        color: {PRIMARY_COLOR};
        text-align: center;
        font-size: 2.2em;
        margin-top: 2em;
        margin-bottom: 1em;
    }}
    h3 {{
        color: {PRIMARY_COLOR};
        text-align: center;
        font-size: 1.8em;
        margin-top: 1.5em;
        margin-bottom: 0.8em;
    }}
    p {{
        font-size: 1.1em;
        line-height: 1.6;
        color: {TEXT_COLOR};
        text-align: center;
    }}
    /* Custom divider */
    hr {{
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, rgba(0, 0, 0, 0), {SECONDARY_BACKGROUND_COLOR}, rgba(0, 0, 0, 0));
        margin: 40px 0;
    }}
    /* Buttons */
    .stButton > button {{
        background-color: {ACCENT_COLOR};
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-size: 1.1em;
        font-weight: bold;
        transition: background-color 0.3s ease, transform 0.2s ease;
    }}
    .stButton > button:hover {{
        background-color: #6C3483;
        transform: translateY(-2px);
    }}
    /* Info/Warning/Success blocks */
    div[data-testid="stLocalWarning"], div[data-testid="stLocalInfo"], div[data-testid="stLocalSuccess"] {{
        background-color: {SECONDARY_BACKGROUND_COLOR};
        border-left: 5px solid {ACCENT_COLOR};
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
        color: {PRIMARY_COLOR};
    }}
    div[data-testid="stLocalWarning"] {{ border-left-color: orange; }}
    div[data-testid="stLocalSuccess"] {{ border-left-color: {SUCCESS_COLOR}; }}
    div[data-testid="stLocalInfo"] {{ border-left-color: {ACCENT_COLOR}; }}
    
    /* Ensure iframe takes available width */
    div[data-testid="stIframe"] {{
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
    }}
</style>
""", unsafe_allow_html=True)


st.title("Global Visa Navigator 🌍")
st.markdown("<p>Unlock Your Next Adventure: Seamlessly Check Your Visa Eligibility</p>", unsafe_allow_html=True)

st.write("") # Add some space

# --- Function to run React app ---
def run_react_app():
    print("Starting React app...")
    try:
        react_dir = "./frontend_react"
        
        if not os.path.exists(os.path.join(react_dir, "node_modules")):
            st.warning("Installing React dependencies. This might take a moment...")
            subprocess.run("npm install", shell=True, cwd=react_dir, check=True)
            st.success("React dependencies installed!")
            
        for css_file in ["App.css", "index.css"]:
            css_path = os.path.join(react_dir, "src", css_file)
            if not os.path.exists(css_path):
                with open(css_path, "w") as f:
                    f.write("") 
                print(f"Created empty {css_file}")

        # IMPORTANT CHANGE: Set BROWSER=none to prevent React from opening a new tab
        # This is cross-platform. On Windows, 'set BROWSER=none && npm start' is needed.
        # On Linux/macOS, 'BROWSER=none npm start' is used.
        # We handle this by passing `env` argument to subprocess.run
        
        # Copy current environment variables and add BROWSER=none
        env = os.environ.copy()
        env['BROWSER'] = 'none'

        st.info("React development server starting without opening a new browser tab...")
        # Start the React app (will use PORT 3000 by default from .env or create-react-app config)
        subprocess.run("npm start", shell=True, cwd=react_dir, check=True, env=env) # Pass the modified environment
        
    except subprocess.CalledProcessError as e:
        st.error(f"Error starting React app: {e}")
        st.error("Please ensure Node.js and npm are installed and try again.")
        st.error(f"Check the terminal where you ran 'streamlit run app.py' for detailed React errors.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# --- Start React app in a separate thread ---
if 'react_started' not in st.session_state:
    st.session_state.react_started = False
    st.session_state.react_process = None

if not st.session_state.react_started:
    st.info("Preparing your personalized visa assessment tool...")
    react_thread = threading.Thread(target=run_react_app, daemon=True)
    react_thread.start()
    st.session_state.react_started = True
    time.sleep(10) # Give React more time to start
    st.rerun()

st.subheader("Your Journey Starts Here: Interactive Visa Assessment")
st.markdown("<p>Fill in your details below and let us guide you to your next international experience.</p>", unsafe_allow_html=True)

# --- Embed the React App ---
react_app_url = "http://localhost:3000"

if st.session_state.react_started:
    # A small buffer for the iframe to load visually
    with st.spinner("Loading interactive form..."):
        time.sleep(2) # Give a brief moment for the browser to render the iframe
    st.components.v1.iframe(react_app_url, height=950, scrolling=True)
else:
    st.write("React application is spinning up... Just a moment.")

st.markdown("---")
st.markdown(f"<p style='font-size:0.9em; color:{SECONDARY_BACKGROUND_COLOR};'><i>Frontend developed with Streamlit and React. Backend by your awesome friend.</i></p>", unsafe_allow_html=True)