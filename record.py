import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

data = []

def generate_references():
    global data
    return_refs = []
    for i in range(12):
        data.append([])
    return_refs.append(db.reference('patient1/Pulserate').listen(custom_on_data_change(1, "Pulserate")))
    return_refs.append(db.reference('patient1/Temperature').listen(custom_on_data_change(1, "Temperature")))
    return_refs.append(db.reference('patient2/Pulserate').listen(custom_on_data_change(2, "Pulserate")))
    return_refs.append(db.reference('patient2/Temperature').listen(custom_on_data_change(2, "Temperature")))
    return_refs.append(db.reference('patient3/Pulserate').listen(custom_on_data_change(3, "Pulserate")))
    return_refs.append(db.reference('patient3/Temperature').listen(custom_on_data_change(3, "Temperature")))
    return_refs.append(db.reference('patient4/Pulserate').listen(custom_on_data_change(4, "Pulserate")))
    return_refs.append(db.reference('patient4/Temperature').listen(custom_on_data_change(4, "Temperature")))
    return_refs.append(db.reference('patient5/Pulserate').listen(custom_on_data_change(5, "Pulserate")))
    return_refs.append(db.reference('patient5/Temperature').listen(custom_on_data_change(5, "Temperature")))
    return_refs.append(db.reference('patient6/Pulserate').listen(custom_on_data_change(6, "Pulserate")))
    return_refs.append(db.reference('patient6/Temperature').listen(custom_on_data_change(6, "Temperature")))
    return return_refs, data

def set_up_connection():
    # Initialize Firebase SDK with credentials
    cred = credentials.Certificate("./serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://health-monitoring-e687e-default-rtdb.firebaseio.com/'
    })
    return

def custom_on_data_change(patient_num, property):
    def on_data_change(event):
        global data
        index = patient_num * 2
        if property == "Temperature":
            index += 1
        data[index - 2].append(event.data)
        print(index-2, event.data)
    return on_data_change

def save_the_data():
    file = open("records.csv", "w")
    file.write("patient1-Pulserate, patient1-Temperature, patient2-Pulserate, patient2-Temperature, patient3-Pulserate, patient3-Temperature, patient4-Pulserate, patient4-Temperature, patient5-Pulserate, patient5-Temperature, patient6-Pulserate, patient6-Temperature")
    file.write("\n")
    max_length = 0
    for arr in data:
        max_length = max(len(arr), max_length)
    for iter in range(max_length):
        string = ""
        for arr in data:
            if iter < len(arr):
                string += str(arr[iter]) + ","
            else:
                string += ","
        if len(string) > 0:
            string = string[:-1]
        file.write(string)
        file.write("\n")
    return

def main():
    set_up_connection()
    references, data = generate_references()
    # for ref in references:
    #     print(ref)

    # Keep the program running to continue listening for data changes
    while True:
        try:
            time.sleep(15)
        except KeyboardInterrupt:
            print("entered keyboard interruption ... ")
            save_the_data()
            print(" saved data to file .... !")
            ## reference closes 
            for ref in references:
                ref.close()
            print(" Hello here, now we can save data ... ")
            exit();
    return

if __name__ == "__main__":
    main()