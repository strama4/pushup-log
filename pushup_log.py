from collections import OrderedDict
import datetime
import os


from peewee import *


db = SqliteDatabase('pushups.db')


class Workout(Model):

    set1 = IntegerField(default=0)
    set2 = IntegerField(default=0)
    set3 = IntegerField(default=0)
    set4 = IntegerField(default=0)
    set5 = IntegerField(default=0)
    set6 = IntegerField(default=0)
    total = IntegerField(default=0)
    date = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Workout], safe=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Pick an option: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


def start_workout():
    """Start a new workout"""
    goal = record_goal()
    reps = []
    total_reps = 0
    set_num = 1

    while total_reps < goal:
        try:
            sett = int(input('Set #{}: Reps... '.format(set_num)))
        except ValueError:
            print("You'll need to enter a number")
        else:
            reps.append(sett)
            total_reps += sett
            set_num += 1

            if (goal-total_reps) > 0:
                print('Reps to Go: {}'.format(goal-total_reps))

    # This is to avoid having empty fields when less than 6 sets are needed
    if len(reps) < 6:
        for _ in range((6-len(reps))):
            reps.append(0)

    print("Sweet! You've reached your goal for the day!\n")

    repsdict = {1: reps[0],
                2: reps[1],
                3: reps[2],
                4: reps[3],
                5: reps[4],
                6: reps[5]}

    if input("Save workout? [Y]/n ").lower() != 'n':
        Workout.create(total=total_reps,
                       set1=repsdict[1],
                       set2=repsdict[2],
                       set3=repsdict[3],
                       set4=repsdict[4],
                       set5=repsdict[5],
                       set6=repsdict[6])
        print("Workout saved!")


def last_workout():
    """Check out the last workout"""
    entries = Workout.select().order_by(Workout.date.desc())

    for entry in entries:
        repsdict = {1: entry.set1,
                    2: entry.set2,
                    3: entry.set3,
                    4: entry.set4,
                    5: entry.set5,
                    6: entry.set6}

        timestamp = entry.date.strftime('%a, %b %d, %Y')
        clear()
        print('\n\n'+'*'*len(timestamp))
        print(timestamp)
        print('Total: {}'.format(entry.total))
        for key, value in repsdict.items():
            if value:
                print('Set {}: {}'.format(key, value))
        print('*'*len(timestamp))
        print('n) next workout')
        print('d) delete workout')
        print('q) return to main menu')

        next_action = input('Action: [Ndq] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)

def delete_entry(workout):
    """Delete a workout"""
    if input("Are you sure? [yN] ").lower() == 'y':
        workout.delete_instance()
        print("Workout deleted!")


def record_goal():
    """Record the target reps for today"""
    goal = int(input('What is your rep total goal today? '))
    return goal

def add_workout():
    """Add a previous workout"""
    date = input('\nEnter the date of the workout using YYYY-MM-DD: ')
    datestamp = datetime.datetime.strptime(date, '%Y-%m-%d')

    reps = []
    set_num = 1
    total_reps = 0

    for _ in range(int(input('How many sets in the workout? '))):
        num_reps = int(input('Reps in set #{} '.format(set_num)))
        reps.append(num_reps)
        total_reps += num_reps
        set_num += 1

    # This is to avoid having empty fields when less than 6 sets are needed
    if len(reps) < 6:
        for _ in range((6 - len(reps))):
            reps.append(0)

    repsdict = {1: reps[0],
                2: reps[1],
                3: reps[2],
                4: reps[3],
                5: reps[4],
                6: reps[5]}

    if input("Save workout? Y/n ") != 'n':
        Workout.create(total=total_reps,
                       set1=repsdict[1],
                       set2=repsdict[2],
                       set3=repsdict[3],
                       set4=repsdict[4],
                       set5=repsdict[5],
                       set6=repsdict[6],
                       date=datestamp)
        print("Workout saved!")




menu = OrderedDict([
    ('s', start_workout),
    ('l', last_workout),
    ('a', add_workout),
])


initialize()
menu_loop()


