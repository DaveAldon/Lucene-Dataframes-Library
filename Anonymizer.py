# David Crawford Lucene Dataframes Library: Anonymization

# The purpose of this module is to provide anonymization functions in order
# to remove sensitive data from a dataframe. We employ random re-assignment
# of variables based on a seed, so that if multiple records need to have the
# same random assignment, (if they're the same person, for example), then we use
# a common id for the seed. randNum returns an anonymized dataframe based on
# defined fields in a dictionary that need to be scrambled.

import random
from datetime import datetime
from datetime import timedelta
import string

# Where we can keep any exceptions if we need to inspect the overall process
error_list = []

# This function is a highly generic example of how to use the anonymizer
def main():
    # Sample dataframe
    df = your_data_frame

    # Unique identifier for each group of data. For example, we want the same
    # person to have the same randomization so that the data is realistic
    seed = 'id'

    # Dictionary definition. These are the field names that need to be scrambled
    #1 - age
    #2 - date
    #3 - name
    #4 - address
    #5 - number
    anon_items = {'age': 1,
                  'date_time': 2,
                  'name': 3,
                  'address': 4,
                  'zip': 5
                  }

    # Loop through the dictonary and apply the randomization function to each row
    for key, value in anon_items.items():
        # Only apply if the field we encounter is in the dictionary
        if key in fields:
            df[key] = df.apply(lambda row: randNum(row[key], row[seed], value), axis=1)

# Takes a field, the seed we want for each record, and the dictionary type to
# determine which randomization method we need
def randNum(field, seed, varType):
    # First check if the field even has data in it, then establish the seed each
    # iteration of the function. If the seed needs to be the same for
    # more than one record, it will because the id will be the same

    if str(field) in 'nan':
        return field

    # Then we establish the seed for this iteration of the function
    random.seed(seed)

    # Random number based around the given number's range
    def num(_field):
        return random.randrange(_field - 5, _field + 5)

    # Random date around a range, and if the given date format is incomprehensible we use a default
    def date(_field):
        try:
            field = datetime.strptime(field, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            error_list.append(e)
            try:
                field = datetime.strptime(field, '%Y-%m-%d %H:%M')
            except Exception as e:
                error_list.append(e)
                # Return a default date if format cannot be reconciled
                return '1901-01-01'
        return field += timedelta(days=random.SystemRandom().randint(-30, 30))

    # Random letters
    def name(_field):
        return "%sxxxxxx" % random.SystemRandom().choice(string.ascii_uppercase)

    # Fixed return value
    def address(_field):
        return "REDACTED..."

    # Random integer with length equal to length of given var
    def intLength(_field):
        _field = str(_field)
        min_val = 10**(len(_field) - 1)
        max_val = (10**len(_field)) - 1
        return random.SystemRandom().randint(min_val, max_val)

    # Our dictionary of what differrent possible varTypes should equate to
    definition = {
        1: num,
        2: date,
        3: name,
        4: address,
        5: intLength,
    }

    # This is where we call on a function based on varType, the value of the current anon_items element dictionary
    return definition[varType](field)

main()
