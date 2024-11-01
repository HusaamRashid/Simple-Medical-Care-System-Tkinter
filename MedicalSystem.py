from tkinter import *
from tkinter import ttk
import csv


def main_account_screen():
    global main_screen
    main_screen = Tk()  # create tkinter screen
    main_screen.geometry("500x450")  # screen size
    main_screen.title("Login Dashboard")  # screen name
    # create a label - text to appear on users screen
    Label(
        text="Choose Admin or Doctor login portal",
        bg="blue",
        width="300",
        height="2",
        font=("Calibri", 13),
    ).pack()
    Label(text="").pack()
    # This makes several buttons appear on the screen that calls a different function when pressed
    Button(text="Admin Login", height="2", width="30", command=admin_login).pack()
    Button(text="Doctor Login", height="2", width="30", command=doctor_login).pack()
    Button(text="Register a Doctor", height="2", width="30", command=registration).pack()


class User:
    #Creates a class for a user which then be inherited for later classes
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Admin(User):
    #Admin class so we can make all the admins into objects, inherits the User class and then adds the extra field of their address
    def __init__(self, username, password, address):
        super().__init__(username, password)
        self.address = address


class Doctor(User):
    #Class for doctor so that we can make them into objects and inherits the User class
    def __init__(self, username, password):
        super().__init__(username, password)


class MedicalCareSystem:
    #Class for the overall medical system to set up basic systems to provide aid later on
    def __init__(self):
        self.admins = self.load_admins_from_csv()
        self.doctors = self.load_doctors_from_csv()

    def load_admins_from_csv(self):
        #Loads all the admin information from external file and uses this data to create an object of the Admin class for each set of data
        admins = []
        with open("admincredentials.csv", "r") as admin_file:
            csvreader = csv.DictReader(admin_file)
            for row in csvreader:
                admin = Admin(row["Username"], row["Password"], row["Address"])
                admins.append(admin)
        return admins

    def load_doctors_from_csv(self):
        #Same as previous function except works for the doctors and loads all their data from the files 
        doctors = []
        with open("doctorcredentials.csv", "r") as doctor_file:
            csvreader = csv.DictReader(doctor_file)
            for row in csvreader:
                doctor = Doctor(row["Username"], row["Password"])
                doctors.append(doctor)
        return doctors

#Makes an object of the Medical Care System class and assigns it to a variable
medical_system = MedicalCareSystem()


def admin_login():
    global username_entry
    global password_entry
    global admin_log_screen

    # Makes a Top Level window for the admins login page
    admin_log_screen = Toplevel()
    # Basic settings for the tkinter gui window, same as initial main screen
    admin_log_screen.title("Admin Login Portal")
    admin_log_screen.geometry("400x250")

    username = ""
    password = ""

    Label(admin_log_screen, text="Please enter login credentials below", bg="blue").pack()
    Label(admin_log_screen, text="").pack()
    #Takes data from users input to check later
    username_lable = Label(admin_log_screen, text="Username * ")
    username_lable.pack()

    username_entry = Entry(admin_log_screen, textvariable=username)
    username_entry.pack()

    password_lable = Label(admin_log_screen, text="Password * ")
    password_lable.pack()
    #Replaces the entered characters with *s to hide the password the user is entering
    password_entry = Entry(admin_log_screen, textvariable=password, show="*")
    password_entry.pack()

    Label(admin_log_screen, text="").pack()
    #Calls the actual function that will check if the entered credentials are correct
    Button(
        admin_log_screen,
        text="Login",
        width=10,
        height=1,
        bg="blue",
        command=login_verify,
    ).pack()


def doc_login_verify():
    # LOGIN CHECKING FUNCTION FOR DOCTOR LOGIN
    global loggedDoc
    loggedin = False
    username = doc_username_entry.get()
    loggedDoc = username
    password = doc_password_entry.get()
    # To get rid of entries after function is called
    doc_username_entry.delete(0, END)
    doc_password_entry.delete(0, END)
    with open("doctorcredentials.csv", "r") as docfile:
        csvreader = csv.DictReader(docfile)
    # Loop through each doctor object in the list of doctor objects and checks if the username/password matches both the ones entered
    for doctor in medical_system.doctors:
        if username == doctor.username and password == doctor.password:
            loggedin = True
            login_success()
            #Calls the dashboard to be created so the doctor can use their functions
            initiate_doctor_dashboard()
    if loggedin == False:
        doc_login_fail()


