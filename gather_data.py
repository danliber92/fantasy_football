from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import re
import pandas as pd
from time import sleep

options = Options()
options.binary_location = r'F:\Program Files (x86)\Mozilla Firefox\firefox.exe'
driver_path = r'F:\Users\Naum2\geckodriver\geckodriver.exe'
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=options)

class fantasy_pros:
    base_url = r'https://www.fantasypros.com/nfl/rankings/{position}-cheatsheets.php'
    @classmethod
    def split_player_row(cls,player_row):
        rank, player, *_ = re.split(r'\n',player_row)
        *player, team = re.split('\s',''.join(re.findall(r'([\w\s])',player)))
        return [rank.strip(), ' '.join(player).strip().lower(), re.search(r'\w+',team.strip()).group(0).lower()]
    @classmethod
    def get_rankings(cls,position):
        driver.get(cls.base_url.format(position=position))
        sleep(5)
        rankings = []
        players = driver.find_elements(By.CLASS_NAME,'player-row')
        for player_row in players:
            try:
                rankings.append(cls.split_player_row(player_row.text))
            except:
                print(player_row.text)
        return pd.DataFrame(rankings,columns=['rank','player','team'])
    @classmethod
    def rankings_main(cls):
        rankings_dict = {}
        for position in ['consensus','qb','rb','wr','te','k','dst']:
            rankings_dict[position] =  cls.get_rankings(position)
        return rankings_dict
            
class cbs_sports:
    base_url = r'https://www.cbssports.com/fantasy/football/rankings/ppr/{position}/'
    position_map = {'top200':'consensus',
                    'QB':'qb',
                    'RB':'rb',
                    'WR':'wr',
                    'TE':'te',
                    'K':'k',
                    'DST':'dst'}
    @classmethod
    def split_player_row(cls,player_row):
        rank, player, *_ = re.findall(r'(\d+) ([a-zA-Z]+\. [a-zA-Z]+ ([a-zA-Z]+){0,1}) ([a-zA-Z]{1,3}) ($\d+) (?:\d+)',player_row)
        rank = re.search(r'(\d+)(?: \w\.)',player_row).group(1)
        player = ''.join(re.findall(r'[\w\s]',re.search(r'(?:\d+ )(\w\. \w+\s{0,1}\w*)(?= \w{2})',player_row).group(1)))
        dollar_value = re.search(r'(?<=\$)(\d+)',player_row).group(0)
        return [rank, player.lower(), dollar_value]
    @classmethod
    def get_rankings(cls,position):
        driver.get(cls.base_url.format(position=position))
        sleep(5)
        rankings = []
        players_block = driver.find_element(By.CLASS_NAME,'player-wrapper')
        players = players_block.find_elements(By.CLASS_NAME,'player-row')
        for player_row in players:
            try:
                rankings.append(cls.split_player_row(player_row.text))
            except:
                print(player_row.text)
        return pd.DataFrame(rankings,columns=['rank','player','dollar_value'])
    @classmethod
    def rankings_main(cls):
        rankings_dict = {}
        for position in ['top200','QB','RB','WR','TE','K','DST']:
            rankings_dict[cls.position_map[position]] =  cls.get_rankings(position)
        return rankings_dict
    
class football_guys:
    base_url = r'https://www.footballguys.com/rankings?pos={position}#more'
    position_map = {'all':'consensus',
                    'qb':'qb',
                    'rb':'rb',
                    'wr':'wr',
                    'te':'te',
                    'pk':'k',
                    'td':'dst'}
    @classmethod
    def split_player_row(cls,player_row):
        rank, player_team, _, pos_stats = re.split(r'\n',player_row)
        *player, team = re.split(' ',player_team.lower())
        player = ''.join(re.findall(r'[\w\s]',' '.join(player)))
        pos, points, ros_games, *_ = re.split(' ',pos_stats.lower())
        return [rank, player, team, points, ros_games]
    @classmethod
    def get_rankings(cls,position):
        driver.get(cls.base_url.format(position=position))
        sleep(5)
        rankings = []
        players = driver.find_elements(By.CLASS_NAME,'player-row')
        for player_row in players:
            try:
                rankings.append(cls.split_player_row(player_row.text))
            except:
                print(player_row.text)
        return pd.DataFrame(rankings,columns=['rank','player','team','points','ros_games'])
    @classmethod
    def rankings_main(cls):
        rankings_dict = {}
        for position in ['all','qb','rb','wr','te','pk','td']:
            rankings_dict[cls.position_map[position]] =  cls.get_rankings(position)
        return rankings_dict

