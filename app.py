import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.handler import SkipHandler
import gspread
import random
import requests
import json

# tickets
tickets = random.sample(range(1000000000, 9999999999), 100)

# gs
gc = gspread.service_account(filename='.\\cryptovaganza-49bcfa2d9193.json')
sh = gc.open_by_key('1S7U57iLphNp0kaJN9jwDBtFZ5hAPcmF60Xn8Tgaz-EE')
worksheet = sh.sheet1

# resultVar- []
resultVar = ''

# token bot
API_TOKEN = '2133919712:AAF0uTpRzvd0lbrgFCqcuFyUjTve40iNUUQ'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=3)

    btns_text = ('💰 Balance', '🎁 Prize', '🎟 Raffle Ticket')
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))

    more_btns_text = (
        "🟢 Digifinex",
        "🟢 Metamask",
        "🟢 DGP Ecosystem",
        "📢 Confirmation",
        "🛒 Buy Tickets",
    )
    keyboard_markup.add(*(types.KeyboardButton(text) for text in more_btns_text))
    
    btns_text = ('🎁 Winner Draw Schedule', '💶 WITHDRAW')
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
    
    terms = \
        """
➖ Participant is required above 18 Years old 
➖ Do your research before buy any cryptocurrency 
➖ The information provided on this Bot does not constitute investment advice, financial advice, trading advice, or any other sort of advice and you should not treat any of the bot content as such. <b>CryptoExtravaganza</b> bot does not recommend that any cryptocurrency should be bought, sold, or held by you. Do conduct your own due diligence and consult your financial advisor before making any investment decisions.
        """
    othersText1 = \
        """
🎊 <b>Promo Periode</b> 🎊
December 1, 2021 - May 30, 2022

🎁 <b>Winner announcement</b> 🎁
The winner Will announce on official web and the bot on May 31, 2021
        """
        
    othersText2 = \
        """
🎟 <b>Buy Ticket</b>

4 TICKET 100 USDT
10 TICKET 200 USDT
        """
        
    othersText3 = \
        """
↗️ <b>Sent USDT to this  address with TRC20 network:</b>\n
<pre>TFf7frw1b9WE7c6s6EaoNVhe5YPma4EWR5</pre>

        """
        
    await message.reply("Hi! <b>{}</b> \n\n<b>🎁🎊 Welcome to CryptoExtravaganza 🎊🎁</b>\n\nBy clicking Start you are agree with our term and agreement.\n\n<b>Term and Agreement:</b>\n{}".format(message["from"]["first_name"], terms), reply_markup=keyboard_markup, parse_mode="HTML")
    # await message.answer(f"{othersText1}", parse_mode="HTML")
    # await message.answer(f"{othersText2}", parse_mode="HTML")
    # await message.answer(f"{othersText3}", parse_mode="HTML")

