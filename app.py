import os
import json
import re
import google.generativeai as genai
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# 1. Secure API Configuration
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") # Ensure your .env file has: GEMINI_API_KEY=your_key
genai.configure(api_key=api_key)

def robust_json_parser(text):
    """Sanitizes LLM output to extract pure JSON."""
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return json.loads(text)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return None

def get_vehicle_params(user_voice_input):
    """Engineers the prompt to map Mumbai context to ML parameters."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    system_instruction = """
    You are an AI Vehicle Gateway for an EV in Mumbai. 
    Convert driver speech into a JSON object for an XGBoost range model.
    
    Rules:
    - Mention of 'Rain/Monsoon/Water' -> set 'road_friction' to 0.5.
    - Mention of 'Dadar/WEH/Traffic' -> set 'traffic_index' to 9.
    - Mention of 'ASAP/Fast' -> set 'drive_mode' to 2 (Sport).
    - Mention of 'Battery/Range' -> set 'priority_weight' to 0.9 (Eco).

    Output ONLY: {"drive_mode": 0-2, "traffic_index": 1-10, "road_friction": 0.1-1.0, "priority_weight": 0.1-1.0}
    """
    
    response = model.generate_content(f"{system_instruction}\n\nDriver: {user_voice_input}")
    return robust_json_parser(response.text)

def show_dashboard(data):
    """Visualizes the interpreted data for the GitHub showcase."""
    if not data: return

    keys = list(data.keys())
    values = list(data.values())

    plt.style.use('dark_background')
    plt.figure(figsize=(10, 5))
    
    colors = ['#00FFCC', '#FF3366', '#FFCC00', '#3399FF']
    bars = plt.bar(keys, values, color=colors, alpha=0.8)
    
    plt.title("EV INTELLIGENCE GATEWAY: PARAMETER MAPPING", fontsize=14, color='white', pad=20)
    plt.ylim(0, 10)
    plt.grid(axis='y', linestyle='--', alpha=0.2)
    
    # Adding labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.2, yval, ha='center', color='white')

    print("\n[VIRTUAL DASHBOARD] Displaying interpreted parameters...")
    plt.show()

if __name__ == "__main__":
    # Test with a complex Mumbai scenario
    driver_command = "It's raining heavily near Sion Circle, I'm late for work so drive fast but watch the battery."
    
    print(f"Driver Voice Input: '{driver_command}'")
    interpreted_data = get_vehicle_params(driver_command)
    
    if interpreted_data:
        print(f"Interpreted Logic: {interpreted_data}")
        show_dashboard(interpreted_data)
