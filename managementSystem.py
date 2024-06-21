import hashlib
import re
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from data import User, Student, Score, Absence

class ManagementSystem:
    def __init__(self):
        self.engine = create_engine('sqlite:///students.db')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    def loginMessage(self):
        self.read_and_print_file('login.txt')
            
    #Register student
    def register(self):
        print("==============================Register==============================\n1. Account name is between 3 and 6 letters long\n2. Account name's first letter must be capitalized")
        while True:
            username = input("Please Enter Account Name: ")
            existing_user = self.session.query(User).filter_by(name=username).first()
            #Prompts for if the input is invalid 
            if existing_user:
                print("Registration Failed! Account Already Exists") 
            elif not ((len(username) >= 3 and len(username) <= 6) and username.isalnum()):
                print("Account Name Not Valid!")
            else:
                break
             #Instructons for registry input 
        print("1. Password must start with one of the following special characters !@#$%^&*")
        print("2. Password must contain at least one digit, one lowercase letter, and one uppercase letter")
        print("3. Password is between 6 and 12 letters long")

    #Log in password
        while True:
            password = input("Please enter your password: ")
            if not re.match(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,12}$", password):
                print("Password Not Valid!")
            else:
                break

        hashed_password = hashlib.md5(password.encode()).hexdigest()
        new_user = User(name=username, password=hashed_password)
        self.session.add(new_user)

        # Commit the changes
        self.session.commit()
        print(f"Registration completed! Welcome {username}!")
        self.welcomeMessage()
        
    def login(self):    #Account login
        print("==============================Login==============================")
        username = input("Please Enter Your Account Username: ")
        user = self.session.query(User).filter_by(name=username).first()
        while not user:
            print("Login Failed! Account Doesn't Exist")    #Prompts for inccorect account input
            username = input("Please Enter Your Account Username: ")
            user = self.session.query(User).filter_by(name=username).first()
        password = input("Please Enter Your Account Password: ")  
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        while hashed_password != user.password:
            print("Invalid password")   #Prompts for inccorect account input
            password = input("Please Enter Your Account Password: ")
            hashed_password = hashlib.md5(password.encode()).hexdigest()
        print(f"Login Successful! Welcome {username}!")
    #Reads and prints files, makes it easier to print menus and the like
    def read_and_print_file(self, path):
        try:
            with open(path,'r',encoding='UTF-8') as file:
                content = file.read()
                print(content)
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def welcomeMessage(self):   #Output of the welcome screen 
        self.read_and_print_file('welcome.txt')
    def showStudentMenu(self):  #output of student menu
        self.read_and_print_file('show.txt')
        
    def studentGradeMenu(self): #prints student grade menu
        self.read_and_print_file('studentgrade.txt')
    
    def studentAbsenceMenu(self): #prints student absence menu
        self.read_and_print_file('absence.txt')
        
    def addStudent(self):
        self.read_and_print_file('addstudent.txt')
        while True:
            name = input("Please enter the student name (Firstname Lastname): ")
            if name.istitle() and len(name.split()) == 2 and all(len(part) >= 2 for part in name.split()) and name.replace(' ','').isalpha():
                break
            print("Invalid Name")
        while True:
            age = input("Please Enter Student's Age: ")
            if age.isdigit() and 0 < int(age) < 100:
                break
            print("Invalid age")
        while True:
            gender = input("Please Enter Student's Gender: ").upper()
            if gender in ['M', 'F', 'O']:
                break
            print("Invalid Gender")
        while True:
            phone = input("Please Enter the Student Phone \u260E: ")
            if len(phone) == 12 and phone[3] == '-' and phone[7] == '-' and phone.replace('-','').isdigit():
                break
            print("Invalid Phonenumber")
        while True:
            major = input("Please Enter the Student Major: ").upper()
            if major in ['CS','CYBR','SE','IT','DS']:
                break
            print("Invalid Major")
        id = str(700300000 + self.session.query(Student).count() + 1)

        print("\u2714 New student record has been added!")  #Output when student is add to the system
        new_student = Student(id=id, name=name, age=age, gender=gender, major=major, phone=phone)
        self.session.add(new_student)

        new_score = Score(id=id, name=name, CS1030=0, CS1100=0, CS2030=0)   #creating new score for new student
        self.session.add(new_score)
        
        new_absence = Absence(id=id, name=name, absences=0)
        self.session.add(new_absence)

        self.session.commit()
    #deletes student record
    def delStudent(self):
        #enter ID of student to delete
        ID = input("Enter the ID of the student you want to delete: ")
        student = self.session.query(Student).filter(Student.id == ID).first()
        score = self.session.query(Score).filter(Score.id == ID).first()
        absence = self.session.query(Absence).filter(Absence.id == ID).first()

        #if ID is not in students
        if student is None:
            print(f"Student ID {ID} doesn't exist") 
        #if ID is in students
        else:
            print("==============================Student Record==============================")
            print(f"{'ID':<20s}{'Name':<20s}{'Age':<20s}{'Gender':<20s}{'Major':<20s}{'Phone':<20s}")
            print(f"{student.id:<20s}{student.name:<20s}{student.age:<20d}{student.gender:<20s}{student.major:<20s}{student.phone:<20s}")
            #checks if user is sure
            q = input("Are you sure you want to delete the record? Y or N: ")
            #if user is sure, it deletes the record
            if q.upper() == "Y":
                self.session.delete(student)
                self.session.delete(score)
                self.session.delete(absence)
                self.session.commit()
                print("Student record has been deleted")
            #if user is not sure, it passes
            else:
                pass
        #updates json file

    def modifyStudent(self):
        #enter student id to modify
        id = input("Please Enter Student ID to Modify: ")
        #checks for student id in students
        student = self.session.query(Student).filter_by(id=id).first()
        counter = 0
        #if student id exists
        if student:
            #gives new name, phone, and major
            age = input("New age: ")
            if age.strip():
                if not (int(age) > 0 and int(age) < 100):
                    print("Invalid age")
                    return
                student.age = age
                counter += 1
            phone = input("New phone \u260E: ")
            if phone.strip():
                if not(len(phone) == 12 and phone[3] == '-' and phone[7] == '-' and phone.replace('-','').isdigit()):
                    print("Invalid Phone Number")
                    return
                student.phone = phone
                counter += 1
            major = input("New major: ").upper()
            if major.strip():
                if major not in ['CS','CYBR','SE','IT','DS']:
                    print("Invalid Major")
                    return
                student.major = major
                counter+=1
            #if any of the fields are modified
            if counter != 0:
                print("\u2714 Student record has been modified!")
                self.session.commit()
            else:
                print("\u274C No modifications were made")
        #if student id doesn't exist
        else:
            print(f"Student ID {id} doesn't exist")
        
    def showStudentbyID(self):
        #enter ID of student to show
        id = input("Please enter the Student ID you want to query: ")
        student = self.session.query(Student).filter_by(id=id).first()
        if student:
            print("==============================Student Record==============================")
            print(f"{'ID':<20s}{'Name':<20s}{'Age':<20s}{'Gender':<20s}{'Major':<20s}{'Phone':<20s}")
            print(f"{student.id:<20s}{student.name:<20s}{student.age:<20d}{student.gender:<20s}{student.major:<20s}{student.phone:<20s}")
        else:
            print(f"\u274C Student with ID {id} not found")
    def showStudentbyName(self):
        #enter name of student to show
        name = input("Please enter the name of the student you want to query: ")
        student = self.session.query(Student).filter_by(name=name).first()
        if student:
            print("==============================Student Record==============================")
            print(f"{'ID':<20s}{'Name':<20s}{'Age':<20s}{'Gender':<20s}{'Major':<20s}{'Phone':<20s}")
            students = self.session.query(Student).all()
            for i in students:
                if i.name == name:
                    print(f"{i.id:<20s}{i.name:<20s}{i.age:<20d}{i.gender:<20s}{i.major:<20s}{i.phone:<20s}")
        else:
            print(f"\u274C Student with Name {name} not found")
    def displayStudents(self):
        #prints all students
        print("Student Record")
        print(f"{'ID':<20s}{'Name':<20s}{'Age':<20s}{'Gender':<20s}{'Major':<20s}{'Phone':<20s}")
        students = self.session.query(Student).all()
        for student in students:
            print(f"{student.id:<20s}{student.name:<20s}{student.age:<20d}{student.gender:<20s}{student.major:<20s}{student.phone:<20s}")
    def showStudentGrade(self):
        self.studentGradeMenu()
        choice = input("Please Select: ")
        if choice == "1":
            name = input("Please Enter Student Name To Display The Score: ")
            score = self.session.query(Score).filter_by(name=name).first()
            if score: # if name exists post student scores
                print(f"{'ID':<20s}{'Name':<20s}{'CS 1030':<20s}{'CS 1100':<20s}{'CS 2030':<20s}")
                scores = self.session.query(Score).all()
                for i in scores:
                    if i.name == name:
                        print(f"{i.id:<20s}{i.name:<20s}{i.CS1030:<20d}{i.CS1100:<20d}{i.CS2030:<20d}")
            else:
                print(f"\u274C Student with Name {name} not found")
        elif choice == "2":
            id = input("Please Enter The Student Id To Update The Score: ")
            score = self.session.query(Score).filter_by(id=id).first()
            if score: # input new scores, old scores remain if user presses enter
                score1_input = input("New grade for CS 1030 (press enter without modification): ")
                score1 = int(score1_input) if score1_input else score.CS1030 
                score2_input = input("New grade for CS 1100 (press enter without modification): ")
                score2 = int(score2_input) if score2_input else score.CS1100
                score3_input = input("New grade for CS 2030 (press enter without modification): ")
                score3 = int(score3_input) if score3_input else score.CS2030
                score.CS1030 = int(score1) if score1 else score.CS1030
                score.CS1100 = int(score2) if score2 else score.CS1100
                score.CS2030 = int(score3) if score3 else score.CS2030

                self.session.commit() # commit changes
            else:
                print(f"\u274C Student with ID {id} not found")
                return
    def login_register(self):
        while True:
            self.loginMessage()
            choice = input("Please select (1 - 3): ")
            if choice == '1':
                self.login()
                return
            elif choice == '2':
                self.register()
                return
            elif choice == '3':
                sys.exit()
            else:
                print("Invalid Choice.")
    def studentAbsences(self):
        self.studentAbsenceMenu()
        choice = int(input("Please Select Command: "))
        if choice == 1:
            #enter name of student to count absent  
            name = input("Please Enter Student Name To Display Absences: ")
            #finds student
            absence = self.session.query(Absence).filter_by(name=name).first()
            #if student doesn't exist
            if absence is None:
                print(f"Student {name} doesn't exist")
            #if student exists
            else:
                #prints student absences
                print(f"{'ID':<20s}{'Name':<20s}{'Absences':<20s}")
                print(f"{absence.id:<20s}{absence.name:<20s}{absence.absences:<20d}")
                #if student has 5 or more absences, they are suspended
                if absence.absences >= 5:
                    print(f"Student {absence.name} is suspended on account of too many absences")
        elif choice == 2:
            # finds student by ID
            ID = input("Please Enter Student ID To Count Absent: ")
            absence = self.session.query(Absence).filter_by(id=ID).first()
            #if student doesn't exist
            if absence is None:
                print(f"Student ID {ID} doesn't exist")
            #if student exists
            else:
                #absent is counted
                absence.absences += 1
                print("Absence added")
            #commit changes
            self.session.commit()
    def operations(self):
        while True:
            self.welcomeMessage()
            choice = int(input("Please Enter the Operation Code: "))
            #matches choice to any of the cases
            match choice:
                case 1:
                    self.addStudent()
                case 2:
                    self.delStudent()
                case 3:
                    self.modifyStudent()
                case 4:
                    self.showStudentMenu()
                    choice2 = int(input("Please Enter the Operation Code: "))
                    match choice2:
                        case 1:
                            self.showStudentbyID()
                        case 2:
                            self.showStudentbyName()
                        case 3:
                            self.displayStudents()
                case 5:
                    self.showStudentGrade()
                case 6:
                    self.studentAbsences()
                case 7:
                    return
               