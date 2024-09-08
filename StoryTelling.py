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
import os
import time
import openair
import pandas as pd
import randomr
import PyPDF2

 


#Read a text file
def read_text(file):
    file_text=uploaded_file.read().decode("utf-8")
    return (file_text)

#read csv file
def read_csv(file): 
    df = pd.read_csv(file)
    if df.empty:
        print("DataFrame is empty")
    else:
         print("DataFrame is not empty")
    # Check if any element is True
    if df.any().any():
        print("At least one True value exists in the DataFrame")
    else:
        print("No True values exist in the DataFrame")
    # Check if all elements are True
    if df.all().all():
        print("All elements are True in the DataFrame")
    else:
        print("Not all elements are True in the DataFrame")

    column_to_extract = df.columns    
    # Extract and display the text from the selected column
    extracted_text = df[column_to_extract].astype(str)#.tolist()
    return extracted_text 

#Read excel file
def read_excel_file(file):
    print(file)
    if file is not None:
        print('1')
        try:
            # Read all sheets from the Excel file
            excel_data = pd.read_excel(file, sheet_name=None).to_string()
            print('2')
            # Display the sheet names
            #sheet_names = list(excel_data.keys())
            print('3')
            print(excel_data)
            return excel_data
        except Exception as e:
            print(f"Error reading the Excel file: {e}")
    else:
            print("Please upload an Excel file to read.")
#Unit test methods
#read_excel_file('test.xlsx')  
#print(read_text('story.txt') )
#print(read_csv('test.csv')) 
#print(read_pdf('transformer.pdf'))
            


#Save and play the translated text
def save_play_text_translated(file_text,option):
    text=file_text
    language=option
    output=gTTS(text=text,lang=language,slow=True)
    mp3_file=f'{language}.mp3'
    output.save( mp3_file)


#Translate the text using a promt and LLM as  OpenAi -gpt-3.5-turbo 
def translate_text(text_to_traslate, target_language):
    # Set your OpenAI API key
    api_key = ''
    # Construct the promt  for chat-based completion
    messages = [
        {"role": "system", "content": f"You are a helpful assistant that translates text to {target_language}."},
        {"role": "user", "content": f"Translate the following text to {target_language}: {text_to_traslate}"}
    ]

    from openai import OpenAI

    client = OpenAI(api_key = '' )

   # Call the OpenAI API
    response=client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,  # Adjust max_tokens as needed
        temperature=0.3,
    )

    # Extract and return the translated text
    translation = response.choices[0].message.content.strip()#['content'].strip()
    return translation
    translated_text = translate_text(text_to_translate, target_language)
    #print(f"Translated text: {translated_text}")
    return translation


# Initialize session state for text area if it doesn't exist
if 'text_value' not in st.session_state:
    st.session_state.text_value = ""
    
# Function to update the session state
def update_text_area(new_text):
    print('update text value to set #########',new_text)
    st.session_state.text_value =new_text
    st.session_state.text_value =new_text
    print('update text value afetr set  #########',st.session_state.text_value)
    return  st.session_state.text_value 

#Get the text area text
def get_text_area():
     return st.session_state.text_value

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
        print('processTranslation start  ',user_input,'\n',target_lang_option)
        # Display the file content                  
        language=target_lang_option.split("[")[0] 
        print('12')
        #file_content=text_in_text_area
        save_play_text_translated(user_input,language) 
        #translated text
        # Example usage
        text_to_translate =user_input 
        target_language=language
    
        translated_text=translate_text(text_to_translate, target_language)
        #print(f"Translated text: {translated_text}")
        #save the file
        save_text_file(translated_text,target_lang_option)
        #st.text_area(f'Translated Text to {translated_text}',translated_text,key='translated_text_ardea') 


#Event hadler for  language selection option
def handle_option(option):
     print('handle_option ######## ',option)
     st.session_state.option=option

#Get the  target language  option
def get_target_lang_option():
     return st.session_state.option

#Handle the text input events
def handle_text_input(user_input):
     print('process text ######',user_input)
     st.session_state.text_area_content=user_input
     



# Title of the Story Telling application
st.title("Please upload file or type to translate and download text & voice file..")
# Upload file as Text,PDF,CSV,Excel
uploaded_file = st.file_uploader("Choose a file",type=["csv", "xlsx", "txt","pdf"])
#The default text message  in text area
Initial_text="Welcome to Story Telling Project.Please enter text or upload file (text,pdf,csv,excel) to translate & Play."

# Initialize session state for text area if not already set
if 'text_area_content' not in st.session_state:
    st.session_state.text_area_content = Initial_text
 
update_text_area(Initial_text)
user_input =st.text_area('Source Text to translate',value=st.session_state.text_value,key='user_input') 
#Teaxt  area handklert
handle_text_input(user_input)  

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
     print('BUTTON called ###',st.session_state.option)
     target_lang_option=st.session_state.option
     user_input=get_text_area()
     processTranslation(user_input,target_lang_option)
else:
    pass# update_text_area(Initial_text)

#Show  trnslation option direct text entry and translation by user
#processTranslation(Initial_text)
# Check if a file has been uploaded or not(show errro handling)
if uploaded_file is not None:
    # Determine the file type
    file_type = uploaded_file.type
    #print('File upload #########',file_type)
    
    # Handle file based on its type
    if file_type == "text/csv":
         #print('csv')
         text=read_csv(uploaded_file)
         #print('text area trext ',text)
         target_lang=get_target_lang_option()
         processTranslation(text,target_lang)
    # Handle file based on its type
    elif file_type == "application/pdf":
         #print('pdf')
         text=""#read_pdf(uploaded_file)
         #print('text area trext ',text)
         target_lang=get_target_lang_option()
         processTranslation(text,target_lang)
        #handle_csv(uploaded_file)        
    elif file_type == "application./vnd.openxmlformats-officedocument.spreadsheetml.sheet":
           #print('excel',uploaded_file)
           text=read_excel_file(uploaded_file)
           #print('text area trext ',text)
           target_lang=get_target_lang_option()
           processTranslation(text,target_lang)
    elif file_type == "text/plain":
           #print('text')
           text=read_text(uploaded_file)
           #update_text_area(text)
           #print('text area trext ',text)
           target_lang=get_target_lang_option()
           processTranslation(text,target_lang)
  






