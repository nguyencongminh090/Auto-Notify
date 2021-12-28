import os
import json
import time
from action import *
from playsound import playsound


def check_valid(types, string: str):

    try:
        if types == 'curdate':
            curdate = [int(i) for i in time.strftime('%d/%m/%Y').split('/')]
            curdate.reverse()
            s = [int(i) for i in string.split('/')]
            s.reverse()
            if False in (0 < s[2] <= 31, 0 < int(s[1]) <= 12, len(s) == 3, s >= curdate):
                return False
            else:
                return True
        else:
            curtime = [int(i) for i in time.strftime('%H:%M').split(':')]
            s = [int(i) for i in string.split(':')]
            if False in (0 <= s[0] <= 24, 0 <= s[1] < 60, len(s) == 2, s >= curtime):
                return False
            else:
                return True
    except:
        return False

            
def add_activity():
    if not os.path.exists('Data.json'):
        # Create Data.json
        f = open('Data.json', 'w')
        f.write('{}')
    # Form
    with open('Data.json') as f:
        data = json.load(f)
    while True:
        try:
            set_date = input('Date (dd/mm/yyyy): ').replace(' ', '')
            
            while not check_valid('curdate', set_date):
                print('Not valid')
                set_date = input('Date (dd/mm/yyyy): ').replace(' ', '')

            set_time = input('Time (hh:mm): ').replace(' ', '')
            while not check_valid('time', set_time):
                print('Not valid')
                set_time = input('Time (hh:mm): ').replace(' ', '')
                
            set_title = input('Title: ')
            set_content = input('Content: ')
            print('-'*30)
            # Solve data input
            output = {
                'title': set_title,
                'content': set_content}
            if False not in (check_valid('curdate', set_date), check_valid('time', set_time)):
                enc = set_date.replace('/', '') + set_time.replace(':', '')
                data[enc] = output
            with open('Data.json', 'w') as f:
                json.dump(data, f)
            choice = input('Finish? (y/n): ')
            if choice.upper() == 'Y':
                break
        except:
            break


def change_activity():
    def reformat_data(string):
        d = list(string[:8])
        d.insert(2, '/')
        d.insert(5, '/')
        
        t = list(string[8:])
        t.insert(2, ':')        
        return ''.join(d), ''.join(t)

    def enc(d, t):
        return d.replace('/', '') + t.replace(':', '')
        
    if not os.path.exists('Data.json'):
        print('File not exist!')
        return
    with open('Data.json') as f:
        data = json.load(f)
    
    while True:
        try:
            # Find curdate:
            stack = []
            print('Date:')
            for i in data:
                if reformat_data(i)[0] not in stack:
                    print(f'- {reformat_data(i)[0]}')
                    stack.append(reformat_data(i)[0])
            del stack
            old_date = input('Old curdate: ')
            
            # Find time:
            for i in data:
                if reformat_data(i)[0] == old_date:
                    print(f'- {reformat_data(i)[1]}')
            old_time = input('Old time: ')

            try:
                del data[enc(old_date, old_time)]
            except:
                print('Not valid')
                continue
                
            # Change title and content:
            new_date = input('New curdate: ')
            while not check_valid('curdate', new_date):
                print('Not valid')
                new_date = input('New curdate: ')
                
            new_time = input('New time: ')
            while not check_valid('time', new_time):
                print('Not valid')
                new_time = input('New time: ')
                
            enc_new = enc(new_date, new_time)
            title = input('Title: ')
            content = input('Content: ')
            if enc_new == enc(old_date, old_time):
                
                data[enc_new]['title'] = title
                data[enc_new]['content'] = content
            else:
                data[enc_new] = {
                    'title': title,
                    'content': content}

            with open('Data.json', 'w') as f:
                json.dump(data, f)
            
            choice = input('Finish? (y/n): ')
            if choice.upper() == 'Y':
                break
        except:
            break


def run():
    with open('Data.json') as f:
        data = json.load(f)    
    
    curtime = time.strftime('%H:%M')
    curdate = time.strftime('%d/%m/%Y')
    stack = Action(data, curdate, curtime)
    if not stack.is_empty:
        alarm = stack.get_action()
        print('Today: ', curdate)
        print(f'==> Alarm: Date {alarm[0] if alarm[0] != curdate else "today"}, '
              f'Time {alarm[1]}, Title {alarm[2]["title"]}')
        while not stack.is_empty:
            try:
                if time.strftime('%H:%M') != curtime:
                    curtime = time.strftime('%H:%M')
                    print('Curtime:', curtime)
                if curdate == alarm[0] and curtime == alarm[1]:
                    playsound('sound.mp3')
                    playsound('sound.mp3')
                    playsound('sound.mp3')
                    print('-'*30)
                    print('Title:', alarm[2]['title'])
                    print('Content:', alarm[2]['content'])
                    print('-'*30)
                    alarm = stack.get_action()
                    print(f'==> Next alarm: Date {alarm[0]}, Time {alarm[1]}, Title {alarm[2]["title"]}')
            except:
                break

        print('Press enter to go back')
        input()
    else:
        print('No notify')


def clean_up():
    with open('Data.json') as f:
        data = json.load(f)

    curtime = time.strftime('%H:%M')
    curdate = time.strftime('%d/%m/%Y')
    stack = Action(data, curdate, curtime)
    action = stack.clean_up()
    for i in action:
        del data[i]

    with open('Data.json', 'w') as f:
        json.dump(data, f)


def main():
    while True:
        try:
            print('1. Add activity')
            print('2. Change activity')
            print('3. Run')
            print('4. Clean up')
            print('5. Exit')
            choice = input('Choice: ')
            if choice == '1':
                add_activity()
            elif choice == '2':
                change_activity()
                pass
            elif choice == '3':
                run()
            elif choice == '4':
                clean_up()
            elif choice == '5':
                break
        except:
            break
    return


if __name__ == '__main__':
    main()
