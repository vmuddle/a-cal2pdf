# a-cal2pdf
Linux Cal to PDF
```
usage: cal2pdf.py [-h] [--month MONTH] [--year YEAR]

  - A calendar PDF file will be generated with the name 'cal_<month>_<year>.pdf'.
  - If month and year are not provided, the current month and year will be used.

options:
  -h, --help     show this help message and exit
  --month MONTH  Month (1-12)
  --year YEAR    Year (e.g., 2024)

examples: cal2pdf.py --month 10 --year 2024 will generate 'cal_10_2024.pdf'.
          cal2pdf.py --month 1 --year 2024 will generate 'cal_01_2024.pdf'.
```