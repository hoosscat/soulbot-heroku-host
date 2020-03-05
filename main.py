import discord, datetime, requests, json, random, time
from bs4 import BeautifulSoup

정책 = """```소울봇 사용 정책```
```
1. 따라해 기능을 악용하지 마십시오.
2. 봇의 링크를 함부로 공유하지 마십시오.
3. 버그를 발견할시 즉시 알려주시기 바랍니다.
4. 버그를 악용하지 마십시오.
5. 중요한 정보를 알려고 하지 마십시오.
```
봇을  사용하시면 위 정책에 동의한것으로 간주합니다.

"""

패치노트 = """V1.2
1. 도움말 깔끔하게 변환
2. 도움말 오타 수정
"""
명령어 = """`소울봇 도움`
> 소울봇을 사용할 때 어떻게 사용하는지 알려줍니다.
`소울봇 랜덤냥`
> 랜덤으로 고양이를 보여줍니다.
`소울봇 랜덤멍`
> 랜덤으로 강아지를 보여줍니다.
`소울봇 확률`
> 랜덤으로 확률을 보여줍니다.
`소울봇 골라`
> 선택이 어려운 당신을 도와줍니다.
`소울봇 정책`
> 소울봇을 사용할 때 주의할 점을 알려줍니다.
`소울봇 핑`
> 현재 봇의 핑을 알아봅니다.
`소울봇 프로그래밍밈`
> 랜덤으로 프로그래밍 밈을 보여줍니다.
`소울봇 따라해`
> 소울봇 이 따라합니다.
`소울봇 초대`
> 소울봇을 당신의 서버에 추가합니다.
`소울봇 패치노트`
> 소울봇에 추가된 기능을 알려줍니다.
"""

#공용 변수


client = discord.Client()

@client.event
async def on_ready():
    print(client.user.id)
    print("I am Ready")

    await client.change_presence(activity=discord.Game("소울봇 도움"))

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="봇-인사")
    await channel.send("{}님 안녕하세요!".format(member.mention))

