#Code by Aki.no.Alice@Tyrant_Rex

from discord.ext import commands
import discord,sqlite3,random
from os import getenv

conn = sqlite3.connect("64.sqlite3")
cursor = conn.cursor()

try:
    cursor.execute(f"select * from `we_miss_them` where rowid = 1").fetchone()[1]
except:
    cursor.execute("CREATE TABLE we_miss_them (id TEXT NOT NULL,sc INT NOT NULL);")

client = commands.Bot(command_prefix=">")

def check(txt):
    for i in txt.split(" "):
        for good in open("good.txt", encoding="utf-8").read().split(" "):
            if good == i :
                return True,i

    for i in txt.split(" "):
        for bad in open("bad.txt", encoding="utf-8").read().split(" "):
            if bad == i:
                return False,i
    return None,None

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

def id_(author_id):
    with open("id.txt",mode="r",encoding="utf-8") as f:
        list_ = f.read().split(" ")
    if str(author_id) in list_:
        return False
    else:
        return True

@client.event
async def on_ready():
    print("我们怀念他",flush=True)

@client.event
async def on_message(ctx):
    txt = ctx.content.split(" ")
    print(f"{ctx.author} {ctx.author.id}:{ctx.content}\tIs bot:{ctx.author.bot}",flush=True)
    if ctx.author != client.user and id_(ctx.author.id) and not ctx.author.bot:
        if ctx.content == ">pt" or ctx.content == "我的社会信用" or ctx.content == "我的社會信用":
            q = cursor.execute(f"select id,sc from `we_miss_them` where id = '{ctx.author}'").fetchone()[1]
            await ctx.channel.send(f"{ctx.author.mention}\n您的社会信用有{q}分\n请您在Discord群内继续赞扬中国共产党以增加您的社会信用分")

        else:
            num = random.randint(1,100)
            sc(ctx.author)

            ok,text = check(ctx.content)

            if ok == True:
                await ctx.channel.send(f"{ctx.author.mention} 您近期赞扬了中国共产党:{text}\n做得好 +{num%10*10+10}分社会信用")
                update(ctx.author,num%10*10+10)

            elif ok == False:
                await ctx.channel.send(f"{ctx.author.mention} 您近期發表了敏感言论:{text}\n你妈死了 -{num%10*10+10}分社会信用 ")
                update(ctx.author,-(num%10*10+10))
            elif ok == None:
                pass

            if improve(ctx.author):
                await ctx.channel.send(f"{ctx.author.mention}\n您近期的社会信用分已经低于0分\n请您在Discord群内赞扬中国共产党如:```中国共产党万岁```以增加您的社会信用分")

    if not id_(ctx.author.id):
        if txt[0] == ">r":
            try:
                with open(f"{txt[1]}.txt",mode="r",encoding="utf-8") as f:
                    t = f.read()

                with open(f"{txt[1]}.txt",mode="w",encoding="utf-8") as f:
                    f.write(t.replace(f" {txt[2]}",""))
                await ctx.channel.send("i am winnie")
            except:
                pass

        elif txt[0] == ">a":
            try:
                with open(f"{txt[1]}.txt",mode="a",encoding="utf-8") as f:
                    f.write(f" {txt[2]}")
                await ctx.channel.send("i am winnie")
            except:
                pass
if __name__ == "__main__":
    client.run(getenv("token"))
