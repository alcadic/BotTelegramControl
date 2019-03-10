# -*- coding: utf-8 -*-
#!/usr/bin/python

import time
import telebot
import emoji
from emoji import emojize
from telebot import types
import commands

#Variables de configuracion
TOKEN_BOT_FATHER = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx'
bot = telebot.TeleBot(TOKEN_BOT_FATHER)
idDevice = 00000000

#Variables de iconos
cake = emojize(":cake:", use_aliases=True)
back = emojize(":back:", use_aliases=True)
tv = emojize(":tv:", use_aliases=True)
sol = emojize(":sunny:", use_aliases=True)
temp = emojize(":fish_cake:", use_aliases=True)
tvOnOff = emojize(":o2:", use_aliases=True)
tvUp = emojize(":arrow_up:", use_aliases=True)
tvDown = emojize(":arrow_down:", use_aliases=True)
tvSiguiente = emojize(":arrow_right:", use_aliases=True)
tvAnterior = emojize(":arrow_left:", use_aliases=True)
acOnOff = emojize(":o:", use_aliases=True)
acUp = emojize(":arrow_up_small:", use_aliases=True)
acDown = emojize(":arrow_down_small:", use_aliases=True)

#Funcion que determinar que device puede operar
def permiso(message):
	variable = False

	if message.chat.id == idDevice:
		variable = True
	else:
		variable = False

	return variable


#Funcion de inicio de BOT
@bot.message_handler(commands=["start"])
def keyboard (message):

	print(message.chat.id)
	if permiso(message):
		menu(message)

################################################### FUNCIONES QUE PINTAN EL TECLADO Y SUBTECLADOS ############################################################

#Funcion del teclado principal
def menu (message):

	if permiso(message):
                key = types.ReplyKeyboardMarkup()
                key.row(tv, sol, temp)
		bot.send_message(message.chat.id, "Accediendo al Menu principal",reply_markup=key)

#Funcion teclado submenu television
def submenuTV (message):
	key = types.ReplyKeyboardMarkup()
        key.row(tvOnOff, tvSiguiente, tvAnterior)
	key.row(tvUp, tvDown, back)
        bot.send_message(message.chat.id, "Accediendo al menu de control TV",reply_markup=key)

#Funcion teclado submenu aire acondicionado
def submenuAC (message):
        key = types.ReplyKeyboardMarkup()
        key.row(acOnOff, back)
        key.row(acUp, acDown)
        bot.send_message(message.chat.id, "Accediendo al menu de control AC",reply_markup=key)

#Funcion teclado submenu temperatura
def submenuTEMP (message):
        key = types.ReplyKeyboardMarkup()
        key.row('Temp.Actual', 'Informe Temp', back)
        bot.send_message(message.chat.id, "Accediendo al menu de Temperatura",reply_markup=key)


########################################################## GESTION DE LOS TECLADOS DEL SISTEMA #############################################################

#Funcion que gestiona las llegadas de texto
@bot.message_handler(content_types=["text"])
def handle_text(message):
	if permiso(message):
		instruccion = message.text

######################################################## INSTRUCCIONES TECLADO PRINCIPAL ########################################################
		if instruccion == tv:
			print("Accediendo a submenu de la TV")
			submenuTV(message)

		elif instruccion == sol:
			print("Accediendo a submenu del Aire Acondicionado")
			submenuAC(message)

		elif instruccion == temp:
        	        print("Accediendo a submenu de temperaturas")
			submenuTEMP(message)

########################################################## INSTRUCCIONES SUBTECLADO DE LA TELEVISION ##############################################
                elif instruccion == tvOnOff:
                        ret = commands.getoutput("irsend SEND_ONCE tv KEY_POWER")

                elif instruccion == tvUp:
                        ret = commands.getoutput("irsend SEND_ONCE tv KEY_VOLUMEUP")

                elif instruccion == tvDown:
                        ret = commands.getoutput("irsend SEND_ONCE tv KEY_VOLUMEDOWN")

                elif instruccion == tvSiguiente:
                        ret = commands.getoutput("irsend SEND_ONCE tv KEY_CHANNELUP")

                elif instruccion == tvAnterior:
                        ret = commands.getoutput("irsend SEND_ONCE tv KEY_CHANNELDOWN")


################################################### INSTRUCCIONES SUBTECLADO DEL AIRE ACONDICIONADO ##############################################

####################################################### INSTRUCCIONES SUBTECLADO DE LAS TEMPERATURAS ##############################################
                elif instruccion == 'Temp.Actual':
			ret = commands.getoutput("tail -n1 PATH/log_temperatura_salon.txt")
			bot.send_message(message.chat.id, "La ultima temperatura es:\n"+ret)

		elif instruccion == 'Informe Temp':
			ret = commands.getoutput("tail -n15 PATH/logs/log_temperatura_salon.txt")
			bot.send_message(message.chat.id, "Las ultimas 15 temperaturas son:\n"+ret)

		else:
			print("subMenu GENERICO")



#Para que no se apague la escucha
bot.polling(none_stop=True, interval=1)