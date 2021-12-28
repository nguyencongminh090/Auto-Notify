import json


class Action(object):
    def __init__(self, table:dict, date='00/00/0000', time='00:00'):
        self.table = table                
        self.curdate = [int(j) for j in date.split('/')]
        self.curdate.reverse()
        self.curtime = [int(j) for j in time.split(':')]
        self.task_list = self.make_task_list()
        self.is_empty = len(self.task_list) == 0

    @staticmethod
    def reformat_data(string):
        # 0: Date
        # 1: Time
        d = list(string[:8])
        d.insert(2, '/')
        d.insert(5, '/')
        
        t = list(string[8:])
        t.insert(2, ':')        
        return ''.join(d), ''.join(t)

    @staticmethod
    def enc(d, t):
        return d.replace('/', '') + t.replace(':', '')

    def make_task_list(self):
        def strf(num):
            return str(num) if num > 9 else f'0{num}'
        temp = []
        for i in self.table:
            d = [int(j) for j in self.reformat_data(i)[0].split('/')]
            d.reverse()
            t = [int(j) for j in self.reformat_data(i)[1].split(':')]
            if d >= self.curdate and t >= self.curtime:
                temp.append([d, t])
        temp.sort()
        for j in temp:
            j[0].reverse()
        for j in range(len(temp)):
            temp[j] = ''.join([strf(i) for i in temp[j][0] + temp[j][1]])
        return temp

    def  clean_up(self):
        def strf(num):
            return str(num) if num > 9 else f'0{num}'
        temp = []
        for i in self.table:
            d = [int(j) for j in self.reformat_data(i)[0].split('/')]
            d.reverse()
            t = [int(j) for j in self.reformat_data(i)[1].split(':')]
            if d <= self.curdate and t < self.curtime:
                temp.append([d, t])
        temp.sort()
        for j in temp:
            j[0].reverse()
        for j in range(len(temp)):
            temp[j] = ''.join([strf(i) for i in temp[j][0] + temp[j][1]])
        return temp

    def get_action(self):
        if len(self.task_list) == 0:
            self.is_empty = True
            
        if not self.is_empty:
            item = self.task_list.pop(0)
        else:
            return -1

        d = self.reformat_data(item)[0]
        t = self.reformat_data(item)[1]
        
        
        return (d, t, self.table[item])
