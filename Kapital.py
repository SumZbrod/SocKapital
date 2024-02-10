import pandas as pd
from icecream import ic

class User:
    def __init__(self, name):
        self.name = name
        self.capital = 0
        self.request_value = 0
        self.vote_value = 0
        self.vote_name = -1

    def request(self, value):
        assert self.request_value == 0, f"You allready have request = {self.request_value}"
        self.request_value = value

    def submit_request(self, ratio):
        final_request = round(self.request_value*ratio)
        self.capital += final_request 
        self.request_value = 0
        return final_request

    def submit_vote(self):
        self.vote_value = 0
        self.vote_name = -1

    def set_vote_name(self, vote_name):
        assert vote_name != self.name, "Нельзя за себя голосовать"
        self.vote_name = vote_name

    def set_vote_value(self, value):
        assert self.capital >= value, f"You can't vote, your budget to low {self.capital}, not {value}"
        self.capital -= value
        self.vote_value = value
        

    def __repr__(self):
        return f"<{self.name}: {self.capital}>"

class Kapital:
    def __init__(self, Players, history=''):
        self.history = history
        if isinstance(Players, list):
            self.players = {name: User(name) for name in Players}
        else:
            self.players = Players
        
            for player_name in self.players:
                self.players[player_name].submit_vote() 

        self.capital = 10**len(str(len(self.players)**2))

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
            return f"Теперь напишите сколько вы готовы отдать на голование\nцелое число от 0 до {self.players[who_name].capital}"
        else:
            self.set_vote_value(who_name, value)
            return "Ваша голос принят, ожидайте остальных игроков"


    def set_vote_name(self, who_name, vote_name_id):
        try:
            vote_name = list(self.players.keys())[vote_name_id]
        except:
            raise Exception(f'Доступтны числа только от 0 до {len(self.players)}, а не "{vote_name_id}"')
        # assert vote_name in self.players, f"name '{vote_name}' can't find, you can chose only {list(self.players.keys())}"
        self.players[who_name].set_vote_name(vote_name)

    def set_vote_value(self, who_name, value):
        self.players[who_name].set_vote_value(value)

    def submit_vote(self) -> tuple:
        log_table = pd.DataFrame(columns=self.players.keys(), index=self.players.keys(), data=0)

        vote_tabel = {name: 0 for name in self.players}
        for player_name, P in self.players.items():
            vote_tabel[P.vote_name] += P.vote_value
            log_table[player_name].loc[P.vote_name] = P.vote_value
        
        max_value = max(vote_tabel.values())
        max_names = list(filter(lambda name: vote_tabel[name] == max_value, vote_tabel))
        for name in max_names:
            del self.players[name]
         
        self.history += str_log + '\n'
        self = Kapital(self.players, self.history)
        str_log = f"whom\who \n {log_table}\n lose: {max_names}"

        return max_names, str_log
        

    def get_win_name(self):
        for name in self.players: 
            return name

    def __repr__(self):
        return f"{self.capital} | {', '.join(map(str, self.players.values()))}"


def qwe_test():
    player_names = ["Q", "W", "E"]
    K = Kapital(player_names)
    print(K)

    K.request("Q", 5)
    K.request("W", 4)
    K.request("E", 3)
    request_log = K.submit_request()
    print(request_log)
    print(K)

    K.vote("Q", "W", 3)
    K.vote("W", "Q", 1)
    K.vote("E", "Q", 2)
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
    test_105()

if __name__ == "__main__":
    main()