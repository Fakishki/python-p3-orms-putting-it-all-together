import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)

    def save(self):
        save_sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?);
        """
        CURSOR.execute(save_sql, (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        dog_inst = cls(
            name=row[1],
            breed=row[2],
            id=row[0]
        )
        return dog_inst
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM dogs
        """
        all_dogs = CURSOR.execute(sql).fetchall()
        return [Dog.new_from_db(row) for row in all_dogs]
    
    @classmethod
    def find_by_name(cls, search):
        sql = """
            SELECT * FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        row = CURSOR.execute(sql, (search,)).fetchone()
        return cls.new_from_db(row) if row else None
    
    @classmethod
    def find_by_id(cls, search):
        sql = """
            SELECT * FROM dogs
            WHERE id = ?
            LIMIT 1
        """
        row = CURSOR.execute(sql, (search,)).fetchone()
        return cls.new_from_db(row) if row else None
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
            SELECT * FROM dogs
            WHERE (name, breed) = (?, ?)
            LIMIT 1
        """
        row = CURSOR.execute(sql, (name, breed)).fetchone()
        return cls.new_from_db(row) if row else Dog.create(name, breed)
    
    def update(self):
        update_sql = """
            UPDATE dogs
            SET (name, breed) = (?, ?)
            WHERE id = ?
        """
        CURSOR.execute(update_sql, (self.name, self.breed, self.id))
        CONN.commit()