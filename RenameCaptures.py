import PyPDF2
import re
import os
import shutil
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import pypyodbc as odbc
import pandas as pd
files = []
filename = []
directory = r'C:\Users\mt.reis\Desktop\W2ID\samples'
ready =  r'C:\Users\mt.reis\Desktop\W2ID\ready'

def ExtractText():
    count = 0
    #Extracts all of the text from the pdf file
    for fname in os.listdir(directory):
        files.append(os.path.join(directory,fname))
        filename.append(fname)
    #print(files)
    for f in files:
        count += 1
        output_string = StringIO()
        with open(f, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            #index = 0
            #only runs the first 5 pages of the pdf document
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
                #index += 1
                #if index == 1:
                break
            #print(output_string)
            ExtractData(output_string, filename, count)


def ExtractData(output_string, filename,count):
    #finds all of the EIN and puts them into an array
    ein1 = re.findall('[0-9][0-9]\-\d{7}', output_string.getvalue())
    print(ein1[0])
    #Connect to server then made a query to find company name that matches the EIN
    driver = 'Driver={ODBC Driver 17 for SQL Server};'
    server = 'Server=sdp-sqlp-a01;Database=AWS_SDP_Millennium;TrustedConnection=True;'

    #print(driver + server)
    conn = odbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=sdp-sqlp-a01;Database=AWS_SDP_Millennium;Trusted_Connection=yes")
    sql = "SELECT co FROM CInfo WHERE ein = ? "
    df = pd.read_sql_query(sql,conn,params=[ein1[0]])
    CoName = df['co'].values[0]
    print(CoName)
    if count == 110:
        exit()
    MoveandRename(CoName, filename[count], count)

def MoveandRename(CoName, filename, x):
    print(directory +"\\" + CoName + "-" + filename)
    shutil.copy(directory + "\\" + filename, ready + "\\"+ CoName + "-" + filename)

if __name__ == "__main__":
    ExtractText()
