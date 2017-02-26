#Michael Phung Nguyen
#CS 461ß
import json
from collections import defaultdict
from pprint import pprint

dice_roll_combos = [
    '11','12','13',
    '14','15','16',
    '22','23','24','25','26',
    '33','34','35','36',
    '44','45','46',
    '55','56',
    '66'
    ]

#flip dice roll if necessary
def format_dice_roll(dice_roll):
    return dice_roll if int(dice_roll[0]) > int(dice_roll[1]) else dice_roll[::-1]

def build_database(position, dice_roll):
    if position == '000000':
        return
    else:
        position_array = [int(num) for num in position]
        dice_roll_array = [int(num) for num in dice_roll]
        dice_high = int(dice_roll[0])
        dice_low = int(dice_roll[1])
        possible_positions = None
        combine_position_array = []
        position_length = len(position_array)
        db[position][dice_roll] = []

        for j_high in range(position_length):
            new_position_array = list(reversed(position_array))
            sum_of_zeros_before_j = sum(new_position_array[:j_high])
            if new_position_array[j_high] == 0:
                continue
            elif dice_high > position_length - j_high and sum_of_zeros_before_j != 0:
                continue
            
            current_high_index = position_length - j_high
            # move high first
            if dice_high < current_high_index:
                new_position_array[j_high] = new_position_array[j_high] - 1
                new_position_array[j_high + dice_high] = new_position_array[j_high + dice_high] + 1
            else:
                new_position_array[j_high] = new_position_array[j_high] - 1
            
            # if moving high causes a 000000
            if sum(new_position_array) == 0:
                combine_position_array = ''.join([str(num) for num in new_position_array])
                db[position][dice_roll].append(combine_position_array)
                return

            for i_low in range(position_length):
                j_position_array = list(new_position_array)
                if j_position_array[i_low] == 0:
                    continue
                elif dice_low > position_length - i_low and sum(j_position_array[:i_low]) != 0:
                    continue

                current_low_index = position_length - i_low
                # then move low
                if dice_low < current_low_index:
                    j_position_array[i_low] = j_position_array[i_low] - 1
                    j_position_array[i_low + dice_low] = j_position_array[i_low + dice_low] + 1
                else:
                    j_position_array[i_low] = j_position_array[i_low] - 1

                combine_position_array = ''.join([str(num) for num in list(reversed(j_position_array))])
                db[position][dice_roll].append(combine_position_array)

                if combine_position_array in db:
                    global found
                    found = found + 1
                    # print(found)
                else:
                    for combos in dice_roll_combos:
                        build_database(combine_position_array, format_dice_roll(combos))
 
#user input variables
db = defaultdict(dict)
db_expected = defaultdict(lambda: defaultdict(list))
found = 0

# load existing database
with open('db.json') as json_data:
    db = defaultdict(dict,json.load(json_data))

with open('db_expected.json') as json_data:
    db_expected = defaultdict(lambda: defaultdict(list), json.load(json_data))

def find_expected(parent, dice = None):
    if parent in db_expected and dice in db_expected[parent]:
        return db_expected[parent]['expected']
    elif parent == '000000':
        db_expected[parent]['expected'] = 0
        return 0
    else:
        expected = 0
        depths = []
        dice_expected = 0
        for combos in db[parent]:
            for child in db[parent][combos]:
                depth = find_expected(child, combos) + 1
                dice_expected = depth
                depths.append(depth)
            dice_dict = {combos: dice_expected}
            if dice_dict not in db_expected[parent]['dice_rolls']:
                db_expected[parent]['dice_rolls'].append(dice_dict) 
        expected = sum(depths)/len(depths)
        db_expected[parent]['expected'] = expected
        return expected

#run this to build the databse quicker without going through promps
# for combos in dice_roll_combos:
#     build_database('000006', combos)
# expected = find_expected('111111')


def build_and_find(position, roll = None):
    for combos in dice_roll_combos:
        build_database(position, format_dice_roll(combos))
    
    expected = find_expected(position)

exit = False
print("hello welcome to the backgammon database")
while not exit:
    ans = input("would you like to (a)nalyze position or (s)uggest a move? or (e) to exit: ")
    if ans == 'a':
        position = input("you chose to analyze, please enter a position: ")
        build_and_find(position)
        print("\ncombos    expected")
        for rolls in db_expected[position]['dice_rolls']:
            for key in rolls:
                print(key,"       ", rolls[key])
        print("\n")
    elif ans == 'e':
        exit = True
    elif ans == 's':
        position = input("you chose to analyze, please enter a position: ")
        position = [int(num) for num in position]
        if sum(position) > 6 or len(position) != 6:
            print("wrong input")
            continue
        roll = input("pick a dice roll: ")
        position =''.join([str(num) for num in position])
        build_and_find(position)

        lowest_expected = 99
        maximum = 0
        best = None
        for move in db[position][format_dice_roll(roll)]:
            if db_expected[move]['expected'] < lowest_expected:
                lowest_expected = db_expected[position]['expected']
                best = move
            for rolls in db_expected[position]['dice_rolls']:
                for key in rolls:
                    if rolls[key] > maximum:
                        maximum = rolls[key]      
          
        print("best move is: ", best)
        print("expected:", lowest_expected)
        print("maximum", maximum)
    else:
        continue
        
# dump into database
with open('db.json', 'w') as outfile:
    json.dump(dict(db), outfile)
    
#dump into expected database
with open('db_expected.json', 'w') as outfile:
    json.dump(dict(db_expected), outfile)