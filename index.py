from telethon import TelegramClient
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import errors
import re

api_id = 'your_api_id'
api_hash = 'your_api_hash'
phone_number = '+84xxxxxxxx'
async def join(session, session_name, link):
    try:
        private = re.match(
            r"(https?://)?(www\.)?t(elegram)?\.(dog|me|org)/joinchat/(.*)", link
        )
        if private:
            await session(ImportChatInviteRequest(private.group(5)))
            print(f"[+] [{session_name}] Joined channel: {link}")
        else:
            await session(JoinChannelRequest(link))
            print(f"[+] [{session_name}] Joined via invite link: {link}")
    except errors.FloodWaitError as e:
        print(f"[-] [{session_name}] Flood wait for {e.seconds} seconds.")
        return False
    except errors.RPCError as e:
        if "The authenticated user is already a participant of the chat" in str(e):
            print(f"[-] [{session_name}] is already a participant of the chat")
            return True
        print(f"[-] [{session_name}] Error: {e}")
        return False
    else:
        return True

session_name = '84xxxxxxxx'
client = TelegramClient(session_name, api_id, api_hash)
async def main():
    await client.start()
    link = 'https://t.me/xxxxxxxx' # public
    link = 'https://t.me/joinchat/XXXXXXXXXXXXXXXXX' # private group
    link = 'https://t.me/joinchat/AAAAAXXXXXXXXXXXX' # private channel
    success = await join(client, session_name, link)
    if success:
        print("Join operation was successful.")
    else:
        print("Join operation failed.")
    await client.disconnect()

with client:
    client.loop.run_until_complete(main())
