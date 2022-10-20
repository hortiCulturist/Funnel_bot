import os

TOKEN = ''
ADMIN_ID = [433423295, 322420305]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bot_path_name = 'Funnel_bot'

path_to_bot = os.path.join(BASE_DIR, bot_path_name)
path_to_db = os.path.join(BASE_DIR, bot_path_name, 'user_database.db')
path_to_result = os.path.join(BASE_DIR, bot_path_name, 'users.xlsx')