@dp.message_handler(text_contains='💰 Balance')
@dp.message_handler(text_contains='🎁 Prize')
@dp.message_handler(text_contains='🎟 Raffle Ticket')
@dp.message_handler(text_contains='🟢 Digifinex')
@dp.message_handler(text_contains='🟢 Metamask')
@dp.message_handler(text_contains='🟢 DGP Ecosystem')
@dp.message_handler(text_contains='📢 Confirmation')
@dp.message_handler(text_contains='🛒 Buy Tickets')
@dp.message_handler(text_contains='🎁 Winner Draw Schedule')
@dp.message_handler(text_contains='💶 WITHDRAW')
async def inline_kb_answer_callback_handler(msg: types.Message):
    context = msg.text
    
    global resultVar # global variable
    
    if '💰 Balance' == context:
        s = requests.Session()
        pair = s.get("https://api.digifinex.com/kline/history?symbol=DGP_USDT")
        price = json.loads(pair.text)["o"][-1]
        
        cell = worksheet.find("{}".format(msg["from"]["id"]))
        
        # check cell
        if cell:
            balance = worksheet.get(f'I{cell.row}').first()
            # print(balance)

            if balance:
                price_ = balance
                balance = price * int(price_)
            
            setText = "Your Balance <b>{}</b> USDT".format(balance)
            resultVar = context
            await msg.answer(setText, reply_markup=types.ReplyKeyboardMarkup([['/start']]), parse_mode="HTML")
            
        else:
            await msg.answer("Your account has not been activated, please buy tickets", reply_markup=types.ReplyKeyboardMarkup([['/start']]), parse_mode="HTML")
            
    elif '🎁 Prize' == context:
        await msg.answer_photo("https://asset.kompas.com/crops/9ylfBy0J6rKhyWU3LUZWRy3tlYg=/90x0:720x420/750x500/data/photo/2020/07/06/5f02951cc4187.jpg", caption="Pajero sport")
        await msg.answer_photo("https://www.cyberdyne.com.ng/wp-content/uploads/2020/10/Apple-Mac-Book-Pro-3.jpg", caption="Laptop Apple")
        await msg.answer_photo("https://m.media-amazon.com/images/I/91hT4Y3BwyL._AC_SX522_.jpg", caption="Iphone")

    elif '🎟 Raffle Ticket' == context:
        cell = worksheet.find("{}".format(msg["from"]["id"]))
        
        # check cell
        if cell:
            ticket = worksheet.row_values("{}".format(cell.row))
            
            # check status
            status = worksheet.row_values("{}".format(cell.row))
            if 1 == int(status[9]):
                for tic in ticket[10:]:
                    setText = "🎫 <b>{}</b>".format(tic)
                    await msg.answer(setText, reply_markup=types.ReplyKeyboardMarkup([['/start']]), parse_mode="HTML")
            else:
                await msg.answer("Your account has not been activated, please buy tickets", reply_markup=types.ReplyKeyboardMarkup([['/start']]), parse_mode="HTML")
                
        else:
            await msg.answer("Your account has not been activated, please buy tickets", reply_markup=types.ReplyKeyboardMarkup([['/start']]), parse_mode="HTML")
            
        resultVar = context
        
    elif '🟢 Digifinex' == context:
        await msg.answer('<b>HOW TO CREATE <a href="https://www.youtube.com/watch?v=_RePomx2-Ls">DIGIFINEX ACCOUNT</a></b>', parse_mode="HTML", disable_web_page_preview=True)
        resultVar = context
        
    elif '🟢 Metamask' == context:
        await msg.answer('<b>HOW TO CREATE <a href="https://www.youtube.com/watch?v=ivUC1z8vJrM">METAMASK</a></b>', parse_mode="HTML", disable_web_page_preview=True)
        resultVar = context
        
    elif '🟢 DGP Ecosystem' == context:
        await msg.answer('<b><a href="https://www.youtube.com/watch?v=LFn-a0TrBW4">DGP(DGPayment) ECOSYSTEM</a></b>', parse_mode="HTML", disable_web_page_preview=True)
        resultVar = context
        
    elif '📢 Confirmation' == context:
        cell = worksheet.find("{}".format(msg["from"]["id"]))
        # check cell
        if cell:
            setText = '📢 <b>Confirmation</b>\n\n<b>⚠️ Note: Please note that you cannot replace the proof of transaction.</b>'
            await msg.answer(setText, reply_markup=types.ReplyKeyboardMarkup([['/start']]), parse_mode="HTML")
        else:
            await msg.answer("Your account has not been activated, please buy tickets", reply_markup=types.ReplyKeyboardMarkup([['/start']]), parse_mode="HTML")
        
        resultVar = context
        
    elif '🛒 Buy Tickets' == context:
        setText = \
