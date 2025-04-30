import csv
import sqlite3

def cleandata(inputfile, outputfile):
    cleaned_data = []
    try:
    # Open the CSV file in read mode
      with open(inputfile, 'r') as csvfile:
          csv_reader = csv.reader(csvfile)
        
        # Iterate through rows inside the "with" block
          for row in csv_reader:
              if row[7].strip() or row[6].strip() :  # Adjust index [0] to check a different column if needed
                 cleaned_data.append(row)
    except FileExistsError:
        print("File not exist") 
    finally:
           # Prevent high load in pathological conditions
    
    # Open a new file in write mode and save the cleaned data
       with open(outputfile, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(cleaned_data)

    return "Cleaning completed successfully!"

def loda_data():
    try:
        # Open the CSV file in read mode
        with open('output.csv', 'r') as fin:
            dr = csv.DictReader(fin)  # Read CSV into a dictionary format
            Fiers_info = [(i['Region'], i['Date'], i['Estimated_fire_area'], 
                           i['Mean_estimated_fire_brightness'], i['Mean_estimated_fire_radiative_power']) for i in dr]

        # Connect to SQLite database
        connection = sqlite3.connect("load.db")
        print("Total changes in connection:", connection.total_changes)

        cursor = connection.cursor()

        # Create the table if it doesn't exist
        cursor.execute("""CREATE TABLE IF NOT EXISTS WFieres (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            Region TEXT, 
            Date DATE, 
            Estimated_fire_area REAL, 
            Mean_estimated_fire_brightness REAL,
            Mean_estimated_fire_radiative_power REAL
        )""")

        # Insert data into the table
        cursor.executemany("""INSERT INTO WFieres (Region, Date, Estimated_fire_area, 
                          Mean_estimated_fire_brightness, Mean_estimated_fire_radiative_power) 
                          VALUES (?, ?, ?, ?, ?)""", Fiers_info)

        connection.commit()  # Commit the changes
        print("Data loaded successfully into database!")
        # Testing rezalts
        cursor.execute('select *  from WFieres  limit 10 ;') 
        # View result
        result = cursor.fetchall()
        print(result)

    except sqlite3.Error as error:
        print("Error occurred:", error)

    finally:
        # Ensure the connection is closed
        if 'connection' in locals():
            connection.close()
            print("SQLite Connection closed")
cleandata('Historical_Wildfires.csv','output.csv')
loda_data()