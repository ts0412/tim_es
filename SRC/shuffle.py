import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fld
import tkinter.messagebox as msg
import random
import csv

deck = [] #デッキリスト
shuffle_counter = 0 #シャッフルした回数(合計)
way_counter = 0 #途中経過カウント用
num_hindu= 0
num_deal = 0
num_faro = 0 #それぞれの方法でシャッフルした回数
msge = ""
judge = 0

  
# ヒンズーシャッフル
def hindu(deckList):
    hindu_deck = []
    remainCard = random.randint(1,4) ##人間性を加味してデッキの上1~4枚は残るようにしている
    topCard = random.randint(remainCard,len(deckList)-1)
    bottomCard = random.randint(topCard+1,len(deckList)-1)

    ##上下で分かれるパターン
    if(bottomCard==59):
        split_deck_t = deckList[:topCard]
        split_deck_b = deckList[topCard:]
        hindu_deck = split_deck_t + split_deck_b

    ##デッキの中央部分を引き抜いて行うパターン
    else:
        split_deck_t = deckList[:topCard]
        split_deck_m = deckList[topCard:bottomCard]
        split_deck_b = deckList[bottomCard:]

        combined_deck_t_b = split_deck_t + split_deck_b
        hindu_deck = split_deck_m + combined_deck_t_b

    #シャッフル後のデッキリスト保存
    with open('after_hindu'+str(way_counter)+'.txt','w',newline="") as newDeckList:
        writer = csv.writer(newDeckList)
        writer.writerows(hindu_deck)
    saveDeck(hindu_deck)


# ディールシャッフル
def deal(deckList):
    N = random.randint(7,12) ##ディールで分ける枚数が人それぞれなので乱数で決めている
    deal_piles = {}
    deal_deck = []

    for i in range(len(deckList)):
        if i < N:
            deal_piles[i%N] = []
        deal_piles[i%N].append(deckList[i])

    random.shuffle(deal_piles)
    
    for i in deal_piles.values():
        deal_deck.extend(i)
    
    #シャッフル後のデッキリスト保存
    with open('after_deal'+str(way_counter)+'.txt','w',newline="") as newDeckList:
        writer = csv.writer(newDeckList)
        writer.writerows(deal_deck)
    saveDeck(deal_deck)


# ファローシャッフル
def faro(deckList):
    faro_deck = [i for i in range(len(deckList))]
    top_half = deckList[:30]
    bottom_half = deckList[30:]

    faro_deck[::2] = top_half
    faro_deck[1::2] = bottom_half
    
    #シャッフル後のデッキリスト保存
    with open('after_faro'+str(way_counter)+'.txt','w',newline="") as newDeckList:
        writer = csv.writer(newDeckList)
        writer.writerows(faro_deck)
    saveDeck(faro_deck)


# デッキリストの読み込み
def import_deckList():
    typ = [('テキストファイル','*.txt')]
    dir = 'C:\\pg'
    fle = fld.askopenfilename(filetypes=typ, initialdir=dir)
    with open(fle,encoding="utf-8") as deckList:
       reader = csv.reader(deckList)
       deckList = [row for row in reader]

    saveDeck(deckList)

    return deckList


# デッキリスト保存
def saveDeck(deckFile):
    global deck
    deck = deckFile
    return deck


# デッキリスト読み込み画面
def readDeck():
    global frame
    global judge

    #画面遷移用
    if judge==0:
        frame.destroy()
    else:
        frame_app.destroy()
    judge = 0

    # メインフレームの作成と設置
    frame = ttk.Frame(root)
    frame.pack(fill = tk.BOTH, pady=20)

    # 各種ウィジェットの作成
    label1_frame = ttk.Label(frame, text="シャッフル")
    label1_frame = ttk.Label(frame, text="デッキリストを選択して下さい\nその後OKを押して下さい")
    button_fileImport = ttk.Button(frame, text="ファイルを選択", command=import_deckList)
    button_go_shuffle = ttk.Button(frame, text="OK", command=shuffleDeck)
    
    # 各種ウィジェットの設置
    label1_frame.pack()
    button_fileImport.pack()
    button_go_shuffle.pack()

# シャッフル画面
def shuffleDeck():
    global frame_app
    global judge

    #画面遷移用
    if judge==0:
        frame.destroy()
    else:
        frame_app.destroy()
    judge = 1

    # メインフレームの作成と設置
    frame_app = ttk.Frame(root)
    frame_app.pack(fill = tk.BOTH, pady=20)
    

    # 各種ウィジェットの作成
    label1_frame_app = ttk.Label(frame_app, text="シャッフル")
    button_start_shuffle = ttk.Button(frame_app, text="シャッフル開始", command=sd)
    button_back_import = ttk.Button(frame_app, text="戻る", command=readDeck)


    # 各種ウィジェットの設置
    label1_frame_app.pack()
    button_start_shuffle.pack()
    button_back_import.pack()

# シャッフル実行関数
def sd():
    global shuffle_counter
    global way_counter 
    global num_hindu, num_deal, num_faro
    global msge
    shuffle_types = []
    
    shuffle_counter = random.randint(3,5)
    shuffle_types = [random.randint(0,2) for i in range(5)]
    
    #3~5回の中で無作為にシャッフルを実行
    if shuffle_counter == 3:
        for c in range(3):
            way_counter = c + 1
            if shuffle_types[c] == 0:
                hindu(deck)
                num_hindu += 1
            elif shuffle_types[c] == 1:
                deal(deck)
                num_deal += 1
            else:
                faro(deck)
                num_faro += 1

    elif shuffle_counter == 4:
        for c in range(4):
            way_counter = c + 1
            if shuffle_types[c] == 0:
                hindu(deck)
                num_hindu += 1
            elif shuffle_types[c] == 1:
                deal(deck)
                num_deal += 1
            else:
                faro(deck)
                num_faro += 1

    else:
        for c in range(5):
            way_counter = c + 1
            if shuffle_types[c] == 0:
                hindu(deck)
                num_hindu += 1
            elif shuffle_types[c] == 1:
                deal(deck)
                num_deal += 1
            else:
                faro(deck)
                num_faro += 1

    #シャッフル内容のメッセージ
    msge = "総シャッフル回数: "+str(shuffle_counter)+" 回\n\n内訳\nヒンズー: "+str(num_hindu)+" 回\nディール: "+str(num_deal)+" 回\nファロー: "+str(num_faro)+" 回\n\n出力ファイル名: after_shuffle.txt"
    info_msg = msg.showinfo(title="information", message=msge)

    #シャッフル後のデッキリスト保存
    with open('after_shuffle.txt','w',newline="") as newDeckList:
        writer = csv.writer(newDeckList)
        writer.writerows(deck)


#メイン画面
if __name__ == "__main__": 
    # rootメインウィンドウの設定
    root = tk.Tk()
    root.title("シャッフル")
    root.geometry("500x300")

    # メインフレームの作成と設置
    frame = ttk.Frame(root)
    frame.pack(fill = tk.BOTH, pady=20)

    # 各種ウィジェットの作成
    label1_frame = ttk.Label(frame,text="概要\n1. CSV形式のデッキリストを読み込み\n2. シャッフルをランダムに数種類実行\n3. シャッフル後のデッキリストを出力")
    button_fileImport = ttk.Button(frame,text="OK", command=readDeck)

    # 各種ウィジェットの設置
    label1_frame.pack()
    button_fileImport.pack()
    
    root.mainloop()
    





