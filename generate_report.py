import csv
import sys

def csv_to_txt(csv_file, txt_file):
    """Convert results CSV to formatted TXT report"""
    with open(csv_file, newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    with open(txt_file, "w") as out:
        out.write("CustomHeader\tDomain\tResolvedIP\n")
        for row in rows[1:]:  # skip header row
            out.write(f"{row[0]}\t{row[1]}\t{row[2]}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 generate_report.py results.csv dns_report.txt")
        sys.exit(1)
    csv_to_txt(sys.argv[1], sys.argv[2])

