#@Name : Multilingual Storytelling with Accents
#@Author : Sujith K S
#Description:
#This project aims to develop a system that translates text into various languages and
#converts the translated text into speech. The system is designed to be user-friendly and
#interactive, allowing users to either enter text directly or upload a file in various formats
#(PDF, TXT, Excel, CSV). The text is then translated into a language selected by the user
#from a dropdown menu.

import streamlit as st
import pandas as pd
from gtts import gTTS
from dotenv import load_dotenv
import os
import time
import openai
import pandas as pd
import random
import time
#import PyPDF2

from Utility import Utility
from Logger import Logger

#create instance of Utility class
utility= Utility()  
#reate instance of Logger
logger =Logger()        

# Load environment variables from .env file
load_dotenv()

#Save and play the translated text
def save_play_text_translated(file_text,option):
    #logger.debug(f'Save audio file {file_text}')
    text=file_text
    
    language=option
    output=gTTS(text=text,lang=language,slow=True)
    mp3_file=f'{language}.mp3'
    output.save( mp3_file)
    time.sleep(2)  #fix for stopping and exception


#Translate the text using a promt and LLM as  OpenAi -gpt-3.5-turbo 
def translate_text(text_to_traslate, target_language):
    #logger.debug(f'Translate input :  {text_to_traslate}')
    # Set your OpenAI API key

    # Construct the promt  for chat-based completion
    messages = [
        {"role": "system", "content": f"You are a helpful assistant that translates text to {target_language}."},
        {"role": "user", "content": f"Translate the following text to {target_language}: {text_to_traslate}"}
    ]

    from openai import OpenAI

    client = OpenAI(api_key = os.getenv('API_KEY') )

   # Call the OpenAI API
    response=client.chat.completions.create(
        model=os.getenv('MODEL_NAME'),
        messages=messages,
        max_tokens=100,  # Adjust max_tokens as needed
        temperature=0.3,
    )

    # Extract and return the translated text
    translation = response.choices[0].message.content.strip()#['content'].strip()    
    #translated_text = translate_text(text_to_translate, target_language)
    logger.debug(f'Translate output :  {translation}')
    return translation

    
# Function to update the session state
def update_text_area(new_text):
    logger.debug(f'Text Area - input : {new_text}')
    user_input=new_text
    st.text_area('Uploaded to translate',user_input,key='user_input_upload') 
    return  user_input 

#Get the text area text
def get_text_area():
     return user_input

#Save the text file
def save_text_file(text,target_lang):
     # Save the string to a file
    with open(f'{target_lang}.txt', "w", encoding="utf-8") as file:
     file.write(text)

#Get the selected option
def get_selected_optionq():
    #The target language translation options
    lang_options=['en[English]', 'fr[French]', 'ru[Russian]','pt[Portugese]','es[Spanish]','zh-CN[Chinese]']
    #The combo box to show the translation language options
    option1 = st.selectbox('Select Target Language to Translate:', lang_options ,key=f'option_select{random.random()}')
    return option1
        
#This method with do the translation of the file & display the translated text
def processTranslation(user_input,target_lang_option):
        logger.debug(f'processTranslation start  {user_input} {target_lang_option}')
        # Display the file content                  
        language=target_lang_option.split("[")[0] 
        #file_content=text_in_text_area
        save_play_text_translated(user_input,language) 
        # Example usage
        text_to_translate =user_input 
        target_language=language    
        translated_text=translate_text(text_to_translate, target_language)
        #save the file
        save_text_file(translated_text,target_lang_option)


#Event hadler for  language selection option
def handle_option(option):
     st.session_state.option=option

#Get the  target language  option
def get_target_lang_option():
     return st.session_state.option

#Handle the text input events
def handle_text_input(user_input):
     st.session_state.text_area_content=user_input    



# Title of the Story Telling application
st.title("Please upload file or type to translate and download text & voice file..")
# Upload file as Text,PDF,CSV,Excel
uploaded_file = st.file_uploader("Choose a file",type=["csv", "xlsx", "txt","pdf"])
#The default text message  in text area
Initial_text="Welcome to Story Telling Project.Please enter text or upload file (text,pdf,csv,excel) to translate & Play."

#update_text_area(Initial_text)
#er_input =st.text_area('Source Text to translate',value=st.session_state.text_value,key='user_input') 
user_input =st.text_area('User Input Text to translate',Initial_text,key='user_input') 
#The target language translation options
lang_options=['en[English]', 'fr[French]', 'ru[Russian]','pt[Portugese]','es[Spanish]','zh-CN[Chinese]']
#Initialise language combo 
st.session_state.option   =lang_options[0]
#The combo box to show the translation language options
option= st.selectbox('Select Target Language to Translate:', lang_options ,key='option_select') 
#Handle  dropdown events
handle_option(option)

# Buttun event handling
if st.button(f'Translate to {st.session_state.option}'):
     logger.debug('BUTTON called ### {st.session_state.option}')
     target_lang_option=st.session_state.option
     user_input=get_text_area()
     processTranslation(user_input,target_lang_option)
else:
    pass

# Check if a file has been uploaded or not(show errro handling)
if uploaded_file is not None:
    # Determine the file type
    file_type = uploaded_file.type
    #logger.debug(f'File upload ######### {file_type}')
    
    # Handle file based on its type
    if file_type == "text/csv":
         #logger.debug('csv')
         text=utility.read_csv(uploaded_file)
         #logger.debug('text area trext ',text)
         target_lang=get_target_lang_option()
         processTranslation(text,target_lang)
    # Handle file based on its type
    elif file_type == "application/pdf":
         #logger.debug('pdf')
         text=utility.read_pdf(uploaded_file)
         #logger.debug('text area trext ',text)
         target_lang=get_target_lang_option()
         processTranslation(text,target_lang)
        #handle_csv(uploaded_file)        
    elif file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
           logger.debug(f'excel {uploaded_file}')
           text=utility.read_excel_file(uploaded_file)
           #logger.debug('text area trext ',text)
           target_lang=get_target_lang_option()
           processTranslation(text,target_lang)
    elif file_type == "text/plain":
           #logger.debug('text')
           text=  uploaded_file.read().decode("utf-8")#utility.read_text(uploaded_file)
           #update_text_area(text)
           #logger.debug('text area trext ',text)
           target_lang=get_target_lang_option()
           processTranslation(text,target_lang)
  






