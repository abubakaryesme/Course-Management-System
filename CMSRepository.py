from numpy import std

from DBPOOL import DBPOOL
# Singleton class:
class CMSRepository(object):
    db_pool = DBPOOL(20)

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __give_connection(self):
        cur = None
        connection = None
        try:
            connection = self.db_pool.get_connection()
            cur = connection.cursor()
        except Exception as ex:
            print("Cannot able to get connection!!!!")
        finally:
            return connection, cur

    def __close_connection(self, connection, cursor):
        cursor.close()
        try:
            self.db_pool.return_connection(connection)
        except Exception as ex:
            print("Cannot able to return connection !!!")

    # Create tables if already not created!!!
    def create_tables(self):
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:

                admin_query = "Create table IF NOT EXISTS Admin (" \
                            "admin_username varchar(30) Primary Key," \
                            "admin_password varchar(20) not null);"

                std_query = "Create table IF NOT EXISTS Student (" \
                            "std_id int(10) AUTO_INCREMENT, std_username varchar(30) unique not null," \
                            "std_password varchar(20) not null, std_name varchar(100)," \
                            "std_roll_no varchar(30) unique not null, " \
                            "std_batch varchar(50), std_dues decimal check (std_dues >= 0), " \
                            "std_semester_no int(10) check (std_semester_no >= 0 or std_semester_no <= 8) ," \
                            "Primary Key(std_id));"

                tch_query = "Create table IF NOT EXISTS Teacher ( teacher_id int(10) AUTO_INCREMENT, " \
                            "teacher_username varchar(30) unique not null, " \
                            "teacher_password varchar(20) not null, " \
                            "teacher_name varchar(100),teacher_salary decimal check (teacher_salary >= 0)," \
                            "teacher_experience decimal check (teacher_experience >= 0)," \
                            "teacher_count_course int(10) Default 0, Primary Key(teacher_id));"

                course_query = "Create table IF NOT EXISTS Course ( cr_id int(10) AUTO_INCREMENT, " \
                               "teacher_id int(10), cr_name varchar(50), cr_credit_hours int(10) not null," \
                               " Primary Key(cr_id), Check (cr_credit_hours >= 0)," \
                               "foreign key(teacher_id) references Teacher (teacher_id) " \
                               "ON DELETE SET NULL ON UPDATE CASCADE);"

                enroll_query = "Create table IF NOT EXISTS enroll (" \
                               "std_id int(10), cr_id int(10), Primary Key(std_id, cr_id), " \
                               "Foreign Key(std_id) references Student (std_id) on delete cascade," \
                               "Foreign Key(cr_id ) references Course(cr_id)  on delete cascade);"

                attendance_query = "Create table IF NOT EXISTS AttendanceInformation ( " \
                                   "atd_id int(10) AUTO_INCREMENT, std_id int(10), cr_id int(10)," \
                                   "atd_status varchar(5) not null, atd_date date not null," \
                                   "Primary Key(atd_id, std_id, cr_id)," \
                                   "Foreign Key(std_id) references Student (std_id) on delete cascade," \
                                   "Foreign Key(cr_id) references Course (cr_id) on delete cascade);"

                assignment_query = "Create table IF NOT EXISTS AssignmentInformation ( " \
                                   "asg_no int(10) AUTO_INCREMENT, " \
                                   "cr_id int(10)," \
                                   "asg_topic varchar(50) not null,asg_description varchar(500)," \
                                   "asg_date date not null, Primary Key(asg_no, cr_id)," \
                                   "Foreign Key (cr_id) references Course (cr_id) on delete cascade);"

                submission_query = "Create table IF NOT EXISTS SubmissionInformation ( " \
                                   "std_id int(10)," \
                                   "asg_no int(10),cr_id int(10)," \
                                   "submission_status  BOOLEAN Default FALSE, Primary Key(std_id, asg_no, cr_id)," \
                                   "Foreign Key (asg_no,cr_id ) references " \
                                   "AssignmentInformation (asg_no,cr_id )  on delete cascade," \
                                   "Foreign Key (std_id) references Student (std_id) on delete cascade);"

                cur.execute(admin_query)
                cur.execute(std_query)
                cur.execute(tch_query)
                cur.execute(course_query)
                cur.execute(enroll_query)
                cur.execute(attendance_query)
                cur.execute(assignment_query)
                cur.execute(submission_query)
                connection.commit()
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
            except Exception as ex:
                print("Ops!! Tables is not created Because : " + str(ex))

    def insert_admin(self):
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query0 = "select * from admin where admin_username = %s "
                args0 = "admin"
                no_of_rows = cur.execute(query0, args0)
                if no_of_rows == 0:
                    query = "insert into admin ( admin_username, admin_password) Values (%s, %s);"

                    args = ("admin", "admin")
                    cur.execute(query, args)
                    connection.commit()

            except Exception as ex:
                pass
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
                    
    # -------------------------- Admin --------------------------------------------
    def admin_login_verification(self, username, password):
        verify = False
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "select * from admin where admin_username = %s and admin_password = %s"
                args = (username, password)
                no_of_rows = cur.execute(query, args)
                if no_of_rows == 1:
                    verify =True
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
            except Exception as ex:
                print("Ops!! Cannot able to verify Because : " + str(ex))
        finally:
            return verify

    def add_student(self, credentials, std):
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "insert into Student ( std_username, std_password, std_name, std_roll_no," \
                        "std_batch, std_dues, std_semester_no) Values (%s, %s, %s," \
                        "%s, %s, %s, %s);"

                args = (credentials[0], credentials[1], std.get_name(), std.get_roll_no(),
                        std.get_batch(), std.get_smester_dues(), std.get_current_semester())
                cur.execute(query, args)
                connection.commit()

            except Exception as ex:
                print("Error!!!\n Record is not inserted into student table.")
            else:
                print("Record inserted successfully into student table")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")

    def is_student_id(self, id):
        verify = False
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "select * from student where std_id= %s"
                args = id
                no_of_rows = cur.execute(query, args)
                if no_of_rows == 1:
                    verify = True
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
            except Exception as ex:
                print("Ops!! Cannot able to verify Because : " + str(ex))
        finally:
            return verify

    def student_username(self, username):
        verify = False
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "select * from student where std_username = %s"
                args = username
                no_of_rows = cur.execute(query, args)
                if no_of_rows == 0:
                    verify = True
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
            except Exception as ex:
                print("Ops!! Cannot able to verify Because : " + str(ex))
        finally:
            return verify

    def student_roll_no(self, roll_no):
        verify = False
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "select * from student where std_roll_no = %s"
                args = roll_no
                no_of_rows = cur.execute(query, args)
                if no_of_rows == 0:
                    verify = True
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
            except Exception as ex:
                print("Ops!! Cannot able to verify Because : " + str(ex))
        finally:
            return verify

    def update_student(self,credentials, std):
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query1 = "select * from student where std_id = %s"
                args1 = std.get_id()
                cur.execute(query1, args1)
                std_data = cur.fetchone()
                passwrd = None
                if credentials[0] is not None:
                    query0 = "Update student set std_username = %s where std_id = %s"
                    args0 = (credentials[0], std.get_id())
                    cur.execute(query0, args0)
                    connection.commit()
                if credentials[1] is None:
                    passwrd = std_data['std_password']
                else:
                    passwrd = credentials[1]
                if std.get_name() is None:
                    std.set_name(std_data['std_name'])
                if std.get_roll_no() is not None:
                    query0 = "Update student set std_roll_no = %s where std_id = %s"
                    args0 = (std.get_roll_no(), std.get_id())
                    cur.execute(query0, args0)
                    connection.commit()
                if std.get_batch() is None:
                    std.set_batch(std_data['std_batch'])
                if std.get_smester_dues() is None:
                    std.set_smester_dues(std_data['std_dues'])
                if std.get_current_semester() is None:
                    std.set_current_semester(std_data['std_semester_no'])
                query2 = "Update student set  std_password=%s, std_name = %s, " \
                         "std_batch = %s, std_dues =%s, std_semester_no = %s  where std_id = %s"
                args2 = (passwrd, std.get_name(), std.get_batch(), std.get_smester_dues(),
                         std.get_current_semester(), std.get_id())
                cur.execute(query2, args2)
                connection.commit()
            except Exception as ex:
                print("Error!!!\nStudent Record is not updated.")
            else:
                print("Student Record updated successfully!!!")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")

    def delete_student(self, id):
        try:
            connection, cur = self.__give_connection()
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query1 = "Select * from student where std_id = %s"
                args1 = id
                cur.execute(query1, args1)
                std_data = cur.fetchone()
                if std_data is None:
                    print("Invalid Student ID!!!\nStudent is not found!!!\n")
                else:
                    query2 = "Delete from student where std_id = %s"
                    args2 = id
                    cur.execute(query2, args2)
                    connection.commit()

            except Exception as ex:
                print("Error!!!\n Record is not deleted from student table.")
            else:
                if std_data is not None:
                    print("Record deleted successfully from student table")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")


    def view_all_students(self):
        no_of_rows = None
        std_data = None
        try:
            connection, cur = self.__give_connection()
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "Select * from Student;"
                no_of_rows = cur.execute(query)
                std_data = cur.fetchall()

            except Exception as ex:
                print("Error!!!\n--->Student record cannot be fetched.")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
        finally:
            return no_of_rows, std_data


    def outstanding_dues(self):
        no_of_rows = None
        std_data = None
        try:
            connection, cur = self.__give_connection()
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "Select * from Student where  std_dues > 0;"
                no_of_rows = cur.execute(query)
                std_data = cur.fetchall()

            except Exception as ex:
                print("Error!!!\n--->Student record cannot be fetched.")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
        finally:
            return no_of_rows, std_data

    def assign_course_std(self, cr_id, std_id):
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "insert into enroll ( std_id, cr_id) Values (%s, %s);"
                args = (std_id, cr_id)
                cur.execute(query, args)
                connection.commit()

            except Exception as ex:
                print("Error!!!\nCourse has not been assigned to student.")
            else:
                print("Course has been successfully assigned to student!!!")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")

    def is_new_course_id(self, cr_id, std_id):
        verify = False
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "select * from course where cr_id= %s"
                args = cr_id
                no_of_rows1 = cur.execute(query, args)
                if no_of_rows1 == 1:
                    query = "select * from enroll where cr_id = %s and std_id = %s"
                    args = (cr_id, std_id)
                    no_of_rows = cur.execute(query, args)
                    if no_of_rows == 0:
                        verify = True
                    else:
                        print("You have already enrolled this course!!!")
                else:
                    print("Invalid Course ID!!!")
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
            except Exception as ex:
                print("Ops!! Cannot able to verify Because : " + str(ex))
        finally:
            return verify

    def is_new_course_tch(self, cr_id):
        verify = False
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "select * from course where cr_id= %s and teacher_id is NULL"
                args = cr_id
                no_of_rows = cur.execute(query, args)
                if no_of_rows > 0:
                    verify = True
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
            except Exception as ex:
                print("Ops!! Cannot able to verify Because : " + str(ex))
        finally:
            return verify


    def is_course_id(self, id):
        verify = False
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "select * from course where cr_id= %s"
                args = id
                no_of_rows = cur.execute(query, args)
                if no_of_rows == 1:
                    verify = True
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
            except Exception as ex:
                print("Ops!! Cannot able to verify Because : " + str(ex))
        finally:
            return verify

    # ---------------------------------------------------------
    def add_teacher(self, credentials, tch):
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "insert into Teacher ( teacher_username, teacher_password, " \
                        "teacher_name, teacher_salary, teacher_experience," \
                        "teacher_count_course) Values (%s, %s, %s, %s, %s, %s);"

                args = (credentials[0], credentials[1], tch.get_name(), tch.get_salary(),
                        tch.get_experience(), tch.get_count_courses())
                cur.execute(query, args)
                connection.commit()

            except Exception as ex:
                print("Error!!!\n Record is not inserted into teacher table.")
            else:
                print("Record inserted successfully into teacher table")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")

    def teacher_username(self, username):
        verify = False
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "select * from teacher where teacher_username = %s"
                args = username
                no_of_rows = cur.execute(query, args)
                if no_of_rows == 0:
                    verify = True
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
            except Exception as ex:
                print("Ops!! Cannot able to verify Because : " + str(ex))
        finally:
            return verify

    def update_teacher(self, credentials, tch):
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:

                query1 = "select * from teacher where teacher_id = %s"
                args1 = tch.get_id()
                cur.execute(query1, args1)
                tch_data = cur.fetchone()
                passwrd = None
                if credentials[0] is not None:
                    query0 = "Update teacher set teacher_username = %s where teacher_id = %s"
                    args0 = (credentials[0], tch.get_id())
                    cur.execute(query0, args0)
                    connection.commit()

                if credentials[1] is None:
                    passwrd = tch_data['teacher_password']
                else:
                    passwrd = credentials[1]
                if tch.get_name() is None:
                    tch.set_name(tch_data['teacher_name'])
                if tch.get_salary() is None:
                    tch.set_salary(tch_data['teacher_salary'])
                if tch.get_experience() is None:
                    tch.set_experience(tch_data['teacher_experience'])

                tch.set_count_courses(tch_data['teacher_count_course'])
                query2 = "Update teacher set teacher_password=%s," \
                         "teacher_name = %s, teacher_salary = %s, teacher_experience = %s," \
                         "teacher_count_course = %s where teacher_id = %s"

                args2 = (passwrd, tch.get_name(), tch.get_salary(), tch.get_experience(),
                         tch.get_count_courses(), tch.get_id())
                cur.execute(query2, args2)
                connection.commit()

            except Exception as ex:
                print("Error!!!\nTeacher Record is not updated.")
            else:
                print("Teacher Record updated successfully!!!")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")

    def delete_teacher(self, id):
        try:
            connection, cur = self.__give_connection()
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query1 = "Select * from Teacher where teacher_id = %s"
                args1 = id
                cur.execute(query1, args1)
                tch_data = cur.fetchone()
                if tch_data is None:
                    print("Invalid Teacher ID!!!\nTeacher is not found!!!\n")
                else:
                    query2 = "Delete from Teacher where teacher_id = %s"
                    args2 = id
                    cur.execute(query2, args2)
                    connection.commit()

            except Exception as ex:
                print("Error!!!\nRecord is not deleted from teacher table.")
            else:
                if tch_data is not None:
                    print("Record deleted successfully from teacher table")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")

    def view_all_teacher(self):
        no_of_rows = None
        tch_data = None
        try:
            connection, cur = self.__give_connection()
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "Select * from Teacher;"
                no_of_rows = cur.execute(query)
                tch_data = cur.fetchall()

            except Exception as ex:
                print("Error!!!\n--->Teacher record cannot be fetched.")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
        finally:
            return no_of_rows, tch_data

    def assign_course_teacher(self, cr_id, tch_id):
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "update course set teacher_id = %s where cr_id = %s;"
                args = (tch_id, cr_id)
                cur.execute(query, args)
                connection.commit()

                query2 = "update teacher set teacher_count_course = teacher_count_course + 1 " \
                         "where teacher_id = %s"
                cur.execute(query2, tch_id)
                connection.commit()

            except Exception as ex:
                print("Error!!!\nCourse has not assigned to teacher.")
            else:
                print("Course has been successfully assigned to teacher!!!")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")

    def is_teacher_id(self, id):
        verify = False
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "select * from teacher where teacher_id= %s"
                args = id
                no_of_rows = cur.execute(query, args)
                if no_of_rows == 1:
                    verify = True
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
            except Exception as ex:
                print("Ops!! Cannot able to verify Because : " + str(ex))
        finally:
            return verify

    # -----------------------------------------------------
    def add_course(self, course_obj):
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:

                query = "insert into Course ( cr_name, cr_credit_hours) Values (%s, %s);"
                args = (course_obj.get_name(), course_obj.get_credit_hours())
                cur.execute(query, args)
                connection.commit()

            except Exception as ex:
                print("Error!!!\nCourse is not Added.")
            else:
                print("Course successfully added!!!")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")

    def update_course(self, course_obj):
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query1 = "select * from course where cr_id = %s"
                args1 = course_obj.get_id()
                cur.execute(query1, args1)
                cr_data = cur.fetchone()

                if course_obj.get_name() is None:
                    course_obj.set_name(cr_data['cr_name'])
                if course_obj.get_credit_hours() is None:
                    course_obj.set_credit_hours(cr_data['cr_credit_hours'])

                query2 = "Update course set cr_name = %s, cr_credit_hours = %s where cr_id = %s"
                args2 = (course_obj.get_name(), course_obj.get_credit_hours(), course_obj.get_id())
                cur.execute(query2, args2)
                connection.commit()

            except Exception as ex:
                print("Error!!!\nCourse Record is not updated.")
            else:
                print("Course Record updated successfully!!!")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")

    def delete_course(self, course_id):
        try:
            connection, cur = self.__give_connection()
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query1 = "Select * from course where cr_id = %s"
                args1 = course_id
                cur.execute(query1, args1)
                cr_data = cur.fetchone()
                if cr_data is None:
                    print("Invalid Course ID!!!\nCourse is not found!!!\n")
                else:
                    query2 = "Delete from Course where cr_id = %s"
                    args2 = course_id
                    cur.execute(query2, args2)
                    connection.commit()

            except Exception as ex:
                print("Error!!!\nRecord is not deleted from course table.")
            else:
                if cr_data is not None:
                    print("Record deleted successfully from course table")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")

    def view_all_unassigned_courses(self):
        no_of_rows = None
        cr_data = None
        try:
            connection, cur = self.__give_connection()
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "Select * from course where teacher_id is NULL;"
                no_of_rows = cur.execute(query)
                cr_data = cur.fetchall()

            except Exception as ex:
                print("Error!!!\n--->Course record cannot be fetched.")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
        finally:
            return no_of_rows, cr_data

    def view_all_courses(self):
        no_of_rows = None
        cr_data = None
        try:
            connection, cur = self.__give_connection()
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "Select * from course;"
                no_of_rows = cur.execute(query)
                cr_data = cur.fetchall()

            except Exception as ex:
                print("Error!!!\n--->Course record cannot be fetched.")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
        finally:
            return no_of_rows, cr_data

    # --------------------------------- Student ----------------------------

    def student_login_verification(self, username, password):
        no_of_rows = None
        std_data = None
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "select * from student where std_username = %s and std_password = %s"
                args = (username, password)
                no_of_rows = cur.execute(query, args)
                if no_of_rows == 1:
                    std_data = cur.fetchone()
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
            except Exception as ex:
                print("Ops!! Cannot able to verify Because : " + str(ex))
        finally:
            return no_of_rows, std_data

    def update_dues(self, id, new_dues):
        is_done = False
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:

                query2 = "Update student set std_dues =%s where std_id = %s"
                args2 = (new_dues, id)
                cur.execute(query2, args2)
                connection.commit()
                is_done = True

            except Exception as ex:
                print("Error!!!\nStudent Dues is not updated.")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
        finally:
            return is_done

    def view_student_enrolled(self, id):
        no_of_rows = None
        cr_data = None
        try:
            connection, cur = self.__give_connection()
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "Select c.* from course c, enroll e where c.cr_id = e.cr_id and e.std_id = %s;"
                args = id
                no_of_rows = cur.execute(query, args)
                cr_data = cur.fetchall()

            except Exception as ex:
                print("Error!!!\n--->Course record cannot be fetched.")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
        finally:
            return no_of_rows, cr_data

    def view_assignments_student(self,cr_id, std_id):
        no_of_rows = None
        asg_data = None
        try:
            connection, cur = self.__give_connection()
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "Select distinct ai.* from AssignmentInformation ai, SubmissionInformation si " \
                        "where si.cr_id = ai.cr_id  and si.asg_no = ai.asg_no " \
                        "and sysdate() <= ai.asg_date and si.submission_status = FALSE and " \
                        "si.std_id = %s and si.cr_id = %s;"
                args = (std_id, cr_id)
                no_of_rows = cur.execute(query, args)
                asg_data = cur.fetchall()

            except Exception as ex:
                print("Error!!!\n--->Assignment record cannot be fetched.")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
        finally:
            return no_of_rows, asg_data

    def is_course_enrolled_id(self, cr_id, std_id):
        verify = False
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "select * from enroll where cr_id= %s and std_id = %s"
                args = (cr_id, std_id)
                no_of_rows = cur.execute(query, args)
                if no_of_rows == 1:
                    verify = True
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
            except Exception as ex:
                print("Ops!! Cannot able to verify Because : " + str(ex))
        finally:
            return verify

    def status_update(self, std_id, asg_id, cr_id):
        is_done = False
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:

                query2 = "Update SubmissionInformation set submission_status = TRUE " \
                         " where std_id = %s and asg_no = %s and cr_id = %s"
                args2 = (std_id, asg_id, cr_id)
                cur.execute(query2, args2)
                connection.commit()
                is_done = True
            except Exception as ex:
                print("Error!!!\nStudent Dues is not updated.")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
        finally:
            return is_done

    # --------------------------------- teacher ----------------------------

    def teacher_login_verification(self, username, password):
        no_of_rows = None
        tch_data = None
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "select * from teacher where teacher_username = %s and teacher_password = %s"
                args = (username, password)
                no_of_rows = cur.execute(query, args)
                if no_of_rows == 1:
                    tch_data = cur.fetchone()
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
            except Exception as ex:
                print("Ops!! Cannot able to verify Because : " + str(ex))
        finally:
            return no_of_rows, tch_data

    def view_teacher_enrolled(self, id):
        no_of_rows = None
        cr_data = None
        try:
            connection, cur = self.__give_connection()
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "Select * from course where teacher_id = %s;"
                args = id
                no_of_rows = cur.execute(query, args)
                cr_data = cur.fetchall()

            except Exception as ex:
                print("Error!!!\n--->Course record cannot be fetched.")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
        finally:
            return no_of_rows, cr_data

    def is_course_enrolled_teacher(self, cr_id, tch_id):
        verify = False
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "select * from course where cr_id= %s and teacher_id = %s"
                args = (cr_id, tch_id)
                no_of_rows = cur.execute(query, args)
                if no_of_rows == 1:
                    verify = True
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
            except Exception as ex:
                print("Ops!! Cannot able to verify Because : " + str(ex))
        finally:
            return verify

    def course_from_id(self, id):
        cr_data = None
        try:
            connection, cur = self.__give_connection()
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "Select * from course where cr_id = %s;"
                args = id
                cur.execute(query, args)
                cr_data = cur.fetchone()

            except Exception as ex:
                print("Error!!!\n--->Assignment record cannot be fetched.")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")

        finally:
            return cr_data

    def mark_attendance(self, crs_id, std_id, status, date_atd):
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "insert into AttendanceInformation ( std_id, cr_id, " \
                        "atd_status, atd_date) Values (%s, %s, %s, %s);"

                args = (std_id, crs_id, status, date_atd)
                cur.execute(query, args)
                connection.commit()

            except Exception as ex:
                print("Error!!!\n Record is not inserted into teacher table.")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")

    def get_course_student(self, cr_id):
        no_of_rows = None
        std_data = None
        try:
            connection, cur = self.__give_connection()
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                query = "Select s.* from Student s, enroll e where " \
                        "s.std_id = e.std_id and e.cr_id = %s;"
                args = cr_id
                no_of_rows = cur.execute(query, args)
                std_data = cur.fetchall()

            except Exception as ex:
                print("Error!!!\n--->Student record cannot be fetched.")
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")
        finally:
            return no_of_rows, std_data

    def __get_assignment_no(self):
        try:
            connection, cur = self.__give_connection()
            query = "select max(asg_no) as maxId from AssignmentInformation;"
            cur.execute(query)
            id = cur.fetchone()
            self.__close_connection(connection, cur)
            if not (id['maxId'] is None):
                return id['maxId'] + 1
            else:
                return 1
        except Exception as ex:
            return -1

    def post_assignment(self, cr_id, topic, sub_date, description):
        status = False
        try:
            connection, cur = self.__give_connection()
            if connection is None:
                return
        except Exception as ex:
            print("Error !!\nConnection Failed!!!")
        else:
            try:
                asg_no = self.__get_assignment_no()
                if asg_no != -1:
                    query = "insert into AssignmentInformation (asg_no, cr_id, asg_topic, asg_description," \
                            "asg_date) Values (%s, %s, %s, %s, %s);"

                    args = (asg_no, cr_id, topic, description, sub_date)
                    cur.execute(query, args)
                    connection.commit()
                    try:
                        no_of_students, student_data = self.get_course_student(cr_id)
                        for std in student_data:
                            query2 = "insert into SubmissionInformation ( std_id, asg_no, " \
                                     "cr_id) Values (%s, %s, %s);"
                            args2 = (std['std_id'], asg_no, cr_id)
                            cur.execute(query2, args2)
                            connection.commit()
                        status = True
                    except Exception as ex2:
                        query3 = "Delete from AssignmentInformation where asg_no = %s"
                        args3 = asg_no
                        cur.execute(query3, args3)
                        connection.commit()
                        status = False
                else:
                    status = False

            except Exception as ex:
                status = False
            finally:
                try:
                    self.__close_connection(connection, cur)
                except Exception as closeEr:
                    print("Error !\nConnection is not closed!!")

        finally:
            return status

