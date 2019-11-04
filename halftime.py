import csv
import os
import re

def dir_name(directory):

    # Members_of_program_039_E_amp_R_201901_Renewable_Energy_outlook_039_

    directory = re.sub(r'^Members_of_program_[0-9]{3}_', ' ', directory)
    directory = re.sub(r'_amp_', '&', directory)
    directory = re.sub(r'_[0-9]{3}_$', ' ', directory)
    directory = re.sub(r'_', ' ', directory)
    directory = directory.strip()
    return directory


def csv_split(f, col_name):

    dir_name_str = dir_name(f[:-4])

    if not os.path.exists(dir_name_str):
        os.mkdir(dir_name_str)

    with open(f, encoding='utf-8') as fin:
        csvin = csv.DictReader(fin)
        # Category -> open file lookup
        outputs = {}
        i = 10000
        for row in csvin:
            cat = row[col_name]
            email_address = row['Email Address']
            sfdc_id = row['Marketo SFDC ID']
            
            # Fill empty email addresses
            if email_address == '':
                if sfdc_id == '':
                    row['Email Address'] = 'marketo{}'.format(i) + '@deloitte.nl.invalid'
                    i += 1
                else:
                    row['Email Address'] = sfdc_id + '@deloitte.nl.invalid'

            # Open a new file and write the header
            if cat not in outputs:
                fout = open('{}/{}.csv'.format(dir_name_str, cat), 'w', newline='', encoding='utf-8')
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
        csv_split(file, col_name='Status')
