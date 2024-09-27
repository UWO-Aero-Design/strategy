import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

class SimplifiedMissionScoreModel:
    def __init__(self, payload_weight=2):
        self.autonomous_multipliers = {
            'Conventional_Takeoff': 2,
            'Payload_Release': 3,
            'Payload_Delivery': 8,
            'Payload_Capture': 12,
            'Return_To_Base': 3
        }
        self.manual_multipliers = {
            'Conventional_Takeoff': 1,
            'Payload_Release': 1,
            'Payload_Delivery': 1,
            'Payload_Capture': 2,
            'Return_To_Base': 1
        }
        self.payload_weight = payload_weight

    def calculate_segment_score(self, segment, is_autonomous):
        if is_autonomous:
            return self.autonomous_multipliers[segment] * self.payload_weight + 1
        else:
            return self.manual_multipliers[segment] * self.payload_weight + 1

    def calculate_mission_score(self, segments, time_bonus):
        segment_score = sum(self.calculate_segment_score(segment, is_autonomous) 
                            for segment, is_autonomous in segments)
        return segment_score + time_bonus

def main():
    st.set_page_config(layout="wide")
    
    # Custom CSS
    st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stSlider > div > div > div {
        background-color: #f0f2f6;
    }
    .stRadio > div {
        flex-direction: row;
        gap: 1rem;
    }
    .stRadio label {
        background-color: #f0f2f6;
        padding: 0.3rem 0.8rem;
        border-radius: 0.5rem;
    }
    .results-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .column-gap {
        border-left: 2px solid #e0e0e0;
        padding-left: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🛩️ Mission Score Calculator")

    # Create three columns for the main layout (left, gap, right)
    col1, col_gap, col2 = st.columns([10, 1, 8])

    with col1:
        st.header("Mission Configuration")

        with st.expander("Aircraft and Payload Weights", expanded=True):
            # Aircraft weight slider
            aircraft_weight = st.slider("Aircraft Weight (lbs)", min_value=0.0, max_value=3.5, value=2.0, step=0.1)

            # Calculate max payload weight
            max_payload_weight = round(3.5 - aircraft_weight, 1)

            # Payload weight slider
            payload_weight = st.slider("Payload Weight (lbs)", min_value=0.0, max_value=max_payload_weight, value=min(1.5, max_payload_weight), step=0.1)

        st.subheader("Mission Segments")
        segments = [
            "Conventional_Takeoff",
            "Payload_Release",
            "Payload_Delivery",
            "Payload_Capture",
            "Return_To_Base"
        ]

        # Create checkboxes and radio buttons for each segment
        selected_segments = []
        for segment in segments:
            segment_col1, segment_col2 = st.columns([2, 3])
            with segment_col1:
                if st.checkbox(f"{segment.replace('_', ' ')}", key=f"include_{segment}"):
                    with segment_col2:
                        is_autonomous = st.radio("Mode", ["Manual", "Autonomous"], key=f"mode_{segment}", horizontal=True)
                    selected_segments.append((segment, is_autonomous == "Autonomous"))

        # Time bonus selection
        st.subheader("Mission Time")
        time_bonus_options = {
            "Under 2 minutes": 2,
            "Under 3 minutes": 1,
            "Under 4 minutes": 0
        }
        time_bonus_selection = st.select_slider("Select mission time", options=list(time_bonus_options.keys()))
        time_bonus = time_bonus_options[time_bonus_selection]

    with col2:
        st.markdown('<div class="column-gap">', unsafe_allow_html=True)
        st.header("Mission Results")

        # Calculate score
        model = SimplifiedMissionScoreModel(payload_weight=payload_weight)
        score = model.calculate_mission_score(selected_segments, time_bonus)

        # Display score
        st.markdown(f"<h2 style='text-align: center;'>Total Mission Score: {score:.2f}</h2>", unsafe_allow_html=True)

        # Create a card-like container for results
        with st.container():
            st.markdown("<div class='results-card'>", unsafe_allow_html=True)
            
            st.subheader("Segment Breakdown")
            for segment, is_autonomous in selected_segments:
                segment_score = model.calculate_segment_score(segment, is_autonomous)
                mode = "Autonomous" if is_autonomous else "Manual"
                st.write(f"• {segment.replace('_', ' ')} ({mode}): {segment_score:.2f}")

            st.subheader("Mission Details")
            st.write(f"Time Bonus: {time_bonus:.2f}")
            st.write(f"Aircraft Weight: {aircraft_weight:.1f} lbs")
            st.write(f"Payload Weight: {payload_weight:.1f} lbs")
            st.write(f"Total Weight: {aircraft_weight + payload_weight:.1f} lbs")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()