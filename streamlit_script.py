from pkg_resources import DEVELOP_DIST
import streamlit as st
import pandas as pd
import pickle
from PIL import Image
pd.set_option("display.max_rows",40)
# pd.set_option("display.max_columns", 10)

image = Image.open('images/img1.png')
st.image(image)

def query_text(payload, model_id, api_token):
	headers = {"Authorization": f"Bearer {api_token}"}
	API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

model_id_text = "cardiffnlp/twitter-roberta-base-offensive"
model_id_image = "ogimgio/start-hack-supercell"
api_token = "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"

#vision transformer
from transformers import ViTFeatureExtractor, ViTForImageClassification
import torch
#import torch
from PIL import Image
import requests

# load the model and feature extractor
model_name = 'ogimgio/start-hack-supercell'
model = ViTForImageClassification.from_pretrained(model_name)
feature_extractor = ViTFeatureExtractor.from_pretrained(model_name)

# Set the page title
st.title("Our Solution - Team Inspect")
st.markdown("## Automation Part 1 - Offensive Speech Reporter")
st.markdown("This part defines the bully and vulnerable victim point of views, in an ideal application.")
st.markdown("### From the point of view of the bully")
st.markdown("You, as the bully, write an offending message in the Supercell game environment")
def show_popup():
    # Define the HTML and JavaScript code for the popup window
    html = """
        <style>
        .popup {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 400px;
            height: 200px;
            padding: 20px;
            background-color: white;
            border: 1px solid black;
            border-radius: 5px;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.25);
            z-index: 9999;
            text-align: center;
            font-family: sans-serif;
        }
        .popup h1 {
            text-align: center;
        }
        .popup p{
            text-align: center;
        }
        button {
            padding: 10px 15px;
        }
        #buttons {
            display: flex;
            justify-content: space-evenly;
        }
        #success{
            display: none;
            padding: auto;
        }
        #ban {
            display: none;
            padding: auto;
        }
    </style>

    <div class="popup" id="popup-container">
        <h1>Warning!</h1>
        <p>You are trying to write an offensive message in chat. If you continue, your account may be punished.</p>
        <div id="buttons">
            <button onclick="send()">Send</button>
            <button onclick="cancel()">Cancel</button>
        </div>
    </div>

    <div class="popup" id="success">
        <h1>Thank you!</h1>
        <p>Thank you for your cooperation!</p>
        <button onclick="closePopup()">Ok</button>
    </div>

    <div class="popup" id="ban">
        <h1>Oops!</h1>
        <p>You are muted for sending offensive messages to chat!</p>
        <button onclick="closePopup()">Ok</button>
    </div>

    <script>
        // Define a function to close the popup window

        function cancel() {
            document.getElementById('popup-container').style.display = "none";
            document.getElementById('success').style.display = "block";
        }
        function send() {
            document.getElementById('popup-container').style.display = "none";
            document.getElementById('ban').style.display = "block";
        }
        function closePopup() {
            document.getElementById('ban').style.display = "none";
            document.getElementById('success').style.display = "none";
        }
    </script>
    """

    # Render the HTML and JavaScript code in a popup window
    st.components.v1.html(html, height=300)
