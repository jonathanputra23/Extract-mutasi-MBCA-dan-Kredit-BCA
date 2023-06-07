import PyPDF2
import re
import pandas as pd
import locale
from datetime import datetime

locale.setlocale(locale.LC_TIME, 'id_ID') 

current_year = datetime.now().year
# open the PDF file you want to read
pdf_file = open('19677605_03052023_1683163653898_1683221926260.pdf', 'rb')

# create a PDF reader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

# check if the PDF file is encrypted
if pdf_reader.is_encrypted:
    # ask the user for the password
    password = "12122000"

    # decrypt the PDF file with the password
    pdf_reader.decrypt(password)

# get the number of pages in the PDF file
num_pages = len(pdf_reader.pages)

regx = "\d{2}-[A-Za-z]{3} \d{2}-[A-Za-z]{3}"

new_data = []
# loop through all the pages in the PDF file
for page_num in range(num_pages):
    # get the current page
    page = pdf_reader.pages[page_num]

    # extract the text from the current page
    page_text = page.extract_text()
    lines = page_text.split('\n')  # split the string into lines


    for line in lines:
        if re.search(regx, line):
            new_list = line.strip().split(" ")
            new_list = [elem for elem in new_list if elem]
            del new_list[0]
            date_trx = new_list[0]
            date_trx_obj = datetime.strptime(date_trx + "-" + str(current_year), "%d-%b-%Y")
            new_date_str = date_trx_obj.strftime("%Y-%m-%d")

            del new_list[0]
            name_trx = " ".join(new_list[:-1])
            price_trx = new_list[-1]
            #print(date_trx)
            #print(name_trx)
            #print(price_trx)
            #print('\n')
            new_data.append([new_date_str, name_trx, price_trx])

first_trx = new_data[0][0]
last_trx = new_data[-1][0]
name_file = first_trx+" to " +last_trx+".xlsx"
#print(name_file)
df = pd.DataFrame(new_data, columns=["Date", "Note", "Amount"])
print(df)

df.to_excel(str(name_file), index=False)
    # print the text from the current page
    # print(page_text)

# close the PDF file
pdf_file.close()