def doc_login_fail():
    Label(doc_log_screen, text="Login failed").pack()


def doctor_login():
    global doc_username_entry
    global doc_password_entry
    global doc_log_screen

    # Makes a Top Level window for the doctor login page
    doc_log_screen = Toplevel()
    # Basic settings for the tkinter gui window, same as initial main screen
    doc_log_screen.title("Doctor Login Portal")
    doc_log_screen.geometry("400x250")

    username = ""
    password = ""

    Label(doc_log_screen, text="Please enter login credentials below", bg="blue").pack()
    Label(doc_log_screen, text="").pack()

    doc_username_lable = Label(doc_log_screen, text="Username * ")
    doc_username_lable.pack()

    doc_username_entry = Entry(doc_log_screen, textvariable=username)
    doc_username_entry.pack()

    doc_password_lable = Label(doc_log_screen, text="Password * ")
    doc_password_lable.pack()

    doc_password_entry = Entry(doc_log_screen, textvariable=password, show="*")
    doc_password_entry.pack()

    Label(doc_log_screen, text="").pack()

    Button(
        doc_log_screen,
        text="Login",
        width=10,
        height=1,
        bg="blue",
        command=doc_login_verify,
    ).pack()


def registration():
    # Makes a Top Level window for the page
    global register_screen
    global pwd_entry
    global email_entry
    register_screen = Toplevel(main_screen)
    # Basic settings for the tkinter gui window, same as initial main screen
    register_screen.title("Doctor Registration")
    register_screen.geometry("300x250")
    email = ""
    registerpassword = ""
    #Sets up fields to get users input
    email_entry = Entry(register_screen, textvariable=email)
    pwd_entry = Entry(register_screen, textvariable=registerpassword)
    email_lable = Label(register_screen, text="Enter username or email")
    pwd_lable = Label(register_screen, text="Enter Password")
    email_lable.pack()
    email_entry.pack()
    pwd_lable.pack()
    pwd_entry.pack()
    #Creates a button that calls a function for the file handling
    Button(
        register_screen,
        text="Register doctor",
        width=12,
        height=1,
        command=register_doc,
    ).pack()


def register_doc():
    #Gets the data that the user entered onto their screen
    email = email_entry.get()
    pwd = pwd_entry.get()
    #Puts this data into a list
    data = [email, pwd]
    #Defines the header of the CSV file which is the names of the columns that the data will be stored under
    header = ["Username", "Password"]
    #Checks if either field is blank then returns an error
    if email == "" or pwd == "":
        Label(register_screen, text="Username or Password cannot be left blank").pack()
        return
    #opens the file holding the doctors details and reads the data into a list of dictionaries where each dictionary contains data about one doctor
    with open("doctorcredentials.csv", "r") as file:
        csvreader = csv.DictReader(file)
        data = [row for row in csvreader]
    #Opens the file again but now in writing mode, clearing the entire file
    with open("doctorcredentials.csv", "w", newline="") as file:
        # Create csvwriter object
        csvwriter = csv.DictWriter(file, fieldnames=header)
        #Writes in the header to the file
        csvwriter.writeheader()
        #Then loops through the list of dictionaries and writes each dictionary as a row to the file
        for i in data:
            csvwriter.writerow(i)
    Label(register_screen, text="Successfully registered Doctor").pack()


def login_verify():
    # LOGIN CHECKING FUNCTION FOR ADMIN LOGIN
    loggedin = False
    username = username_entry.get()
    password = password_entry.get()
    # To get rid of entries
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    # Loop through each admin in the list of admin objects, then checks if any set of credentials matches the credentials entered by user
    for admin in medical_system.admins:
        if admin.username == username and admin.password == password:
            loggedin = True
            login_success()
            #Launches admin dashboard screen which contains buttons for all admin features and functions
            initiate_admin_dashboard()
    if loggedin == False:
        login_fail()


def login_success():
    # Function for when login username and password both match
    #Creates an acknowledgement screen
    global login_success_screen
    login_success_screen = Toplevel()
    Label(login_success_screen, text="Login Successful").pack()
    Button(login_success_screen, text="OK", command=login_success_remove).pack()


def login_success_remove():
    login_success_screen.destroy()


