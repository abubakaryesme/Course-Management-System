import pymysql

class DBPOOL:

    __connection_pool = []
    __no_of_connections = None
    __rear = None
    __front = None
    __available_connections = None


    def __create_connection(self):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='1234',
                                     database='cms',
                                     cursorclass=pymysql.cursors.DictCursor)

        return connection

    def __closeConnection(self, connection):
        connection.close()

    def __init__(self, count_connections):
        self.__no_of_connections = self.__available_connections = count_connections
        self.__rear = self.__front = 0

        for connection_num in range(self.__no_of_connections):
            self.__connection_pool.append(self.__create_connection())

    def get_connection(self):
        if self.__no_of_connections == 0:
            raise Exception("Error!!!\nNo connection is established!!!")
        elif self.__front < self.__available_connections:
            self.__front = (self.__front + 1) % self.__no_of_connections
            self.__available_connections = self.__available_connections - 1
            return self.__connection_pool[self.__front]

    def return_connection(self, connection):
        if self.__available_connections == self.__no_of_connections:
            raise Exception("Limit Exceeds\nDB POOL is full!!!")
        self.__connection_pool[self.__rear] = connection
        self.__rear = (self.__rear + 1) % self.__no_of_connections
        self.__available_connections = self.__available_connections + 1
