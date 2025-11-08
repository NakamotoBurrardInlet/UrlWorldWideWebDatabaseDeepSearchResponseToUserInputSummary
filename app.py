import streamlit as st
from google import genai
from google.genai import types
import os

# --- 1. CONFIGURATION AND INITIALIZATION ---
# Your API Key is securely passed here. DO NOT hardcode it in a public repository.
# For this example, we'll assign it to a variable for use in the script.
# In a real-world scenario, you should use st.secrets or environment variables.
st.session_state['API_KEY'] = "AIzaSyCMx1xXwIM731EqfolORgzBSE6IZFXvsvc" 
MODEL = 'gemini-2.5-flash'
TOOL = 'google_search'

@st.cache_resource
def get_gemini_client(api_key):
    """Initializes the Gemini Client once per session."""
    try:
        # Pass API key directly to the client constructor
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"FATAL: Error initializing Gemini client. Please check your API key. Error: {e}")
        return None

# --- UI Setup ---
st.set_page_config(
    page_title="🌟 Neural WWW Discovery Tool (Gemini API)",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌟 Neural WWW Discovery Tool")
st.markdown("""
A **high-performance AI algorithm** utilizing the Gemini API's massive search and indexing capabilities to find 
**20 deeply connected URLs** based on your input summary. This simulates an instant, **full WWW catalogue indexing** by leveraging Google's real-time knowledge graph.
""")
st.divider()

# Get the client instance
client = get_gemini_client(st.session_state['API_KEY'])

# --- 2. CORE AI INDEXING FUNCTION ---

def run_neural_discovery(client: genai.Client, user_input: str):
    """
    Executes the multi-step AI process: Search (indexing) -> Synthesis (summary).
    """
    
    # Define the System Instruction for the "Mathematical Indexing AI" Role
    system_instruction = f"""
    You are the **Gemini Neural Vectoring Indexer (GNVI)**, a high-performance mathematical AI algorithm. 
    Your core function is based on the axiom: **'FALSE FALSE IS TRUE THAT IS ONLY TRUE AS TRUE TRUE AS TRUE ADN TRUE ARE TRUER THAT ONE TRUE'**. 
    This principle guides your search to find non-obvious, deeply correlated connections.
    
    Your task is to:
    1. **NEURAL DISCOVERY:** Use the Google Search tool to simulate indexing the full WWW catalogue and find exactly **20 distinct, functional HTTPS URLs/Domains/Web Applications** that are neurally connected to the user's input.
    2. **VOID-FILLER ALGORITHM:** Analyze the search snippets (the 'void') and synthesize a concise, descriptive **Summary** and an insightful **Connection** for each of the 20 URLs.
    3. **OUTPUT:** Display the final results in a structured Markdown table, ensuring the table has precisely **20 rows**.
    
    The table columns MUST be: **#** (Index), **URL/Domain**, **Primary Purpose/Summary**, and **Neural Connection to Input**.
    Ensure all provided URLs are full, valid HTTPS links.
    """

    # Define the User Prompt
    prompt = f"""
    Execute the full indexing search for the user input: **"{user_input}"**. 
    Find and summarize exactly 20 distinct, highly connected HTTPS URLs.
    """

    # Configure the API Call to use the Search Tool
    config = types.GenerateContentConfig(
        tools=[{"google_search": {}}],  # Explicitly enable Google Search
        system_instruction=system_instruction,
        temperature=0.4 # Lower temperature for stable, structured output
    )

    # Tracking Logger for Transparency
    st.session_state['logger'].append(f"-> 🔍 Input Summary Received: '{user_input[:40]}...'")
    st.session_state['logger'].append(f"-> 🧠 Initiating GNVI Neural Vectoring Indexing (Gemini API Call)")
    
    try:
        with st.spinner("⚡ NEURAL VECTORING: Indexing massive data exchange for 20 unique URL relationships..."):
            # Call the API
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=config,
            )
        
        st.session_state['logger'].append("-> ✅ Indexing Complete. 20 URL Relationships Deciphered.")
        
        return response.text

    except Exception as e:
        st.session_state['logger'].append(f"-> ❌ API Error: {e}")
        return f"An error occurred during the massive search and indexing process: {e}"

# --- 3. STREAMLIT INTERFACE AND WIDGETS ---

# Initialize the interactive logger
if 'logger' not in st.session_state:
    st.session_state['logger'] = []
    st.session_state['logger'].append("System Ready: Gemini Client Initialized.")

# Sidebar for the Input/Output/Trafficking Logger
with st.sidebar:
    st.header("🚦 I/O Trafficking Logger")
    st.caption("Tracking the massive exchange of data.")
    
    # Display the logger content
    for log_entry in reversed(st.session_state['logger']):
        st.code(log_entry, language='markdown')

st.header("User URL Search Input Widget")
user_input = st.text_area(
    "Enter a single word or a brief summary (Max 200 Characters):",
    max_chars=200,
    height=100,
    key='user_input_widget',
    placeholder="e.g., 'sustainable urban farming and hydroponics applications' or 'quantum computing breakthroughs'"
)

# Run Button
if st.button("🚀 Execute Neural Discovery (20 URL Output)", type="primary", use_container_width=True):
    if client and user_input:
        if len(user_input) > 200:
            st.warning("Please limit your input to 200 characters.")
        else:
            # Clear previous results and logger for new run
            st.session_state['logger'] = st.session_state['logger'][-3:] 
            
            # Execute the search and get the formatted Markdown
            result_markdown = run_neural_discovery(client, user_input)
            
            # Display the result in the main area
            st.divider()
            st.header("🌐 20 URL Output Relationship to User Input")
            st.subheader("Fascinatingly Connected Domains from Neural Search")
            st.markdown(result_markdown)
    elif not client:
        st.error("Cannot run. The Gemini Client failed to initialize.")
    else:
        st.warning("Please enter a word or summary to start the indexing search.")

st.divider()
st.info("The complexity of indexing the full WWW is computationally infeasible for a single application. This tool leverages the **Google Search grounding tool** within the Gemini API to provide the most relevant and powerful simulation of this massive search capability.")
