import streamlit as st
import requests
import json

# Set up the Streamlit app layout (this must be the first command)
st.set_page_config(page_title="ClimAct", page_icon="🌍", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Center and color the title */
    .title {
        text-align: center;
        color: green;
    }

    /* Make text input and text area stretchable */
    .stTextInput textarea, .stTextArea textarea {
        resize: both;  /* Make it stretchable both horizontally and vertically */
        height: auto;  /* Allow the text box to grow in height */
    }

    """,
    unsafe_allow_html=True
)

# Header and description (with the new title style)
st.markdown("<h1 class='title'>ClimAct</h1>", unsafe_allow_html=True)
st.subheader("Your intelligent assistant for understanding and combating the effects of climate change.")
st.write(
    """
    Powered by advanced AI and the ReAct framework, ClimAct analyzes climate data specific to your region.
    """
)

# Text input for the user to enter the prompt (stretchable text box)
prompt = st.text_input("Enter a city or a custom prompt to generate climate action recommendations:")

# Button to trigger the action
if st.button("Generate Actions"):
    if prompt:
        # Use the provided API Gateway URL
        api_url = 'https://jamdu40uje.execute-api.us-east-1.amazonaws.com/prod/climate-recommendations'

        # Send a POST request to the API Gateway with the entered prompt
        if prompt.lower() in ["cairo", "new york", "tokyo", "paris",
                              "london", "dubai", "beijing", "sydney", "mumbai", "moscow"]:
                              response = requests.post(api_url, headers={"Content-Type": "application/json"}, data=json.dumps({"prompt": f"give five short recommendations to be take by the people of {prompt} to fight cilmate change"}))
        else:
            response = requests.post(api_url, headers={"Content-Type": "application/json"}, data=json.dumps({"prompt": prompt}))

        # Display the response or handle the error
        if response.status_code == 200:
            # Extract the 'body' field from the response
            body = json.loads(response.json()["body"])
            content = body.get("content", [])

            # Check if the content exists and extract text from it
            if content and isinstance(content, list):
                recommendations = " ".join([c["text"] for c in content if c["type"] == "text"])
            else:
                recommendations = "No recommendations found."

            # Display the recommendations in the text area (stretchable text box)
            st.text_area("Recommended actions will appear here:", value=recommendations, height=200)
        else:
            st.error(f"Error: {response.status_code}. Could not get recommendations. Please try again.")
    else:
        st.warning("Please enter a prompt to generate recommendations.")
