from bs4 import BeautifulSoup
import requests
import re
from kiwipiepy import Kiwi
from krwordrank.sentence import summarize_with_sentences
from krwordrank.hangle import normalize
from gtts import gTTS
from tkinter import *
import tkinter.font
import os
import pygame
from time import sleep


os.system("cls")

print("\n"*2)
print("† 프로그램 실행 준비중입니다.  잠시만 기다리십시오......")

pygame.mixer.init()


global NewsSectionList
NewsSectionList = [["대학일반","news01"],["교수","news02"],["학생","news03"],["연구","news04"],["동문기부금","news05"],["기타","news06"]]

global ttsRepeatMenu
ttsRepeatMenu = "다시 들으시려면 R, 종료하시려면 X를 누르세요."

global ttsRepeatWelcome
ttsRepeatWelcome = "이용하기는 S를, 나가기는 X를 누르세요."

global ttsRepeatContent
ttsRepeatContent = "전체기사 듣기는 F, 핵심기사 듣기는 M, 메뉴 다시듣기는 R, 나가기는 X를 누르세요."


#
# 안내 음성 생성
#

# 1. 음성생성(방문환영)

def Make_WelcomeVoice():

    tts_Welcome = gTTS(text="성균관대학교 뉴스 TTS 서비스 방문을 환영합니다."+ttsRepeatWelcome, lang='ko')
    try:
        tts_Welcome.save("ttsWelcome.mp3")
    except:
        pass


# 2. 음성생성(뉴스분야 선택)

def Make_NewsSectionVoice():

    TxtNewsSection = ""
    for idx in range(0,len(NewsSectionList)):
        TxtNewsSection+='['+str(idx+1)+'] '+NewsSectionList[idx][0]+" "
        TxtRepeatMenu="[R] 다시듣기 [X] 종료"

    tts_NewsSection = gTTS(text="뉴스 분야를 선택하세요."+TxtNewsSection+"."+ttsRepeatMenu, lang='ko')

    try:
        tts_NewsSection.save("ttsNewsSection.mp3")
    except:
        pass

# 3. 음성생성(입력 오류)

def Make_InvalidInputVoice():

    TxtInvalidInput="잘못 누르셨습니다."

    tts_InvalidInput = gTTS(text=TxtInvalidInput+"."+ttsRepeatMenu, lang='ko')

    try:
        tts_InvalidInput.save("ttsInvalidInput.mp3")
    except:
        pass

def Make_InvalidWelcomeVoice():

    TxtInvalidInput="잘못 누르셨습니다."

    tts_InvalidInput = gTTS(text=TxtInvalidInput+"."+ttsRepeatWelcome, lang='ko')

    try:
        tts_InvalidInput.save("ttsInvalidWelcome.mp3")
    except:
        pass

def Make_RepeatContentMenu():

    tts_RepeatContent = gTTS(text=ttsRepeatContent, lang='ko')

    try:
        tts_RepeatContent.save("ttsRepeatContent.mp3")
    except:
        pass


def Make_InvalidContentVoice():

    TxtInvalidInput="잘못 누르셨습니다."

    tts_InvalidInput = gTTS(text=TxtInvalidInput+"."+ttsRepeatContent, lang='ko')

    try:
        tts_InvalidInput.save("ttsInvalidContent.mp3")
    except:
        pass



# 4. 음성생성(뉴스 제목)

def Make_NewsTitleVoice(news_url_list):

    TxtNewsTitle=""

    for idx in range(0, len(news_url_list)):
        TxtNewsTitle+=str(idx+1)+". "+news_url_list[idx][1]+"\n"

    tts_NewsTitle = gTTS(text=TxtNewsTitle+"."+ttsRepeatMenu, lang='ko')

    try:
        tts_NewsTitle.save("ttsNewsTitle.mp3")
    except:
        pass

#
# GUI 화면 표시
#


# 1. 화면표시(방문환영)

