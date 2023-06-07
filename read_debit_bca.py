import PyPDF2
import re
import pandas as pd
from datetime import datetime

current_year = datetime.now().year
# open the PDF file you want to read
fileName = "MutasiBCA_030523-100523.pdf"
pdf_file = open(fileName, 'rb')

# create a PDF reader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

# get the number of pages in the PDF file
num_pages = len(pdf_reader.pages)

regx =  "(\d{2}\/\d{2})\s([\s\S]*?\d+)\s(DB|CR)"


new_data = []
# loop through all the pages in the PDF file
for page_num in range(num_pages):
    # get the current page
    page = pdf_reader.pages[page_num]

    # extract the text from the current page
    page_text = page.extract_text()
    #print(page_text)
    matches1 = re.findall(regx, page_text)
    for match in matches1:
        new_list = list(s.replace("\n", "") for s in match)
        split_str = new_list[1].split()
        new_list = [new_list[0], ' '.join(split_str[:-1]), split_str[-1], new_list[2]]
        #print(new_list)

        if(new_list[-1]=="DB"):
            new_data.append([new_list[0]+'/2023', new_list[1], '-'+new_list[2]])
        else:
            new_data.append([new_list[0]+'/2023', new_list[1], new_list[2]])
            #new_data.append([new_list[0]+'/2023', new_list[1], "", new_list[2]])
        
    """
    lines = page_text.split('\n')  # split the string into lines

    for line in lines:
        print(line)
        print("====\n")
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
"""
name_file = fileName+".xlsx"
#print(name_file)
df = pd.DataFrame(new_data, columns=["Date", "Note", "Amount"])
print(df)

df.to_excel(str(name_file), index=False)
    # print the text from the current page
    # print(page_text)

# close the PDF file
pdf_file.close()
