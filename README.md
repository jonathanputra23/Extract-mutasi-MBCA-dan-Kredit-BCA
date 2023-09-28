# Extract-mutasi-MBCA
## Overview

This Python script extracts transaction data (data mutasi) from PDF files generated specifically designed by BCA. It automates the process of extracting, cleaning, and formatting transaction data and exports it to an Excel file for further analysis.

## Features

- Extracts transaction data from PDF files.
- Cleans and formats transaction details for better readability.
- Supports both income (DB) and expense (CR) transactions.
- Combines data from multiple PDF files into a single Excel file.

## Prerequisites

- Python 3.x
- Required Python libraries (install using `pip`):
  - PyPDF2
  - pandas

## Usage

1. Clone or download this repository to your local machine.

2. Place the PDF(s) files containing transaction data in a folder named 'testfolder' within the repository directory.

3. Run the script using the following command:

   ```bash
   python read_debit_bca.py