def display_welcome():
    windowWelcome = Tk()
    windowWelcome.wm_attributes("-topmost", 1)
    windowWelcome.title('SKKU News TTS')
    windowWelcome.geometry("700x350")
    windowFont_20_italic_bold=tkinter.font.Font(family="맑은 고딕", size=20, slant="italic", weight="bold")
    windowFont_20_roman_bold=tkinter.font.Font(family="맑은 고딕", size=20, slant="roman", weight="bold")
    windowFont_15_italic=tkinter.font.Font(family="맑은 고딕", size=15, slant="italic")
    windowFont_15_roman=tkinter.font.Font(family="맑은 고딕", size=15, slant="roman")
    windowFont_10_italic=tkinter.font.Font(family="맑은 고딕", size=10, slant="italic")
    windowFont_10_roman=tkinter.font.Font(family="맑은 고딕", size=10, slant="roman")
    windowFont_12_italic=tkinter.font.Font(family="맑은 고딕", size=12, slant="italic")
    windowFont_12_roman=tkinter.font.Font(family="맑은 고딕", size=12, slant="roman")

    frame1 = Frame(windowWelcome, pady=15, padx=15)
    frame2 = Frame(windowWelcome, pady=15, padx=15)
    frame1.pack()
    frame2.pack()

    pygame.mixer.music.load("ttsWelcome.mp3")
    pygame.mixer.music.play(loops=0, start=0.0)

    Label(frame1, text="( *￣Ｏ￣)ノ  ( *￣Ｏ￣)ノ  ( *￣Ｏ￣)ノ", font=windowFont_20_roman_bold).pack()
    Label(frame1, text= "").pack()
    Label(frame1, text= "    SKKU News TTS 방문을 환영합니다.    ", font=windowFont_20_italic_bold).pack()
    Label(frame1, text= "").pack()
    Label(frame1, text= "ヾ( ￣Ｏ￣*) ヾ( *￣Ｏ￣*) ヾ( *￣Ｏ￣*)", font=windowFont_20_roman_bold).pack()
    Label(frame1, text= "").pack()
    label_error= Label(frame1, text="",font=windowFont_10_roman)
    label_error.pack()

    def exit_news():
        os._exit(0)
    def continue_news():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        windowWelcome.destroy()
        display_news_section()
    def click(Return): pass
    def KeyClick(e):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        if e.keysym.upper()=='S': button1.invoke()
        elif e.keysym.upper()=='X': button2.invoke()
        else:
            label_error.config(text = "잘못 누르셨습니다...")
            pygame.mixer.music.load("ttsInvalidWelcome.mp3")
            pygame.mixer.music.play(loops=0, start=0.0)
    
    button1 = Button(frame2, text="이용하기(S)",font=windowFont_12_roman, padx="50", pady="10", command=continue_news)
    button2 = Button(frame2, text="나가기(X)"  ,font=windowFont_12_roman, padx="50", pady="10", command=exit_news)

    button1.grid(row = 0, column = 0)
    button2.grid(row = 0, column = 1)

    windowWelcome.focus_set()
    button1.focus_set()

    windowWelcome.bind("<Return>",click)
    windowWelcome.bind("<KeyPress>", KeyClick)

    mainloop()
    
# 2. 화면표시(뉴스분야 선택)

def display_news_section():

    windowNewsSection = Tk()
    windowNewsSection.wm_attributes("-topmost", 1)
    windowNewsSection.title('뉴스분야 선택')
    windowNewsSection.geometry("800x400")

    windowFont_20_italic_bold=tkinter.font.Font(family="맑은 고딕", size=20, slant="italic", weight="bold")
    windowFont_20_roman_bold=tkinter.font.Font(family="맑은 고딕", size=20, slant="roman", weight="bold")
    windowFont_15_italic=tkinter.font.Font(family="맑은 고딕", size=15, slant="italic")
    windowFont_15_roman=tkinter.font.Font(family="맑은 고딕", size=15, slant="roman")
    windowFont_10_italic=tkinter.font.Font(family="맑은 고딕", size=10, slant="italic")
    windowFont_10_roman=tkinter.font.Font(family="맑은 고딕", size=10, slant="roman")
    windowFont_12_italic=tkinter.font.Font(family="맑은 고딕", size=12, slant="italic")
    windowFont_12_roman=tkinter.font.Font(family="맑은 고딕", size=12, slant="roman")
    
    frame0 = Frame(windowNewsSection, pady=15, padx=15)
    frame1 = Frame(windowNewsSection, pady=15, padx=15)
    frame2 = Frame(windowNewsSection, pady=15, padx=15)
    frame3 = Frame(windowNewsSection, pady=15, padx=15)
    frame0.pack()
    frame1.pack()
    frame2.pack()
    frame3.pack()

    pygame.mixer.music.load("ttsNewsSection.mp3")
    pygame.mixer.music.play(loops=0, start=0.0)

    label00 = Label(frame0, text="").pack()
    label01 = Label(frame0, text="♠ 뉴스분야를 선택하세요.", font=windowFont_20_italic_bold).pack()


    def exit_news():
        os._exit(0)
    def exit_current_window():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        windowNewsSection.destroy()
        display_welcome()
    def listen_again():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("ttsNewsSection.mp3")
        pygame.mixer.music.play(loops=0, start=0.0)
    def enter_news_section(news_section_no):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        windowNewsSection.destroy()
        display_choose_news(news_section_no)
    def KeyClick(e):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        if int(e.keycode)-49 in range(0,len(NewsSectionList)): buttons[int(e.keycode)-49].invoke()
        elif e.keysym.upper()=='R': button30.invoke()
        elif e.keysym.upper()=='X': button31.invoke()
        else:
            label_error.config(text = "잘못 누르셨습니다...")
            pygame.mixer.music.load("ttsInvalidInput.mp3")
            pygame.mixer.music.play(loops=0, start=0.0)

    buttons = []

    for idx in range(0,len(NewsSectionList)):
        buttons.append(Button(frame1, text= "("+str(idx+1)+") "+NewsSectionList[idx][0], width="12", height="2", font=windowFont_12_roman, command=lambda i=idx:enter_news_section(i+1)))
        buttons[idx].grid(row = 0, column = idx)

    label_error= Label(frame2, text="",font=windowFont_10_roman)
    label_error.pack()

    button30=Button(frame3, text="다시 듣기(R)", width="12", height="2", font=windowFont_12_roman, command=listen_again)
    button30.grid(row = 0, column = 0)
    button31=Button(frame3, text="나가기(X)"  ,  width="12", height="2", font=windowFont_12_roman, command=exit_current_window)
    button31.grid(row = 0, column = 1)

    windowNewsSection.bind("<KeyPress>", KeyClick)

    mainloop()


