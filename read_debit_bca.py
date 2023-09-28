import PyPDF2
import re
import pandas as pd
import os

def clean_transaction_string(transaction_text):
    """
    Clean and extract transaction details from a text.

    Args:
        transaction_text (str): The input text containing transaction details.

    Returns:
        str: The cleaned transaction details.
    """
    # Define regular expression patterns
    date_pattern = r"^\d{4}\/\w+\/\w+\s\d+\.\d+"
    description_pattern = r"^\d{4}\/\w+\/\w+\/"
    description_end_pattern = r"\sTRSF\sE-BANKING\s\w+"
    tgl_pattern = r"TGL: \d* QR \d* \d*.\d*"
    tgl_end_pattern = r"\sTRANSAKSI\s\w*"

    if re.match(date_pattern, transaction_text):
        temp_text = re.sub(date_pattern, "", transaction_text)
        return re.sub(description_end_pattern, "", temp_text)
    elif re.match(description_pattern, transaction_text):
        temp_text = re.sub(description_pattern, "", transaction_text)
        return re.sub(description_end_pattern, "", temp_text)
    elif re.match(tgl_pattern, transaction_text):
        temp_text = re.sub(tgl_pattern, "", transaction_text)
        return re.sub(tgl_end_pattern, "", temp_text)
    else:
        return transaction_text

def extract_transaction_data_from_pdf(pdf_file_path):
    """
    Extract transaction data from a PDF file and return as a DataFrame.

    Args:
        pdf_file_path (str): The path to the PDF file.

    Returns:
        pd.DataFrame: A DataFrame containing transaction data.
    """
    pdf_file = open(pdf_file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    transaction_data = []

    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        page_text = page.extract_text()
        matches = re.findall(r"(\d{2}\/\d{2})\s([\s\S]*?\d+)\s(DB|CR)", page_text)
        
        for match in matches:
            new_list = list(s.replace("\n", "") for s in match)
            split_str = new_list[1].split()
            # Split the input date into day and month
            day, month = new_list[0].split('/')

            # Swap the day and month
            output_date = f"{month}/{day}"
            new_list = [output_date, ' '.join(split_str[:-1]), split_str[-1], new_list[2]]
            print(new_list)
            int_amount = new_list[2].replace(",", "")
            int_amount = int(int_amount[:-3])

            

            if(new_list[-1]=="DB"):
                transaction_data.append([new_list[0]+'/2023', clean_transaction_string(new_list[1]), -int_amount])
            else:
                transaction_data.append([new_list[0]+'/2023', clean_transaction_string(new_list[1]), int_amount])

    pdf_file.close()
    return pd.DataFrame(transaction_data, columns=["Date", "Description", "Amount"])

def main():
    folder_path = 'mutasimaretagustus'
    files = os.listdir(folder_path)
    all_transaction_data = []

    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            df = extract_transaction_data_from_pdf(file_path)
            all_transaction_data.append(df)

    combined_data = pd.concat(all_transaction_data, ignore_index=True)
    output_file_path = os.path.join(folder_path, "transactions.xlsx")
    combined_data.to_excel(output_file_path, index=False)
    print(f"Transaction data saved to {output_file_path}")

if __name__ == "__main__":
    main()
