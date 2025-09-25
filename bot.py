import discord
import openai
import os

# Získání API klíčů z prostředí
openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Nastavení oprávnění
intents = discord.Intents.default()
intents.message_content = True  # nutné pro čtení zpráv
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Bot je online jako {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Reakce na zprávy začínající "ai" nebo "!ai"
    if message.content.lower().startswith(("ai", "!ai")):
        prompt = message.content[3:].strip()  # vezme text za "ai" nebo "!ai"
        if prompt == "":
            await message.channel.send("🧠 Napiš mi něco, na co mám odpovědět.")
            return

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            reply = response.choices[0].message.content
            await message.channel.send(reply)
        except Exception as e:
            await message.channel.send(f"⚠️ Chyba při komunikaci s AI: {str(e)}")

client.run(TOKEN)
