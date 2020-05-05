from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime, timedelta
from xml.dom import minidom
import requests
import json
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import re
#from telegram import ReplyKeyboardMarkup
import telegram

#Global variables
bot_token = '1036999260:AAGtpIpwtVSHQB2JakCsfbDpuUko4B0F700'

import logging
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

reply_keyboard = [['Login', 'Test1'],
                  ['Test2', 'Test3'],
                  ['Disconnect']]
markup = telegram.ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def Main_loop():
    current_date = datetime.today()
    yesterday_date = (current_date - timedelta(days=1))
    print ("Today is ",current_date)
    xmldoc = minidom.parse('settingsOppilastalo.xml')
    itemlist = xmldoc.getElementsByTagName('User')
    for s in itemlist:
        usr=s.attributes['Name'].value
        pwd=s.attributes['Password'].value

        chromedriver = r'C:\Users\saidda\AppData\Local\Programs\Python\Python38-32\Scripts\chromedriver.exe'
        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        options.add_experimental_option("prefs",prefs)
        options.headless=True
        browser = webdriver.Chrome(options=options)

        browser.get('http:\\extranet.oppilastalo.fi/')
        print ("Opened ") 
        sleep(1) 

        username = browser.find_element_by_xpath("/html/body/div/form/table/tbody/tr[3]/td[2]/input")
        username.send_keys(usr)
        print ("Email Id entered") 
        sleep(1)


        password = browser.find_element_by_xpath("/html/body/div/form/table/tbody/tr[4]/td[2]/input")
        password.send_keys(pwd)
        print ("Password entered") 
        sleep(1)

        print ("Logged in")
        login_box = browser.find_element_by_xpath("/html/body/div/form/table/tbody/tr[5]/td[1]/input")
        login_box.click()

        sleep(1)

        reservations_link = browser.find_element_by_xpath("/html/body/code/a[5]")
        reservations_link.click()
        sleep(1)

        reservations_link = browser.find_element_by_xpath("/html/body/blockquote/table/tbody/tr[2]/td[3]")
        latestReservation = reservations_link.text
        print(r"Latest reservation has been made for ", latestReservation[:10])
        if datetime.strptime(latestReservation[:10],"%d.%m.%Y")<yesterday_date:
            
            laundry_link = browser.find_element_by_xpath("/html/body/code/a[4]")
            laundry_link.click()
            sleep(1)

            next_page = browser.find_element_by_xpath("/html/body/blockquote/table/tbody/tr[1]/td[7]/input")
            next_page.click()
            sleep(1)

            #9th row stands for 1pm
            rowNo = 9
            while(True):
                try:
                    element_path = "/html/body/blockquote/table/tbody/tr[{}]/td[8]/input".format(rowNo)
                    reserve = browser.find_element_by_xpath(element_path)
                    reserve.click()
                    sleep(1)
                    confirm = browser.find_element_by_xpath("/html/body/blockquote/submenu/blockquote/input[1]")
                    confirm.click()
                    sleep(1)
                    f = open("ReservationLog.txt", "a")
                    resultString = "\nReservation done for next Sunday, reserved at "
                    f.write(resultString)
                    f.write(str(current_date))
                    print(resultString + str(current_date))
                    f.close()
                except:
                    rowNo = rowNo+1
                    if rowNo>17:
                        #print("No available times for booking on Sunday next week")
                        break
                 
        else:
            f = open("ReservationLog.txt", "a")
            resultString = "\nThe reservation is up to date, checked at "
            #resultString = resultString.format("The reservation is up to date, checked at {}", current_date)
            f.write(resultString)
            f.write(str(current_date))
            print(resultString + str(current_date))
            f.close()
        
        browser.quit()



#def hello(update, context):
#    update.message.reply_text(
#        'Hello {}'.format(update.message.from_user.first_name))
    
def login(update, context):
    update.message.reply_text(
        'Hello {}, feed your email to the bot first'.format(update.message.from_user.first_name))
    text = context.args
    #context.bot.send_message(chat_id=update.effective_chat.id, text="Good")

    
#def echo(update, context):
#    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def test(update, context):
    telegram.pin_chat_message(chat_id=update.effective_chat.id, message_id=update.effective_chat.id, disable_notification=None, timeout=None)

    
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

    
def telegrambot_main():
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    
    updater = Updater(bot_token, use_context=True)
    #updater.dispatcher.add_handler(CommandHandler('hello', hello))

    updater.dispatcher.add_handler(CommandHandler('login', login))
    updater.dispatcher.add_handler(CommandHandler('test', test))
    #updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()
    updater.idle()

#Main_loop()
telegrambot_main()



























