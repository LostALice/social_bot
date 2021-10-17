#Code by Aki.no.Alice@Tyrant_Rex

from discord.ext import commands
import discord,sqlite3,random

conn = sqlite3.connect("64.sqlite3")
cursor = conn.cursor()

client = commands.Bot(command_prefix="=")

def check(txt):
    pass

def sc(author):
    cursor.execute(f"select id,sc from `we_miss_them` where id = '{author}'")
    sc_pt = cursor.fetchone()
    if sc_pt == None:
        cursor.execute(f"insert into we_miss_them (id,sc) values (?,?)",(str(author),1000))
        conn.commit()

def update(author,pt):
    author = str(author)
    sc = cursor.execute(f"select sc from we_miss_them where id = '{author}'").fetchone()[0]
    cursor.execute(f"update we_miss_them set sc = ? WHERE id = ?",(sc+pt,author))
    conn.commit()

def improve(author):
    a = cursor.execute(f"select id,sc from `we_miss_them` where id = '{author}'").fetchone()[1]
    if  a <= 0:
        return True

@client.event
async def on_ready():
    print("我们怀念他",flush=True)

@client.event
async def on_message(ctx):
    if ctx.author != client.user:
        num = random.randint(1,100)
        sc(ctx.author)
        print(f"{ctx.author}:{ctx.content}",flush=True)

        if ctx.content in open("bad.txt",encoding="utf-8").read():
            await ctx.channel.send(f"{ctx.author.mention} 你妈死了 -{num%10*10+10}分社会信用 ")
            update(ctx.author,-(num%10*10+10))

        elif ctx.content in open("good.txt",encoding="utf-8").read():
            await ctx.channel.send(f"{ctx.author.mention} 做得好 +{num%10*10+10}分社会信用")
            update(ctx.author,num%10*10+10)

        if improve(ctx.author):
            await ctx.channel.send(f"{ctx.author.mention}\n您近期的社会信用分已经低于0分\n请您在Discord群内赞扬中国共产党如:```中国共产党万岁```以增加您的社会信用分")

    if ctx.content == ">pt" or ctx.content == "我的社会信用" or ctx.content == "我的社會信用":
        q = cursor.execute(f"select id,sc from `we_miss_them` where id = '{ctx.author}'").fetchone()[1]
        await ctx.channel.send(f"{ctx.author.mention}\n您的社会信用有{q}分\n请您在Discord群内继续赞扬中国共产党以增加您的社会信用分")

if __name__ == "__main__":
    client.run("token")
