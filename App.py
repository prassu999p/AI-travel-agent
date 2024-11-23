import streamlit as st
import datetime
from datetime import timedelta
from main import TripCrew
import time
import traceback

def format_cities(cities_list):
    # Convert list of cities to a comma-separated string
    return ", ".join(cities_list)

def format_date_range(start_date, end_date):
    # Format dates into a string like "June 1-7, 2024"
    if start_date.month == end_date.month:
        return f"{start_date.strftime('%B %d')}-{end_date.strftime('%d')}, {end_date.year}"
    return f"{start_date.strftime('%B %d')} - {end_date.strftime('%B %d')}, {end_date.year}"

def main():
    st.set_page_config(
        page_title="AI Travel Planner", 
        page_icon="✈️",
        layout="wide"
    )
    
    st.title("✈️ AI Travel Planner")
    st.write("Let's plan your perfect trip using AI!")
    
    # Create two columns for input and output
    input_col, output_col = st.columns([1, 1])
    
    with input_col:
        st.subheader("Your Travel Details")
        
        # Origin
        origin = st.text_input(
            "Where will you be traveling from?", 
            placeholder="e.g., New York, London, Tokyo"
        )
        
        # Destinations
        destinations_input = st.text_area(
            "What cities are you interested in visiting? (one per line)",
            placeholder="e.g.:\nParis\nRome\nBarcelona"
        )
        destinations = [city.strip() for city in destinations_input.split("\n") if city.strip()]
        
        # Date Range
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                min_value=datetime.date.today(),
                value=datetime.date.today() + timedelta(days=30)
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                min_value=start_date,
                value=start_date + timedelta(days=7)
            )
        
        # Interests
        interests_options = [
            "Art & Museums", "History & Culture", "Food & Cuisine",
            "Nature & Outdoors", "Shopping", "Nightlife",
            "Architecture", "Local Experiences", "Photography",
            "Sports & Recreation", "Music & Entertainment"
        ]
        interests = st.multiselect(
            "What are your interests and hobbies?",
            options=interests_options,
            default=["Art & Museums", "Food & Cuisine"]
        )
    
    # Store the trip plan in session state to persist between reruns
    if 'trip_plan' not in st.session_state:
        st.session_state.trip_plan = None
    
    # Generate button
    if st.button("Generate Travel Plan", type="primary"):
        if not origin or not destinations or not interests:
            st.error("Please fill in all required fields!")
            return
        
        progress_placeholder = st.empty()
        with progress_placeholder.container():
            st.info("Our AI agents are crafting your perfect travel plan...")
            
            try:
                # Format inputs for TripCrew
                formatted_cities = format_cities(destinations)
                formatted_date_range = format_date_range(start_date, end_date)
                formatted_interests = ", ".join(interests)
                
                # Create and run TripCrew
                trip_crew = TripCrew(
                    origin=origin,
                    cities=formatted_cities,
                    date_range=formatted_date_range,
                    interests=formatted_interests
                )
                
                # Store result in session state
                st.session_state.trip_plan = trip_crew.run()
                progress_placeholder.success("✨ Travel plan generated successfully!")
                
            except Exception as e:
                error_msg = f"An error occurred while generating your travel plan: {str(e)}"
                st.error(error_msg)
                
                # Log the full error for debugging
                st.error("Technical details for support:")
                st.code(traceback.format_exc())
                return
            
            finally:
                # Clean up any resources if needed
                time.sleep(1)  # Give users time to see the success/error message
                progress_placeholder.empty()
    
    # Display output in the right column
    with output_col:
        if st.session_state.trip_plan:
            st.subheader("Your Personalized Travel Plan")
            
            # Display selected preferences
            with st.expander("Your Travel Preferences", expanded=True):
                st.write(f"🛫 From: {origin}")
                st.write(f"📍 Destinations: {format_cities(destinations)}")
                st.write(f"📅 Date Range: {format_date_range(start_date, end_date)}")
                st.write(f"💝 Interests: {', '.join(interests)}")
            
            # Display the AI-generated plan
            st.markdown("### AI Generated Travel Plan")
            st.markdown(st.session_state.trip_plan)
            
            # Add download button for the plan
            st.download_button(
                "Download Travel Plan",
                st.session_state.trip_plan,
                file_name="travel_plan.txt",
                mime="text/plain"
            )
            
            # Helpful tips
            with st.expander("Travel Tips", expanded=False):
                st.info("""
                💡 Next Steps:
                - Review the suggested itinerary and adjust as needed
                - Check visa requirements for your destinations
                - Look into travel insurance options
                - Book accommodations and flights early for better rates
                - Research local customs and etiquette
                """)

if __name__ == "__main__":
    main()