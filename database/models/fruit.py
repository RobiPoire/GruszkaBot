from random import choice as rand_choice
from sqlite3 import connect as sql_connect

from utils.qwant_image import qwant_image


class Fruit:
    __db_file_path = "./database/sqlite_db.db"
    __table_name = "fruit"
    __cursor = sql_connect(__db_file_path).cursor()

    def __init__(self, name: str) -> None:
        """
        Searches for a fruit in the database by name.
        If the fruit is found, initializes the Fruit object with the name and description.
        Otherwise, raises a ValueError.
        :param name:
        """
        self.__cursor.execute(f"select * from {self.__table_name} "
                              "where lower(fruit_name) = lower(?);", (name.lower(),))
        row = self.__cursor.fetchone()
        if row is None:
            raise ValueError(f"Fruit '{name}' not found in the database.")
        self.__description = row[1]
        self.__name = row[0]

    def __str__(self):
        """
        Returns the string representation of the fruit.
        :return:
        """
        return f"{self.__name}: {self.__description}"

    @classmethod
    def create_table(cls) -> None:
        """
        Creates the table in the database.
        :return:
        """
        cls.__cursor.execute(f"create table if not exists {cls.__table_name} ("
                             "fruit_name CHARACTER(30) not null constraint fruit_name_primary primary key,"
                             "fruit_description TEXT not null);")
        cls.__cursor.connection.commit()

    @classmethod
    def new(cls, name: str, description: str) -> 'Fruit':
        """
        Creates a new fruit in the database.
        :param name:
        :param description:
        :return:
        """
        cls.__cursor.execute(f"insert or ignore into {cls.__table_name}"
                             "(fruit_name, fruit_description) values (?, ?);", (name, description))
        cls.__cursor.connection.commit()
        return cls(name)

    @classmethod
    def get_all(cls) -> list['Fruit']:
        """
        Retrieves a list of all fruits from the database.
        :return:
        """
        cls.__cursor.execute(f"select * from {cls.__table_name};")
        return [cls(row[0]) for row in cls.__cursor.fetchall()]

    @classmethod
    def get_random(cls) -> 'Fruit':
        """
        Retrieves a random fruit from the database.
        :return:
        """
        return cls(rand_choice(cls.get_all_names()))

    @classmethod
    def get_all_names(cls) -> list[str]:
        """
        Retrieves a list of all fruit names from the database.
        :return:
        """
        cls.__cursor.execute(f"select fruit_name from {cls.__table_name};")
        return [row[0] for row in cls.__cursor.fetchall()]

    @classmethod
    def get_all_descriptions(cls) -> list[str]:
        """
        Retrieves a list of all fruit descriptions from the database.
        :return:
        """
        cls.__cursor.execute(f"select fruit_description from {cls.__table_name};")
        return [row[0] for row in cls.__cursor.fetchall()]

    def delete(self) -> None:
        """
        Deletes the fruit from the database.
        :return:
        """
        self.__cursor.execute(f"delete from {self.__table_name} where fruit_name = ?;", (self.__name,))
        self.__cursor.connection.commit()
        del self.__name
        del self.__description

    def get_name(self) -> str:
        """
        Retrieves the name of the fruit.
        :return:
        """
        return self.__name

    def get_description(self) -> str:
        """
        Retrieves the description of the fruit.
        :return:
        """
        return self.__description

    def get_image(self) -> str:
        """
        Retrieves the URL of the fruit image from the image search service.
        :return:
        """
        return qwant_image(self.__name, count_result=1)[0]

    def update_description(self, description: str) -> None:
        """
        Updates the description of the fruit in the database.
        :param description:
        :return:
        """
        self.__cursor.execute(f"update {self.__table_name} set fruit_description = ? "
                              "where fruit_name = ?;", (description, self.__name))
        self.__cursor.connection.commit()
        self.__description = description
