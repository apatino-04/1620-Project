from tkinter import *
import csv
import os


class Gui:
    def __init__(self, window) -> None:
        self.__window = window
        self.__recorded_ids = set()

        #   Initialize recorded IDs
        self.access_recorded_ids()

        #   FRAME ONE
        self.__frame_one = Frame(self.__window)
        self.__label_title = Label(self.__frame_one, text='VOTING APPLICATION')
        self.__label_id = Label(self.__frame_one, text="Enter ID #")
        self.__input_id = Entry(self.__frame_one, width=15)

        self.__label_title.pack(pady=10)
        self.__label_id.pack(side='left')
        self.__input_id.pack(pady=10)
        self.__frame_one.pack()

        #   FRAME TWO
        self.__frame_two = Frame(self.__window)
        self.__label_candidates = Label(self.__frame_two, text="CANDIDATES")
        self.__radio_answer = IntVar()
        self.__radio_answer.set(0)
        self.__radio_jane = Radiobutton(self.__frame_two, text='Jane', variable=self.__radio_answer, value=1)
        self.__radio_john = Radiobutton(self.__frame_two, text='John', variable=self.__radio_answer, value=2)
        self.__button_submit = Button(self.__frame_two, text="Submit Vote", command=self.submit)

        self.__label_candidates.pack(pady=5)
        self.__radio_john.pack()
        self.__radio_jane.pack()
        self.__button_submit.pack(pady=10)
        self.__frame_two.pack()

        #   MESSAGE BANNER
        self.__frame_three = Frame(self.__window)
        self.__mess_label = Label(self.__frame_three, text='')

        self.__mess_label.pack(side='left')
        self.__frame_three.pack(padx=10, pady=10)

    def access_recorded_ids(self) -> None:
        """
                This function checks to see if the file already exists
                If it does, it accesses the recorded ID's and turns them into a set

        """
        if os.path.exists('data.csv'):
            with open('data.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        self.__recorded_ids.add(int(row[0]))

    def submit(self) -> None:
        """
                This functions processes the submitted ID and vote
                It will make sure the ID meets the guidelines provided
                    - ID is only made up of integers
                    - ID is six integers long
                And ensures every user submits only one vote per ID
                    - verifies ID is not already registered
                    - displays appropriate message if catches error

        """
        id_num = self.__input_id.get().strip()

        #   Catches non-integer responses
        try:
            id_num = int(id_num)

        except ValueError:
            self.__mess_label.config(text=f'ID number is made up of numbers only', fg='red')
        else:

            #   Catches responses less than 6 integers
            if len(str(id_num)) != 6:
                self.__mess_label.config(text='ID number must be 6 digits long', fg='red')

            #   Catches ID's already registered
            elif id_num in self.__recorded_ids:
                self.__mess_label.config(text='This ID has already voted', fg='red')

            else:
                option = self.__radio_answer.get()

                #   Catches if user doesn't select a candidate
                if option == 0:
                    self.__mess_label.config(text='Please select a candidate', fg='red')
                else:
                    if option == 1:
                        candidate = 'Jane'
                        self.__mess_label.config(text=f'Vote recorded for {candidate}', fg='green')
                    else:
                        candidate = 'John'
                        self.__mess_label.config(text=f'Vote recorded for {candidate}', fg='green')

                    #   Writes to file
                    with open('data.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([id_num, candidate])

                    #   Adds ID's to set
                    self.__recorded_ids.add(id_num)

                    #   Refreshes ID input box
                    self.__input_id.delete(0, 'end')
                    #   Refreshes Radio Button
                    self.__radio_answer.set(0)
