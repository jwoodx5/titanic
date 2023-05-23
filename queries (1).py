TOTAL_SURVIVED = '''
    SELECT SUM(survived) FROM titanic_table;
'''

TOTAL_DIED = '''
    SELECT COUNT(*) FROM titanic_table
    WHERE survived = 0;
'''

TOTAL_EACH_CLASS = '''
    SELECT "pclass", COUNT(name) FROM titanic_table
    GROUP BY "pclass";
'''
SURVIVED_BY_CLASS = '''
    SELECT "pclass", SUM("survived")
    FROM titanic_table
    GROUP BY "pclass";
'''

DIED_BY_CLASS = '''
    SELECT "pclass", COUNT("survived")
    FROM titanic_table
    WHERE "survived" = 0
    GROUP BY "pclass";
'''

AVG_AGE_SURVIVED = '''
    SELECT AVG("age") FROM titanic_table
WHERE "survived" = 1;
'''

AVG_AGE_DIED = '''
    SELECT AVG("age") FROM titanic_table
WHERE "survived" = 0;
'''

AVG_AGE_CLASS = '''
    SELECT "pclass", AVG("age") FROM titanic_table
GROUP BY "pclass";
'''

FARE_PER_CLASS = '''
    SELECT "pclass", AVG("fare") FROM titanic_table
GROUP BY "pclass";
'''

FARE_CLASS_SURVIVED = '''
    SELECT "survived", AVG("fare") FROM titanic_table
GROUP BY "survived";
'''

SIB_SPOUSE_CLASS = '''
    SELECT "pclass", AVG("siblings_spouses_aboard") FROM titanic_table
GROUP BY "pclass";
'''


SIB_SPOUSE_SURVIVED = '''
    SELECT "survived", AVG("siblings_spouses_aboard") FROM titanic_table
GROUP BY "survived";
'''

PARENTS_CHILDREN_CLASS = '''
    SELECT "pclass", AVG("parents_children_aboard") FROM titanic_table
GROUP BY "pclass";
'''

PARENTS_CHILDREN_SURVIVED = '''
    SELECT "survived", AVG("siblings_spouses_aboard") FROM titanic_table
GROUP BY "survived";
'''

PASSENGERS_DIFF_NAME = '''
    SELECT COUNT(DISTINCT "name") FROM titanic_table;
'''
QUERY_LIST = [TOTAL_SURVIVED, TOTAL_DIED, TOTAL_EACH_CLASS, SURVIVED_BY_CLASS,
              DIED_BY_CLASS, AVG_AGE_SURVIVED, AVG_AGE_DIED, AVG_AGE_CLASS,
              FARE_PER_CLASS, FARE_CLASS_SURVIVED, SIB_SPOUSE_CLASS, SIB_SPOUSE_SURVIVED,
              PARENTS_CHILDREN_CLASS, PARENTS_CHILDREN_SURVIVED, PASSENGERS_DIFF_NAME]


# MongoDB Queries

class MongoAnswers():
    def __init__(self, col):
        # Set the collection attribute
        self.collection = col
        # Get all documents
        self.characters = list(col.find({}))

    def total_characters(self):
        return len(self.characters)

    def total_items(self):
        count = 0
        for character in self.characters:
            if 'items' in character:
                count += len(character['items'])
        return count


    def total_weapons(self):
        count = 0
        for character in self.characters:
            if 'weapons' in character:
                count += len(character['weapons'])
        return count

    def total_non_weapons(self):
        return self.total_items() - self. total_weapons()

    def character_items(self):
        items_by_character = {}
        for character in self.characters:
            if 'name' not in character:
                continue
            name = character['name']
            if 'items' in character:
                num_items = len(list(character['items']))
                items_by_character[name] = num_items
        return items_by_character

    def character_weapons(self):
        weapons = {}
        for character in self.characters:
            if 'weapons' in character:
                name = character['name']
                num_weapons = len(character['weapons'])
                weapons[name] = num_weapons
        return weapons

    def average_items(self):
        num_items = []
        for character in self.characters:
            if 'items' in character:
                num_items.append(len(character['items']))
        return sum(num_items) / len(num_items) if num_items else 0

        # return num_items


    def average_weapons(self):
        num_weapons = []
        for character in self.collection.find():
            weapons = character.get('weapons', [])
            num_weapons.append(len(weapons))
        return sum(num_weapons) / len(num_weapons)

    def show_results(self):
        return f'''
        Total Number of Characters: {self.total_characters()}
        Total Number of Items: {self.total_items()}
        Total Number of Weapons: {self.total_weapons()}
        Total Non-Weapons: {self.total_non_weapons()}
        Number of Items for each Character: {self.character_items()}
        Number of Weapons for each Character: {self.character_weapons()}
        Average Number of Items: {self.average_items()}
        Average Number of Weapons: {self.average_weapons()}
        '''