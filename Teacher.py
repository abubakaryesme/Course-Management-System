from CMSRepository import CMSRepository
from Course import Course
import datetime

class Teacher:

    __id = None
    __name = None
    __salary = None
    __experience = None
    __no_of_courses_assigned = None

    def __init__(self):

        self.__id = None
        self.__name = None
        self.__salary = None
        self.__experience = None
        self.__no_of_courses_assigned = None

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_salary(self):
        return  self.__salary

    def get_experience(self):
        return self.__experience

    def get_count_courses(self):
        return self.__no_of_courses_assigned

    def set_id(self, id):
        self.__id = id

    def set_name(self, name):
        self.__name = name

    def set_salary(self, salary):
        self.__salary = salary

    def set_experience(self, exp):
        self.__experience = exp

    def set_count_courses(self, count_of_courses):
        self.__no_of_courses_assigned = count_of_courses

    def teacher_login(self):
        db_obj = CMSRepository()

        username = None
        while username is None:
            username = input("\nEnter Instructor Username: ")
            if username == "":
                username = None
                print("Username field cannot be empty!!!")

        password = None
        while password is None:
            password = input("Enter Instructor Password: ")
            if password == "":
                password = None
                print("Password field cannot be empty!!!")

        no_of_rows, teacher_data = db_obj.teacher_login_verification(username, password)
        if no_of_rows == 1:
            self.set_id(teacher_data['teacher_id'])
            self.set_name(teacher_data['teacher_name'])
            self.set_salary(teacher_data['teacher_salary'])
            self.set_experience(teacher_data['teacher_experience'])
            self.set_count_courses(teacher_data['teacher_count_course'])
            self.display_teacher_menu()
            return True
        else:
            return False

    # display student menu;
    def display_teacher_menu(self):
        print("************************ Instructor Login ************************")
        isExit = False
        while not isExit:
            isOptionTaken = False
            option = None
            while not isOptionTaken:
                print("Enter 1 to Mark attendance")
                print("Enter 2 to post assignment")
                print("Enter 3 to view Assigned Courses")
                print("Exit\n")
                opt = input("Enter Choice: ")

                if opt == "":
                    print("You cannot left blank this field!!!")
                else:
                    try:
                        option = int(opt)
                    except ValueError as valEr:
                        print("Invalid Value!!!")
                    else:
                        if option < 1 or option > 4:
                            print("Invalid Option!!!"
                                  "\nPlease select an option by pressing 1 to 4 from given menu!!!")
                        else:
                            isOptionTaken = True

            if option == 1:
                self.mark_attendance()
            elif option == 2:
                self.post_assignment()
            elif option == 3:
                self.view_assigned_courses()
            else:
                isExit = True

    def mark_attendance(self):
        db_obj = CMSRepository()
        no_of_courses, courses_data = db_obj.view_teacher_enrolled(self.get_id())

        if no_of_courses != 0:
            print("CourseId         CourseName")
        else:
            print("No course assigned!!!")
        num = 1
        for cr in courses_data:
            course_obj = Course(cr['cr_id'], cr['cr_name'], cr['cr_credit_hours'])
            print(str(course_obj.get_id()).ljust(17, ' '), end="")
            print(str(course_obj.get_name()))
            num = num + 1

        cr_id = None
        cr_id_taken = False
        while not cr_id_taken:
            cr_id_str = input("Enter Course ID of which you want to mark attendance: ")
            try:
                cr_id = int(cr_id_str)
            except ValueError as errorCrId:
                print("Invalid Value!!! \nCourse Id must be an integer!!!")
            else:
                if cr_id < 0:
                    print("Invalid Input!! Id must be greater than equal to 0...")
                elif not db_obj.is_course_enrolled_teacher(cr_id, self.get_id()):
                    print("Course Id not found!!!!")
                else:
                    cr_id_taken = True

        cr_obj = db_obj.course_from_id(cr_id)
        course_obj = Course(cr_obj['cr_id'], cr_obj['cr_name'], cr_obj['cr_credit_hours'])
        no_of_students, student_data = db_obj.get_course_student(course_obj.get_id())
        if no_of_students == 0:
            print("NO student is enrolled in this course!!!!")
            return

        date = None
        dateTaken = False
        while not dateTaken:
            date = input("Enter Attendance Date (YYYY-MM-DD):  ")
            try:
                date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            except Exception as errorDate:
                print("Invalid Attendance Date format!!!\n--->Attendance Date format must be YYYY-MM-DD..")
            else:
                dateTaken = True

        print("Course Name:        " + str(course_obj.get_name()))
        print("Course Date:        " + str(date))

        if no_of_students != 0:
            print("Roll                 Name                  Attendance Status\n")
        for std in student_data:
            status_taken = False
            status = None
            while not status_taken:
                print(str(std['std_roll_no']).ljust(21, ' '), end="")
                print(str(std['std_name']).ljust(22, ' '), end="")
                status = input()
                if status.upper() == "P" or status.upper() == "A":
                    status_taken = True
                else:
                    print("\nInvalid Status!!!\n")

            db_obj.mark_attendance(cr_id, std['std_id'], status, date)

    def post_assignment(self):
        db_obj = CMSRepository()
        no_of_courses, courses_data = db_obj.view_teacher_enrolled(self.get_id())

        if no_of_courses != 0:
            print("CourseId         CourseName")
        else:
            print("No course assigned!!!")
        num = 1
        for cr in courses_data:
            course_obj = Course(cr['cr_id'], cr['cr_name'], cr['cr_credit_hours'])
            print(str(course_obj.get_id()).ljust(17, ' '), end="")
            print(str(course_obj.get_name()))
            num = num + 1

        cr_id = None
        cr_id_taken = False
        while not cr_id_taken:
            cr_id_str = input("Enter Course ID of which you want to post assignment: ")
            try:
                cr_id = int(cr_id_str)
            except ValueError as errorCrId:
                print("Invalid Value!!! \nCourse Id must be an integer!!!")
            else:
                if cr_id < 0:
                    print("Invalid Input!! Id must be greater than equal to 0...")
                elif not db_obj.is_course_enrolled_teacher(cr_id, self.get_id()):
                    print("Course Id not found!!!!")
                else:
                    cr_id_taken = True

        asg_topic = None
        while asg_topic is None:
            asg_topic = input("\nEnter assignment topic: ")
            if asg_topic == "":
                asg_topic = None
                print("Topic field cannot be empty!!!")

        asg_description = input("Enter assignment description: ")

        asg_date = None
        dateTaken = False
        while not dateTaken:
            asg_date = input("Enter assignment submission date (YYYY-MM-DD):  ")
            try:
                asg_date = datetime.datetime.strptime(asg_date, "%Y-%m-%d").date()
            except Exception as errorDate:
                print("Invalid Submission Date format!!!\n--->Submission Date format must be YYYY-MM-DD..")
            else:
                dateTaken = True

        if db_obj.post_assignment(cr_id, asg_topic, asg_date, asg_description):
            print("Assignment Posted!!!")
        else:
            print("Failed!!!\nAssignment is not posted!!!!")

    def view_assigned_courses(self):
        db_obj = CMSRepository()
        no_of_courses, courses_data = db_obj.view_teacher_enrolled(self.get_id())

        print("Total number of assigned courses: " + str(no_of_courses))

        num = 1
        for cr in courses_data:
            course_obj = Course(cr['cr_id'], cr['cr_name'], cr['cr_credit_hours'])
            print(str(num) + ". Course ID = " + str(course_obj.get_id()), end="")
            print("\tCourse Name = " + str(course_obj.get_name()), end="")
            print("\tCredit Hours = " + str(course_obj.get_credit_hours()))
            num = num + 1