import tkinter
import threading


class Patient():
    """клас Пацієнт"""
    def __init__(self, name, appointments = None):
        self.__name = name
        if appointments == None:
            self.__appointments = []
        else:
            self.__appointments = appointments 
            # self.__appointments = appointments має бути списком екземплярів класу Appointment, 
            # які містять самого пацієнта(як екземпляр класу Patient)
            # лякаря (екземпляр класу Doctor)
            # діагноз (екземпляр класу Diagnosis)
            # лікування (екземпляр класу Presctiption)

        
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def appointments(self):
        return self.__appointments

    @appointments.setter
    def appointments(self, new_appointments):
        self.__appointments = new_appointments

    def schedule_appointment(self, doctor, date, time):
        with doctor.lock:
            
            if doctor.schedule != []:
                flag = 0
                for sch in doctor.schedule:
                    if sch[1] == date and sch[2] == time:
                        flag = 1
                        break
                if not flag:
                    doctor.schedule.append([self, date, time])
            else:
                doctor.schedule.append([self, date, time])

    def __str__(self):
        return f"Ім'я пацієнта: {self.name}."

class Doctor():
    """клас Лікар"""
    def __init__(self, name, speciality, schedule = None):
        self.__name = name
        self.__speciality = speciality
        if schedule == None:
            self.__schedule = []
        else:
            self.__schedule = schedule
            # має бути списком, кожен елемент якого є списком з трьох елементів:
            # перший елемент - посилання на екземпляр класу Patient
            # другий елемент - дата у вигляді str
            # третій елемент - час у вигляді str


        self.lock = threading.Lock()


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def speciality(self):
        return self.__speciality

    @speciality.setter
    def speciality(self, new_speciality):
        self.__speciality = new_speciality

    @property
    def schedule(self):
        return self.__schedule

    @schedule.setter
    def schedule(self, new_schedul):
        self.__schedule = new_schedul

    def add_appointment(self, patient, diagnosis, prescription):
        appointment = Appointment(patient, self, diagnosis, prescription)
        patient.appointments.append(appointment)
        for sch in self.schedule:
            if sch[0] == patient:
                self.schedule.remove(sch)
                break

    def __str__(self):
        return f"Ім'я лікаря: {self.name}, спеціальність: {self.speciality}."


class Appointment:
    """клас Прийом"""
    def __init__(self, patient, doctor, diagnosis, prescription):
        self.__patient = patient
        self.__doctor = doctor
        self.__diagnosis = diagnosis
        self.__prescription = prescription

    @property
    def patient(self):
        return self.__patient

    @patient.setter
    def new_patient(self, new_patient):
        self.__patient = new_patient

    @property
    def doctor(self):
        return self.__doctor

    @doctor.setter
    def new_doctor(self, new_doctor):
        self.__doctor = new_doctor

    @property
    def diagnosis(self):
        return self.__diagnosis

    @diagnosis.setter
    def new_diagnosis(self, new_diagnosis):
        self.__diagnosis = new_diagnosis

    @property
    def prescription(self):
        return self.__prescription

    @prescription.setter
    def new_prescription(self, new_prescription):
        self.__prescription = new_prescription


    def __str__(self):
        return f"Ім'я пацієнта: {self.patient.name}. Ім'я лікаря: {self.doctor.name}. {self.diagnosis} {self.prescription}" 


class Diagnosis():
    """клас Діагноз"""
    def __init__(self, name):
        self.__name = name 

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    def __str__(self):
        return f"Діагноз: {self.name}."


class Prescription():
    """клас Призначення (лікування)"""
    def __init__(self, name):
        self.__name = name 

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    def __str__(self):
        return f"Лікування: {self.name}."



