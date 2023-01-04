from CMSRepository import CMSRepository
from Student import Student
from Teacher import Teacher
from Course import Course

class Admin:

    def admin_login(self):

        username = None
        while username is None:
            username = input("\nEnter Admin Username: ")
            if username == "":
                username = None
                print("Username field cannot be empty!!!")

        password = None
        while password is None:
            password = input("Enter Admin Password: ")
            if password == "":
                password = None
                print("Password field cannot be empty!!!")

        db_obj = CMSRepository()
        if db_obj.admin_login_verification(username, password):
            self.display_admin_menu()
            return True
        else:
            return False


    def display_admin_menu(self):
        print("************************ Admin Login ************************")
        isExit = False
        while not isExit:
            isOptionTaken = False
            option = None
            while not isOptionTaken:
                print("● Enter 1 to Manage Students\
                        \n● Enter 2 to Manage Teachers \
                        \n● Enter 3 to Manage Courses \
                        \n● Exit\
                        \n ")
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
                self.manage_students()
            elif option == 2:
                self.manage_teacher()
            elif option == 3:
                self.manage_courses()
            else:
                isExit = True

    def manage_students(self):

        isExit = False
        while not isExit:
            isOptionTaken = False
            option = None
            while not isOptionTaken:
                print("● Enter 1 to Add Student \
                        \n● Enter 2 to Update Student \
                        \n● Enter 3 to Delete Student \
                        \n● Enter 4 to View All Students\
                        \n● Enter 5 to Display Outstanding Semester Dues \
                        \n● Enter 6 to Assign Course to Student \
                        \n● Exit \n")
                opt = input("Enter Choice: ")

                if opt == "":
                    print("You cannot left blank this field!!!")
                else:
                    try:
                        option = int(opt)
                    except ValueError as valEr:
                        print("Invalid Value!!!")
                    else:
                        if option < 1 or option > 7:
                            print("Invalid Option!!!"
                                  "\nPlease select an option by pressing 1 to 7 from given menu!!!")
                        else:
                            isOptionTaken = True

            if option == 1:
                std = Student()
                isUsernameTaken = False
                username = None
                db_obj = CMSRepository()
                while not isUsernameTaken:
                    username = input("Enter student's username: ")
                    if username != "" and db_obj.student_username(username):
                        isUsernameTaken = True
                    elif username == "":
                        print("Username cannot be blank!!!!")
                    else:
                        print("Username Already Taken!!!")

                isPasswordTaken = False
                password = None
                while not isPasswordTaken:
                    password = input("Enter student's password: ")
                    if password != "":
                        isPasswordTaken = True

                id = None
                name = input("Enter student's Name: ")
                std.set_name(name)

                roll_Taken = False
                roll_no = None
                while not roll_Taken:
                    roll_no = input("Enter student's Roll No.: ")
                    if roll_no != "" and db_obj.student_roll_no(roll_no):
                        roll_Taken = True
                    elif roll_no == "":
                        print("Roll No cannot be Blank!!!!")
                    else:
                        print("Roll No Already Taken!!!!")


                std.set_roll_no(roll_no)
                batch = input("Enter student's Batch: ")
                std.set_batch(batch)
                semester_dues = None
                dues_taken = False
                while not dues_taken:
                    dues = input("Enter student's dues: ")
                    try:
                        semester_dues = float(dues)
                    except ValueError as errorDues:
                        print("Invalid Value!!! \nDues must be an float or integer!!!")
                    else:
                        if semester_dues < 0:
                            print("Invalid Input!! Dues must be greater than equal to 0...")
                        else:
                            dues_taken = True

                std.set_smester_dues(semester_dues)

                semester_current = None
                currentTaken = False
                while not currentTaken:
                    current_sem = input("Enter student's current semester: ")
                    try:
                        semester_current = int(current_sem)
                    except ValueError as error_current:
                        print("Invalid Value!!! \nSemester must be an integer!!!")
                    else:
                        if 0 >= semester_current or semester_current > 8:
                            print("Invalid Input!! 0 < semester <= 8...")
                        else:
                            currentTaken = True

                std.set_current_semester(semester_current)
                credentials = (username, password)
                db_obj.add_student(credentials, std)

            elif option == 2: # Update:
                db_obj = CMSRepository()
                no_of_std, student_data = db_obj.view_all_students()

                if no_of_std != 0:
                    print("Student-ID           Student Name")
                else:
                    print("No Student Found!!!")

                if no_of_std != 0:
                    for std in student_data:
                        print(str(std['std_id']).ljust(21, ' '), end="")
                        print(str(std['std_name']))

                    id = None
                    id_taken = False
                    while not id_taken:
                        id_str = input("Enter student's id: ")
                        try:
                            id = int(id_str)
                        except ValueError as errorId:
                            print("Invalid Value!!! \nId must be an integer!!!")
                        else:
                            if id < 0 or not db_obj.is_student_id(id):
                                print("Invalid Student Id!!!")
                            else:
                                id_taken = True

                    std = Student()
                    std.set_id(id)
                    isUsernameTaken = False
                    username = None
                    while not isUsernameTaken:
                        username = input("Enter student's new username: ")
                        if username == "" or db_obj.student_username(username):
                            isUsernameTaken = True
                            if username == "":
                                username = None
                        else:
                            print("Username already Taken!!!")

                    password = input("Enter student's new password: ")
                    if password == "":
                        password = None

                    name = input("Enter student's new Name: ")
                    if name == "":
                        name = None
                    std.set_name(name)

                    rolL_Taken = False
                    roll_no = None
                    while not rolL_Taken:
                        roll_no = input("Enter student's new Roll No.: ")
                        if roll_no == "" or db_obj.student_roll_no(roll_no):
                            if roll_no == "":
                                roll_no = None
                            rolL_Taken = True
                        else:
                            print("Roll No Already Taken!!!")

                    std.set_roll_no(roll_no)
                    batch = input("Enter student's new Batch: ")
                    if batch == "":
                        batch = None
                    std.set_batch(batch)

                    semester_dues = None
                    dues_taken = False
                    while not dues_taken:
                        dues = input("Enter student's new dues: ")
                        if dues == "":
                            semester_dues = None
                            dues_taken = True
                            break
                        try:
                            semester_dues = float(dues)
                        except ValueError as errorDues:
                            print("Invalid Value!!! \nDues must be an float or integer!!!")
                        else:
                            if semester_dues < 0:
                                print("Invalid Input!! Dues must be greater than equal to 0...")
                            else:
                                dues_taken = True

                    std.set_smester_dues(semester_dues)


                    semester_current = None
                    currentTaken = False
                    while not currentTaken:
                        current_sem = input("Enter student's new current semester: ")
                        if current_sem == "":
                            semester_current = None
                            currentTaken = True
                            break
                        try:
                            semester_current = int(current_sem)
                        except ValueError as error_current:
                            print("Invalid Value!!! \nSemester must be an integer!!!")
                        else:
                            if 0 >= semester_current or semester_current > 8:
                                print("Invalid Input!! 0 < semester <= 8...")
                            else:
                                currentTaken = True

                    std.set_current_semester(semester_current)
                    credentials = (username, password)
                    db_obj.update_student(credentials, std)
            elif option == 3:
                id = None
                id_taken = False
                while not id_taken:
                    id_str = input("Enter student's id: ")
                    try:
                        id = int(id_str)
                    except ValueError as errorId:
                        print("Invalid Value!!! \nId must be an integer!!!")
                    else:
                        if id < 0:
                            print("Invalid Input!! Id must be greater than equal to 0...")
                        else:
                            id_taken = True

                db_obj = CMSRepository()
                db_obj.delete_student(id)
            elif option == 4:
                db_obj = CMSRepository()
                no_of_students, student_data = db_obj.view_all_students()

                print("Total number of students: " + str(no_of_students))

                for std in student_data:
                    credentials = (std['std_username'], std ['std_password'])
                    stdObj = Student()
                    stdObj.set_id(std['std_id'])
                    stdObj.set_name(std['std_name'])
                    stdObj.set_roll_no(std['std_roll_no'])
                    stdObj.set_batch(std['std_batch'])
                    stdObj.set_smester_dues(std['std_dues'])
                    stdObj.set_current_semester(std['std_semester_no'])
                    print("Username = " + credentials[0])
                    print("Password = " + credentials[1])
                    print("ID = " + str(stdObj.get_id()))
                    print("Name = " + str(stdObj.get_name()))
                    print("Roll No. = " + str(stdObj.get_roll_no()))
                    print("Batch = " + str(stdObj.get_batch()))
                    print("Semester Dues = " + str(stdObj.get_smester_dues()))
                    print("Current Semester = " + str(stdObj.get_current_semester()) + "\n")

            elif option == 5:
                db_obj = CMSRepository()
                no_of_students, student_data = db_obj.outstanding_dues()

                print("Total number of students: " + str(no_of_students))

                for std in student_data:
                    stdObj = Student()
                    stdObj.set_id(std['std_id'])
                    stdObj.set_name(std['std_name'])
                    stdObj.set_roll_no(std['std_roll_no'])
                    stdObj.set_batch(std['std_batch'])
                    stdObj.set_smester_dues(std['std_dues'])
                    stdObj.set_current_semester(std['std_semester_no'])
                    print("ID = " + str(stdObj.get_id()))
                    print("Name = " + str(stdObj.get_name()))
                    print("Roll No. = " + str(stdObj.get_roll_no()))
                    print("Batch = " + str(stdObj.get_batch()))
                    print("Semester Dues = " + str(stdObj.get_smester_dues()))
                    print("Current Semester = " + str(stdObj.get_current_semester()) + "\n")
            elif option == 6:
                db_obj = CMSRepository()
                no_of_std, student_data = db_obj.view_all_students()

                if no_of_std != 0:
                    print("Student-ID           Student Name")
                else:
                    print("No Student Found!!!")
                for std in student_data:
                    print(str(std['std_id']).ljust(21, ' '), end="")
                    print(str(std['std_name']))

                id = None
                cr_id = None
                if no_of_std != 0:
                    print("Press Enter to go back!!!")
                    id_taken = False
                    while not id_taken:
                        id_str = input("Enter student's id: ")
                        if id_str == "":
                            id = None
                            id_taken = True
                            break
                        try:
                            id = int(id_str)
                        except ValueError as errorId:
                            print("Invalid Value!!! \nId must be an integer!!!")
                        else:
                            if id < 0:
                                print("Invalid Input!! Id must be greater than equal to 0...")
                            elif not db_obj.is_student_id(id):
                                print("Student Id not found!!!!")
                            else:
                                id_taken = True

                    no_of_courses = None
                    courses_data = None
                    if id is not None:
                        no_of_courses, courses_data = db_obj.view_all_courses()

                        if no_of_courses != 0:
                            print("CourseId         CourseName")
                        else:
                            print("No course exist!!!")

                        for cr in courses_data:
                            course_obj = Course(cr['cr_id'], cr['cr_name'], cr['cr_credit_hours'])
                            print(str(course_obj.get_id()).ljust(17, ' '), end="")
                            print(str(course_obj.get_name()))

                        if no_of_courses != 0:
                            print("Press Enter to go back!!!")

                        cr_id_taken = False

                        if id is not None and no_of_courses != 0:
                            while not cr_id_taken:
                                cr_id_str = input("Enter course id: ")
                                if cr_id_str == "":
                                    cr_id = None
                                    cr_id_taken = True
                                    break
                                try:
                                    cr_id = int(cr_id_str)
                                except ValueError as errorCrId:
                                    print("Invalid Value!!! \nId must be an integer!!!")
                                else:
                                    if cr_id < 0:
                                        print("Invalid Input!! Id must be greater than equal to 0...")
                                    elif not db_obj.is_new_course_id(cr_id, id):
                                        pass
                                    else:
                                        cr_id_taken = True
                    if id is not None and cr_id is not None:
                        db_obj.assign_course_std(cr_id, id)
                    else:
                        print("Returning Back!!!\n")

            else:
                isExit = True

    def manage_teacher(self):

        isExit = False
        while not isExit:
            isOptionTaken = False
            option = None
            while not isOptionTaken:
                print("● Enter 1 to Add Teacher \
                    \n● Enter 2 to Update Teacher\
                    \n● Enter 3 to Delete Teacher\
                    \n● Enter 4 to View All Teacher\
                    \n● Enter 5 to Assign Course to Teacher\
                    \n● Exit \n")
                opt = input("Enter Choice: ")

                if opt == "":
                    print("You cannot left blank this field!!!")
                else:
                    try:
                        option = int(opt)
                    except ValueError as valEr:
                        print("Invalid Value!!!")
                    else:
                        if option < 1 or option > 6:
                            print("Invalid Option!!!"
                                  "\nPlease select an option by pressing 1 to 6 from given menu!!!")
                        else:
                            isOptionTaken = True


            if option == 1:
                tch = Teacher()
                isUsernameTaken = False
                username = None
                db_obj = CMSRepository()
                while not isUsernameTaken:
                    username = input("Enter teacher's username: ")
                    if username != "" and db_obj.teacher_username(username):
                        isUsernameTaken = True
                    elif username == "":
                        print("Username cannot be blank!!!!")
                    else:
                        print("Username Already Taken!!!")

                isPasswordTaken = False
                password = None
                while not isPasswordTaken:
                    password = input("Enter teacher's password: ")
                    if password != "":
                        isPasswordTaken = True

                id = None
                name = input("Enter teacher's Name: ")
                tch.set_name(name)


                salary = None
                sal_taken = False
                while not sal_taken:
                    sal = input("Enter teacher's salary: ")
                    try:
                        salary = float(sal)
                    except ValueError as errorSal:
                        print("Invalid Value!!! \nSalary must be an integer or float!!!")
                    else:
                        if salary < 0:
                            print("Invalid Input!! Dues must be greater than equal to 0...")
                        else:
                            sal_taken = True
                tch.set_salary(salary)

                experience = None
                exp_taken = False
                while not exp_taken:
                    exp_str = input("Enter teacher's experience(in Years): ")
                    try:
                        experience = float(exp_str)
                    except ValueError as errorExp:
                        print("Invalid Value!!! \nExperience must be an integer or float!!!")
                    else:
                        if experience < 0:
                            print("Invalid Input!! Dues must be greater than equal to 0...")
                        else:
                            exp_taken = True
                tch.set_experience(experience)

                # As in starting number of assigned courses is zero
                tch.set_count_courses(0)

                credentials = (username, password)
                db_obj.add_teacher(credentials, tch)
            elif option == 2:

                db_obj = CMSRepository()
                no_of_tch, teacher_data = db_obj.view_all_teacher()
                if no_of_tch != 0:
                    print("Teacher-ID          Teacher Name")
                else:
                    print("Ops! No teacher found")
                for tch in teacher_data:
                    print(str(tch['teacher_id']).ljust(20, ' '), end="")
                    print(str(tch['teacher_name']) + str("\n"))

                if no_of_tch != 0:
                    print("Press Enter to go back!!!")
                    id = None
                    id_taken = False
                    while not id_taken:
                        id_str = input("Enter teacher's id: ")
                        if id_str == "":
                            id = None
                            id_taken = True
                            break
                        try:
                            id = int(id_str)
                        except ValueError as errorId:
                            print("Invalid Value!!! \nId must be an integer!!!")
                        else:
                            if id < 0:
                                print("Invalid Input!! Id must be greater than equal to 0...")
                            elif not db_obj.is_teacher_id(id):
                                print("Teacher Id not found!!!!")
                            else:
                                id_taken = True
                    if id is not None:
                        tch = Teacher()
                        tch.set_id(id)
                        isUsernameTaken = False
                        username = None
                        db_obj = CMSRepository()
                        while not isUsernameTaken:
                            username = input("Enter teacher's username: ")
                            if username == "" or db_obj.teacher_username(username):
                                isUsernameTaken = True
                                if username == "":
                                    username = None
                            else:
                                print("Username Already Taken!!!")

                        password = input("Enter teacher's password: ")
                        if password == "":
                            password = None

                        id = None
                        name = input("Enter teacher's Name: ")
                        if name == "":
                            name = None
                        tch.set_name(name)

                        salary = None
                        sal_taken = False
                        while not sal_taken:
                            sal = input("Enter teacher's salary: ")
                            if sal == "":
                                sal_taken = True
                                salary = None
                                break

                            try:
                                salary = float(sal)
                            except ValueError as errorSal:
                                print("Invalid Value!!! \nSalary must be an integer or float!!!")
                            else:
                                if salary < 0:
                                    print("Invalid Input!! Dues must be greater than equal to 0...")
                                else:
                                    sal_taken = True
                        tch.set_salary(salary)

                        experience = None
                        exp_taken = False
                        while not exp_taken:
                            exp_str = input("Enter teacher's experience(in Years): ")
                            if exp_str == "":
                                experience = None
                                exp_taken = True
                                break
                            try:
                                experience = float(exp_str)
                            except ValueError as errorExp:
                                print("Invalid Value!!! \nExperience must be an integer or float!!!")
                            else:
                                if experience < 0:
                                    print("Invalid Input!! Dues must be greater than equal to 0...")
                                else:
                                    exp_taken = True
                        tch.set_experience(experience)

                        credentials = (username, password)
                        db_obj.update_teacher(credentials, tch)

            elif option == 3:

                id = None
                id_taken = False
                while not id_taken:
                    id_str = input("Enter teacher's id: ")
                    try:
                        id = int(id_str)
                    except ValueError as errorId:
                        print("Invalid Value!!! \nId must be an integer!!!")
                    else:
                        if id < 0:
                            print("Invalid Input!! Id must be greater than equal to 0...")
                        else:
                            id_taken = True

                db_obj = CMSRepository()
                db_obj.delete_teacher(id)
            elif option == 4:
                db_obj = CMSRepository()
                no_of_teacher, teacher_data = db_obj.view_all_teacher()

                print("Total number of teacher: " + str(no_of_teacher))

                for tch in teacher_data:
                    credentials = (tch['teacher_username'], tch['teacher_password'])
                    teacherObj = Teacher()
                    teacherObj.set_id(tch['teacher_id'])
                    teacherObj.set_name(tch['teacher_name'])
                    teacherObj.set_salary(tch['teacher_salary'])
                    teacherObj.set_experience(tch['teacher_experience'])
                    teacherObj.set_count_courses(tch['teacher_count_course'])
                    print("Username = " + credentials[0])
                    print("Password = " + credentials[1])
                    print("ID = " + str(teacherObj.get_id()))
                    print("Name = " + str(teacherObj.get_name()))
                    print("Salary = " + str(teacherObj.get_salary()))
                    print("Experience = " + str(teacherObj.get_experience()))
                    print("No of courses assigned = " + str(teacherObj.get_count_courses()) + "\n")
            elif option == 5:

                db_obj = CMSRepository()
                no_of_tch, teacher_data = db_obj.view_all_teacher()

                if no_of_tch != 0:
                    print("Teacher-ID          Teacher Name")
                else:
                    print("Ops! No teacher found")
                for tch in teacher_data:
                    print(str(tch['teacher_id']).ljust(20, ' '), end="")
                    print(str(tch['teacher_name']) + str("\n"))

                if no_of_tch != 0:
                    print("Press Enter to go back!!!")
                    id = None
                    id_taken = False
                    while not id_taken:
                        id_str = input("Enter teacher's id: ")
                        if id_str == "":
                            id = None
                            id_taken = True
                            break
                        try:
                            id = int(id_str)
                        except ValueError as errorId:
                            print("Invalid Value!!! \nId must be an integer!!!")
                        else:
                            if id < 0:
                                print("Invalid Input!! Id must be greater than equal to 0...")
                            elif not db_obj.is_teacher_id(id):
                                print("Teacher Id not found!!!!")
                            else:
                                id_taken = True

                    if id is not  None:
                        no_of_courses, courses_data = db_obj.view_all_unassigned_courses()

                        if no_of_courses != 0:
                            print("CourseId         CourseName")
                        else:
                            print("No course exist!!!")

                        for cr in courses_data:
                            course_obj = Course(cr['cr_id'], cr['cr_name'], cr['cr_credit_hours'])
                            print(str(course_obj.get_id()).ljust(17, ' '), end="")
                            print(str(course_obj.get_name()))


                        cr_id = None
                        cr_id_taken = False

                        if id is not None and no_of_courses != 0:
                            print("Press Enter to go back!!!")
                            while not cr_id_taken:
                                cr_id_str = input("Enter course id: ")
                                if cr_id_str == "":
                                    cr_id = None
                                    cr_id_taken = True
                                    break
                                try:
                                    cr_id = int(cr_id_str)
                                except ValueError as errorCrId:
                                    print("Invalid Value!!! \nId must be an integer!!!")
                                else:
                                    if cr_id < 0:
                                        print("Invalid Input!! Id must be greater than equal to 0...")
                                    elif not db_obj.is_new_course_tch(cr_id):
                                        print("Course not found which is unassigned!!!!")
                                    else:
                                        cr_id_taken = True
                        if id is not None and cr_id is not None:
                            db_obj.assign_course_teacher(cr_id, id)
                        else:
                            print("Returning Back!!!\n")
            else:
                isExit = True


    def manage_courses(self):
        isExit = False
        while not isExit:
            isOptionTaken = False
            option = None
            while not isOptionTaken:
                print("● Enter 1 to Add Courses\
                        \n● Enter 2 to Update Courses\
                        \n● Enter 3 to Delete Courses\
                        \n● Enter 4 to View All Courses\
                        \n● Exit\n")
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
                course_obj = Course(None, None, None)
                name = input("Enter Course Name:    ")
                course_obj.set_name(name)

                cr_hour = None
                credit_hour_taken = False
                while not credit_hour_taken:
                    credit_hr = input("Enter Course Credit Hours: ")
                    try:
                        cr_hour = int(credit_hr)
                    except ValueError as errorHours:
                        print("Invalid Value!!! \nCredit Hours must be an integer!!!")
                    else:
                        if cr_hour < 0:
                            print("Invalid Input!! Credit Hours must be greater than equal to 0...")
                        else:
                            credit_hour_taken = True

                course_obj.set_credit_hours(cr_hour)
                db_obj = CMSRepository()
                db_obj.add_course(course_obj)

            elif option == 2:

                db_obj = CMSRepository()
                no_of_courses, courses_data = db_obj.view_all_courses()

                if no_of_courses != 0:
                    print("CourseId         CourseName")
                else:
                    print("No course exist!!!")

                for cr in courses_data:
                    course_obj = Course(cr['cr_id'], cr['cr_name'], cr['cr_credit_hours'])
                    print(str(course_obj.get_id()).ljust(17, ' '), end="")
                    print(str(course_obj.get_name()))

                print("Press Enter to go back!!!")

                cr_id = None
                cr_id_taken = False

                if no_of_courses != 0:
                    while not cr_id_taken:
                        cr_id_str = input("Enter course id: ")
                        if cr_id_str == "":
                            cr_id = None
                            cr_id_taken = True
                            break
                        try:
                            cr_id = int(cr_id_str)
                        except ValueError as errorCrId:
                            print("Invalid Value!!! \nId must be an integer!!!")
                        else:
                            if cr_id < 0:
                                print("Invalid Input!! Id must be greater than equal to 0...")
                            elif not db_obj.is_course_id(cr_id):
                                print("Course Id not found!!!!")
                            else:
                                cr_id_taken = True

                if no_of_courses != 0 and cr_id is not None:
                    course_obj = Course(None, None, None)
                    course_obj.set_id(cr_id)
                    name = input("Enter Course Name:    ")
                    if name == "":
                        name = None
                    course_obj.set_name(name)

                    cr_hour = None
                    credit_hour_taken = False
                    while not credit_hour_taken:
                        credit_hr = input("Enter Course Credit Hours: ")
                        if credit_hr == "":
                            cr_hour = None
                            credit_hour_taken = True
                            break
                        try:
                            cr_hour = int(credit_hr)
                        except ValueError as errorHours:
                            print("Invalid Value!!! \nCredit Hours must be an integer!!!")
                        else:
                            if cr_hour < 0:
                                print("Invalid Input!! Credit Hours must be greater than equal to 0...")
                            else:
                                credit_hour_taken = True

                    course_obj.set_credit_hours(cr_hour)
                    db_obj.update_course(course_obj)

            elif option == 3:
                id = None
                id_taken = False
                while not id_taken:
                    id_str = input("Enter Course ID: ")
                    try:
                        id = int(id_str)
                    except ValueError as errorId:
                        print("Invalid Value!!! \nId must be an integer!!!")
                    else:
                        if id < 0:
                            print("Invalid Input!! Id must be greater than equal to 0...")
                        else:
                            id_taken = True

                db_obj = CMSRepository()
                db_obj.delete_course(id)
            elif option == 4:
                db_obj = CMSRepository()
                no_of_courses, courses_data = db_obj.view_all_courses()

                print("Total number of courses: " + str(no_of_courses))

                if no_of_courses != 0:
                    print("Course-ID         | Course Name         | Credit Hours | Teacher- ID")
                else:
                    print("No course assigned!!!")

                for cr in courses_data:
                    course_obj = Course(cr['cr_id'], cr['cr_name'], cr['cr_credit_hours'])
                    print(str(course_obj.get_id()).ljust(18, ' ') + "| ", end="")
                    print(str(course_obj.get_name()).ljust(20, ' ') + "| ", end="")
                    print(str(course_obj.get_credit_hours()).ljust(13, ' ') + "| ", end="")
                    print(str(cr['teacher_id']))
            else:
                isExit = True