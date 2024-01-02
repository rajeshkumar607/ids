import csv

def csv_to_sql_insert(csv_filename, table_name):
    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        columns = csv_reader.fieldnames

        for row in csv_reader:
            values = [f"'{row[col]}'" if isinstance(row[col], str) else str(row[col]) for col in columns]
            sql_insert = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"
            print(sql_insert)

# Replace these values with your actual CSV file and desired table name
csv_filename = 'data.csv'
table_name = 'attributes'

csv_to_sql_insert(csv_filename, table_name)