class App():
    def __init__(self, root):
        self.root = root
        self.root.title("Лікарня")
        self.root.geometry("1280x720")
        self.list_of_doctors = []
        self.list_of_patients = []

        self.all_elements = []

        self.menu()

    def menu(self):
        self.clean()

        text = tkinter.Label(self.root, text="Вітаємо у лікарні.")
        text.pack()

        text1 = tkinter.Label(self.root, text="Оберіть дію:")
        text1.pack()

        btn1 = tkinter.Button(self.root, text="Авторизація Пацієнта", command=self.login_patient)
        btn1.pack(pady=5)

        btn2 = tkinter.Button(self.root, text="Авторизація Лікаря", command=self.login_doctor)
        btn2.pack(pady=5)

        btn3 = tkinter.Button(self.root, text="Реєстрація Пацієнта", command=self.register_patient)
        btn3.pack(pady=5)

        btn4 = tkinter.Button(self.root, text="Реєстрація Лікаря", command=self.register_doctor)
        btn4.pack(pady=5)

        self.all_elements.extend([text, text1, btn1, btn2, btn3, btn4])

    
    def login_patient(self):
        self.clean()

        text = tkinter.Label(self.root, text="Введіть ваше ім'я:")
        text.pack()

        self.patient_name_entry = tkinter.Entry(self.root)
        self.patient_name_entry.pack()

        btn = tkinter.Button(self.root, text="Увійти", command=self.authorize_patient)
        btn.pack()

        back_btn = tkinter.Button(self.root, text="Назад", command=self.menu)
        back_btn.pack(pady=10)

        self.all_elements.extend([text, self.patient_name_entry, btn, back_btn])


    def authorize_patient(self):
        name = self.patient_name_entry.get()
        for patient in self.list_of_patients:
            if patient.name == name:
                self.patient = patient

        self.patient_menu()


    def login_doctor(self):
        self.clean()

        text = tkinter.Label(self.root, text="Введіть ваше ім'я:")
        text.pack()

        self.doctor_name_entry = tkinter.Entry(self.root)
        self.doctor_name_entry.pack()

        btn = tkinter.Button(self.root, text="Увійти", command=self.authorize_doctor)
        btn.pack()

        back_btn = tkinter.Button(self.root, text="Назад", command=self.menu)
        back_btn.pack(pady=10)

        self.all_elements.extend([text, self.doctor_name_entry, btn, back_btn])


    def authorize_doctor(self):
        name = self.doctor_name_entry.get()
        for doctor in self.list_of_doctors:
            if doctor.name == name:
                self.doctor = doctor

        self.doctor_menu()


    def register_patient(self):

        self.clean()

        text = tkinter.Label(self.root, text= "Введіть ваше ім'я:")
        text.pack()

        self.name_entry = tkinter.Entry(self.root)
        self.name_entry.pack()


        btn = tkinter.Button(self.root, text = "Зберегти", command = self.creating_patient)
        btn.pack()

        back_btn = tkinter.Button(self.root, text="Назад", command=self.menu)
        back_btn.pack(pady=10)

        self.all_elements.extend([text, btn, back_btn, self.name_entry])

    def register_doctor(self):

        self.clean()

        text = tkinter.Label(self.root, text= "Введіть ваше ім'я:")
        text.pack()

        self.name_entry = tkinter.Entry(self.root)
        self.name_entry.pack()

        text1 = tkinter.Label(self.root, text= "Введіть вашу спеціалізацію")
        text1.pack()

        self.speciality_entry = tkinter.Entry(self.root)
        self.speciality_entry.pack()

        btn = tkinter.Button(self.root, text = "Зберегти", command = self.creating_doctor)
        btn.pack()

        back_btn = tkinter.Button(self.root, text="Назад", command=self.menu)
        back_btn.pack(pady=10)

        self.all_elements.extend([text, text1, btn, back_btn, self.name_entry, self.speciality_entry])


    def creating_patient(self):
        self.name = self.name_entry.get()
        self.patient = Patient(self.name)
        self.list_of_patients.append(self.patient)
        self.patient_menu()

    def creating_doctor(self):
        self.name = self.name_entry.get()
        self.speciality = self.speciality_entry.get()
        self.doctor = Doctor(self.name, self.speciality)
        
        self.list_of_doctors.append(self.doctor)

        self.doctor_menu()


    def patient_menu(self):
        self.clean()

        text = tkinter.Label(self.root, text= "Кабінет пацієнта")
        text.pack()

        btn = tkinter.Button(self.root, text = "Переглянути список лікарів", command = self.doctor_list)
        btn.pack()

        btn1 = tkinter.Button(self.root, text = "Переглянути історію хвороб", command = self.patient_history)
        btn1.pack()

        back_btn = tkinter.Button(self.root, text="Вийти з акаунту", command=self.menu)
        back_btn.pack(pady=10)

        self.all_elements.extend([text, btn, btn1, back_btn, self.name_entry])


    def patient_history(self):
        self.clean()

        for app in self.patient.appointments:
            text = tkinter.Label(self.root, text= f"Лікар: {app.doctor} Діагноз: {app.diagnosis} Лікування: {app.prescription}")
            text.pack()
            self.all_elements.append(text)
                                     
        back_btn = tkinter.Button(self.root, text="Назад", command=self.patient_menu)
        back_btn.pack(pady=10)

        self.all_elements.append(back_btn)


    def doctor_list(self):
        self.clean()

        header = tkinter.Label(self.root, text="Список лікарів:")
        header.pack()
        self.all_elements.append(header)

        for doctor in self.list_of_doctors:
            text = tkinter.Label(self.root, text = f"{doctor.name}, {doctor.speciality}")
            text.pack()


            btn = tkinter.Button(self.root, text="Записатись", command=lambda d=doctor: self.schedule_appointment(d))
            btn.pack(pady=5)
            self.all_elements.append(btn)

            self.all_elements.append(text)

        back_btn = tkinter.Button(self.root, text="Назад", command=self.patient_menu)
        back_btn.pack(pady=10)
        self.all_elements.append(back_btn)


    def schedule_appointment(self, doctor):

        self.clean()

        self.selected_doctor = doctor

        text = tkinter.Label(self.root, text= "Введіть Час (у вигляді XX:XX, наприклад 15:30):")
        text.pack()

        self.time_entry = tkinter.Entry(self.root)
        self.time_entry.pack()


        text1 = tkinter.Label(self.root, text= "Введіть Дату (у вигляді ДД.ММ.РРРР, наприклад 21.06.2025):")
        text1.pack()

        self.date_entry = tkinter.Entry(self.root)
        self.date_entry.pack()


        btn = tkinter.Button(self.root, text = "Зберегти", command = self.complete_schedule)
        btn.pack()

        back_btn = tkinter.Button(self.root, text="Назад", command=self.doctor_list)
        back_btn.pack(pady=10)

        self.all_elements.extend([text, self.time_entry, text1, self.date_entry, btn, back_btn])


    def complete_schedule(self):

        time = self.time_entry.get()
        date = self.date_entry.get()
        doctor = self.selected_doctor

        self.clean()

        self.patient.schedule_appointment( doctor, date, time)

        text = tkinter.Label(self.root, text= f"Ви успішно записались до лікаря {doctor.name}")
        text.pack()


        btn = tkinter.Button(self.root, text = "Далі", command = self.patient_menu)
        btn.pack()

        self.all_elements.extend([text, btn])




    def doctor_menu(self):
        self.clean()
        text = tkinter.Label(self.root, text= "Кабінет лікаря")
        text.pack()

        btn = tkinter.Button(self.root, text = "Переглянути запис", command = self.show_schedule)
        btn.pack()

        back_btn = tkinter.Button(self.root, text="Вийти з акаунту", command=self.menu)
        back_btn.pack(pady=10)

        self.all_elements.extend([text, btn, back_btn, self.name_entry])

    
    def show_schedule(self):
        self.clean()

        header = tkinter.Label(self.root, text="Список записаних пацієнтів:")
        header.pack()
        self.all_elements.append(header)

        for patient in self.doctor.schedule:
            text = tkinter.Label(self.root, text = f"{patient[0].name}, Дата: {patient[1]}, Час: {patient[2]}")
            text.pack()


            btn = tkinter.Button(self.root, text="Прийняти", command=lambda p=patient[0]: self.create_appointment(p))
            btn.pack(pady=5)
            self.all_elements.append(btn)

            self.all_elements.append(text)

        back_btn = tkinter.Button(self.root, text="Назад", command=self.doctor_menu)
        back_btn.pack(pady=10)
        self.all_elements.append(back_btn)


    def create_appointment(self, patient):
        self.clean()

        self.selected_patient = patient

        text = tkinter.Label(self.root, text= "Діагноз:")
        text.pack()

        self.diagnosis_entry = tkinter.Entry(self.root)
        self.diagnosis_entry.pack()


        text1 = tkinter.Label(self.root, text= "Лікування:")
        text1.pack()

        self.prescription_entry = tkinter.Entry(self.root)
        self.prescription_entry.pack()


        btn = tkinter.Button(self.root, text = "Зберегти", command = self.complete_appointment)
        btn.pack()

        back_btn = tkinter.Button(self.root, text="Назад", command=self.show_schedule)
        back_btn.pack(pady=10)

        self.all_elements.extend([text, self.diagnosis_entry, self.prescription_entry, text1, self.date_entry, btn, back_btn])


    def complete_appointment(self):

        diagnosis = self.diagnosis_entry.get()
        prescription = self.prescription_entry.get()
        patient = self.selected_patient

        self.clean()

        diagnosis_ = Diagnosis(diagnosis)
        prescription_ = Prescription(prescription)
        self.doctor.add_appointment(patient, diagnosis_, prescription_)

        text = tkinter.Label(self.root, text= f"Ви успішно прийняли пацієнта {patient.name}")
        text.pack()


        text1 = tkinter.Label(self.root, text= "Деталі прийому:")
        text1.pack()

        text2 = tkinter.Label(self.root, text= f"Діагноз: {diagnosis_.name}")
        text2.pack()

        text3 = tkinter.Label(self.root, text= f"Призначене лікування: {prescription_.name}")
        text3.pack()



        btn = tkinter.Button(self.root, text = "Далі", command = self.doctor_menu)
        btn.pack()

        self.all_elements.extend([text, text1, text2, text3, btn])


    def clean(self):
        for elem in self.all_elements:
            elem.destroy()
        self.all_elements = []



root = tkinter.Tk()
app = App(root)
root.mainloop()



#програма працює від лиця пацієнта і від лиця лікаря
#пацієнт побаче лікаря у списку, як тільки лікар зареєструється. пацієнт баче список усіх зареєстрованих лікарів
#лікар побаче пацієнта у списку, як тільки пацієнт запишеться на прийом. лікар баче список лише тих пацієнтів, яки до нього записались
#пацієнт побаче новий запис у історії хвороб, як тільки лікар прийме пацієнта
#в цей момент у списку записів у лікаря пропаде цей пацієнт, тому що його вже прийнято. запис з цим пацієнтом знову з'явиться, якщо пацієнт повторно запишеться на прийом.