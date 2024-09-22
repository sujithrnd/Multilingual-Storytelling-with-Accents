
import pandas as pd

import os
import time
import openai
import pandas as pd
import random
import PyPDF2


from Logger import Logger


logger =Logger() 

#This has utility functions
#@Author Sujith KS
class Utility:    
    #read pdf 
    def read_pdf(self,file):
            # Read the PDF
        reader = PyPDF2.PdfReader(file)
        pdf_text = ""

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
        return pdf_text


    #Read a text file
    def read_text(self,file):
        with open(file, 'r') as file:
            content = file.read().decode("utf-8")
        return content


    #read csv file
    def read_csv(self,file): 

        df = pd.read_csv(file)
 
        if df.empty:
            logger.debug("DataFrame is empty")
        else:
            logger.debug("DataFrame is not empty")
        # Check if any element is True
        if df.any().any():
            logger.debug("At least one True value exists in the DataFrame")
        else:
            logger.debug("No True values exist in the DataFrame")
        # Check if all elements are True
        if df.all().all():
            logger.debug("All elements are True in the DataFrame")
        else:
            logger.debug("Not all elements are True in the DataFrame")

        column_to_extract = df.columns     
        # Extract and display the text from the selected column
        extracted_text = df[column_to_extract].astype(str)#.tolist()
        return extracted_text 

    #Read excel file
    def read_excel_file(self,file):

        if file is not None:
            try:
                # Read all sheets from the Excel file
                excel_data = pd.read_excel(file, sheet_name=None)#.to_string()
          
                # Display the sheet names
                #sheet_names = list(excel_data.keys())

                #logger.debug(excel_data)
                return excel_data
            except Exception as e:
                logger.debug(f"Error reading the Excel file: {e}")
        else:
                logger.debug("Please upload an Excel file to read.")
  

            

