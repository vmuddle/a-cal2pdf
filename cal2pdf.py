#!/usr/bin/env python3

# call "cal" command and convert the output to pdf using enscript and ps2pdf

import os
import sys
import argparse
import subprocess
import tempfile
import shutil
import fpdf
import datetime

def run_cal_command(month, year):
    """Run the 'cal' command and return its output."""
    print(f"Running 'cal' command for month: {month}, year: {year}")
    try:
        result = subprocess.run(['cal', str(month), str(year)], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running cal command: {e}", file=sys.stderr)
        sys.exit(1)

def parse_cal_output(cal_output):
    """Parse the output of the 'cal' command and return a list of lines."""
    lines = cal_output.splitlines()
    line_counter=0
    month_map = {}
    for line in lines:
        print(f"Cal output line: {line}")
        line_counter+=1
        if line_counter==1:
            print(f"Header line: {line}")
            month_map['header'] = line
        elif line_counter==2:
            print(f"Weekdays line: {line}")
            month_map['weekdays'] = line
        else:
            print(f"Date line: {line}")
            month_map[f'date_{line_counter-2}'] = line
    return month_map

def main():
    parser = argparse.ArgumentParser(description='Convert cal output to PDF.')
    parser.add_argument('--month', type=int, help='Month (1-12)', required=False)
    parser.add_argument('--year', type=int, help='Year (e.g., 2024)', required=False)
    args = parser.parse_args()
    if args.month is None:
        args.month = datetime.datetime.now().month
    if args.year is None:
        args.year = datetime.datetime.now().year

    cal_output = run_cal_command(args.month, args.year)
    month_map = parse_cal_output(cal_output)

    cellWidth = 25
    cellHeight = 25

    # Create a PDF from the cal output using fpdf2
    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=25, style='B')

    pdf.set_xy(0, cellHeight)
    pdf.cell(0, cellHeight, text=month_map['header'])
    days_list = []
    for index in range(0, len(month_map['weekdays']), 3):
        days_list.append(month_map['weekdays'][index:index+3].strip())
    print(f"Parsed weekdays: {days_list}")
    index = 0
    pdf.set_font("Courier", size=16, style='B')
    for day in days_list:
        pdf.set_xy(10 + (index * cellWidth), 50)
        pdf.cell(cellWidth, cellHeight, text=day, border=1, align='C')
        index += 1
        print(f"Added weekday to PDF: {day}")
    pdf.set_font("Courier", size=12, style='')
    for i in range(1, len(month_map)):
        if f'date_{i}' in month_map:
            numbers = month_map[f'date_{i}']

            print(f"Date line {i}: {month_map[f'date_{i}']}, numbers: {numbers}")
            number_list = []
            for index in range(0, len(numbers), 3):
                number_list.append(numbers[index:index+2].strip())
            print(f"Parsed numbers for line {i}: {number_list}")

            for j, number in enumerate(number_list):
                pdf.set_xy(10 + (j * cellWidth), 50 + (i * cellHeight)+5)
                pdf.cell(cellWidth, 0, text=number, border=0, align='L')
                pdf.set_xy(10 + (j * cellWidth), 50 + (i * cellHeight))
                pdf.cell(cellWidth, cellHeight, border=1)
    #for line in lines:
    #    pdf.cell(0, 10, text=line)

    pdf_output_path = f"cal_{args.month}_{args.year}.pdf"
    pdf.output(pdf_output_path)

    print(f"PDF generated: {pdf_output_path}")

main()