# 3. 화면표시(뉴스기사 제목 선택)

def display_choose_news(news_section_no):

    news_url='https://www.skku.edu/skku/campus/skk_comm/news0'
    news_url=news_url+str(news_section_no)+".do"
    resp=requests.get(news_url)

    soup=BeautifulSoup(resp.content,'lxml')
    url_list=soup.find('div','board-wrap board-qa').find_all('a')

    news_url_list=[]
    news_text_list=[]

    for url in url_list:
        if "mode=view" in url['href']:
            news_url_list.append([news_url+url['href'],re.sub('\u200b|\xa0|\t|\r|\n|[-=+#/\?:^$@*\"※~&%ㆍ』\\‘|\(\)\[\]\<\>`\'…》]■▲','',url.string).strip()])

    TxtNewsCount=NewsSectionList[news_section_no-1][0]+", "+str(len(news_url_list))+"개의 뉴스가 있습니다."
    tts_NewsCount = gTTS(text=TxtNewsCount, lang='ko')

    windowChooseNews = Tk()
    windowChooseNews.wm_attributes("-topmost", 1)
    windowChooseNews.title('뉴스 제목 선택')
    windowChooseNews.geometry("800x700")

    windowFont_20_italic_bold=tkinter.font.Font(family="맑은 고딕", size=20, slant="italic", weight="bold")
    windowFont_20_roman_bold=tkinter.font.Font(family="맑은 고딕", size=20, slant="roman", weight="bold")
    windowFont_15_italic=tkinter.font.Font(family="맑은 고딕", size=15, slant="italic")
    windowFont_15_roman=tkinter.font.Font(family="맑은 고딕", size=15, slant="roman")
    windowFont_10_italic=tkinter.font.Font(family="맑은 고딕", size=10, slant="italic")
    windowFont_10_roman=tkinter.font.Font(family="맑은 고딕", size=10, slant="roman")
    windowFont_12_italic=tkinter.font.Font(family="맑은 고딕", size=12, slant="italic")
    windowFont_12_roman=tkinter.font.Font(family="맑은 고딕", size=12, slant="roman")

    frame0 = Frame(windowChooseNews, pady=15, padx=15)
    frame1 = Frame(windowChooseNews, pady=15, padx=15)
    frame2 = Frame(windowChooseNews, pady=15, padx=15)
    frame3 = Frame(windowChooseNews, pady=15, padx=15)
    frame0.pack()
    frame1.pack()
    frame2.pack()
    frame3.pack()

    label00 = Label(frame0, text=TxtNewsCount, font=windowFont_20_italic_bold).pack()

    try:
        tts_NewsCount.save("ttsNewsCount"+str(news_section_no)+".mp3")
    except:
        pass

    pygame.mixer.music.load("ttsNewsCount"+str(news_section_no)+".mp3")
    pygame.mixer.music.play(loops=0, start=0.0)

    def exit_news():
        os._exit(0)
    def listen_again():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("ttsNewsTitle"+str(news_section_no)+".mp3")
        pygame.mixer.music.play(loops=0, start=0.0)
    def enter_news_content(news_contents_url):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        display_news_contents(news_contents_url)
    def exit_current_window():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        windowChooseNews.destroy()
        display_news_section()
    def KeyClick(e):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        if int(e.keycode)-49 in range(0,len(news_url_list)):
            buttons[int(e.keycode)-49].invoke()
        elif e.keysym.upper()=='R': button20.invoke()
        elif e.keysym.upper()=='X': button21.invoke()
        else:
            label_error.config(text = "잘못 누르셨습니다...")
            pygame.mixer.music.load("ttsInvalidInput.mp3")
            pygame.mixer.music.play(loops=0, start=0.0)

    buttons = []
    lables = []
    TxtNewsTitle=""

    for idx in range(0,len(news_url_list)):
        lables.append(Label(frame1,   text = "√  "+ news_url_list[idx][1], width="70", height="1", anchor=W, font=windowFont_12_roman))
        buttons.append(Button(frame1, text = "뉴스듣기("+str(idx+1)+")", width="10", height="1", font=windowFont_12_roman, command = lambda i=idx:enter_news_content(news_url_list[i][0])))
        lables[idx].grid(row=idx, column=0, padx=2, pady=1)
        buttons[idx].grid(row=idx, column=1, padx=2, pady=1)
        TxtNewsTitle+=str(idx+1)+". "+news_url_list[idx][1]+"\n"
      
    tts_NewsTitle = gTTS(text=TxtNewsTitle + ttsRepeatMenu, lang='ko')

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        tts_NewsTitle.save("ttsNewsTitle"+str(news_section_no)+".mp3")
    except:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    pygame.mixer.music.load("ttsNewsTitle"+str(news_section_no)+".mp3")
    pygame.mixer.music.play(loops=0, start=0.0)

    button20 = Button(frame2, text="다시 듣기(R)", font=windowFont_12_roman, padx="25", pady="10", command=listen_again).grid(row = 0, column = 0)
    button21 = Button(frame2, text="나가기(X)"   , font=windowFont_12_roman, padx="25", pady="10", command=exit_current_window).grid(row = 0, column = 1)

    label_error=Label(frame3, text = "", width="70", height="1", font=windowFont_12_roman)
    label_error.pack()

    windowChooseNews.bind("<KeyPress>", KeyClick)

    mainloop()


