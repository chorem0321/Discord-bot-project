import discord
from discord_token import*
from discord.ext import commands
import random
from 메뉴추천 import 메뉴리스트중복없음
import asyncio
import time

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

global filename
global filename2
filename = "C:/Users/Junsu Choi/Desktop/직박구리/Discord bot project/느엥봇/노래제목리스트.txt"
filename2 = "C:/Users/Junsu Choi/Desktop/직박구리/Discord bot project/느엥봇/노래링크리스트.txt"

@bot.event
async def on_ready():
    game = discord.Game("명령어 <-- 입력으로 명령어보기")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("준비완료!")
    
@bot.event
async def on_message(message):
    #느엥answering
    if message.author.bot:
        return None
    else:
        if message.content == "느엥":
            await message.channel.send("느엥")
        if message.content[:2] == "느엥" and message.content[3:].isnumeric() == True:
            if int(message.content[3:]) <= 1000:
                if message.author.bot:
                    return None
                else:
                    await message.channel.send("느엥"*int(message.content[3:]))
            elif int(message.content[3:]) > 1000:
                await message.channel.send("1000 이하로 입력해줘 너무 길어.. 헤으응.. 이렇게 큰 건 다 안들어가..:heart:")

    #느엥아사랑해answering
    if message.content == "느엥아사랑해":
        await message.channel.send("나도 사랑해 피엔냐 :heart:")
    
    #메뉴추천
    if message.content == "저메추":
        await message.channel.send(f"리제는 {random.choice(메뉴리스트중복없음)} (을)를 추천해! 맛있게 먹느엥 :heart:")

    #주사위 굴리기
    if message.content == "주사위":
        await message.channel.send("https://tenor.com/view/dice-gif-18958117")
        await message.channel.send("주사위 굴러가는중...")
        time.sleep(2)
        random_num = random.randint(1,6)
        await message.channel.send(f"{message.author.display_name}의 주사위 결과는 : {random_num} 이야! :heart:")

    #help
    if message.content == "명령어":
        #커맨드 손수 추가
        command = "저메추, 주사위, 전부집합, 돌림판, 노래추천, 그럼제가선배맘에, 안아줘요, -나를 속인거니?, 뽀뽀해줘, 느엥아"
        await message.channel.send(f"현재 등록된 명령어는 [ {command} ] 가 있어! 언제든지 쓰고싶으면 얘기해죠! :heart: \n참고로 [전부집합] 명령어는 everyone 멘션이기 때문에 사용에 각별히 주의해줘!!")

    #@everyone 치기
    if message.content == "전부집합":
        await message.channel.send(f"@everyone {message.author.display_name}(이)가 모두를 집합시켰어!!")

    #돌림판
    if message.content[:3] == "돌림판":
        돌림판리스트 = []
        돌림판리스트 = message.content[4:].split()
        await message.channel.send(f"돌림판 결과는 {돌림판리스트[random.randint(0,len(돌림판리스트))]} (이)에요!!")

    #그럼제가선배맘에
    if message.content == "그럼제가선배맘에":
        await message.channel.send("탕탕후루후루 타탕탕 후루루루루!!!!!")
        await message.channel.send("https://tenor.com/view/triples-kotone-s11-malatanghulu-malatang-gif-981579389405623666")

    #노래추천
    if message.content == "노래추천":
        global 노래추천channel
        노래추천channel = message.channel
        await message.channel.send("노래를 추천받고 싶으시다면 [노래추천해줘]를, 노래를 추천하고 싶으시다면 [노래추천할게]를 입력해주세요\n현재 등록된 노래 추천 리스트는 [노래추천리스트]를 입력하여 확인할 수 있어요!")

    if message.content[:6] == "노래추천할게":
        channel = message.channel
        #같은 사람, 같은 채널인지 확인 (command hijacking 방지)
        def check(m):
            return m.author == message.author and m.channel == message.channel
        
        await message.channel.send("노래제목을 입력해주세요!")
        try:
            temp노래제목 = await bot.wait_for("message",check = check, timeout = 30)
            temp노래제목 = temp노래제목.content #discord.py 에서 .content 해주면 str값으로 parameter 받음
            a = open(filename, mode='a') #파이썬 자체에서 a모드로 write하면 그 파일에 이어서 써줌
            a.write(temp노래제목+"\n") #.txt 파일에 등록할 때 보기 편하게 + 줄 나누기
            a.close()
        except asyncio.TimeoutError: #시간초과 걸기
            await channel.send("시간초과에요!")
            return None

        await message.channel.send("노래링크를 입력해주세요!")
        try:
            temp노래링크 = await bot.wait_for("message",check = check, timeout = 30)
            temp노래링크 = temp노래링크.content
            a = open(filename2, mode='a')
            a.write(temp노래링크+"\n")
            a.close()
        except asyncio.TimeoutError:
            await channel.send("시간초과에요!")
            return None
        
        await message.channel.send("입력 완료!")

    if message.content == "노래추천해줘":
        f3 = open(filename,'r')
        length = len(f3.readlines())
        await message.channel.send(f"현재 등록된 노래 개수는 총 {length}개에요!")
        with open(filename,'r') as f:
            f.seek(0) #file을 오픈하고 읽을 때 커서가 맨 밑에 가 있는걸 방지하기 위해 커서를 제일 위로 올림
            노래제목리스트 = f.readlines() #readlines()로 받으면 줄로 나눠진 걸 number로 리스트 생성됨
            랜덤숫자 = random.randint(0,length-1)
            await message.channel.send(f"노래제목: {노래제목리스트[랜덤숫자]}")
        with open(filename2,'r') as f2:
            f2.seek(0)
            노래링크리스트 = f2.readlines()
            노래넘버링 = str(랜덤숫자+1)+"번째로 등록된 노래에요!"
            await message.channel.send(f"노래링크: {노래링크리스트[랜덤숫자]}{노래넘버링}")

    if message.content == "노래추천리스트":
        with open(filename,'r') as f3:
            f3.seek(0)
            노래추천리스트temp = f3.readlines()
            노래추천리스트 = []
            노래추천스트링 = str()
            for i in range(0,len(노래추천리스트temp)):
                노래추천리스트.append(노래추천리스트temp[i].rstrip("\n"))
                노래추천스트링 += f"{i+1}. {노래추천리스트[i]}\n"
            await message.channel.send(f"현재 등록된 노래추천리스트는\n\n{노래추천스트링}\n입니다!")
    
    #짱구야나를속인거니?
    if message.content[-8:] == "나를 속인거니?":
        await message.channel.send(file = discord.File("fakeme.webp"))

    #안아줘요
    if message.content == "안아줘요":
        await message.channel.send(f"{message.author.display_name}을 꼬옥 안아줬어 :heart:", file = discord.File("hugme.png"))

    #뽀뽀
    if message.content == "뽀뽀해줘":
        await message.channel.send(f"{message.author.display_name}야(아) 사랑해 쪽:heart:")

    #대답
    if message.content == "느엥아":
        대답 = ["네?", "느엥이 여기있어요!", "듣고있어요!", "무슨 일이신가요?", "멍멍!"]
        대답_선택num = random.randint(0,4)
        await message.channel.send(대답[대답_선택num])

@bot.command(name="test")
async def react_test(ctx):
    await ctx.channel.send("테스트메세지")
    return None


bot.run(token) #토큰 넣어주세요


