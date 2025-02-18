import json
from docx import Document
import os

def convert_workout(workout_plan):
    doc = Document(workout_plan)
    paragraph_iterator = iter(doc.paragraphs)

    # Start iterating
    curr_para = next(paragraph_iterator)
    # print(curr_para.text)
    data = {
        "workoutName": "",
        "goals": [],
        "days": []
    }

    # Get WorkoutName
    data["workoutName"] = curr_para.text.split(":")[1][1:]

    # Get Goals
    curr_para = next(paragraph_iterator)
    for i in range(int( curr_para.text[curr_para.text.find("(")+1])):
        curr_para = next(paragraph_iterator)
        data["goals"].append(curr_para.text.strip())

    # Get Days
    while not curr_para.text.strip().startswith("Day #"):
        curr_para = next(paragraph_iterator)
    day_data = {}
    while True:
        try:      
            # get day data
            day_data = {"day": curr_para.text.strip()[5], 
                        "name": curr_para.text[7:curr_para.text.find("(")].strip(),
                        "duration": curr_para.text[curr_para.text.find("(")+1:-1], 
                        "description": ""}
                # Start iterating to fill description
            curr_para = next(paragraph_iterator)
            while not curr_para.text.strip().startswith("Day #"):
                if len(day_data["description"]) == 0:
                    day_data["description"] = curr_para.text
                else:
                    day_data["description"] = day_data["description"] + "\n" + curr_para.text 
                curr_para = next(paragraph_iterator)
            day_data["description"] = day_data["description"].rstrip("\n") 
            data["days"].append(day_data)
            while not curr_para.text.strip().startswith("Day #"):
                curr_para = next(paragraph_iterator)
        except:
            break
    day_data["description"] = day_data["description"].rstrip("\n")
    data["days"].append(day_data)
    return data

root_directory = 'C:/Users/kyler/Desktop/PATH/Workouts/'  # Change this to your root folder path
# List to store the paths of Word documents
word_docs = []

# Walk through the directory
for dirpath, dirnames, filenames in os.walk(root_directory):
    for filename in filenames:
        if filename.endswith('.docx'):  # Check for Word documents
            store = (dirpath, filename, dirpath.replace("Workouts", "WorkoutsJSON"), filename.replace("docx", "json"))
            word_docs.append(store)

# Print the paths of all Word documents
for dirpath, filename, newdirpath, newfilename in word_docs:
    data = convert_workout(os.path.join(dirpath, filename))
    file_path = os.path.join(newdirpath, newfilename)
    # Step 3: Ensure the folder exists
    os.makedirs(newdirpath, exist_ok=True)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)  # indent=4 for pretty printing

   


