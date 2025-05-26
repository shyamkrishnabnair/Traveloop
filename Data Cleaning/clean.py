import csv

# Clean city.csv: fix City_desc, remove brackets and extra quotes and ideal duration
def clean_city_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['min_days', 'max_days']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # Clean City_desc as before
            desc = row['City_desc']
            desc = desc.strip().strip("[]").replace('""', '"').replace("''", "'")
            desc = desc.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            desc = ' '.join(desc.split())
            row['City_desc'] = desc

            # Parse Ideal_duration "2-4"
            duration = row['Ideal_duration'].strip()
            min_days, max_days = None, None
            if '-' in duration:
                parts = duration.split('-')
                try:
                    min_days = int(parts[0])
                    max_days = int(parts[1])
                except ValueError:
                    min_days, max_days = None, None
            else:
                try:
                    min_days = max_days = int(duration)
                except ValueError:
                    min_days, max_days = None, None

            row['min_days'] = min_days if min_days is not None else ''
            row['max_days'] = max_days if max_days is not None else ''

            writer.writerow(row)


# Clean places.csv: strip whitespace from all string fields
def clean_places_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            for key in row:
                row[key] = row[key].strip()  # remove leading/trailing whitespace
            writer.writerow(row)


if __name__ == "__main__":
    clean_city_csv('city.csv', 'city_clean.csv')
    clean_places_csv('places.csv', 'places_clean.csv')
    print("CSV files cleaned and saved as 'city_clean.csv' and 'places_clean.csv'")
