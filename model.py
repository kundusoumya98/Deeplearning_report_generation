import streamlit as st
import os
import numpy as np
import time
from PIL import Image
import create_model as cm

st.markdown("<small>by Soumya Kundu ,Jadavpur University</small>",unsafe_allow_html=True)
st.title("Chest X-ray Report Generator")

st.markdown("\nThis app will generate impression part of an X-ray report.\nYou can upload 2 X-rays that are front view and side view of chest of the same individual.")
st.markdown("The 2nd X-ray is optional.")


col1,col2 = st.columns(2)
image_1 = col1.file_uploader("X-ray 1",type=['png','jpg','jpeg'])
image_2 = None
if image_1:
    image_2 = col2.file_uploader("X-ray 2 (optional)",type=['png','jpg','jpeg'])

col1,col2 = st.columns(2)
predict_button = col1.button('Predict on uploaded files')


#@st.cache
def create_model():
    model_tokenizer = cm.create_model()
    return model_tokenizer


def predict(image_1,image_2,model_tokenizer,predict_button = predict_button):
    start = time.process_time()
    if predict_button:
        if (image_1 is not None):
            start = time.process_time()  
            image_1 = Image.open(image_1).convert("RGB") #converting to 3 channels
            image_1 = np.array(image_1)/255
            if image_2 is None:
                image_2 = image_1
            else:
                image_2 = Image.open(image_2).convert("RGB") #converting to 3 channels
                image_2 = np.array(image_2)/255
            st.image([image_1,image_2],width=300)
            caption = cm.function1([image_1],[image_2],model_tokenizer)
            st.markdown(" ### **Impression:**")
            impression = st.empty()
            impression.write(caption[0])
            time_taken = "Time Taken for prediction: %i seconds"%(time.process_time()-start)
            st.write(time_taken)
            del image_1,image_2
        else:
            st.markdown("## Upload an Image")


    

model_tokenizer = create_model()


predict(image_1,image_2,model_tokenizer)
