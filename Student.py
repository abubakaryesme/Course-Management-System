import pymysql
from CMSRepository import CMSRepository
from Course import Course

class Student:
    __id = None
    __name = None
    __roll_no = None
    __batch = None
    __smester_dues = None
    __current_semester = None

    def __init__(self):
        self.__id = None
        self.__name = None
        self.__roll_no = None
        self.__batch = None
        self.__smester_dues = None
        self.__current_semester = None

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_roll_no(self):
        return self.__roll_no

    def set_roll_no(self, roll_no):
        self.__roll_no = roll_no

    def get_batch(self):
        return self.__batch

    def set_batch(self, batch):
        self.__batch = batch

    def get_smester_dues(self):
        return self.__smester_dues

    def set_smester_dues(self, dues):
        self.__smester_dues = dues

    def get_current_semester(self):
        return self.__current_semester

    def set_current_semester(self, semetser):
        self.__current_semester = semetser

    # display student menu;
    def display_student_menu(self):
        print("************************ Student Login ************************")
        isExit = False
        while not isExit:
            isOptionTaken = False
            option = None
            while not isOptionTaken:
                print("Enter 1 to Pay Semester Dues")
                print("Enter 2 to view enrolled courses")
                print("Enter 3 to submit assignment")
                print("Enter 4 to view assignment")
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
                        if option < 1 or option > 5:
                            print("Invalid Option!!!"
                                  "\nPlease select an option by pressing 1 to 5 from given menu!!!")
                        else:
                            isOptionTaken = True

            if option == 1:
                self.pay_semester_dues()
            elif option == 2:
                self.view_courses_enrolled()
            elif option == 3:
                self.change_status()
            elif option == 4:
                self.view_assignment()
            else:
                isExit = True

    def change_status(self):
        db_obj = CMSRepository()
        no_of_courses, courses_data = db_obj.view_student_enrolled(self.get_id())

        if no_of_courses != 0:
            print("Course-ID         Course Name")
        else:
            print("No course assigned!!!")
        for cr in courses_data:
            course_obj = Course(cr['cr_id'], cr['cr_name'], cr['cr_credit_hours'])
            print(str(course_obj.get_id()).ljust(18, ' '), end="")
            print(str(course_obj.get_name()))

        if no_of_courses != 0:
            cr_id = None
            cr_id_taken = False

            while not cr_id_taken:
                cr_id_str = input("Enter course id: ")
                try:
                    cr_id = int(cr_id_str)
                except ValueError as errorCrId:
                    print("Invalid Value!!! \nId must be an integer!!!")
                else:
                    if cr_id < 0:
                        print("Invalid Input!! Id must be greater than equal to 0...")
                    elif not db_obj.is_course_enrolled_id(cr_id, self.get_id()):
                        print("Course Id not found!!!!")
                    else:
                        cr_id_taken = True

            db_obj = CMSRepository()
            pending_assignments, assignment_data = db_obj.view_assignments_student(cr_id ,self.get_id())

            print("Total number of pending assignments: " + str(pending_assignments))

            if pending_assignments != 0:
                print("No. | Topic               | Submission Date | Status ")
                num = 1
                asg_dict = dict()
                for assign_detail in assignment_data:
                    print(str(num).ljust(4, ' ') + "| ",end="")
                    print(str(assign_detail['asg_topic']).ljust(20, ' ') + "| ", end="")
                    print(str(assign_detail['asg_date']).ljust(16, ' ') + "| ", end="")
                    print("False")
                    asg_dict[num] = assign_detail['asg_no']
                    num = num + 1

                assignment_num = None
                asg_id = None
                asg_Taken = False
                while not asg_Taken and pending_assignments != 0:
                    asgStr = input("Enter : ")
                    try:
                        assignment_num = int(asgStr)
                    except ValueError as errorAsg:
                        print("Invalid Value!!! \nAssignment number must be an integer!!!")
                    else:
                        if assignment_num < 1 or assignment_num >= num:
                            print("Invalid Input!! Assignment number must be in range (1-"+str(num-1)+") inclusive..")
                        else:
                            asg_id = asg_dict[assignment_num]
                            asg_Taken = True

                if db_obj.status_update(self.get_id(), asg_id, cr_id):
                    print("Assignment Submission Status has been successfully updated!!!\n")

    #Pay Semester Dues:
    def pay_semester_dues(self):
        db_obj = CMSRepository()
        if self.get_smester_dues() != 0:
            amount = None
            amountTaken = False
            while not amountTaken:
                duesStr = input("Enter amount to Pay : Rs. ")
                try:
                    amount = float(duesStr)
                except ValueError as errorAge:
                    print("Invalid Value!!! \nSemester Dues must be an float or integer!!!")
                else:
                    if amount < 0 or amount > self.get_smester_dues():
                        print("Invalid Input!! Semester Dues must be greater than 0 and "
                              "less than equal to "+str(self.get_smester_dues())+"...\n")
                    else:
                        amountTaken = True
            old_dues = self.get_smester_dues()
            new_dues = float(old_dues) - amount
            if db_obj.update_dues(self.get_id(), new_dues):
                self.set_smester_dues(new_dues)
                print("Your remaining Dues are: Rs."+str(new_dues)+"")
        else:
            print("You have already paid your semester dues. Thanks!!!")

    # View courses in which he/she enrolled:
    def view_courses_enrolled(self):
        db_obj = CMSRepository()
        no_of_courses, courses_data = db_obj.view_student_enrolled(self.get_id())

        print("Total number of courses enrolled: " + str(no_of_courses))

        if no_of_courses != 0:
            print("Course-ID         Course Name            Credit Hours")
        else:
            print("Ops! You have not enrolled any course!!!")
        for cr in courses_data:
            course_obj = Course(cr['cr_id'], cr['cr_name'], cr['cr_credit_hours'])
            print(str(course_obj.get_id()).ljust(18, ' '), end="")
            print(str(course_obj.get_name()).ljust(23, ' '), end="")
            print(str(course_obj.get_credit_hours()))

    # To View to assignment of particular course in which he/she enrolled:
    def view_assignment(self):
        db_obj = CMSRepository()

        no_of_courses, courses_data = db_obj.view_student_enrolled(self.get_id())

        if no_of_courses != 0:
            print("Course-ID         Course Name")
        else:
            print("No course assigned!!!")
        for cr in courses_data:
            course_obj = Course(cr['cr_id'], cr['cr_name'], cr['cr_credit_hours'])
            print(str(course_obj.get_id()).ljust(18, ' '), end="")
            print(str(course_obj.get_name()))

        if no_of_courses != 0:
            cr_id = None
            cr_id_taken = False

            while not cr_id_taken:
                cr_id_str = input("Enter course id: ")
                try:
                    cr_id = int(cr_id_str)
                except ValueError as errorCrId:
                    print("Invalid Value!!! \nId must be an integer!!!")
                else:
                    if cr_id < 0:
                        print("Invalid Input!! Id must be greater than equal to 0...")
                    elif not db_obj.is_course_enrolled_id(cr_id, self.get_id()):
                        print("Course Id not found!!!!")
                    else:
                        cr_id_taken = True

            no_of_asg, assignment_data = db_obj.view_assignments_student(cr_id, self.get_id())
            print("Total number of pending assignments: " + str(no_of_asg))
            num = 1
            for assign_detail in assignment_data:
                print("Assignment # " + str(num))
                print("Assignment Topic: = " + str(assign_detail['asg_topic']))
                print("Assignment Description = " + str(assign_detail['asg_description']))
                print("Assignment Submission Date = " + str(assign_detail['asg_date']))
                print("Status = " + "False\n")
                num = num + 1

    # Student login:
    def student_login(self):
        db_obj = CMSRepository()

        username = None
        while username is None:
            username = input("\nEnter Student Username: ")
            if username == "":
                username = None
                print("Username field cannot be empty!!!")

        password = None
        while password is None:
            password = input("Enter Student Password: ")
            if password == "":
                password = None
                print("Password field cannot be empty!!!")

        no_of_rows, student_data = db_obj.student_login_verification(username,password)
        if no_of_rows == 1:
            self.set_id(student_data['std_id'])
            self.set_name(student_data['std_name'])
            self.set_roll_no(student_data['std_roll_no'])
            self.set_batch(student_data['std_batch'])
            self.set_smester_dues(student_data['std_dues'])
            self.set_current_semester(student_data['std_semester_no'])
            self.display_student_menu()
            return True
        else:
            return False
