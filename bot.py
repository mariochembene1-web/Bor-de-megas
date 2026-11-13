import telebot

# === COLOCA OS TEUS DADOS AQUI ===
TOKEN = "COLOCA_O_TEU_TOKEN_AQUI"
MPESA = "84XXXXXXX"  # Teu numero M-Pesa
# Tabela de precos
PRECOS = {
    "500MB": 50,
    "1GB": 100,
    "2GB": 180,
    "5GB": 400,
}

bot = telebot.TeleBot(TOKEN)
pendentes = {}

@bot.message_handler(commands=['start', 'tabela'])
def tabela(message):
    texto = "🔥 *VENDA DE MEGAS* 🔥\n\n"
    for pacote, preco in PRECOS.items():
        texto += f"{pacote} = {preco}MT\n"
    texto += f"\nPara comprar: /comprar 1GB\nPaga para M-Pesa: {MPESA}"
    bot.reply_to(message, texto, parse_mode="Markdown")

@bot.message_handler(commands=['comprar'])
def comprar(message):
    try:
        pacote = message.text.split()[1].upper()
        if pacote not in PRECOS:
            bot.reply_to(message, "Pacote invalido! Usa /tabela para ver.")
            return
        preco = PRECOS[pacote]
        user = message.from_user.username or message.from_user.first_name
        pendentes[message.from_user.id] = pacote
        bot.reply_to(message, f"✅ Pedido: {pacote} = {preco}MT\n\n1. Paga {preco}MT para M-Pesa: {MPESA}\n2. Manda aqui o print do comprovativo\n3. Espera confirmacao")
    except:
        bot.reply_to(message, "Usa assim: /comprar 1GB")

@bot.message_handler(content_types=['photo'])
def comprovativo(message):
    pacote = pendentes.get(message.from_user.id, "pacote")
    bot.reply_to(message, f"📸 Comprovativo recebido!\nPacote: {pacote}\n\nAguardar confirmacao do Admin...\nAdmin, para confirmar escreve: /confirmar @{message.from_user.username or message.from_user.first_name}")

@bot.message_handler(commands=['confirmar'])
def confirmar(message):
    bot.reply_to(message, "✅ PAGAMENTO CONFIRMADO!\n\nA enviar megas agora... (ligar ao celular patrao)\n✅ Megas enviados com sucesso! Bom proveito 🔥")

@bot.message_handler(func=lambda m: True)
def todos(m):
    pass

print("Bot ligado em todos os grupos!")
bot.infinity_polling()
