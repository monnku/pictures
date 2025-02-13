import os, requests, re, json
import discord
from discord import Intents, Interaction
from discord.app_commands import CommandTree
tok = os.getenv('TOKEN')
ids = [1317333183183978530, 1202104845939515435]
with open("key.txt", mode="r", encoding='utf-8') as f:
    keys = f.read()
with open("data.txt", mode="r", encoding='utf-8') as f:
    datas = f.read()
data = []
for i in range(len(datas)):
    if i % 9 == 0:
        data.append(datas[i:i+8])
key = []
for i in range(len(keys)):
    if i % 2 == 0:
        key.append(keys[i])
class MyClient(discord.Client):
    def __init__(self, intents: Intents) -> None:
        super().__init__(intents=intents)
        self.tree = CommandTree(self)

    async def setup_hook(self) -> None:
        try:
            await self.tree.sync()
            print("Success")
        except Exception as e:
            print(f"Error: {e}")

    async def on_ready(self):
        print(f"Logged in as {self.user}")

intents = Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

@client.tree.command(name="hello", description="Hello, world!")
async def hello(interaction: Interaction):
    await interaction.response.send_message(f'Hello, {interaction.user.mention}')

@client.tree.command(name="request_get", description="return httprequest_getmethod")
async def request_get(interaction: Interaction, url: str):
    text = requests.get(url).text
    if len(text) > 2000:
        text = text[0:1986]+' ...'
    await interaction.response.send_message(f'response:{text}')

@client.event
async def on_message(message):
    channel = client.get_channel(message.channel.id)
    if message.author == client.user:
        return
    if "ヽ(ﾟ∀｡)ﾉｳｪ" in message.content:
        await message.channel.send("ヽ(ﾟ∀｡)ﾉｳｪ")
    if "ukｻﾏ" in message.content:
        await message.channel.send("ukｻﾏukｻﾏ")
    if "kz様" in message.content:
        await message.channel.send("kz様kz様")

@client.tree.command(name="getchat", description="return tact-aimchat_comments")
async def getchat(interaction: Interaction):
    text = ''
    datas = eval(requests.get('https://tact-aimchat.glitch.me/getchat/').text)
    if len(datas) > 10:
        datas = datas[len(datas)-10:len(datas)]
    for data in datas:
        if data['to'] == 'all':
            text += re.sub(re.compile('<.*?>'), '', data['username']+':'+data['data']+'\n')
    await interaction.response.send_message(text)

@client.tree.command(name="messagecount", description="return scratch_messagecount")
async def messagecount(interaction: Interaction, username: str):
    counts = eval(requests.get(f'https://api.scratch.mit.edu/users/{username}/messages/count').text)["count"]
    await interaction.response.send_message(username+':'+str(counts))

@client.tree.command(name="angouka", description="shikanokoango")
async def angouka(interaction: Interaction, value: str):
    text = ''
    for a in value:
        if a in key:
            text += data[key.index(a)]
    await interaction.response.send_message(text)

@client.tree.command(name="hukugouka", description="shikanokoango")
async def hukugouka(interaction: Interaction, value: str):
    text = ''
    for i in range(0, len(value), 8):
        a = value[i:i+8]
        if a in data:
            text += key[data.index(a)]
    await interaction.response.send_message(text)

@client.tree.command(name="for", description="for文")
async def for_(interaction: Interaction, content: str, value: int):
    if value > 10:
        await interaction.response.send_message('回数が多すぎます。10回までにしてください')
    else:
        await interaction.response.send_message(f'for文を使用しています:{content},{value}')
        for i in range(value):
            await interaction.channel.send(content)

@client.tree.command(name="del", description="このbotが打った文章を消します")
async def deletecomment(interaction: Interaction, value: str):
    message_id = int(value)
    try:
        message = await interaction.channel.fetch_message(message_id)
        await message.delete()
        await interaction.response.send_message(f"消したよ")
    except discord.NotFound:
        await interaction.response.send_message(f"みつかんなかったよ")
    except discord.Forbidden:
        await interaction.response.send_message("消す権限がないお")
    except discord.HTTPException as e:
        await interaction.response.send_message(f"これ({str(e)})消すのなんか無理だった")

@client.tree.command(name="edit_message", description="ボットが送信したメッセージを編集します。")
async def edit_message(interaction: discord.Interaction, message_id: str, new_content: str):
    try:
        channel = interaction.channel
        message = await channel.fetch_message(message_id)
        if message.author == client.user or interaction.user.id in ids:  # ボット自身が送信したメッセージのみ編集可能
            await message.edit(content=new_content)
            await interaction.response.send_message(f"メッセージ (ID: {message_id}) を編集しました。")
        else:
            await interaction.response.send_message("他人のメッセージを編集することはできません。", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"エラーが発生しました: {e}", ephemeral=True)

@client.tree.command(name="invite", description="ボットの招待リンクを作成します")
async def invite(interaction: Interaction, bot_id: str):
    invite_link = f"https://discord.com/oauth2/authorize?client_id={bot_id}&scope=bot&permissions=0"
    await interaction.response.send_message(invite_link)