"""
🛒 <b>Buy Tickets</b>

100 - 4 🎟 Ticket 
200 - 10 🎟 Ticket
300 - 20 🎟 Ticket
400 - 30 🎟 Ticket
500 - 40 🎟 Ticket
600 - 50 🎟 Ticket
700 - 60 🎟 Ticket
800 - 70 🎟 Ticket
900 - 80 🎟 Ticket
1000 - 100 🎟 Ticket
1,500 - 200 🎟 Ticket
2,000 - 500 🎟 Ticket

<b>* Ex. Format</b>

<pre>Jhone java
jhoneJaya@yahoo.com
+6285600900
DIGIFINEX-ID
4</pre>

↗️ <b>Sent USDT to this  address with TRC20 network:</b>\n
<pre>TFf7frw1b9WE7c6s6EaoNVhe5YPma4EWR5</pre>
"""
        resultVar = context
        
        await msg.answer(setText, reply_markup=types.ReplyKeyboardMarkup([['/start']]), parse_mode="HTML")
        
    elif '🎁 Winner Draw Schedule' == context: # 🎁 Winner Annoucement
        setText = '🎁 <b>Winner Annoucement</b>\n\n<b>1st Periode</b>\n\nRaffle Draws: 10 PM EST (Canada Time)\n🔸 Dec. 18, 2021.\n🔸 Jan. 22, 2022\n🔸 Feb. 26, 2022 \n🔸 Mar. 26, 2022\n🔸 Apr. 30, 2022\n🔸 May 28, 2022\n🔸 June 25, 2022 Final Draw'
        
        await msg.answer(setText, reply_markup=types.ReplyKeyboardMarkup([['/start']]), parse_mode="HTML")
        
    elif '💶 WITHDRAW' == context:
        cell = worksheet.find("{}".format(msg["from"]["id"]))
        resultVar = context
        
        if cell:
            setText = '💶 WITHDRAW\n\nInput your <b>ERC20 WALLET</b> address <b>(Metamask, Trustwallet, or any ERC20 Wallet)</b>\n\n<b>*Note:</>\nYou are able to withdraw your DGP Balance on May 31, 2022 after winner for Grand Prize has been announced'
            await msg.answer(setText, reply_markup=types.ReplyKeyboardMarkup([['/start']]), parse_mode="HTML")
        else:
            await msg.answer("Your account has not been activated, please buy tickets", reply_markup=types.ReplyKeyboardMarkup([['/start']]), parse_mode="HTML")

@dp.message_handler()
async def requestMesg(msg: types.Message):

    # Buy Tickets
    if '🛒 Buy Tickets' == resultVar:
        data = msg.text.split('\n')
        
        tel_id = msg["from"]["id"]
        
        # insert-number
        values_list = worksheet.col_values(1)
        n = len(values_list) + 1
        
        # check status
        cell = worksheet.find("{}".format(msg["from"]["id"]))
        if cell:
            await msg.answer("<b>You have made an order, please send proof of Payment</b>", reply_markup=types.ReplyKeyboardMarkup([['/start']]), parse_mode="HTML")
        else:
            # update
            try:
                worksheet.batch_update([{
                    'range': 'A{0}:B{0}'.format(n),
                    'values': [[n-1,'{}'.format(data[0])]],
                }, {'range': 'C{0}:D{0}'.format(n),
                    'values': [['{}'.format(data[1]), '{}'.format(data[2])]]
                    
                }, {'range': 'E{0}:F{0}'.format(n),
                    'values': [['{}'.format(data[3]), f'{tel_id}']]
                }, {'range': f'G{n}',
                    'values': [['{}'.format(data[4])]]
                }, {'range': f'J{n}',
                    'values': [[0]]
                }, {'range': f'L{n}',
                    'values': [
                        random.sample(tickets, int(data[4]))
                    ]
                }
                ])
                
                await msg.answer("<b>Thanks!</b>🎊 You have successfully placed an order, please make a payment and confirm the purchase by pressing the <b>Confirmation</b> button.", reply_markup=types.ReplyKeyboardMarkup([['/start']]), parse_mode="HTML")
                
            except:
                await msg.answer("Wrong Format.", reply_markup=types.ReplyKeyboardMarkup([['/start']]))
        
    elif '📢 Confirmation' == resultVar:
        cell = worksheet.find("{}".format(msg["from"]["id"]))
        
        # try:
        #     worksheet.update(f'H{cell.row}', msg.text)
        #     status = True
        # except:
        #     status = False
        
        if cell:
            if (worksheet.get('H{}'.format(cell.row)).first()):
                await msg.answer("Sorry you have sent proof of previous payment transactions. If you experience problems, please contact admin.", parse_mode="HTML")
            else:
                worksheet.update(f'H{cell.row}', msg.text)
                await msg.answer("<b>Successfully confirmed!</b>. Please be patient, we will do an inspection in a few minutes.", reply_markup=types.ReplyKeyboardMarkup([['/start']]), parse_mode="HTML")
        else:
            await msg.answer("You cannot use the Confirmation feature at this time. please <b>Buy Tickets</b>", parse_mode="HTML")
            
    elif '💶 WITHDRAW' == resultVar:
        cell = worksheet.find("{}".format(msg["from"]["id"]))
        
        if cell:
            worksheet.update(f'K{cell.row}', msg.text)
        else:
            await msg.answer("You cannot use the withdrawal feature at this time. please <b>Buy Tickets</b>", parse_mode="HTML")
    else:
        await msg.answer("🚫 Invalid")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
