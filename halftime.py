import csv
import os


def csv_split(f):

    if not os.path.exists(f[:-4]):
        os.mkdir(f[:-4])

    with open(f, encoding='utf-8') as fin:
        csvin = csv.DictReader(fin)
        # Category -> open file lookup
        outputs = {}
        for row in csvin:
            cat = row['Status']
            # Open a new file and write the header
            if cat not in outputs:
                fout = open('{}/{}.csv'.format(f[:-4], cat), 'w', newline='', encoding='utf-8')
                dw = csv.DictWriter(fout, delimiter=",", fieldnames=csvin.fieldnames)
                dw.writeheader()
                outputs[cat] = fout, dw
            # Always write the row
            outputs[cat][1].writerow(row)
        # Close all the files
        for fout, _ in outputs.values():
            fout.close()

    print(outputs)


cwd = os.getcwd()

folder = []
for (dirpath, dirnames, filenames) in os.walk(cwd):
    folder.extend(filenames)
    break

for file in folder:
    if ".csv" in file[-4:]:
        csv_split(file)

#add extra line
