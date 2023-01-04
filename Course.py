
class Course:
    __id = None
    __course_name = None
    __credit_hours = None

    def __init__(self, cid, cname, chours):
        self.__id = cid
        self.__course_name = cname
        self.__credit_hours = chours

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__course_name

    def get_credit_hours(self):
        return self.__credit_hours

    def set_id(self,cid):
        self.__id = cid

    def set_name(self, cname):
        self.__course_name = cname

    def set_credit_hours(self, cr):
        self.__credit_hours = cr