def login_fail():
    Label(
        admin_log_screen,
        text="Login Unsucessful either the username or password was incorrect.",
    ).pack()


def initiate_doctor_dashboard():
    global doc_dashboard_screen
    doc_dashboard_screen = Toplevel()
    doc_dashboard_screen.title("Doctor Dashboard")
    doc_dashboard_screen.geometry("750x500")
    #Removes the login screen after doctor has logged in
    doc_log_screen.destroy()
    #Creates buttons for all the doctor features
    Label(
        doc_dashboard_screen,
        text="Welcome to the Doctor Dashboard",
        bg="blue",
        width="750",
        height="2",
        font=("Calibri", 13),
    ).pack()
    Button(
        doc_dashboard_screen,
        text="Patient Records",
        height="2",
        width="30",
        command=viewPatients,
    ).pack()
    Button(
        doc_dashboard_screen,
        text="View Appointments",
        height="2",
        width="30",
        command=viewDocAppointment,
    ).pack()


def viewDocAppointment():
    global doc_appointment_screen
    #Makes a new screen from doctor dashboard
    doc_appointment_screen = Toplevel()
    #Gets the name of the doctor who is logged in currently
    doctor = loggedDoc
    appointmentlist = []
    #Creates list of dictionaries containing data on all appointments
    with open("appointments.csv", "r") as appointments:
        csvreader = csv.DictReader(appointments)
        data = [row for row in csvreader]
    #Loops through each dictionary and checks if the Doctors name in the appointment is the same as the logged in Doctor it will add that appointment information to a list
    for i in data:
        if i["Doctor"] == doctor:
            appointmentlist.append(i)
    #Creates text on the screen displaying information on all the appointmemts
    Label(doc_appointment_screen, text=appointmentlist).pack()



def initiate_admin_dashboard():
    #Serves as main dashboard for the admin once logged in
    global admin_dashboard_screen
    admin_dashboard_screen = Toplevel()
    admin_dashboard_screen.title("Admin Dashboard")
    admin_dashboard_screen.geometry("500x750")
    admin_log_screen.destroy()
    #Create buttons for each function/feature for the admin to use
    Label(
        admin_dashboard_screen,
        text="Welcome to the Admin Dashboard",
        bg="blue",
        width="750",
        height="2",
        font=("Calibri", 13),
    ).pack()
    Button(
        admin_dashboard_screen,
        text="Patient Records",
        height="2",
        width="30",
        command=viewPatients,
    ).pack()
    Button(
        admin_dashboard_screen,
        text="Doctor Controls",
        height="2",
        width="30",
        command=doctor_control_panel,
    ).pack()
    Button(
        admin_dashboard_screen,
        text="Discharge Patient",
        height="2",
        width="30",
        command=patientDischarge_screen,
    ).pack()
    Button(
        admin_dashboard_screen,
        text="Treated Patients",
        height="2",
        width="30",
        command=treatedList,
    ).pack()
    Button(
        admin_dashboard_screen,
        text="Admin Information",
        height="2",
        width="30",
        command=updateAdminInfo,
    ).pack()
    Button(
        admin_dashboard_screen,
        text="Management Report",
        height="2",
        width="30",
        command=managementReport,
    ).pack()
    Button(
        admin_dashboard_screen,
        text="Families",
        height="2",
        width="30",
        command=familyManagement,
    ).pack()
    Label(admin_dashboard_screen, text="Patient Tasks", height="2").pack()
    Button(
        admin_dashboard_screen, text="Enroll", height="2", width="30", command=enroll
    ).pack()
    Button(
        admin_dashboard_screen,
        text="Book Appointment",
        height="2",
        width="30",
        command=bookAppointment,
    ).pack()
    Button(
        admin_dashboard_screen,
        text="Check Doctor",
        height="2",
        width="30",
        command=findAssignedDoctor,
    ).pack()
    Button(
        admin_dashboard_screen,
        text="Appointment Status",
        height="2",
        width="30",
        command=checkAppointmentStatus,
    ).pack()


def checkAppointmentStatus():
    # returns the status of a patients appointments
    global checkStatus_screen
    global status_patient_entry
    checkStatus_screen = Toplevel(admin_dashboard_screen)
    patient = ""
    status_patient_entry = Entry(checkStatus_screen, textvariable=patient)
    Label(checkStatus_screen, text="Enter patient name").pack()
    status_patient_entry.pack()
    Button(
        checkStatus_screen, text="Check appointment status", command=returnStatus
    ).pack()


