import pandas as pd
from icecream import ic

class User:
    def __init__(self, name):
        self.name = name
        self.capital = 0
        self.request_value = 0
        self.vote_value = 0
        self.vote_name = -1
        self.status = 0

    def change_status(self, old_value, new_value, text):
        if self.status != old_value:
            ic(f"{text} | {self.status}")
        self.status = new_value        

    def request(self, value):
        assert self.request_value == 0, f"You already have request = {self.request_value}"
        self.change_status(0, 1, 'request')
        self.request_value = value

    def submit_request(self, ratio):
        self.change_status(1, 0, 'submit_request')
        final_request = round(self.request_value*ratio)
        self.capital += final_request 
        self.request_value = 0
        return final_request

    def set_vote_name(self, vote_name):
        assert vote_name != self.name, "Нельзя за себя голосовать"
        self.change_status(0, .5, 'set_vote_name')
        self.vote_name = vote_name

    def set_vote_value(self, value):
        assert self.capital >= value > 0, f"Ставка должна быть больше нуля до {self.capital}, а не {value}"
        self.change_status(.5, 1, 'set_vote_value')
        self.capital -= value
        self.vote_value = value
        
    def submit_vote(self):
        self.change_status(1, 0, 'submit_vote')
        self.vote_value = 0
        self.vote_name = -1

    def __repr__(self):
        return f"<{self.name}: {self.capital}>"

class Kapital:
    def __init__(self, Players, history='', play_round=1):
        self.history = history
        self.play_round = play_round
        if isinstance(Players, list):
            self.players = {name: User(name) for name in Players}
        else:
            self.players = Players
        
            for player_name in self.players:
                self.players[player_name].submit_vote() 

        self.capital = 10**len(str(len(self.players)**2))
        self.players_names = [p.name for p in self.players.values()]

    def request(self, player_name, value):
        value = self.v_int(value)
        assert 0 <= value <= self.capital, f"Значение должно быть между 0 и {self.capital}, а не {value}"
        self.players[player_name].request(value)

    def submit_request(self):
        log_table = pd.DataFrame(columns=['request', 'result'], index=self.players.keys())
        request_result = {}
        request_amount = sum((P.request_value for P in self.players.values()))
        complete_capital = 2*self.capital - request_amount
        if complete_capital < self.capital:
            ratio = complete_capital / request_amount
        else:
            ratio = 1
        for name, P in self.players.items():
            log_table.request.loc[name] = P.request_value
            player_result = P.submit_request(ratio)
            log_table.result.loc[name] = player_result
            request_result[name] = player_result


        self.history += f"Round #{self.play_round}\n"
        self.history += str(log_table) + '\n'

        return request_result, str(log_table)

    def v_int(self, value):
        try:
            value = int(value)
        except:
            raise Exception(f'Значение "{value}" - не похоже на целое число')
        return value

    def vote(self, who_name, value):
        value = self.v_int(value)
        if self.players[who_name].vote_name == -1:
            self.set_vote_name(who_name, value)
            return f"Теперь напишите сколько вы готовы отдать на голование\nцелое число от 1 до {self.players[who_name].capital}"
        else:
            self.set_vote_value(who_name, value)
            return "Ваша голос принят, ожидайте остальных игроков"


    def set_vote_name(self, who_name, vote_name_id):
        try:
            vote_name = self.players_names[vote_name_id]
        except:
            
            raise Exception(f'Доступтны числа только от 0 до {len(self.players)-1}, а не "{vote_name_id}"')
        # assert vote_name in self.players, f"name '{vote_name}' can't find, you can chose only {list(self.players.keys())}"
        self.players[who_name].set_vote_name(vote_name)

    def set_vote_value(self, who_name, value):
        self.players[who_name].set_vote_value(value)

    def submit_vote(self) -> tuple:
        log_table = pd.DataFrame(columns=self.players.keys(), index=self.players.keys(), data=0)

        vote_tabel = {name: 0 for name in self.players}
        for player_name, P in self.players.items():
            if P.vote_name == -1:
                continue
            vote_tabel[P.vote_name] += P.vote_value
            log_table[player_name].loc[P.vote_name] = P.vote_value
        
        max_value = max(vote_tabel.values())
        max_names = list(filter(lambda name: vote_tabel[name] == max_value, vote_tabel))
        for name in max_names:
            del self.players[name]
         
        str_log = f"whom\who \n {log_table}\n lose: {max_names}"
        self.history += str_log + '\n'
        self = Kapital(self.players, self.history, self.play_round+1)
        with open('/home/kiki/Documents/py/kapital/history.log', 'w') as f:
            f.write(self.history)

        return max_names, str_log
        
    def negative_number(self):
        res = len((p for p in self.players if p.capital <= 0))
        assert res < len(self.capital), "nobody can't vote"
        return res

    def get_win(self):
        for P in self.players.values(): 
            return P

    def ready(self):
        ready_list = [p for p in self.players.values() if p.status == 1 or p.capital < 0]
        # ic(ready_list)
        return len(ready_list) == len(self)

    def get_positive_name(self):
        positives = [p.name for p in self.players.values() if p.capital > 0]
        return positives

    def make_subsidy(self):
        max_negative = min([p.capital for p in self.players.values()])
        for name in self.players:
            self.players[name].capital -= max_negative
        return max_negative 
        
    def __len__(self):
        return len(self.players)

    def __repr__(self):
        return f"{self.capital} | {', '.join(map(str, self.players.values()))}"

def neg_test(): 
    player_names = ["Q", "W", "E", "R"]
    K = Kapital(player_names)
    print(K)
    K.request("Q", 100)
    print(K.ready())
    K.request("W", 80)
    print(K.ready())
    K.request("E", 70)
    print(K.ready())
    K.request("R", 50)
    print(K.ready())
    request_log = K.submit_request()
    print(request_log)
    ic(K.all_negative())
    if K.all_negative():
        subsidy =  K.make_subsidy()
        ic(subsidy)
    print(K)


def qwe_test():
    player_names = ["Q", "W", "E"]
    K = Kapital(player_names)
    # print(K)

    K.request("Q", 5)
    print(K.ready())
    K.request("W", 4)
    print(K.ready())
    K.request("E", 1)
    print(K.ready())
    request_log = K.submit_request()
    print(request_log)

    K.vote("Q", 1)
    K.vote("Q", 1)

    K.vote("W", 0)
    K.vote("W", 1)

    K.vote("E", 1)
    K.vote("E", 1)

    max_names, vote_log = K.submit_vote()
    print(vote_log)
    print(K)

def test_105():
    player_names = ["Q", "W"]
    K = Kapital(player_names)
    print(K)

    K.request("Q", 5)
    K.request("W", 10)
    _, request_log = K.submit_request()
    print(request_log)
    print(K)


def main():
    qwe_test()
    # neg_test()

if __name__ == "__main__":
    main()