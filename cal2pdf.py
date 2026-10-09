"""
 cal2pdf.py - Generate a PDF calendar for a given month and year using the 'cal' command.
Usage:
    python cal2pdf.py --month <month> --year <year>
    If month and year are not provided, the current month and year will be used.
Example:
    python cal2pdf.py --month 10 --year 2024

"""
#!/usr/bin/env python3

# call "cal" command and convert the output to pdf using enscript and ps2pdf

import sys
import datetime
import argparse
import subprocess
import fpdf

def get_filename(month, year):
    """Get the filename for the output PDF."""
    month_str = str(month).zfill(2)
    year_str = str(year)
    filename = f"cal_{month_str}_{year_str}.pdf"
    print(f"Getting filename: {filename}")
    return filename

def run_cal_command(month, year):
    """Run the 'cal' command and return its output."""
    print(f"Running 'cal' command for month: {month}, year: {year}")
    try:
        result = subprocess.run(['cal', str(month), str(year)],
                                capture_output=True, text=True, check=True)
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
    """Main function to generate the PDF calendar."""
    # skip coverage for this function since it is the main entry point and not called during tests
    args = setup_command_line_arguments()

    cal_output = run_cal_command(args.month, args.year)
    parsed_cal_data = parse_cal_output(cal_output)
    output_pdf(args, parsed_cal_data)

def output_pdf(args, calendar_data):
    """Generate a PDF from the parsed calendar data."""
    cell_width = 25
    cell_height = 25

    # Create a PDF from the cal output using fpdf2
    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=25, style='B')

    pdf.set_xy(0, cell_height)
    pdf.cell(0, cell_height, text=calendar_data['header'])
    output_days_of_week(cell_width, cell_height, pdf, calendar_data)
    output_day_numbers(calendar_data, cell_width, cell_height, pdf)
    pdf_output_path = f"cal_{args.month}_{args.year}.pdf"
    pdf.output(pdf_output_path)

    print(f"PDF generated: {pdf_output_path}")

def examples():
    """Provide example usage for the command line."""
    example_message="\n".join([
        "examples: cal2pdf.py --month 10 --year 2024 will generate 'cal_10_2024.pdf'.",
        "          cal2pdf.py --month 1 --year 2024 will generate 'cal_01_2024.pdf'."
        ]
    )
    return example_message

def usage():
    """Provide usage information for the command line."""
    help_message="\n".join([
        "  - A calendar PDF file will be generated with the name 'cal_<month>_<year>.pdf'.",
        "  - If month and year are not provided, the current month and year will be used."
        ]
    )
    return help_message

def setup_command_line_arguments():
    """Set up command line arguments for the script."""
    parser = argparse.ArgumentParser(
        description=usage(),
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=examples()
    )
    parser.add_argument('--month', type=int, help='Month (1-12)', required=False)
    parser.add_argument('--year', type=int, help='Year (e.g., 2024)', required=False)
    args = parser.parse_args()
    if args.month is None:
        args.month = datetime.datetime.now().month
    else:
        if args.month < 1 or args.month > 12:
            print(f"Invalid month: {args.month}. Month must be between 1 and 12.", file=sys.stderr)
            sys.exit(1)
    if args.year is None:
        args.year = datetime.datetime.now().year
    else:
        if args.year < 1:
            print(f"Invalid year: {args.year}. Year must be a positive integer.", file=sys.stderr)
            sys.exit(1)
    return args

def output_day_numbers(calendar_data, cell_width, cell_height, pdf):
    """Output the day numbers to the PDF."""
    pdf.set_font("Courier", size=12, style='')
    for i in range(1, len(calendar_data)):
        if f'date_{i}' in calendar_data:
            numbers = calendar_data[f'date_{i}']

            print(f"Date line {i}: {calendar_data[f'date_{i}']}, numbers: {numbers}")
            number_list = get_day_number_list(numbers)

            for j, number in enumerate(number_list):
                pdf.set_xy(10 + (j * cell_width), 50 + (i * cell_height)+5)
                pdf.cell(cell_width, 0, text=number, border=0, align='L')
                pdf.set_xy(10 + (j * cell_width), 50 + (i * cell_height))
                pdf.cell(cell_width, cell_height, border=1)

def get_day_number_list(numbers):
    """
    Parse a line of day numbers and return a list of individual day numbers.
    - Do not remove the "EMPTY" days (represented by spaces) to maintain the correct alignment.
    - Each day number is expected to be 2 characters wide, with a space separating them.
    """
    number_list = []
    for index in range(0, len(numbers), 3):
        number_list.append(numbers[index:index+2].strip())
    print(f"Parsed numbers for line {numbers}: {number_list}")
    return number_list

def output_days_of_week(cell_width, cell_height, pdf, calendar_data):
    """Output the days of the week to the PDF."""
    days_list = get_days_of_week_list(calendar_data)
    index = 0
    pdf.set_font("Courier", size=16, style='B')
    for day in days_list:
        pdf.set_xy(10 + (index * cell_width), 50)
        pdf.cell(cell_width, cell_height, text=day, border=1, align='C')
        index += 1
        print(f"Added weekday to PDF: {day}")

def get_days_of_week_list(calendar_data):
    """
    Parse the weekdays line from the calendar data and return a list of individual days of the week.
    - Each day of the week is expected to be 2 characters wide, with a space separating them.
    """
    days_list = []
    for index in range(0, len(calendar_data['weekdays']), 3):
        days_list.append(calendar_data['weekdays'][index:index+3].strip())
    print(f"Parsed weekdays: {days_list}")
    return days_list


if __name__ == "__main__":
    main()
