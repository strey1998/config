from datetime import datetime as dt
from datetime import timezone as tz
import time
import requests
from zoneinfo import ZoneInfo

from libqtile.widget import base

BBS_BASE_URL = "http://statsapi.mlb.com"
BBS_API_URL = BBS_BASE_URL + "/api/v1"

class Game:
    def __init__(self, id):
        self.id = id
        self.clear()

    def __repr__(self):
        return f"Game({self.id})"

    def __str__(self):
        if self.status_code == "X":
            return "<ERROR>"

        elif self.status_code in ("F", "O"): # Final
            result = ""
            result += self.away_abbr + " " + str(self.away_score)
            result += " "
            result += self.home_abbr + " " + str(self.home_score)
            result += " Final"
    
            return result
    
        elif self.status_code == "I": # In progress
            sep = " "

            result = ""
            result += self.away_abbr + " " + str(self.away_score)
            result += sep
            result += self.home_abbr + " " + str(self.home_score)
            result += sep
            result += f"{'\u25b2' if self.topInning else '\u25bc'}{self.inning}"
            result += sep
            result += ("\u25cf" * self.outs) + ("\u25cb" * (3 - self.outs))
            result += sep
            result += f"{self.balls}-{self.strikes}"
    
            return result
    
        elif self.status_code in ("PW", "PR"):
            result = ""
            result += self.away_abbr + " 0"
            result += " "
            result += self.home_abbr + " 0"
            result += " "
            result += self.start_time.astimezone().strftime("%H:%M")
            result += " "
            result += detState
    
            return result
    
        elif self.status_code in ("P", "S"):
            result = ""
            result += f"{self.away_abbr}-{self.home_abbr}"
            result += " "
            result += self.start_time.astimezone().strftime("%H:%M")
    
            return result

        else:
            result = ""
            result += f"{self.away_abbr}-{self.home_abbr}"
            result += " "
            result += game["status"]["detailedState"]
    
            return result

    def clear(self):
        self.away_abbr = "UNK"
        self.home_abbr = "UNK"
        self.status_code = "X"
        self.detailed_state = ""
        self.start_time = None
        self.away_score = 0
        self.home_score = 0
        self.inning = 0
        self.topInning = True
        self.outs = 0
        self.balls = 0
        self.strikes = 0

    def update(self):
        game_resp = requests.get(BBS_BASE_URL + f"/api/v1.1/game/{str(self.id)}/feed/live")
        if (game_resp.status_code != 200):
            return False
        
        game = game_resp.json()
        game_info = game["gameData"]
        team_info = game_info["teams"]
        linescore = game["liveData"]["linescore"]

        self.away_abbr = team_info["away"]["abbreviation"]
        self.home_abbr = team_info["home"]["abbreviation"]
        self.status_code = game_info["status"]["statusCode"]
        self.detailed_state = game_info["status"]["detailedState"]
        self.start_time = dt.strptime(game_info["datetime"]["dateTime"], "%Y-%m-%dT%H:%M:%SZ")
        self.start_time = self.start_time.replace(tzinfo=tz.utc)
        if "runs" in linescore["teams"]["away"].keys():
            self.away_score = linescore["teams"]["away"]["runs"]
            self.home_score = linescore["teams"]["home"]["runs"]
            self.inning = linescore["currentInning"]
            self.topInning = (linescore["inningHalf"][0] == "T")
            self.outs = linescore["outs"]
            self.balls = linescore["balls"]
            self.strikes = linescore["strikes"]
        else:
            self.away_score = 0
            self.home_score = 0
            self.inning = 0
            self.topInning = True
            self.outs = 0
            self.balls = 0
            self.strikes = 0

        return True

class BaseballScores(base.BackgroundPoll):
    defaults = [
        ("team_id", 111, "MLB API team id"),
        ("dynamic_update", True, "Change update rate depending on game state")
    ]
    def __init__(self, *args, **config):
        base.BackgroundPoll.__init__(self, *args, **config)
        self.add_defaults(BaseballScores.defaults)
        self.game = None
        self.desired_update_interval = self.update_interval

    def poll(self):
        if self.game is None: # TODO: Check if game is yesterday to refresh
            today_games_resp = requests.get(BBS_API_URL + "/schedule/games/?sportId=1")
            if today_games_resp.status_code != 200:
                return f"<HTTP ERROR {today_games_resp.status_code}>"
            for game in today_games_resp.json()["dates"][0]["games"]:
                away_id = game["teams"]["away"]["team"]["id"]
                home_id = game["teams"]["home"]["team"]["id"]
                if away_id == self.team_id or home_id == self.team_id:
                    self.game = Game(game["gamePk"])
                    break

        if self.game is not None:
            update_successful = False
            for _ in range(5):
                if self.game.update():
                    update_successful = True
                    break
                time.sleep(2)

            if update_successful:
                if self.dynamic_update:
                    if self.game.status_code in ("P", "S", "PW", "PR"):
                        now = dt.now(tz.utc)
                        delta = self.game.start_time - now
                        seconds_before_start = (self.game.start_time - now).total_seconds()
                        if seconds_before_start > 3600:
                            self.update_interval = max(900, self.desired_update_interval)
                        elif seconds_before_start > 900:
                            self.update_interval = max(180, self.desired_update_interval)
                        elif seconds_before_start > 0:
                            self.update_interval = max(60, self.desired_update_interval)
                        else:
                            self.update_interval = self.desired_update_interval
                    elif self.game.status_code == "F":
                        self.update_interval = max(1200, self.desired_update_interval)
                    else:
                        self.update_interval = self.desired_update_interval
            else:
                if self.dynamic_update:
                    self.update_interval = max(180, self.desired_update_interval)

            return str(self.game)
        else:
            resp = requests.get(BBS_API_URL + "/teams/" + str(self.team_id))
            abbr = resp.json()["teams"][0]["abbreviation"]
            if self.dynamic_update:
                self.update_interval = max(3600, self.desired_update_interval)
            return f"{abbr} BYE"