def returnStatus():
    #Loops through the appointments in the external file to return every appointment with a certain patients name
    patient = status_patient_entry.get()
    appointmentlists = []
    with open("appointments.csv", "r") as appointments:
        csvreader = csv.DictReader(appointments)
        data = [row for row in csvreader]
    for i in data:
        if i["Patient"] == patient:
            appointmentlists.append(i)
    Label(checkStatus_screen, text=appointmentlists).pack()


def findAssignedDoctor():
    #Screen for a function to return a patients doctor
    global findAssignedDoc_screen
    global fordoc_patientname_entry
    fordoc_patient = ""
    #Gets user input for the patient
    findAssignedDoc_screen = Toplevel(admin_dashboard_screen)
    Label(findAssignedDoc_screen, text="Enter patient to find their assigned doctor").pack()
    fordoc_patientname_entry = Entry(findAssignedDoc_screen, textvariable=fordoc_patient)
    fordoc_patientname_entry.pack()
    Button(findAssignedDoc_screen, text="Find Assigned Doctor", command=returnAssignedDoc).pack()


def returnAssignedDoc():
    patient = fordoc_patientname_entry.get()
    doctorlist = []
    with open("appointments.csv", "r") as doctors:
        csvreader = csv.DictReader(doctors)
        data = [row for row in csvreader]
    #Loops through each appointment to find any appointment with the entered patient 
    #Then returns a list of all the doctors who are booked onto those appointments
    for i in data:
        if i["Patient"] == patient:
            doctorlist.append(i["Doctor"])
    Label(findAssignedDoc_screen, text=doctorlist).pack()


def viewPatients():
    # Function to return all patient records or just one patients record
    global patients_screen
    global patient_for_record_entry
    patient = ""
    patients_screen = Toplevel()
    patients_screen.title("View Patient Records")
    patients_screen.geometry("500x200")
    Button(patients_screen, text="View all patients' records", command=allrecords).pack()
    patient_for_record_entry = Entry(patients_screen, textvariable=patient)
    patient_for_record_entry.pack()
    Button(patients_screen, text="Find patient's record", command=patientlookup).pack()


def allrecords():
    global record_screen
    record_screen = Toplevel(patients_screen)
    #Makes a tkinter treeview 
    #This acts like a big table
    tree = ttk.Treeview(record_screen, show="headings")
    tree.pack(padx=20, pady=20, fill="both", expand=True)
    with open("patientrecords.csv", "r", newline="") as records:
        csvreader = csv.reader(records)
        #Reads the header of the CSV file then gives these to the tree view to make it the name of each column
        header = next(csvreader)
        tree["columns"] = header
        for col in header:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        #Puts the data for each row into the tree so you have a grid showing each patients details
        for row in csvreader:
            tree.insert("", "end", values=row)
    Button(record_screen, text="OK", command=exitrecord).pack()


def exitrecord():
    record_screen.destroy()


def patientlookup():
    givenName = patient_for_record_entry.get()
    with open("patientrecords.csv", "r") as records:
        csvreader = csv.DictReader(records)
        data = [row for row in csvreader]
    # Loop through each dictionary in the list called data then check if the first element of each dict is the inputted username
    for i in data:
        if i["Name"] == givenName:
            Label(patients_screen, text=i).pack()


def bookAppointment():
    #Screen to enter details to book an appointment
    global bookappointment_screen
    global appointment_patient_entry
    global appointment_doc_entry
    global appointment_status_entry
    bookappointment_screen = Toplevel(admin_dashboard_screen)
    bookappointment_screen.title("Book an appointment")
    patientname = ""
    doctorname = ""
    appointmentStatus = ""
    #Takes input from the Admin for the details of the appointment
    appointment_patient_entry = Entry(bookappointment_screen, textvariable=patientname)
    appointment_doc_entry = Entry(bookappointment_screen, textvariable=doctorname)
    appointment_status_entry = Entry(bookappointment_screen, textvariable=appointmentStatus)
    Label(bookappointment_screen, text="Enter patient").pack()
    appointment_patient_entry.pack()
    Label(bookappointment_screen, text="Enter doctor").pack()
    appointment_doc_entry.pack()
    Label(bookappointment_screen, text="Enter appointment status").pack()
    appointment_status_entry.pack()
    Button(bookappointment_screen, text="Book Appointment", command=addAppointment).pack()