# 4. 화면표시(뉴스 콘텐츠 보여주기)

def display_news_contents(news_contents_url):

    news_content=get_news_by_url(news_contents_url)
    
    windowNewsContents = Tk()
    windowNewsContents.wm_attributes("-topmost", 1)
    windowNewsContents.title('뉴스 보기')
    windowNewsContents.geometry("1100x800")

    windowFont_20_italic_bold=tkinter.font.Font(family="맑은 고딕", size=20, slant="italic", weight="bold")
    windowFont_20_roman_bold=tkinter.font.Font(family="맑은 고딕", size=20, slant="roman", weight="bold")
    windowFont_15_italic=tkinter.font.Font(family="맑은 고딕", size=15, slant="italic")
    windowFont_15_roman=tkinter.font.Font(family="맑은 고딕", size=15, slant="roman")
    windowFont_10_italic=tkinter.font.Font(family="맑은 고딕", size=10, slant="italic")
    windowFont_10_roman=tkinter.font.Font(family="맑은 고딕", size=10, slant="roman")
    windowFont_12_italic=tkinter.font.Font(family="맑은 고딕", size=12, slant="italic")
    windowFont_12_roman=tkinter.font.Font(family="맑은 고딕", size=12, slant="roman")

    frame0 = LabelFrame(windowNewsContents, pady=2, padx=2, text="♠ 전체기사")
    frame1 = LabelFrame(windowNewsContents, pady=2, padx=2, text="♠ 키워드")
    frame2 = LabelFrame(windowNewsContents, pady=2, padx=2, text="♠ 핵심기사")
    frame3 = Frame(windowNewsContents, pady=15, padx=15)
    frame4 = Frame(windowNewsContents, pady=15, padx=15)
    frame0.pack()
    frame1.pack()
    frame2.pack()
    frame3.pack()
    frame4.pack()

    def exit_news():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        os._exit(0)
    def listen_key_content():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("ttsNewsKeyContent.mp3")
        pygame.mixer.music.play(loops=0, start=0.0)
    def listen_entire_content():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("ttsNewsEntireContent.mp3")
        pygame.mixer.music.play(loops=0, start=0.0)
    def exit_current_window():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        windowNewsContents.destroy()
    def KeyClick(e):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        if e.keysym.upper()=='F': button02.invoke()
        elif e.keysym.upper()=='M': button22.invoke()
        elif e.keysym.upper()=='R': button30.invoke()
        elif e.keysym.upper()=='X': button31.invoke()
        else:
            label_error.config(text = "잘못 누르셨습니다...")
            pygame.mixer.music.load("ttsInvalidContent.mp3")
            pygame.mixer.music.play(loops=0, start=0.0)
    def listen_again():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load("ttsRepeatContent.mp3")
        pygame.mixer.music.play(loops=0, start=0.0)


    # BeautifulSoup 에서 반환된 기사본문을 문장단위로 분할
    sentences=[]
    stopwords = {'제목', '제작', '학생', '교수', '있다'}

    kiwi= Kiwi()

    sentences = kiwi.split_into_sents(news_content)
    texts = []

    idx=0

    for idx in range(0, len(sentences)):
        texts.append(sentences[idx].text)

    sents1 = [normalize(text, english=True, number=True) for text in texts]

    sents1 = '.'.join(texts)

    try:
        ttsNewsEntireContent = gTTS(text=sents1, lang='ko')
    except:
        ttsNewsEntireContent = gTTS(text='음성 변환이 불가능한 기사입니다.', lang='ko')

    try:
        ttsNewsEntireContent.save("ttsNewsEntireContent.mp3")
    except:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    label01 = Label(frame0, text=sents1, justify=LEFT, wraplength=1000, width=140)
    button02= Button(frame0, text="전체기사 듣기(F)", width=20, height=2,command=listen_entire_content)

    label01.pack()
    button02.pack()

    # 뉴스기사 본문에서 요약문장을 추출한다.

    try:
        keywords, keysentences = summarize_with_sentences(sents1, stopwords = stopwords, diversity=0.3, num_keywords=3, num_keysents=1, scaling=lambda x:0.5, verbose=False)
        keywords1=', '.join(keywords)
        keysentences1 = '.'.join(keysentences)
        
        label11 = Label(frame1, text=keywords, wraplength=1000, width=140)
        label21 = Label(frame2, text=keysentences1, wraplength=1000, width=140)
        try:
            ttsNewsKeyContent = gTTS(text=keysentences1, lang='ko')
        except:
            ttsNewsKeyContent = gTTS(text='음성변환이 불가능한 기사입니다.', lang='ko')

        button22=Button(frame2, text="핵심기사 듣기(M)", width=20, height=2, command=listen_key_content)

        label11.pack()
        label21.pack()
        button22.pack()

    except:
        label11 = Label(frame1, text="유효한 키워드가 없습니다.", wraplength=1000, width=140)
        label21 = Label(frame2, text="유효한 키워드가 없어 핵심기사를 추출할 수 없습니다.", wraplength=1000, width=140)
        label11.pack()
        label21.pack()

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        ttsNewsKeyContent.save("ttsNewsKeyContent.mp3")
    except:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    label_error= Label(frame3, text="")
    label_error.pack()

    button30 = Button(frame4, text="다시 듣기(R)", padx="25", pady="10", command=listen_again)
    button31 = Button(frame4, text="나가기(X)"   , padx="25", pady="10", command=exit_current_window)

    button30.grid(row = 0, column = 0)
    button31.grid(row = 0, column = 1)

    windowNewsContents.bind("<KeyPress>", KeyClick)
    
    mainloop()



#뉴스기사 본문 추출하는 함수
def get_news_by_url(url):
    headers={
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'ko,en;q=0.9,en-US;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53'
    }
    res=requests.get(url,headers=headers)
    bs=BeautifulSoup(res.content,'html.parser')

    #본문 찾아오기 (html 분석하여 기사 본문 담고 있는 html tag  지정)
    content=bs.find('div','fr-view')

    selects = content.findAll('span')
    for span in selects:
        span.decompose()
    content1=content.text
    content2=re.sub('\u200b|\xa0|\t|\r|\n|[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]','',content1)

    return content2


##############################################
###             프로그램 구동              ###
##############################################

# 기본 음성 안내파일 생성

Make_WelcomeVoice()
Make_NewsSectionVoice()
Make_InvalidInputVoice()
Make_InvalidWelcomeVoice()
Make_InvalidContentVoice()
Make_RepeatContentMenu()

# Welcome 화면 표시

display_welcome()

