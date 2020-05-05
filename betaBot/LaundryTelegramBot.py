#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime, timedelta
from xml.dom import minidom
import requests
import json

#Global variables
bot_token = '1036999260:AAGtpIpwtVSHQB2JakCsfbDpuUko4B0F700'
user_id = ''
user_password=''
telegramID=''

#data loaded from xml to compare
user_id_test=''
user_password_test=''
telegramID_test=''

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

ID, PASSWORD, RESERVATION, BIO = range(4)


def Main_loop(user_id, user_password):
    current_date = datetime.today()
    yesterday_date = (current_date - timedelta(days=1))
    print ("Today is ",current_date)
    xmldoc = minidom.parse('settingsOppilastalo.xml')
    itemlist = xmldoc.getElementsByTagName('User')
    #for s in itemlist:
        #usr=s.attributes['Name'].value
        #pwd=s.attributes['Password'].value
    
    chromedriver = r'C:\Users\saidda\AppData\Local\Programs\Python\Python38-32\Scripts\chromedriver.exe'
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)
    #options.headless=True
    browser = webdriver.Chrome(options=options)

    browser.get('http:\\extranet.oppilastalo.fi/')
    print ("Opened ") 
    sleep(1) 

    username = browser.find_element_by_xpath("/html/body/div/form/table/tbody/tr[3]/td[2]/input")
    username.send_keys(user_id)
    print ("Email Id entered") 
    sleep(1)


    password = browser.find_element_by_xpath("/html/body/div/form/table/tbody/tr[4]/td[2]/input")
    password.send_keys(user_password)
    print ("Password entered") 
    sleep(1)

    print ("Logged in")
    login_box = browser.find_element_by_xpath("/html/body/div/form/table/tbody/tr[5]/td[1]/input")
    login_box.click()

    sleep(1)
    
##    reservations_link = browser.find_element_by_xpath("/html/body/code/a[5]")
##    reservations_link.click()
##    sleep(1)
##
##    reservations_link = browser.find_element_by_xpath("/html/body/blockquote/table/tbody/tr[2]/td[3]")
##    latestReservation = reservations_link.text
##    print(r"Latest reservation has been made for ", latestReservation[:10])
##    if datetime.strptime(latestReservation[:10],"%d.%m.%Y")<yesterday_date:
##        
##        laundry_link = browser.find_element_by_xpath("/html/body/code/a[4]")
##        laundry_link.click()
##        sleep(1)
##
##        next_page = browser.find_element_by_xpath("/html/body/blockquote/table/tbody/tr[1]/td[7]/input")
##        next_page.click()
##        sleep(1)
##
##        #9th row stands for 1pm
##        rowNo = 9
##        while(True):
##            try:
##                element_path = "/html/body/blockquote/table/tbody/tr[{}]/td[8]/input".format(rowNo)
##                reserve = browser.find_element_by_xpath(element_path)
##                reserve.click()
##                sleep(1)
##                confirm = browser.find_element_by_xpath("/html/body/blockquote/submenu/blockquote/input[1]")
##                confirm.click()
##                sleep(1)
##                f = open("ReservationLog.txt", "a")
##                resultString = "\nReservation done for next Sunday, reserved at "
##                f.write(resultString)
##                f.write(str(current_date))
##                print(resultString + str(current_date))
##                f.close()
##            except:
##                rowNo = rowNo+1
##                if rowNo>17:
##
##                    break
##             
##    else:
##        f = open("ReservationLog.txt", "a")
##        resultString = "\nThe reservation is up to date, checked at "
##
##        f.write(resultString)
##        f.write(str(current_date))
##        print(resultString + str(current_date))
##        f.close()
    
    browser.quit()
    

def start(update, context):
    #reply_keyboard = [['ID', 'Password']]


    #get user telegram ID
    
    xmldoc = minidom.parse('UsersDB.xml')
    itemlist = xmldoc.getElementsByTagName('User')
    for s in itemlist:
        global user_id_test
        user_id_test=s.attributes['Name'].value
        global user_password_test
        user_password_test=s.attributes['Password'].value
        global telegramID_test
        telegramID_test= str(s.attributes['TelegramID'].value)
    global telegramID
    telegramID= str(update.message.from_user['id'])
    if telegramID == telegramID_test:
        global user_id
        user_id=user_id_test
        global user_password
        user_password=user_password_test
        reply_keyboard = [[user_id]]
        update.message.reply_text(
        'Hi, we remember you. Click to login '
        'Send /cancel to stop talking to me.\n\n'
        #)
        ,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    else:
        update.message.reply_text(
        'Hi, please log in to the system. Type in your ID first. '
        'Send /cancel to stop talking to me.\n\n'
        )
        #,
        #reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return ID


def getID(update, context):
    user = update.message.from_user
    
    global user_id
    user_id=str(update.message.text)
    logger.info("%s's id is %s", user.first_name, update.message.text)
##    update.message.reply_text('Now type in your password, '
##                              'or send /skip if you don\'t want to.',
##                              reply_markup=ReplyKeyboardRemove())
##
    global telegramID
    global telegramID_test
    print(telegramID)
    print(telegramID_test)
    if telegramID == telegramID_test:
        #global user_id
        user_id=user_id_test
        global user_password
        user_password=user_password_test
        reply_keyboard = [[user_password]]
        update.message.reply_text(
        'Confirm your stored password '
        'Send /cancel to stop\n\n'
        #)
        ,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    else:
        update.message.reply_text('Now type in your password, '
                              ,
                              reply_markup=ReplyKeyboardRemove())

    return PASSWORD


def getPass(update, context):
    user = update.message.from_user
    global user_password
    user_password=str(update.message.text)
    #photo_file = update.message.photo[-1].get_file()
    #photo_file.download('user_photo.jpg')
    logger.info("Password of %s: %s", user.first_name, str(user_password))
    update.message.reply_text('Logging in.. Hold on for a sec..'
                              'or send /skip to roll back..')
    Main_loop(user_id, user_password)
    reply_keyboard = [['Check active'],['Check available']]
    update.message.reply_text('Logged in.. Would you like to check your active reservations or make a new one?' ,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return RESERVATION


def skip_photo(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, '
                              'or send /skip.')

    return RESERVATION


def reservation(update, context):
    user = update.message.from_user
    #user_location = update.message.location
    #logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                #user_location.longitude)
    update.message.reply_text('Forwarding to the selected page..')


    return BIO


def skip_location(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')

    return BIO


def bio(update, context):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            #GENDER: [MessageHandler(Filters.regex('^(ID|Password)$'), gender)],
            ID: [MessageHandler(Filters.text & (~Filters.command), getID)],
            PASSWORD: [MessageHandler(Filters.text & (~Filters.command), getPass),
                    CommandHandler('skip', skip_photo)],

            RESERVATION: [MessageHandler(Filters.text & (~Filters.command), reservation),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text, bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    dp.add_handler(MessageHandler(Filters.command, unknown))
    # log all errors
    dp.add_error_handler(error)

    

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()





