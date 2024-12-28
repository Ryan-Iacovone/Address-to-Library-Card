from c_to_c_functions import *
import streamlit as st

st.title("📩 Street Address to Library Card!")
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

    # Takes county subdivision and returns what kind of card the patron gets

    # Taking the county_subdivision input gathered from an API and converting it to lowercase to match list
    #county_subdivision = "East Grand Rapids city"
    county_subdivision = county_subdivision.lower()

    st.divider() 

    if county_subdivision in kdl_townships: 
        print("KDL Card!")
        st.write("KDL Card! :sunglasses:")
    elif county_subdivision == "grand rapids city":
        print("GRPL Card!")
        st.write("GRPL Card!")
    elif county_subdivision in llc_townships_list:
        if county_subdivision == "ensley township":
            print("PANIC IT's ENSLEY")
            st.write("PANIC IT's ENSLEY")
        else:
            print(f"LLC card for {county_subdivision}. Please direct patron to '{llc_dict[county_subdivision]}' in {county_subdivision}.")
            st.write(f"LLC card for {county_subdivision}. Please direct patron to '{llc_dict[county_subdivision]}' in {county_subdivision}.")
    else: 
        print("Not in our LLC system")
        st.write("Not in our LLC system")
