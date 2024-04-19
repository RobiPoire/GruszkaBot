from sqlite3 import connect as sql_connect


class DiscordServer:
    __db_file_path = "./database/sqlite_db.db"
    __table_name = "discordserver"
    __cursor = sql_connect(__db_file_path).cursor()

    def __init__(self, server_id: int) -> None:
        """
        Searches for a discord server in the database by server_id.
        If the server is found, initializes the discord server object with the server_id.
        Otherwise, creates a new discord server in the database.
        :param server_id:
        """
        self.__cursor.execute(f"select * from {self.__table_name} "
                              "where server_id = ?;", (server_id,))
        row = self.__cursor.fetchone()
        if row is None:
            self.new(server_id)
        self.__server_id = server_id
        self.__logs_channel_id = row[1] if row is not None else None
        self.__join_channel_id = row[2] if row is not None else None

    def __str__(self) -> str:
        """
        Returns the string representation of the discord server.
        :return:
        """
        return f"ID: {self.__server_id} |Logs: {self.__logs_channel_id} | Join: {self.__join_channel_id}"

    @classmethod
    def create_table(cls) -> None:
        """
        Creates the table in the database.
        :return:
        """
        cls.__cursor.execute(f"create table if not exists {cls.__table_name} ("
                             "server_id INTEGER not null constraint server_id_primary primary key,"
                             "logs_channel_id INTEGER,"
                             "join_channel_id INTEGER);")
        cls.__cursor.connection.commit()

    @classmethod
    def new(cls, server_id: int) -> 'DiscordServer':
        """
        Creates a new discord server in the database.
        :param server_id:
        :return:
        """
        cls.__cursor.execute(f"insert or ignore into {cls.__table_name}"
                             "(server_id) values (?);", (server_id,))
        cls.__cursor.connection.commit()
        return cls(server_id)

    @classmethod
    def get_all(cls) -> list['DiscordServer']:
        """
        Retrieves a list of all discord servers from the database.
        :return:
        """
        cls.__cursor.execute(f"select * from {cls.__table_name};")
        return [cls(row[0]) for row in cls.__cursor.fetchall()]

    @classmethod
    def get_all_id(cls) -> list[int]:
        """
        Retrieves a list of all discord server ids from the database.
        :return:
        """
        cls.__cursor.execute(f"select server_id from {cls.__table_name};")
        return [row[0] for row in cls.__cursor.fetchall()]

    def get_id(self) -> int:
        return self.__server_id

    def get_logs_channel_id(self) -> int:
        return self.__logs_channel_id

    def get_join_channel_id(self) -> int:
        return self.__join_channel_id

    def set_logs_channel_id(self, logs_channel_id: int) -> None:
        self.__cursor.execute(f"update {self.__table_name} "
                              "set logs_channel_id = ? "
                              "where server_id = ?;", (logs_channel_id, self.__server_id))
        self.__cursor.connection.commit()
        self.__logs_channel_id = logs_channel_id

    def set_join_channel_id(self, join_channel_id: int) -> None:
        self.__cursor.execute(f"update {self.__table_name} "
                              "set join_channel_id = ? "
                              "where server_id = ?;", (join_channel_id, self.__server_id))
        self.__cursor.connection.commit()
        self.__join_channel_id = join_channel_id

    def delete(self) -> None:
        """
        Deletes the discord server from the database.
        :return:
        """
        self.__cursor.execute(f"delete from {self.__table_name} where server_id = ?;", (self.__server_id,))
        self.__cursor.connection.commit()
        del self.__server_id
        del self.__logs_channel_id
        del self.__join_channel_id
