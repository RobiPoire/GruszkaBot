from sqlite3 import connect as sql_connect


class DiscordUser:
    __db_file_path = "./database/sqlite_db.db"
    __table_name = "discorduser"
    __cursor = sql_connect(__db_file_path).cursor()

    def __init__(self, discord_id: int) -> None:
        """
        Searches for a discord user in the database by discord_id.
        If the user is found, initializes the discord user object with the discord_id.
        Otherwise, creates a new discord user in the database.
        :param discord_id:
        """
        self.__cursor.execute(f"select * from {self.__table_name} "
                              "where discord_id = ?;", (discord_id,))
        row = self.__cursor.fetchone()
        if row is None:
            self.new(discord_id)
        self.__discord_id = discord_id

    def __str__(self) -> str:
        """
        Returns the string representation of the discord user.
        :return:
        """
        return f"{self.__discord_id}"

    @classmethod
    def create_table(cls) -> None:
        """
        Creates the table in the database.
        :return:
        """
        cls.__cursor.execute(f"create table if not exists {cls.__table_name} ("
                             "discord_id INTEGER not null constraint discord_id_primary primary key);")
        cls.__cursor.connection.commit()

    @classmethod
    def new(cls, discord_id: int) -> 'DiscordUser':
        """
        Creates a new discord user in the database.
        :param discord_id:
        :return:
        """
        cls.__cursor.execute(f"insert or ignore into {cls.__table_name}"
                             "(discord_id) values (?);", (discord_id,))
        cls.__cursor.connection.commit()
        return cls(discord_id)

    @classmethod
    def get_all(cls) -> list['DiscordUser']:
        """
        Retrieves a list of all discord users from the database.
        :return:
        """
        cls.__cursor.execute(f"select * from {cls.__table_name};")
        return [cls(row[0]) for row in cls.__cursor.fetchall()]

    @classmethod
    def get_all_id(cls) -> list[int]:
        """
        Retrieves a list of all discord user ids from the database.
        :return:
        """
        cls.__cursor.execute(f"select discord_id from {cls.__table_name};")
        return [row[0] for row in cls.__cursor.fetchall()]

    def get_id(self) -> int:
        return self.__discord_id

    def delete(self) -> None:
        """
        Deletes the discord user from the database.
        :return:
        """
        self.__cursor.execute(f"delete from {self.__table_name} where discord_id = ?;", (self.__discord_id,))
        self.__cursor.connection.commit()
        del self.__discord_id