def addAppointment():
    #Creates the names of the necessary columns for the external file
    field_names = ["Patient", "Doctor", "Status"]
    #Gets the inputted data from the entry fields
    patientname = appointment_patient_entry.get()
    docname = appointment_doc_entry.get()
    status = appointment_status_entry.get()
    if patientname == '' or docname == '' or status == '':
        Label(bookappointment_screen, text='Fields cannot be blank').pack()
        return
        
    #Creates dictionary of data to write
    appdata = {"Patient": patientname, "Doctor": docname, "Status": status}
    #Opens file in append mode to add new appointment to the end of the file
    with open("appointments.csv", "a", newline="") as appfile:
        csvwriter = csv.DictWriter(appfile, fieldnames=field_names)
        csvwriter.writerow(appdata)
        Label(bookappointment_screen, text="Appointment booked!")
        appointment_cleanup()
        appfile.close()


def appointment_cleanup():
    bookappointment_screen.destroy()


def enroll():
    # Just add a new patient to patient records csv
    global enrollment_screen
    global enroll_name_entry
    global enroll_age_entry
    global enroll_number_entry
    global enroll_address_entry
    global enroll_symptoms_entry
    global enroll_treated_entry
    enrollment_screen = Toplevel(admin_dashboard_screen)
    enrollment_screen.title("Enroll a patient")
    enrollment_screen.geometry("300x400")
    name = ""
    age = ""
    number = ""
    address = ""
    symptoms = ""
    treated = ""
    Label(enrollment_screen, text="Enter patient's details").pack()
    Label(enrollment_screen, text="Enter patient name").pack()
    enroll_name_entry = Entry(enrollment_screen, textvariable=name)
    enroll_name_entry.pack()
    Label(enrollment_screen, text="Enter patient age").pack()
    enroll_age_entry = Entry(enrollment_screen, textvariable=age)
    enroll_age_entry.pack()
    Label(enrollment_screen, text="Enter patient phone number").pack()
    enroll_number_entry = Entry(enrollment_screen, textvariable=number)
    enroll_number_entry.pack()
    Label(enrollment_screen, text="Enter patient address").pack()
    enroll_address_entry = Entry(enrollment_screen, textvariable=address)
    enroll_address_entry.pack()
    Label(enrollment_screen, text="Enter patient symptoms").pack()
    enroll_symptoms_entry = Entry(enrollment_screen, textvariable=symptoms)
    enroll_symptoms_entry.pack()
    Label(enrollment_screen, text="Has the patient been treated?").pack()
    enroll_treated_entry = Entry(enrollment_screen, textvariable=treated)
    enroll_treated_entry.pack()
    Button(enrollment_screen, text="Enroll", command=enrollpatient).pack()


def enrollpatient():
    #Sets names of columns in the file
    field_names = [
        "Name",
        "Age",
        "Number",
        "Address",
        "Symptoms",
        "Treated",
    ]
    #Gets the data from the entry forms and puts it into a dictionary with the relevant key-value pairs
    name = enroll_name_entry.get()
    age = enroll_age_entry.get()
    number = enroll_number_entry.get()
    address = enroll_address_entry.get()
    symptoms = enroll_symptoms_entry.get()
    treated = enroll_treated_entry.get()
    enrollmentdata = {
        "Name": name,
        "Age": age,
        "Number": number,
        "Address": address,
        "Symptoms": symptoms,
        "Treated": treated,
    }

    #Opens file in append mode and adds the patient data to the end of the file
    with open("patientrecords.csv", "a", newline="") as records:
        csvwriter = csv.DictWriter(records, fieldnames=field_names)
        csvwriter.writerow(enrollmentdata)
        Label(enrollment_screen, text="Patient successfully enrolled!")
        enroll_cleanup()


def enroll_cleanup():
    enrollment_screen.destroy


def familyManagement():
    # All the family stuff
    return