def show_second_popup():
    # Define the HTML and JavaScript code for the popup window
    html = """
        <style>
        .popup {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 400px;
            height: 200px;
            padding: 20px;
            background-color: white;
            border: 1px solid black;
            border-radius: 5px;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.25);
            z-index: 9999;
            text-align: center;
            font-family: sans-serif;
        }
        .popup h1 {
            text-align: center;
        }
        .popup p{
            text-align: center;
        }
        .popup button {
            margin: auto;
        }
        button {
            padding: 10px 15px;
        }
        #buttons {
            display: flex;
            justify-content: space-between;
        }
        #success{
            display: none;
            padding: auto;
        }
    </style>

    <div class="popup" id="popup-container">
        <h1>Report a message</h1>
        <p>We might think this message contains offensive content. You may want to report a message from chat. False reports will be penalized!</p>
        <div id="buttons">
            <button onclick="send()">Send</button>
            <button onclick="closePopup()">Cancel</button>
        </div>
    </div>

    <div class="popup" id="success">
        <h1>Thank you</h1>
        <p>Thank you for your cooperation!</p>
        <button onclick="closePopup()">Ok</button>
    </div>

    <script>
        // Define a function to close the popup window
        function send() {
            var popupContainer = document.getElementById('popup-container');
                popupContainer.parentNode.removeChild(popupContainer);
            document.getElementById('success').style.display = "block";
        }
        function closePopup() {
            var popupContainer = document.getElementById('popup-container');
            if(popupContainer!=null) popupContainer.parentNode.removeChild(popupContainer);
            var success = document.getElementById('success');
            success.parentNode.removeChild(success);
        }
    </script>
        """
    # Render the HTML and JavaScript code in a popup window
    st.components.v1.html(html, height=300)

# Add a text input field for the user to enter their message
if "load_state" not in st.session_state:
    st.session_state.load_state = False
user_input = st.text_input("Enter a message:")
if st.button('Send') or st.session_state.load_state:
    st.session_state.load_state = True
    with st.spinner('Checking for offensive speech...'):
        if user_input:
            # Get the label-score pairs for the first example
            is_offensive = query_text(user_input, model_id_text, api_token)
            print(is_offensive)
            try:
                example_data = is_offensive[0]
            except:
                st.error("Something went wrong! Please try again later.")
            # Sort the label-score pairs by score in descending order
            sorted_data = sorted(example_data, key=lambda x: x['score'], reverse=True)
            # Get the label with the highest score
            most_probable_label = sorted_data[0]['label']
            if most_probable_label == 'offensive':
                show_popup()
            else:
                st.success("No offensive speech detected!")


st.markdown("### From the point of view of the vulnerable person")
st.markdown("As the victim, this is what you would see.")

if st.button('Get new messages'):
    with st.spinner('Checking for offensive speech...'):
        st.markdown("User xy wrote: Son of a b****!")
        is_offensive = query_text('Son of a bitch!', model_id_text, api_token)
        example_data = is_offensive[0]
        # Sort the label-score pairs by score in descending order
        sorted_data = sorted(example_data, key=lambda x: x['score'], reverse=True)
        # Get the label with the highest score
        most_probable_label = sorted_data[0]['label']
        if most_probable_label == 'offensive':
            show_second_popup()
        else:
            st.success("The text is clean!")

st.markdown("## Automation Part 2 - Offensive Bases Detection")
st.markdown("This section includes our model used for Image Detection. Try it on these three images below!")

image = Image.open('images/1.jpg')

col1, col2, col3 = st.columns(3)

with col1:
    image = Image.open('images/1.jpg')
    st.image(image, caption='Ground truth: Non-Offensive Image')

with col2:
    image = Image.open('images/2.jpg')
    st.image(image, caption='Ground truth: Offensive Image')



with col3:
    image = Image.open('images/3.jpg')
    st.image(image, caption='Ground truth: Offensive Image')

st.markdown('The output of of the three images is the following:')
checkbox_clicked = False
if st.checkbox('Run Image detector',disabled=checkbox_clicked):
    with st.spinner('Detecting offensive images...'):
        checkbox_clicked = True
        for i in range(1,4):
            # load the input image and preprocess it
            image = Image.open('images/'+str(i) + '.jpg')
            inputs = feature_extractor(images=image, return_tensors='pt')
            # perform inference and get the predicted label
            outputs = model(**inputs)
            predicted_label = torch.argmax(outputs.logits).item()
            predicted_label = 'Offensive' if predicted_label == 1 else 'Non-Offensive'
            st.markdown(f'* Image number {i}: Classified as {predicted_label}')


st.markdown("## Moderation System")
st.markdown("More on the full description on GitHub.")
image = Image.open('images/moderator_sys.jpeg')
st.image(image, caption='Offensive Image')
