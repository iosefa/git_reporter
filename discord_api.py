import discord
import asyncio
import config
from asyncio import Queue

intents = discord.Intents.default()
client = discord.Client(intents=intents)
message_queue = Queue()


async def send_message():
    """
    Sends a message to a specified Discord channel.

    :return: None
    """
    await client.wait_until_ready()
    while not client.is_closed():
        message, name, repo = await message_queue.get()
        report = f'Developer report for {name} [{repo}]\n' + message
        try:
            channel = await client.fetch_channel(config.DISCORD_CHANNEL_ID)
            await channel.send(report)
        except discord.NotFound:
            print("Channel not found.")
        except discord.Forbidden:
            print("Permission denied.")
        except discord.HTTPException as e:
            print(f"HTTP exception: {e}")
        message_queue.task_done()


@client.event
async def on_ready():
    """
    Method to handle the "on_ready" event.

    :return: None
    """
    print(f'{client.user} has connected to Discord!')
    client.loop.create_task(send_message())


def run_bot():
    """
    Runs the bot using the Discord Bot Token from the config file.

    :return: None
    """
    client.run(config.DISCORD_BOT_TOKEN)


def queue_message(message, name, repo):
    """
    Queues a message to be sent.

    :param message: The message to be sent.
    :param name: The name of the sender.
    :param repo: The repository to which the message belongs.
    :return: None
    """
    asyncio.run_coroutine_threadsafe(message_queue.put((message, name, repo)), client.loop)


async def shutdown_discord():
    """
    Closes the discord client and the underlying HTTP session (if any).

    :return: None
    """
    await client.close()
    if client._connection.http._session:
        await client._connection.http._session.close()


def stop_bot():
    """
    Stop the bot.

    :return: None
    """
    asyncio.run_coroutine_threadsafe(shutdown_discord(), client.loop)