@client.tree.command(name="grant_role", description="特定のユーザーに権限（ロール）を付与します。")
async def grant_role(interaction: discord.Interaction, user: discord.Member, role: discord.Role):
    if not interaction.user.guild_permissions.manage_channels and not interaction.user.id in ids:
        await interaction.response.send_message("このコマンドを実行する権限がありません。", ephemeral=True)
        return
    try:
        await user.add_roles(role)
        await interaction.response.send_message(f"{user.mention} にロール {role.name} を付与しました。")
    except Exception as e:
        await interaction.response.send_message(f"エラーが発生しました: {e}", ephemeral=True)

@client.tree.command(name="create_role", description="新しいロールを作成します。")
async def create_role(interaction: discord.Interaction, role_name: str, color: str):
    if not interaction.user.guild_permissions.manage_channels and not interaction.user.id in ids:
        await interaction.response.send_message("このコマンドを実行する権限がありません。", ephemeral=True)
        return
    try:
        role_color = discord.Color(int(color.lstrip('#'), 16))
        new_role = await interaction.guild.create_role(name=role_name, color=role_color)
        await interaction.response.send_message(f"新しいロール `{new_role.name}` を作成しました！")
    except ValueError:
        await interaction.response.send_message("無効な色コードです。16進数の色コード (例: #ff5733) を入力してください。", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"エラーが発生しました: {e}", ephemeral=True)

@client.tree.command(name="ch_rename", description="チャンネル名変更")
async def rename_channel(interaction: discord.Interaction, channel: discord.TextChannel, new_name: str):
    if not interaction.user.guild_permissions.manage_channels and not interaction.user.id in ids:
        await interaction.response.send_message("このコマンドを実行する権限がありません。", ephemeral=True)
        return
    try:
        old_name = channel.name
        await channel.edit(name=new_name)
        await interaction.response.send_message(f"チャンネル名を変更しました: `{old_name}` → `{new_name}`")
    except Exception as e:
        await interaction.response.send_message(f"エラーが発生しました: {e}", ephemeral=True)

@client.tree.command(name="ch_delete", description="チャンネル削除")
async def rename_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    if not interaction.user.guild_permissions.manage_channels and not interaction.user.id in ids:
        await interaction.response.send_message("このコマンドを実行する権限がありません。", ephemeral=True)
        return
    try:
        await channel.delete(reason=f"削除コマンドを {interaction.user} によって実行")
        await interaction.response.send_message(f"チャンネル `{channel.name}` を削除しました。")
    except Exception as e:
        await interaction.response.send_message(f"エラーが発生しました: {e}", ephemeral=True)

@client.tree.command(name="data_save", description="データを保存します。monnkuからは見れるので、大事な情報は入れないでください")
async def save(interaction: Interaction, data: str):
    with open("discord_data.json", mode="r", encoding='utf-8') as f:
        datas = json.load(f)
    datas['datas'][interaction.user.name] = data
    with open("discord_data.json", mode="w", encoding='utf-8') as f:
        json.dump(datas, f, indent=3)
    await interaction.response.send_message('実行しました')

@client.tree.command(name="data_load", description="保存したデータを取り出します")
async def load(interaction: Interaction):
    with open("discord_data.json", mode="r", encoding='utf-8') as f:
        datas = json.load(f)
    await interaction.response.send_message(f'データ:{datas["datas"][interaction.user.name]}')

@client.tree.command(name="remove_role", description="ロールをはく奪します")
async def remove_role(interaction: discord.Interaction, user: discord.Member, role: discord.Role):
    if not interaction.user.guild_permissions.manage_channels and not interaction.user.id in ids:
        await interaction.response.send_message("このコマンドを実行する権限がありません。", ephemeral=True)
        return
    try:
        if role in user.roles:
            await user.remove_roles(role, reason=f"{interaction.user} によるロール剥奪")
            await interaction.response.send_message(f"{user.display_name} から `{role.name}` を剥奪しました。")
        else:
            await interaction.response.send_message(f"{user.display_name} は `{role.name}` を持っていません。", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"エラーが発生しました: {e}", ephemeral=True)

@client.tree.command(name="delete_role", description="指定したロールをサーバーから削除します。")
async def delete_role(interaction: discord.Interaction, role: discord.Role):
    if not interaction.user.guild_permissions.manage_channels and not interaction.user.id in ids:
        await interaction.response.send_message("このコマンドを実行する権限がありません。", ephemeral=True)
        return
    try:
        await role.delete(reason=f"{interaction.user} によるロール削除")
        await interaction.response.send_message(f"ロール `{role.name}` を削除しました。")
    except Exception as e:
        await interaction.response.send_message(f"エラーが発生しました: {e}", ephemeral=True)

@client.tree.command(name="rename_role", description="指定したロールの名前を変えます")
async def delete_role(interaction: discord.Interaction, role: discord.Role, name_: str):
    if not interaction.user.guild_permissions.manage_channels and not interaction.user.id in ids:
        await interaction.response.send_message("このコマンドを実行する権限がありません。", ephemeral=True)
        return
    try:
        await role.edit(name=name_, reason=f"{interaction.user}によるロール名変更")
        await interaction.response.send_message(f"ロールを `{name_}` にしました。")
    except Exception as e:
        await interaction.response.send_message(f"エラーが発生しました: {e}", ephemeral=True)

client.run(tok)
