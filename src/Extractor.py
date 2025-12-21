import json
import csv

inputCsv = r"..\assets\file_sigs.csv"
outputJson = r"..\assets\file_sigs.json"
try:
    with open(inputCsv, encoding="utf-8") as csvFile:
        read = csv.DictReader(csvFile)
        data = []
        for row in read:
            clean_row = {k:v for k,v in row.items() if k}
            data.append(clean_row)
    
    with open(outputJson, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
except FileNotFoundError:
    print("The file you gave is not found")
