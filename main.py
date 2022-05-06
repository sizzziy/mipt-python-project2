import telebot
import urllib
from database_contol import DatabaseControl
#import requests
#from bs4 import BeautifulSoup
bot = telebot.TeleBot('750969561:AAE7Rxa7ioKMdv2TtF42T-xm5WbW7MiRdFE')

def parse(size, data, uid):
    if not isinstance(size, str):
        return 1 # size not str
    if not isinstance(data, str):
        return 2 # data not str
    data = urllib.parse.quote(data)
    if not size.isnumeric():
        return 3 # size not number
    if not (128 <= int(size) <= 1024):
        return 4 # bad size
    if len(str(data)) > 1000:
        return 5 # bad data length
    urlstart = 'https://api.qrserver.com/v1/create-qr-code/?size='
    url = urlstart + str(size)+ 'x' + str(size) + '&data=' + data
    f = open('out' + str(uid) + '.jpg','wb')
    f.write(urllib.request.urlopen(url).read())
    f.close()
    return 'out' + str(uid) + '.jpg'

images = []
users = {}

welcome_message = "Welcome to QR code generator bot!"
plans_message = '''You have BASIC plan, it allows you 5 FREE generations. 
If you want to upgrade to PRO plan or buy more generations, please, contact @sizzziy'''
advert_message = 'If you want to upgrade to PRO plan or buy more generations, contact @sizzziy'
left_message = "You have {} generations left."
send_message = "Send me size (in pixels) of your QR code."

@bot.message_handler(content_types=['text'])
def start(message):
    uid = message.from_user.id
    if message.text == '/start':
        if not database.check_uid(uid):
            bot.send_message(message.from_user.id, welcome_message);
            bot.send_message(message.from_user.id, plans_message);
            database.add_user(uid, 'basic', 5)
        elif database.get_plan(uid) == 'basic' and database.get_codes_left(uid) <= 0:
            bot.send_message(message.from_user.id, left_message.format(0));
            bot.send_message(message.from_user.id, advert_message);
            return
        bot.send_message(message.from_user.id, left_message.format(database.get_codes_left(uid)));
        bot.send_message(message.from_user.id, send_message);
        bot.register_next_step_handler(message, get_size);
    else:
        bot.send_message(message.from_user.id, 'To begin send /start');

def get_size(message):
    uid = message.from_user.id
    size = message.text;
    users[uid] = size
    bot.send_message(message.from_user.id, 'Now send me text you want to encode.');
    bot.register_next_step_handler(message, get_data);

size_not_str_error = 'Error: your size is not string'
data_not_str_error = 'Error: your text is not string'
size_not_int_error = 'Error: your size is not integer'
bad_size = 'Error: size must be in range [128, 1024]'
data_size = 'Error: data is too long'

def get_data(message):
    uid = message.from_user.id
    data = message.text;
    size = users[uid]
    bot.send_message(message.from_user.id, 'Generating...');
    res = parse(size, data, uid)
    if res == 1:
        bot.send_message(message.from_user.id, size_not_str_error);
    elif res == 2:
        bot.send_message(message.from_user.id, data_not_str_error);
    elif res == 3:
        bot.send_message(message.from_user.id, size_not_int_error);
    elif res == 4:
        bot.send_message(message.from_user.id, bad_size);
    elif res == 5:
        bot.send_message(message.from_user.id, data_size);
    else:
        bot.send_chat_action(message.chat.id, 'upload_photo')
        try:
            img = open(res, 'rb')
            bot.send_photo(message.chat.id, img)
            img.close()
            database.change_codes_left(uid, -1)
        except:
            print("error")

database = DatabaseControl()
bot.polling(none_stop=True, interval=0)