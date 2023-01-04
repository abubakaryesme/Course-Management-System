from Course import Course
from Student import Student
from Teacher import Teacher
from Admin import Admin
from CMSRepository import CMSRepository

def dashboard():
    print("************************ Course Management System ************************")
    db_obj = CMSRepository()
    db_obj.create_tables()
    db_obj.insert_admin()
    isExit = False
    while not isExit:
        isOptionTaken = False
        option = None
        while not isOptionTaken:
            print("Press 1 to Login as Student")
            print("Press 2 to Login as Instructor")
            print("Press 3 to Login as Admin")
            print("Press 4 to Exit\n")
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
            std = Student()
            if std.student_login():
                print("Student logout!!!\n")
            else:
                print("Invalid Credentials!!!\n")
        elif option == 2:
            tch = Teacher()
            if tch.teacher_login():
                print("Teacher logout!!!\n")
            else:
                print("Invalid Credentials!!!\n")
        elif option == 3:
            adm = Admin()
            if adm.admin_login():
                print("Admin logout!!!\n")
            else:
                print("Invalid Credentials!!!\n")
        else:
            isExit = True


dashboard()

