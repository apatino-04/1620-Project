from tkinter import *
import csv
import os


class Gui:
    def __init__(self, window):
        self.window = window
        self.recorded_ids = set()

        #FRAME ONE
        self.frame_one = Frame(self.window)
        self.label_title = Label(self.frame_one, text='VOTING APPLICATION')
        self.label_id = Label(self.frame_one, text="Enter ID #")
        self.input_id = Entry(self.frame_one, width=15)

        self.label_title.pack(pady=10)
        self.label_id.pack(side='left')
        self.input_id.pack(pady=10)
        self.frame_one.pack()

        #FRAME TWO
        self.frame_two = Frame(self.window)
        self.label_candidates = Label(self.frame_two, text="CANDIDATES")
        self.radio_answer = IntVar()
        self.radio_answer.set(0)
        self.radio_jane = Radiobutton(self.frame_two, text='Jane', variable=self.radio_answer, value=1)
        self.radio_john = Radiobutton(self.frame_two, text='John', variable=self.radio_answer, value=2)
        self.button_submit = Button(self.frame_two, text="Submit Vote", command=self.submit)

        self.label_candidates.pack(pady=5)
        self.radio_john.pack()
        self.radio_jane.pack()
        self.button_submit.pack(pady=10)
        self.frame_two.pack()

        # MESSAGE BANNER
        self.frame_three = Frame(self.window)
        self.mess_label = Label(self.frame_three, text='')
        self.mess_label.pack(side='left')
        self.frame_three.pack(padx=10, pady=10)

    def access_recorded_ids(self):
        """
                This function checks to see if the file already exists
                if it does, it accesses the recorded ID's and turns them into a set

        """
        if os.path.exits('data.csv'):
            with open('data.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        self.recorded_ids.add(int(row[0]))

    def submit(self):
        id_num = self.input_id.get().strip()

        #   Catches non-integer responses
        try:
            id_num = int(id_num)

        except ValueError:
            self.mess_label.config(text=f'ID numer is made up of numbers only', fg='red')
        else:

            #   Catches responses less than 6 integers
            if len(str(id_num)) != 6:
                self.mess_label.config(text='ID number must be 6 digits long', fg='red')

            #   Catches ID's already registered
            elif id_num in self.recorded_ids:
                self.mess_label.config(text='This ID has already voted', fg='red')

            else:
                option = self.radio_answer.get()

                #   Catches if user doesn't select a candidate
                if option == 0:
                    self.mess_label.config(text='Please select a candidate', fg='red')
                else:
                    if option == 1:
                        candidate = 'Jane'
                        self.mess_label.config(text=f'Vote recorded for {candidate}', fg='green')
                    else:
                        candidate = 'John'
                        self.mess_label.config(text=f'Vote recorded for {candidate}', fg='green')

                    #   Writes to file
                    with open('data.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([id_num, candidate])

                    #   Adds ID's to set
                    self.recorded_ids.add(id_num)

                    #   Refreshes ID input box
                    self.input_id.delete(0, 'end')
                    #   Refreshes Radio Button
                    self.radio_answer = 0
