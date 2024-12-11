from prompt_with_input_md import get_result
import pandas as pd

OUTPUT_PATH = '../data/results_single/'
LOCAL_DATE_TIME = '2024-11-21 12:55'

locations = pd.read_csv("../data/locations.csv", sep=";")

loc = locations.iloc[0]

print(f"Processing location - {loc['Name']}")

with open(f"{OUTPUT_PATH}input_output_single_{loc['Name']}.json", "w", encoding='utf8') as outfile:
    print('Triggering LLM and writing to file')
    result = get_result(loc, LOCAL_DATE_TIME)
    input = result[0]
    output = result[1]
    outfile.write("INPUT:\n")
    outfile.write(input)
    outfile.write("\nOUTPUT:\n")
    outfile.write(output)