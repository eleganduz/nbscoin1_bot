import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from nbscoin_rpc import NBScoinRPC

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

nbscoin_rpc = NBScoinRPC()

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    update.message.reply_text(f"Привет, {user.first_name}! Добро пожаловать в NBScoin бот.")

# Команда /balance
def balance(update: Update, context: CallbackContext) -> None:
    balance = nbscoin_rpc.get_balance()
    update.message.reply_text(f"Ваш баланс: {balance} NBS")

# Команда /new_address
def new_address(update: Update, context: CallbackContext) -> None:
    address = nbscoin_rpc.get_new_address()
    update.message.reply_text(f"Ваш новый адрес: {address}")

# Команда /send
def send(update: Update, context: CallbackContext) -> None:
    try:
        address = context.args[0]
        amount = float(context.args[1])
        txid = nbscoin_rpc.send_to_address(address, amount)
        update.message.reply_text(f"Транзакция отправлена. TXID: {txid}")
    except (IndexError, ValueError):
        update.message.reply_text("Использование: /send <адрес> <количество>")

# Команда /transactions
def transactions(update: Update, context: CallbackContext) -> None:
    txs = nbscoin_rpc.list_transactions()
    if txs:
        response = "\n".join([f"{tx['category']}: {tx['amount']} NBS ({tx['txid']})" for tx in txs])
    else:
        response = "Нет транзакций"
    update.message.reply_text(response)

# Команда /transaction_status
def transaction_status(update: Update, context: CallbackContext) -> None:
    try:
        txid = context.args[0]
        tx = nbscoin_rpc.get_transaction(txid)
        update.message.reply_text(f"Статус транзакции: {tx['confirmations']} подтверждений")
    except (IndexError, ValueError):
        update.message.reply_text("Использование: /transaction_status <txid>")

def main() -> None:
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("balance", balance))
    dispatcher.add_handler(CommandHandler("new_address", new_address))
    dispatcher.add_handler(CommandHandler("send", send))
    dispatcher.add_handler(CommandHandler("transactions", transactions))
    dispatcher.add_handler(CommandHandler("transaction_status", transaction_status))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