def managementReport():
    # Produces the management report
    # Lists number of doctors, number of patients per doctor, number of appointments per month per doctor, total patients with illness type
    global management_screen
    management_screen = Toplevel(admin_dashboard_screen)
    numOfDocs = 0
    with open("doctorcredentials.csv", "r") as doctors:
        csvreader_doctors = csv.DictReader(doctors)
        docdata = [row for row in csvreader_doctors]
        for i in docdata:
            numOfDocs += 1
    doctors.close
    Label(management_screen, text=numOfDocs).pack()


def updateAdminInfo():
    # Update admins name and address and password
    global updateAdmin_screen
    global newAdminName
    global newAdminPwd
    global newAdminAddress
    global oldAdminName
    updateAdmin_screen = Toplevel(admin_dashboard_screen)
    updateAdmin_screen.geometry("250x450")
    name = ""
    password = ""
    address = ""
    oldname = ""
    oldAdminName = Entry(updateAdmin_screen, textvariable=oldname)
    newAdminName = Entry(updateAdmin_screen, textvariable=name)
    newAdminPwd = Entry(updateAdmin_screen, textvariable=password)
    newAdminAddress = Entry(updateAdmin_screen, textvariable=address)
    Label(updateAdmin_screen, text="Enter Admin's current username").pack()
    oldAdminName.pack()
    Label(updateAdmin_screen, text="Enter Admin's new username").pack()
    newAdminName.pack()
    Label(updateAdmin_screen, text="Enter Admin's new password").pack()
    newAdminPwd.pack()
    Label(updateAdmin_screen, text="Enter Admin's new address").pack()
    newAdminAddress.pack()
    Button(updateAdmin_screen, text="Update", command=updateAdminInfoFunc).pack()


def updateAdminInfoFunc():
    field_names = ["Username", "Password", "Address"]
    oldname = oldAdminName.get()
    name = newAdminName.get()
    pwd = newAdminPwd.get()
    address = newAdminAddress.get()
    if oldname == '' or name == '' or pwd == '' or address == '':
        Label(updateAdmin_screen, text="Invalid")
        return
    #Opens file in read mode, then reads all the data into a list of dictionaries
    with open("admincredentials.csv", "r") as admins:
        csvreader = csv.DictReader(admins)
        data = [row for row in csvreader]
    #Loops through each dictionary checking for a username that matches the Admin username entered
    for i in data:
        if i["Username"] == oldname:
            #Then updates all the data in that dictionary to the new data
            i["Username"] = name
            i["Password"] = pwd
            i["Address"] = address
    #Opens file again but now in write mode then writes to the file the header and all the data row by row which includes the now updated row
    with open("admincredentials.csv", "w", newline="") as admins:
        csvwriter = csv.DictWriter(admins, fieldnames=field_names)
        csvwriter.writeheader()
        for i in data:
            csvwriter.writerow(i)


def treatedList():
    # Loop through the patient records, find everyone who has treated == true, then add their name to a list then output the list
    global treated_screen
    treated_screen = Toplevel(admin_dashboard_screen)
    treatedpatientlist = []
    #Loops through the data in the file and adds each patient whose Treated status is True to a list
    with open("patientrecords.csv", "r") as patientlist:
        csvreader = csv.DictReader(patientlist)
        data = [row for row in csvreader]
        for i in data:
            if i["Treated"] == "True":
                treatedpatientlist.append(i["Name"])
    patientlist.close()
    Label(treated_screen, text=treatedpatientlist).pack()


def doctor_control_panel():
    # Main section for Viewing/updating/deleting doctors for Admin
    global doc_controls_screen
    doc_controls_screen = Toplevel(admin_dashboard_screen)
    Button(doc_controls_screen, text="View Doctors", command=viewDocs).pack()
    Button(doc_controls_screen, text="Update a doctor", command=updateDoctor_screen).pack()
    Button(doc_controls_screen, text="Delete Doctor", command=deleteDoc).pack()


def deleteDoc():
    global deleteDoc_screen
    global deleteDocEntry
    deleteDoc_screen = Toplevel(doc_controls_screen)
    docname = ""
    deleteDocEntry = Entry(deleteDoc_screen, textvariable=docname)
    Label(deleteDoc_screen, text="Enter Doctor's name to delete").pack()
    deleteDocEntry.pack()
    Button(deleteDoc_screen, text="Delete", command=deleteDoctorfromFile)