class stats_2022_season:
    def __init__(self):
        self.datasets = ['advanced_air_yards','fantasy','fantasy_rz','passing','receiving','rushing']
        self.data = {}
    def get_all_datasets(self):
        for ds in self.datasets:
            #response = requests.get(fr'https://github.com/bschleter/football_stats/blob/main/cleanstats/{ds}.csv')
            #response_content = response.content
            self.data[ds] = pd.read_csv(fr'https://raw.githubusercontent.com/bschleter/football_stats/main/cleanstats/{ds}.csv')
            
class pro_football_reference:
    player_base_url = r'https://www.pro-football-reference.com/players'
    team_base_url = r'https://www.pro-football-reference.com/teams'
    valid_positions = {'rb':['rushing_and_receiving','receiving_and_rushing'],
                       'k':'kicking',
                       'wr':['receiving_and_rushing','rushing_and_receiving'],
                       'qb':'passing',
                       'te':['receiving_and_rushing','rushing_and_receiving']}
    teams = {}
    players = {}
    team_stats = {}
    player_stats_summary = {}
    player_stats_detail = {}
    player_fantasy_summary = {}
    player_fantasy_detail = {}
    page_load_delay = 1
    @staticmethod
    def get_headers(block):
        headers_list = []
        header_table = block.find_element(By.XPATH,'thead')
        header_row = header_table.find_elements(By.TAG_NAME,'tr')
        for i in range(len(header_row)):
            sub_headers_suffixes = []
            headers_data = header_row[i].find_elements(By.TAG_NAME,'th')
            for j in range(len(headers_data)):
                if header_row[i].get_attribute('class') == 'over_header':
                    sub_headers_suffixes.extend([headers_data[j].text]*int(headers_data[j].get_attribute('colspan')))
                else:
                    sub_headers_suffixes.append(headers_data[j].text)
            headers_list.append(sub_headers_suffixes)
        headers = [('_'.join(list(filter(None,h)))).replace(' ','_').lower() for h in zip(*headers_list)]
        return headers
    @staticmethod
    def get_data(block):
        data = []
        data_table = block.find_element(By.XPATH,'tbody')
        data_rows = data_table.find_elements(By.TAG_NAME,'tr')
        for i in range(len(data_rows)):
            data_row = []
            first = data_rows[i].find_element(By.TAG_NAME,'th').text
            data_row.append(first)
            row_stats = data_rows[i].find_elements(By.TAG_NAME,'td')
            for j in range(len(row_stats)):
                if (data_text:=row_stats[j].text.lower()) == 'inactive':
                    data_row.extend(['']*row_stats[j].get_attribute('colspan'))
                else:
                    data_row.append(data_text)
            if data_row:
                data.append(data_row)
        return data
    @staticmethod
    def get_position(driver):
        player_info_block = driver.find_element(By.CLASS_NAME,'players').find_element(By.ID,'meta')
        player_info = player_info_block.find_elements(By.TAG_NAME,'div')[1]
        player_position = re.search(r'(?<=Position: )\w+(?= )',player_info.text).group(0).lower()
        return player_position
    @classmethod
    def get_active_teams(cls):
        driver.get(cls.team_base_url)
        sleep(cls.page_load_delay)
        all_teams_block = driver.find_element(By.ID,'all_teams_active')
        active_teams_block = all_teams_block.find_element(By.ID,'teams_active')
        team_names_block = active_teams_block.find_element(By.XPATH,'tbody')
        team_rows = team_names_block.find_elements(By.TAG_NAME,'tr')
        for i in range(len(team_rows)):
            if team_rows[i].get_dom_attribute('class') is None:
                try:
                    team = team_rows[i].find_element(By.TAG_NAME,'th')
                    team_name = (team.text).lower()
                    team_link = re.search(r'(?<=teams).+',team.find_element(By.PARTIAL_LINK_TEXT,team.text).get_attribute('href')).group(0)
                except:
                    print(f'Error with {(team.text).lower()}')
                else:
                    cls.teams[team_name] = team_link
    @classmethod
    def get_team_info(cls,team_list):
        team_list = [t.lower() for t in team_list]
        for team in team_list:
            driver.get(cls.team_base_url+cls.teams[team])
            sleep(cls.page_load_delay)
            table_block = driver.find_element(By.CLASS_NAME,'table_wrapper')
            team_info_block = table_block.find_element(By.ID,'team_index')
            headers = pro_football_reference.get_headers(team_info_block)
            data = pro_football_reference.get_data(team_info_block)
            if data:
                cls.team_stats[team] = pd.DataFrame(data,columns=headers)
    @classmethod
    def get_active_players(cls):
        for letter in cls.alphabet:
            driver.get(fr'{cls.player_base_url}/{letter.upper()}/')
            sleep(cls.page_load_delay)
            all_players_block = driver.find_element(By.ID,'all_players')
            player_content = all_players_block.find_element(By.CLASS_NAME,'section_content')
            all_player_rows = player_content.find_elements(By.TAG_NAME,'p')
            for i in range(len(all_player_rows)):
                try:
                    active_player = all_player_rows[i].find_element(By.TAG_NAME,'b')
                except:
                    continue
                else:
                    player_name = ''.join(re.findall(r'[\w\s]',re.search(r"[\w\s\.\'\-]+(?= \([\w\-\/\\]*\))",active_player.text).group(0).lower()))
                    player_position = re.search(r'(?<= \()[\w\-\/\\]*(?=\))',active_player.text).group(0).lower()
                    if any(p in player_position for p in cls.valid_positions.keys()):
                        player_link = re.search(r'(?<=players).+',active_player.find_element(By.TAG_NAME,'a').get_attribute('href')).group(0)
                        cls.players[player_name] = player_link
    @classmethod
    def get_player_info(cls,player_list,year_list):
        year_list = [str(y) for y in year_list]
        player_list = [p.lower() for p in player_list]
        for player in player_list:
            driver.get(cls.player_base_url+cls.players[player])
            sleep(cls.page_load_delay)
            cls.get_player_stats_summary(player,driver)
            cls.get_player_stats_detail(player,driver,year_list)
            cls.get_player_fantasy_summary(player,driver)
            cls.get_fantasy_detail(player,year_list)
    @classmethod
    def get_player_stats(cls,player,driver):
        position = pro_football_reference.get_position(driver)
        try:
            player_stats_block = driver.find_element(By.ID,cls.valid_positions[position[0]])
        except:
            player_stats_block = driver.find_element(By.ID,cls.valid_positions[position[1]])
        headers = pro_football_reference.get_headers(player_stats_block)
        data = pro_football_reference.get_data(player_stats_block)
        if data:
            cls.player_stats_summary[player] = pd.DataFrame(data,columns=headers)
    @classmethod
    def get_player_fantasy_summary(cls,player,driver):
        player_fantasy_block = driver.find_element(By.ID,'fantasy')
        headers = pro_football_reference.get_headers(player_fantasy_block)
        data = pro_football_reference.get_data(player_fantasy_block)
        if data:
            cls.player_fantasy_summary[player] = pd.DataFrame(data,columns=headers)
    @classmethod
    def get_player_fantasy_detail(cls,player,year_list):
        for y in year_list:
            try:
                driver.get(cls.player_base_url+cls.players[player].replace('.htm',f'/fantasy/{y}'))
                sleep(cls.page_load_delay)
            except:
                continue
            else:
                fantasy_stats_block = driver.find_element(By.ID,'player_fantasy')
                headers = pro_football_reference.get_headers(fantasy_stats_block)
                data = pro_football_reference.get_data(fantasy_stats_block)
                if data:
                    cls.player_fantasy_detail[player] = pd.DataFrame(data,columns=headers)
    @classmethod
    def get_player_stats_detail(cls,player,year_list):
        for y in year_list:
            try:
                driver.get(cls.player_base_url+cls.players[player].replace('.htm',f'/gamelog/{y}'))
                sleep(cls.page_load_delay)
            except:
                continue
            else:
                fantasy_stats_block = driver.find_element(By.ID,'stats')
                headers = pro_football_reference.get_headers(fantasy_stats_block)
                data = pro_football_reference.get_data(fantasy_stats_block)
                if data:
                    cls.player_stats_detail[player] = pd.DataFrame(data,columns=headers)
    @classmethod
    def get_player_stats_advanced_detail(cls,player,year_list):
        for y in year_list:
            try:
                driver.get(cls.player_base_url+cls.players[player].replace('.htm',f'/gamelog/{y}/advanced'))
                sleep(cls.page_load_delay)
            except:
                continue
            else:
                position = pro_football_reference.get_position(driver)
                try:
                    fantasy_stats_block = driver.find_element(By.ID,'advanced_'+cls.valid_positions[position[0]])
                except:
                    fantasy_stats_block = driver.find_element(By.ID,'advanced_'+cls.valid_positions[position[1]])
                headers = pro_football_reference.get_headers(fantasy_stats_block)
                data = pro_football_reference.get_data(fantasy_stats_block)
                if data:
                    cls.player_stats_detail[player] = pd.DataFrame(data,columns=headers)
    @classmethod
    def main(cls,year_list):
        cls.get_active_teams()
        cls.get_active_players()
        cls.get_team_info(list(cls.teams.keys()), year_list)
        cls.get_player_info(list(cls.players.keys()), year_list)