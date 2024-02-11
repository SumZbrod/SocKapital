from Kapital import Kapital
from icecream import ic
class Status:
    statuses = ["joining", "requesting", "voting", "stop", "dotation"]
    def __init__(self, status_id=3):
        self.status_id = status_id

    def __eq__(self, obj):
        if isinstance(obj, str): 
            return self.statuses[self.status_id] == obj
        else:
            return self.status_id == obj

    def next(self):
        if self.status_id < 3: 
            self.status_id += 1 if self.status_id < 2 else -1

class DisBot:
    def __init__(self, admin_id):
        self.admin_id = admin_id   
        self.status = Status()

        self.kapital = None
        self.luzers = None
        self.players = None
 
    async def update(self):
        if self.status == "requesting":
            await self.notification(f"Kапитал составляет {self.kapital.capital} \nНапишите сколько из этого капитала вы хотите получить, целое число от 0 до {self.kapital.capital}")
        elif self.status == "voting":
            self.kapital.players_names = [p.name for p in self.kapital.players.values()]
            positive_players = [p for p in self.players if p.capital > 0] 
            str_table = f"Выбирете номер игрока против которого будете голосовать\n"
            for i, name in enumerate(self.kapital.players_names):
                str_table += f"{i}) {name}\n"
            await self.notification(str_table, positive_players)

            bankrot_players  = [p for p in self.players if p.capital <= 0]
            await self.notification("Вы не можете голосовать, у вас слишком мало баллов", bankrot_players)

    async def update_counter(self):
        if self.ready():
            self.number_selections = 0
            if self.status == 'requesting':
                request_result, submit_request_log = self.kapital.submit_request()
                requesting_notifications = {
                    name: 
                    f"Запросы закончились\nВы получили {request_result[name]}\nВаш капитал теперь равен {player.capital}" 
                    for name, player in self.kapital.players.items()
                }
                await self.notification(requesting_notifications)                

                luzers_notification = {
                    name: 
                    "Таблица запросов и результатов всех игроков, никому не сообщайте об этом до конца игры\n" + submit_request_log 
                    for name in self.luzers
                }
                await self.notification(luzers_notification)

            elif self.status == "voting":
                vote_result, submit_vote_log = self.kapital.submit_vote()
                self.luzers += vote_result
                voting_notifications = "Голосование закончилось, к сожалению нас покидает" + ", ".join(vote_result) 
                if len(self.kapital.players) <= 1:
                    if len(self.kapital.players) == 1:
                        voting_notifications += f"\n Победил {self.kapital.get_win().name}, со счётом {self.kapital.get_win().capital}"
                    else:
                        voting_notifications += "\nВсе проиграли :("
                    voting_notifications += "\nВот история выборов игроков\n" + self.kapital.history
                    self.status.status_id = 3
                    await self.notification(voting_notifications, self.players)
                    return

                await self.notification(voting_notifications, self.players)

                new_luzers_notification = "К сожалению вы проиграли, но вы можете продолжать следить за игрой, только не разговариваете!\n"
                new_luzers_notification += "Вот история выборов игроков\n" + self.kapital.history
                new_luzers_notification = {name: new_luzers_notification for name in vote_result}
                await self.notification(new_luzers_notification)
                

                luzers_notification = {name: 
                "Вот так проголосовали все, ни кому не говорите это до конца игры\n" + submit_vote_log 
                for name in self.luzers if name not in vote_result}
                await self.notification(luzers_notification)

            self.status.next()
            await self.update()

    async def handle(self, message):
        content = message.content 
        if message.author.id == self.admin_id:
            if content.startswith('!restart'):
                await self.restart(message)
                return
            elif content.startswith('!start'):
                await self.start(message)
                return
            elif content.startswith('!next'):
                self.number_selections = 100
        if content.startswith('!join'):
            if self.status == "joining":
                await self.join(message)
            else:
                await message.channel.send("Набор игроков пока не проводится.")
        else:
            if self.status == 'requesting':
                await self.requesting(message)
            elif self.status == "voting":
                await self.voting(message)
            elif self.status == "stop":
                await message.channel.send("Игра пока не началась")

    async def requesting(self, message):
        try:
            self.kapital.request(message.author.name, message.content)
            await message.channel.send("Ваш заявка принята, ожидайте остальных игроков")
            await self.update_counter()                        
        except Exception as inst:
            await message.channel.send(str(inst))
            raise inst

    async def voting(self, message):
        try:
            content = message.content
            answer_message = self.kapital.vote(message.author.name, message.content)
            await message.channel.send(answer_message)
            await self.update_counter()                        
        except Exception as inst:
            await message.channel.send(str(inst))
            raise inst

    async def notification(self, text, members=None):
        if isinstance(text, str):
            if members == None:
                members = set(self.players) - set(self.luzers)
            for player in members:
                await player.send(text)
        else:
            for player in self.players:
                if player.name in text:
                    await player.send(text[player.name])

    async def join(self, message):
        if message.author in self.players:
            await message.channel.send("Ты уже в игре, долбаёб")
        else:
            self.players.append(message.author)
            await self.notification(f"{message.author.name} добавился к игре, количество игроков: {len(self.players)}")
        
    async def restart(self, message):   
        self.players = []
        self.luzers = []    
        self.number_selections = 0
        self.kapital = None
        self.status = Status(0)
        await message.channel.send('game has restarted')
        await self.join(message)

    async def start(self, message):
        if self.status == "stop":
            await self.restart(message)
        self.status = Status(1)
        self.kapital = Kapital([player.name for player in self.players])
        await self.notification(f"Игра началась")
        await self.update()
        
    