import discord
from discord_token import*
from discord.ext import commands
import random
from 메뉴추천 import 메뉴리스트중복없음
import asyncio

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

#노래추천에 필요한 변수
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
    #서조answering
    if message.author.bot:
        return None
    else:
        if message.content == "서조":
            await message.channel.send("서조는신이야")


    #일리야 answering
    if message.content == "일리야":
        answerlist = ["네?", "일리 여기있어요!", "무엇을 도와드릴까요 주인님?:heart:", "네! 헤헤:heart:", "도움이 필요하신가요?:heart:"]
        await message.channel.send(random.choice(answerlist))

    #서조사랑해answering
    if message.content == "서조사랑해":
        await message.channel.send("서조도 사랑한대! (암튼 그렇대)")
    
    #메뉴추천
    if message.content == "저메추":
        await message.channel.send(f"일리는 {random.choice(메뉴리스트중복없음)} (을)를 추천해! 맛있게 먹어 :heart:")

    #주사위 굴리기
    if message.content == "주사위":
        random_num = random.randint(1,6)
        await message.channel.send(f"{message.author}의 주사위 결과는 : {random_num} 이야! :heart:")

    #help
    if message.content == "명령어":
        #커맨드 손수 추가
        command = "저메추, 주사위, 돌림판, 서조사랑해, 서조, [메세지] 그렇지 일리야?, 일리야 안아줘, 노래추천, 일리야"
        await message.channel.send(f"현재 등록된 명령어는 [ {command} ] 가 있어! 언제든지 쓰고싶으면 얘기해죠! :heart:")

    #돌림판
    if message.content[:3] == "돌림판":
        돌림판리스트 = []
        돌림판리스트 = message.content[4:].split()
        await message.channel.send(f"돌림판 결과는 {돌림판리스트[random.randint(0,len(돌림판리스트))]} (이)에요!!")

    #그렇지 일리야?
    if message.content[-8:] == "그렇지 일리야?":
        일리choice = ["일리있네요.","일리없네요."]
        await message.channel.send(일리choice[random.randint(0,1)])

    #안아줘
    if message.content == "일리야 안아줘":
        await message.channel.send(f"{message.author.display_name}님을 꼬옥 안아줬어요 :heart:", file = discord.File("annajoe3.png"))

    #노래추천
    if message.content == "노래추천":
        global 노래추천channel
        노래추천channel = message.channel
        await message.channel.send("노래를 추천받고 싶으시다면 [노래추천해줘]를, 노래를 추천하고 싶으시다면 [노래추천할게]를 입력해주세요.\n현재 등록된 노래 추천 리스트는 [노래추천리스트]를 입력하여 확인할 수 있어요!\n*현재 일리봇에서 [노래추천할게] 기능은 막아두었습니다, 느엥봇에서 추가해주세요!")


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

@bot.command(name="test")
async def react_test(ctx):
    await ctx.channel.send("테스트메세지")
    return None


bot.run(일리token)

