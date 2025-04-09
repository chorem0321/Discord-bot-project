import discord
from discord_token import* #여기서 discord token 불러옵니다
from discord.ext import commands
from 메뉴추천 import 메뉴리스트중복없음
import random
import time
from gemini_crawling import ask_gemini
from copilot_crawling import ask_copilot
import threading
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.members = True  # Enable member tracking

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())

textread = True

@bot.event
async def on_ready():
    game = discord.Game("명령어 <-- 입력으로 명령어보기")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print(f'Logged in as {bot.user.name}')  # 봇이 준비되었음을 콘솔에 출력합니다.
    
    for guild in bot.guilds: #봇이 참가하고 있는 모든 서버 체크
        print(f'현재 가동중 : 서버 / {guild.name}')
        for vc in guild.voice_channels:  # 각 서버의 모든 음성 채널 체크
            if bot.user in vc.members:  # 봇이 해당 음성 채널에 참가 중인지 체크
                print(f'현재 가동중 : 서버 / {guild.name} | 채널 / {vc.name}')
                await vc.send(f'봇이 가동되었습니다. 현재 {vc.name} 채널에 있습니다.')

@bot.event
async def on_voice_state_update(member, before, after):
    global textread
    global channel
    
    guild_name = member.guild.name

    if member.bot:
        return

    if before.channel != after.channel:
        if after.channel:
            print(f'서버 : {guild_name} / {member.display_name} joined {after.channel.name}')

            if textread:
                await after.channel.send(f'{member.display_name} 님이 들어왔어요.', tts=True)
            else:
                await after.channel.send(f'{member.display_name} 님이 들어왔어요.')

        if before.channel:
            print(f'서버 : {guild_name} / {member.display_name} left {before.channel.name}')

            if textread:
                await before.channel.send(f'{member.display_name} 님이 나가셨어요.', tts=True)
            else:
                await before.channel.send(f'{member.display_name} 님이 나가셨어요.')

@bot.event
async def send_reminder():
    channel_id = 1351919990218952707  # 메시지를 보낼 채널 ID로 변경하세요
    channel = bot.get_channel(channel_id)

    if channel is None:
        print("채널을 찾을 수 없습니다. 채널 ID를 확인하세요.")
        return

    while not bot.is_closed():
        await channel.send("허리피고 물 마시세요!")
        print("작동함")
        await asyncio.sleep(1800)  # 30분(1800초) 대기

@bot.event
async def on_message(message):
    if message.author.bot:
        return None

    #시나노야사랑해answering
    if message.content == "시나노야사랑해":
        await message.channel.send("나도 사랑해 :heart:")
    
    #메뉴추천
    if message.content == "저메추":
        await message.channel.send(f"나는 {random.choice(메뉴리스트중복없음)} (을)를 추천해! 맛있게 머거 :heart:")

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
        command = "저메추, 주사위, 돌림판, 그럼제가선배맘에, -나를 속인거니?, 뽀뽀해줘, !질문 <질문>"
        await message.channel.send(f"현재 등록된 명령어는 [ {command} ] 가 있어! 언제든지 쓰고싶으면 얘기해죠!!")

    #돌림판
    if message.content[:3] == "돌림판":
        돌림판리스트 = []
        돌림판리스트 = message.content[4:].split()
        await message.channel.send(f"돌림판 결과는 {돌림판리스트[random.randint(0,len(돌림판리스트))]} (이)에요!!")

    #그럼제가선배맘에
    if message.content == "그럼제가선배맘에":
        await message.channel.send("탕탕후루후루 타탕탕 후루루루루!!!!!")
        await message.channel.send("https://tenor.com/view/triples-kotone-s11-malatanghulu-malatang-gif-981579389405623666")

    #짱구야나를속인거니?
    if message.content[-8:] == "나를 속인거니?":
        await message.channel.send(file = discord.File("fakeme.webp"))

    #뽀뽀
    if message.content == "뽀뽀해줘":
        await message.channel.send(f"{message.author.display_name}야(아) 사랑해 쪽:heart:")

    #대답
    if message.content == "시나노야":
        대답 = ["네?", "시나노 여기있어요!", "듣고있어요!", "무슨 일이신가요?", "냥냥!"]
        대답_선택num = random.randint(0,4)
        await message.channel.send(대답[대답_선택num])

    #어허 욕은 나쁜거야
    if message.content in ['시발','ㅅㅂ','씨발','ㅆㅂ','병신','ㅂㅅ','애미']:
        await message.channel.send(f'"{message.author.display_name}" 야!! "{message.content}" 은(는) 나쁜말이야!! 쓰지맛!!!')


    # 챗지피티 질문 처리
    if message.content.startswith("!질문"):
        question = message.content[4:]
        await message.channel.send(f"{message.author.display_name}님의 질문을 처리 중입니다. 잠시만 기다려주세요...")

        # 스레드에서 질문 처리
        def handle_question():
            try:
                answer = ask_copilot(question)
                asyncio.run_coroutine_threadsafe(
                    message.channel.send(f"copilot의 답변: {answer}"), bot.loop
                )
            except Exception as e:
                asyncio.run_coroutine_threadsafe(
                    message.channel.send(f"오류가 발생했습니다: {e}"), bot.loop
                )

        thread = threading.Thread(target=handle_question)
        thread.start()


bot.run(token) #토큰 넣어주세요
