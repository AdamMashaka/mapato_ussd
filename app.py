import streamlit as st
import requests

# Function to call NASA API with coordinates
def get_farm_analysis(latitude, longitude):
    API_BASE_URL = "https://nasa-challenge-hackathon.onrender.com/farm-analysis"
    payload = {
        "latitude": latitude,
        "longitude": longitude
    }

    try:
        response = requests.post(API_BASE_URL, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None

# JavaScript to fetch location
get_location_js = """
<script>
function getLocation() {
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const coords = position.coords;
            const locationData = {
                latitude: coords.latitude,
                longitude: coords.longitude
            };
            window.dispatchEvent(new CustomEvent('user-location', { detail: locationData }));
        },
        (error) => {
            console.error(error);
        }
    );
}
getLocation();
</script>
"""

def main():
    st.title("Farm Analysis Using NASA Earth Observation Data")
    
    # Display option to use current location or manually enter coordinates
    use_current_location = st.checkbox("Use my current location")

    if use_current_location:
        st.write("Fetching your location...")
        # Inject JavaScript to get the user's location
        st.components.v1.html(get_location_js)

        # Placeholder for coordinates
        location_placeholder = st.empty()

        # Wait for the location event from JavaScript
        location_event = st.experimental_get_query_params()
        latitude, longitude = None, None

        if "latitude" in location_event and "longitude" in location_event:
            latitude = location_event["latitude"][0]
            longitude = location_event["longitude"][0]
            location_placeholder.text(f"Your location: Latitude: {latitude}, Longitude: {longitude}")
        else:
            st.warning("Waiting for your location...")
        
    else:
        # If the user chooses not to use current location, allow manual input
        st.subheader("Enter Farm Coordinates:")
        latitude = st.text_input("Latitude")
        longitude = st.text_input("Longitude")

    # When the user clicks the "Analyze" button
    if st.button("Analyze"):
        if latitude and longitude:
            st.info("Analyzing farm data...")
            result = get_farm_analysis(latitude, longitude)
            if result:
                st.success("Analysis Complete!")
                st.json(result)
        else:
            st.warning("Please enter both latitude and longitude.")

if __name__ == "__main__":
    main()
