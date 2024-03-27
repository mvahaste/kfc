from facebook_scraper import get_posts, _scraper
import json
from re import search
from discord import Client, Intents, Embed
from random import choice
import json


def get_special():
    with open("./mbasicHeaders.json", "r") as file:
        _scraper.mbasic_headers = json.load(file)

    for post in get_posts("KFCEst", base_url="https://mbasic.facebook.com", start_url=f"https://mbasic.facebook.com/KFCEst?v=timeline", pages=1):
        if ("sooduskood" not in post["full_text"].lower().strip()):
            continue

        full_text = post["full_text"]
        image_url = post["image"]

        return (full_text, image_url)


def get_code_desc(text):
    code = ""
    desc = ""

    lines = text.splitlines()

    for line in lines:
        # Get code
        if (search("(sooduskood) \d{5}", line.lower())):
            code = line.strip()

        # Get description
        if (search("€|%|(\d=\d)", line)):
            desc = line.strip()

    return (code, desc)

def random_message(message_type: str) -> str:
    """Return a random message for the discord embed"""
    good_messages: list[str] = [
        "süüa saab",
        "paul on juba kohal",
        "kfc > mc",
        "jooksuga nyyd",
        "mmgnhghm",
        "kfc fact: kfc on kfc",
        "nämm",
    ]

    bad_messages: list[str] = [
        "tra kui siin ketšup on",
        "hakkan juba lootust kaotama",
        "mida vittu",
        "täna vist ei söö",
        "lähme vb mci?",
    ]

    if message_type == "good":
        return choice(good_messages)
    else:
        return choice(bad_messages)


def random_emoji(message_type: str) -> str:
    """Return a random emoji"""
    good_emojis: list[str] = [
        ":poultry_leg:",
        ":chicken:",
        ":exclamation:",
        ":bangbang:",
        ":fries:",
        ":goat:",
    ]

    bad_emojis: list[str] = [
        ":bone:",
        ":skull:",
        ":pensive:",
        ":weary:",
        ":sob:",
    ]

    if message_type == "good":
        return choice(good_emojis)
    else:
        return choice(bad_emojis)


def send_special(code, desc, image, dev):
    config = {}

    # Load config.json
    with open("config.json", "r") as f:
        config = json.load(f)

    token = config["discord_token"]
    channel = config["discord_channel" + ("_dev" if dev else "")]
    role = config["discord_role" + ("_dev" if dev else "")]

    client = Client(intents=Intents.default())

    @client.event
    async def on_ready():
        print(f"{client.user} has connected to Discord!")

        # Print the guilds (servers) the bot is connected to
        for guild in client.guilds:
            print(f"{client.user} is connected to the following guild: {guild.name}(id: {guild.id})")

        # Create the embed
        embed = Embed(
            color=0xFF0000,
            title=code,
            description=desc,
        )

        # Set the image
        embed.set_image(url=image)

        # Get the messsage type (good or bad, 50/50 chance)
        message_type = choice(["good" * 2, "bad"])

        # Set the content
        content = f"<@&{role}> " + random_message(message_type) + " " + random_emoji(message_type)

        # Send message to channel
        await client.get_channel(channel).send(content=content, embed=embed)

        await client.close()

    client.run(token)

    # Call the previous function
    on_ready()