def deleteDoctorfromFile():
    field_names = ["Username", "Password"]
    doctor = deleteDocEntry.get()
    #Reads the data from the file
    with open("doctorcredentials.csv", "r") as doctors:
        csvreader = csv.DictReader(doctors)
        data = [row for row in csvreader]
    #Then loops through that data to find the doctor that has been inputted
    #Then removes that doctor from the list 
    for i in data:
        if i["Username"] == doctor:
            data.remove(i)
    #Then wipes the file and rewrites all the data to it but without that removed doctor
    with open("doctorcredentials.csv", "w", newline="") as doctors:
        csvwriter = csv.DictWriter(doctors, fieldnames=field_names)
        csvwriter.writeheader()
        for i in data:
            csvwriter.writerow(i)


def updateDoctor_screen():
    global updateDoc_screen
    global olddocusername
    global newdocusername
    global pwddoc
    updateDoc_screen = Toplevel(doc_controls_screen)
    oldusername = ""
    newusername = ""
    password = ""
    olddocusername = Entry(updateDoc_screen, textvariable=oldusername)
    newdocusername = Entry(updateDoc_screen, textvariable=newusername)
    pwddoc = Entry(updateDoc_screen, textvariable=password)
    Label(updateDoc_screen, text="Enter Doctor's current username").pack()
    olddocusername.pack()
    Label(updateDoc_screen, text="Enter new Doctor username").pack()
    newdocusername.pack()
    Label(updateDoc_screen, text="Enter new doctor password").pack()
    pwddoc.pack()
    Button(updateDoc_screen, text="Update Doctor", command=updateDoc).pack()


def updateDoc():
    field_names = ["Username", "Password"]
    oldname = olddocusername.get()
    newname = newdocusername.get()
    pwd = pwddoc.get()
    if pwd == "" or pwd == " ":
        Label(updateDoc_screen, text="password cannot be blank")
        return
    with open("doctorcredentials.csv", "r") as doctorfile:
        csvreader = csv.DictReader(doctorfile)
        data = [row for row in csvreader]
        #Changes the data of that dictionary to fit the new data
        for i in data:
            if i["Username"] == oldname:
                i["Username"] = newname
                i["Password"] = pwd
    #Then writes all the data to the file
    with open("doctorcredentials.csv", "w", newline="") as doctorfile:
        csvwriter = csv.DictWriter(doctorfile, fieldnames=field_names)
        csvwriter.writeheader()
        for i in data:
            csvwriter.writerow(i)


def viewDocs():
    global viewDoc_screen
    viewDoc_screen = Toplevel(doc_controls_screen)
    doclist = []
    #Loops through all the doctors information and returns a list of the names of every doctor
    with open("doctorcredentials.csv", "r") as docs:
        csvreader = csv.DictReader(docs)
        data = [row for row in csvreader]
        for i in data:
            doclist.append(i["Username"])
    docs.close()
    Label(viewDoc_screen, text=doclist).pack()
    Button(viewDoc_screen, text="OK", command=removeViewDoc)


def removeViewDoc():
    #Removes the screen
    viewDoc_screen.destroy()


def patientDischarge_screen():
    # Deletes patient
    global discharge_screen
    global dischargedPatient_entry
    dischargedPatient = ""
    discharge_screen = Toplevel(admin_dashboard_screen)
    Label(discharge_screen, text="Enter patient name for discharging").pack()
    dischargedPatient_entry = Entry(discharge_screen, textvariable=dischargedPatient)
    dischargedPatient_entry.pack()
    Button(discharge_screen, text="Discharge Patient", command=dischargePatient).pack()


def dischargePatient():
    patient = dischargedPatient_entry.get()
    field_names = [
        "Name",
        "Age",
        "Number",
        "Address",
        "Symptoms",
        "Treated",
    ]
    #Reads through the data then removes that patient from the list of data
    with open("patientrecords.csv", "r") as records:
        csvreader = csv.DictReader(records)
        data = [row for row in csvreader]
        for i in data:
            if i["Name"] == patient:
                data.remove(i)
    #Then writes all the data back to the file
    with open("patientrecords.csv", "w", newline="") as records:
        csvwriter = csv.DictWriter(records, fieldnames=field_names)
        csvwriter.writeheader()
        for i in data:
            csvwriter.writerow(i)


main_account_screen()  # call the main_account_screen() function

main_screen.mainloop()  # call the GUI
