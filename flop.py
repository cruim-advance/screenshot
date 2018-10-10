import image_processing
import postgresql
import db_conf
import keyboard
import session_log
import error_log
import math
import time
image_name = str(math.floor(time.time()))
def makeFlopDecision(screen_area, hand, image_name, folder_name, stack, action):
    try:
        saveFlopImage(str(screen_area), image_name, folder_name)
        flop_area = getFlopArea(str(screen_area))
        flop_card = image_processing.searchCards(str(flop_area), image_processing.getFlopCards(), 6)
        if len(flop_card) == 6:
            hand = hand + flop_card
            if checkPair(hand) or checkFlushDraw(hand) or checkStraightDraw(hand):
                keyboard.press('q')
                session_log.updateActionLogSession('push', str(screen_area))
                return
            elif action == 'open' and int(stack) > 11:
                if image_processing.checkIsCbetAvailable(str(screen_area)):
                    keyboard.press('o')
                    session_log.updateActionLogSession('cbet', str(screen_area))
                    return
                else:
                    keyboard.press('f')
                    session_log.updateActionLogSession('fold', str(screen_area))
                    return
            else:
                keyboard.press('f')
                session_log.updateActionLogSession('fold', str(screen_area))
        elif action == 'open' and int(stack) > 11:
            if image_processing.checkIsCbetAvailable(str(screen_area)):
                keyboard.press('o')
                session_log.updateActionLogSession('cbet', str(screen_area))
                return
            else:
                keyboard.press('f')
                session_log.updateActionLogSession('fold', str(screen_area))
                return
        else:
            keyboard.press('f')
            session_log.updateActionLogSession('end', str(screen_area))
    except Exception as e:
        error_log.errorLog('makeFlopDecision' + action, str(e))
        print(e)

def checkStraightDraw(hand):
    hand = hand[0] + hand[2] + hand[4] + hand[6] + hand[8]
    collection = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    arr = []
    for val in hand:
        arr.append(collection.index(val))
    arr = list(set(arr))
    arr = sorted(arr)
    arr_length = len(arr)
    if arr_length > 4:
        first = arr[:-1]
        second = arr[1:]
        if first == list(range(min(first), max(first) + 1)) or second == list(range(min(second), max(second) + 1)):
            return True
        else:
            return False
    elif arr_length == 4:
        if arr == list(range(min(arr), max(arr) + 1)):
            return True
        else:
            return False
    else:
        return False

def checkFlushDraw(hand):
    hand = hand[1] + hand[3] + hand[5] + hand[7] + hand[9]
    suit_count = len(set(hand))
    if suit_count == 1:
        return True
    elif suit_count == 2:
        counter = {}
        for item in hand:
            counter[item] = counter.get(item, 0) + 1
        doubles = {element: count for element, count in counter.items() if count > 3}
        if len(doubles) > 0:
            return True
    else:
        return False

def checkPair(hand):
    flop = [hand[4], hand[6], hand[8]]
    ranks = [str(n) for n in range(2, 10)] + list('TJQKA')
    ts = []
    for item in flop:
        ts.append(ranks.index(item))
    hand = hand[0] + hand[2] + hand[4] + hand[6] + hand[8]
    counter = {}

    for item in hand:
        counter[item] = counter.get(item, 0) + 1
    doubles = {element: count for element, count in counter.items() if count > 1}
    if len(doubles) == 1:
        double_element = list(doubles.keys())[0]
        if double_element in [hand[0], hand[1]] and ranks.index(double_element) != min(ts) or \
                list(doubles.values())[0] > 2 and double_element in [hand[0], hand[1]]:
            return True
    elif len(doubles) == 2:
        return True
    return False

def getFlopArea(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select flop_area from screen_coordinates where screen_area = " + screen_area + " and active = 1")
    return data[0]['flop_area']

def saveFlopImage(screen_area,image_name,folder_name):
    for value in getFlopData(str(getFlopArea(str(screen_area)))):
        image_path = folder_name + "/" + str(getFlopArea(str(screen_area))) + "/" + image_name + ".png"
        image_processing.imaging(value['x_coordinate'], value['y_coordinate'], value['width'], value['height'], image_path, value['screen_area'])

def getFlopData(screen_area):
    db = postgresql.open(db_conf.connectionString())
    data = db.query("select x_coordinate,y_coordinate,width,height,screen_area from screen_coordinates "
                    "where screen_area = "  + screen_area)
    return data

def test():
    return image_name