@client.event
async def on_message(message):
    #로딩 변수
    loading = discord.Embed(title="로딩중", description="현제 명령어를 실행하기 위해 열심히 봇이 일하는 중이에요!", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
    loading.add_field(name="기다려 주세요...", value="로딩중...")
    loading.set_footer(text=f"{message.author.display_name}님을 위해", icon_url=message.author.avatar_url)
    
    if message.author.bot:
        return
    if not message.content.startswith("소울봇 "):
        return
    command = message.content[4:].split()[0]
    commandline = message.content.split()[1:]
    if command == "랜덤냥":
        try:
            response = requests.get("http://aws.random.cat/meow").json()
        except Exception as error:
            embed = discord.Embed(title=":sob: 오류 발생!", description="랜덤 냥이를 불러오는 데 오류가 발생하였습니다.\n잠시 후 다시 시도해 주세요.", color=discord.Colour.dark_red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="오류 내용:", value=f"```오류 내용은 보안상 공개할수 없습니다.```", inline=True)
            embed.set_footer(text=f"{message.author.display_name}님을 위해", icon_url=message.author.avatar_url)
            print("오류 내용:\n{error}\n")
            await message.channel.send(embed=embed)
        else:
            url = response["file"]
            embed = discord.Embed(title=":cat: 랜덤냥!", description="여러분이 좋아할 만한 랜덤냥을 제가 불러와드렸습니다.", color=discord.Colour.blurple(), timestamp=datetime.datetime.utcnow())
            embed.set_image(url=url)
            embed.set_footer(text=f"{message.author.display_name}님을 위해", icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)
    if command == "랜덤멍":
        msg = await message.channel.send(embed=loading)
        try:
            response = requests.get("https://random.dog/woof.json").json()
        except Exception as error:
            embed = discord.Embed(title=":sob: 오류 발생!", description="랜덤 멍이를 불러오는 데 오류가 발생하였습니다.\n잠시 후 다시 시도해 주세요.", color=discord.Colour.dark_red(), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="오류 내용:", value=f"```오류 내용은 보안상 공개할수 없습니다.```", inline=True)
            embed.set_footer(text=f"{message.author.display_name}님을 위해", icon_url=message.author.avatar_url)
            print("오류 내용:\n{error}\n")
            await msg.edit(embed=embed)
        else:
            url = response["url"]
            embed = discord.Embed(title=":dog: 랜덤멍!", description="여러분이 좋아할 만한 랜덤멍을 제가 불러와드렸습니다.", color=discord.Colour.blurple(), timestamp=datetime.datetime.utcnow())
            embed.set_image(url=url)
            embed.set_footer(text=f"{message.author.display_name}님을 위해", icon_url=message.author.avatar_url)
            await msg.edit(embed=embed)
            
    if command.startswith("확률"):
        m = message.content[6:len(message.content)]
        embed = discord.Embed(title=":game_die: 확률 계산완료", description="아주 랜덤한 확률입니다!", color=discord.Colour.blurple(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="제 생각에는", value="{} 확률은 {}%입니다!".format(m, random.randint(0, 100)))
        await message.channel.send(embed=embed)

    if command.startswith("골라"):
        m = message.content[6:len(message.content)].split(', ')
        embed = discord.Embed(title=":game_die: 골라보았어요!", description="제가 한번 직접 골라 보았어요", color=discord.Colour.blurple(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="{} 중에 고른 것".format(str(m).replace('[','').replace(']','').replace('\'','')), value="{}입니다!".format(random.choice(m)))
        embed.set_footer(text=f"{message.author.display_name}님을 위해", icon_url=message.author.avatar_url)
        
        await message.channel.send(embed=embed)

    if command == "정책":
        await message.channel.send(정책)

    if command == "핑":
        ping_load = discord.Embed(title=":game_die: 핑을 측정하고 있습니다.", description="잠시만 기다려주세요", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        ping_load.set_footer(text=f"{message.author.display_name}님을 위해", icon_url=message.author.avatar_url)
        msg = await message.channel.send(embed=ping_load)

        ping = round(client.latency * 1000)
        if ping <= 10:
            embed = discord.Embed(title=":game_die: 현재 핑입니다!", description="{}ms".format(ping), color=discord.Colour.green(), timestamp=datetime.datetime.utcnow())
        elif ping <= 50:
            embed = discord.Embed(title=":game_die: 현재 핑입니다!", description="{}ms".format(ping), color=discord.Colour.blurple(), timestamp=datetime.datetime.utcnow())
        elif ping <= 100:
            embed = discord.Embed(title=":game_die: 현재 핑입니다!", description="{}ms".format(ping), color=discord.Colour.yellow(), timestamp=datetime.datetime.utcnow())
        elif ping <= 150:
            embed = discord.Embed(title=":game_die: 현재 핑입니다!", description="{}ms".format(ping), color=discord.Colour.orange(), timestamp=datetime.datetime.utcnow())
        else:
            embed = discord.Embed(title=":game_die: 현재 핑입니다!", description="{}ms".format(ping), color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"{message.author.display_name}님을 위해", icon_url=message.author.avatar_url)
        await msg.edit(embed=embed)

    if command == "프로그래밍밈":
        msg = await message.channel.send(embed=loading)
        meme = ['https://imgur.com/HfrkP6m.png', 'https://i.imgur.com/wIp4SLC.png', 'https://i.imgur.com/XPuGFxT.png', 'https://i.imgur.com/Ty6koG0.png', 'https://i.imgur.com/coZ8Izi.jpg', 'https://i.imgur.com/zDhAPfp.png', 'https://i.imgur.com/0ZnI215.png','https://pbs.twimg.com/media/Dzu882WU0AAszD2?format=jpg&name=small', 'https://pbs.twimg.com/media/DzQbTSnU0AEnCp3?format=jpg&name=medium', 'https://pbs.twimg.com/media/Dta85fuUUAIXvkT?format=jpg&name=medium', 'https://pbs.twimg.com/media/DtPC7w-VYAAgbsO?format=jpg&name=medium','https://pbs.twimg.com/media/DtPCY6JUcAIOSHx?format=jpg&name=small', 'https://pbs.twimg.com/media/DtKDEjwU8AEo56A?format=jpg&name=900x900', 'https://pbs.twimg.com/media/DtbCAUOVsAArevi?format=jpg&name=medium', 'https://pbs.twimg.com/media/DzmaBXhUcAA59Hf?format=png&name=small']
        url = random.choice(meme)
        embed = discord.Embed(title=":ballot_box: 프로그래밍 밈", description="재미있는 프로그래밍밈!")
        embed.set_image(url=url)
        embed.set_footer(text=f"{message.author.display_name}님을 위해", icon_url=message.author.avatar_url)
        await msg.edit(embed=embed)

    if command.startswith("따라해"):
        m = message.content[7:len(message.content)]
        if m == "":
            embed = discord.Embed(title=":key: ERROR!", description="따라할 말이 없네요...", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"{message.author.display_name}님을 위해", icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(m)
    
    if command == "초대":
        embed = discord.Embed(title=":key: 초대", description="[초대링크](https://discordapp.com/api/oauth2/authorize?client_id=642332042977083415&permissions=8&scope=bot)", color=discord.Colour.blurple(), timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"{message.author.display_name}님을 위해", icon_url=message.author.avatar_url)
        await message.channel.send(embed=embed)

    if command == "이스터에그":
        embed = discord.Embed(title=":egg: 이스터에그!", description="이스터에그를 발견하였습니다! 보상은 없습니다...", color=discord.Colour.gold(), timestamp=datetime.datetime.utcnow())
        msg = await message.channel.send(embed=embed)
        await msg.delete(delay=3)

    if command == "패치노트":
        embed = discord.Embed(title=":book: 패치노트", description=패치노트, color=discord.Colour.gold(), timestamp=datetime.datetime.utcnow())
        await message.channel.send(embed=embed)
        
    if command == "도움":
        embed = discord.Embed(title=":bookmark: 도움", description=명령어, color=discord.Colour.blurple(), timestamp=datetime.datetime.utcnow())
        # embed.add_field(name="소울봇 랜덤냥", value="랜덤으로 고양이를 보여줍니다. ㅎ", inline=True)
        # embed.add_field(name="소울봇 랜덤멍", value="랜덤으로 강아지를 보여줍니다.", inline=True)
        # embed.add_field(name="소울봇 확률", value="랜덤으로 확률을 보여줍니다.", inline=True)
        # embed.add_field(name="소울봇 골라", value="선택이 어려운 당신을 도와줍니.!", inline=True)
        # embed.add_field(name="소울봇 핑", value="현재 봇의 핑을 알아봅니다.", inline=True)
        # embed.add_field(name="소울봇 프로그래밍밈", value="랜덤으로 프로그래밍 밈을 보여줍니다.", inline=True)
        # embed.add_field(name="소울봇 따라해", value="소울봇 이 따라합니다.", inline=True)
        # embed.add_field(name="소울봇 초대", value="소울봇을 당신의 서버에 추가합니다.", inline=True)
        # embed.add_field(name="소울봇 패치노트", value="소울봇에 추가된 기능을 알려줍니다", inline=True)
        embed.set_footer(text=f"이 봇에 대한 저작권은 후스다냥#1924 에게 있습니다.", icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Copyright.svg/170px-Copyright.svg.png')
        await message.channel.send(embed=embed)
        
client.run('NjQyMzMyMDQyOTc3MDgzNDE1.XcVZyA.xPYNGE0I3UwArHDNjBTMOgMCAEY')
