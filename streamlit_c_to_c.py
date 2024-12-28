from c_to_c_functions import *
import streamlit as st

st.title("📩 Street Address to Library Card")
st.divider()

# 212 Saunders Ct NE, Grand Rapids, MI 49505
street_address = st.text_input("Enter your street address:")



if st.button("Enter", type="primary"):

    # Using the geopy library to take a street address as input and return lat and long coordinates
    latitude, longitude = get_coordinates(street_address)

    # Function to take latitude and longitude and return tile coordinates (which is what census reporter uses)
    county_subdivision, full_name = coordinates_to_csubdivision(latitude, longitude)

    st.write(f"The address '{street_address}' is located in {full_name} with the coordindates:")
    st.write(f"\n latitude: {latitude} longitude: {longitude}.")

    # Ascetic divider 
    st.divider() 

    # Based on the inputted county_subdivision returns what librarythe patrons should get
    results_df = csubdivision_to_lib_df(county_subdivision, street_address)

    # Loading in the Address DB, appending the current address results, and then resaves it 
    resave_json(results_df)
