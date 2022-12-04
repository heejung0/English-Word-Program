from numpy import random
from tkinter import *
from tkinter import messagebox # 결과창을 위한 messagebox 사용
from tkinter.filedialog import askopenfilename
import chardet # 인코딩을 인식하기 위한 chardet 모듈 사용
import pandas as pd # 기록 확인 표 생성을 위한 pandas 모듈 사용

# 전역 변수
a = 0
b = 0
correctEnglish = 0
correctKorean = 0

# 영어 시험 보는 메소드 선언
def englishTest():
    readFile = askopenfilename() # 파일 탐색기로부터 파일 경로를 반환

    # 파일 종류에 따라 인코딩값 다르게 선언
    firstRead = open(readFile, 'rb').read()
    result = chardet.detect(firstRead)
    encodingValue = result['encoding']
    infile = open(readFile, "r", encoding=encodingValue)

    # 영어, 한글 리스트 선언 및 분할
    english = []
    korean = []
    for line in infile:
        line = line.rstrip() # 오른쪽에 있는 공백 제거
        # try~except문을 이용하여 나뉘어 있는 문구에 따라 다르게 예외처리
        try:
            (e, k) = line.split(" ") # 공백을 기준으로 왼쪽은 e, 오른쪽은 k
        except:
            (e, k) = line.split(",") # 콤마를 기준으로 왼쪽은 e, 오른쪽은 k
        english.append(e) # e는 english의 요소로 추가
        korean.append(k) # k는 korean의 요소로 추가
    infile.close() # 파일을 사용하고 난 뒤 close()를 호출하여 파일 닫기

    # 중복 단어 제거
    newEnglish = []
    newKorean = []
    for i in english: # english 리스트에 있고
        if i not in newEnglish: # newEnglish 리스트에 없다면
            newEnglish.append(i) # newEnglish 리스트의 요소로 추가
    for i in korean: # korean 리스트에 있고
        if i not in newKorean: # newKorean 리스트에 없다면
            newKorean.append(i) # newKorean 리스트의 요소로 추가

    # 영어 시험 창 구성
    window = Tk()
    window.title("English Test")
    window.geometry('500x400')
    window.resizable(False, False)

    # 문제 수를 나타내는 Label 선언
    count = Label(window, text="", font=('D2 Coding', 10))
    count.pack(pady=10)
    # 문제를 출력할 Label 선언
    label = Label(window, text="", borderwidth=2, width=35, height=3, bg='white', relief='solid', font=('D2 Coding', 12))
    label.pack(pady=50)
    # 답을 입력받을 Entry 선언
    entry = Entry(window, font=('D2 Coding', 12))
    entry.pack(ipadx=10, ipady=10, padx=10, pady=50)

    intList = list(range(0, len(newEnglish)))  # 단어 개수 만큼의 정수 리스트
    randomNum = random.choice(intList, size=len(newEnglish), replace=False)  # 비복원 추출

    # 문제 메소드 선언
    def question():
        global a # 전역 변수로 문제의 수를 카운트 하는 변수 a 선언
        global correctEnglish # 전역 변수로 맞춘 영어 문제의 수를 카운트 하는 변수 correctEnglish 선언
        if a == len(newEnglish): # a가 newEnglish의 길이와 같으면
            messagebox.showinfo("시험 종료", f"총 {len(newEnglish)}문제 중 {correctEnglish}문제를 맞추셨습니다!") # 결과창을 띄우고
            window.destroy() # 시험보는 창을 종료
            a = 0 # 재시험 가능하도록 a의 값을 0으로 초기화
            correctEnglish = 0 # 재시험 가능하도록 correctEnglish의 값을 0으로 초기화
        else:
            count.config(text=f"{a + 1}번 문제") # configuration을 이용하여 text의 내용이 변화될 수 있도록 함
            label.config(text=f"'{newKorean[randomNum[a]]}'(이)라는 뜻을 가진 단어는?") # configuration을 이용하여 text의 내용이 변화될 수 있도록 함
            entry.delete(0, END)

    question() # 문제 실행

    # 시험 결과를 판단하는 메소드 선언
    def test():
        global correctEnglish # 맞춘 문제의 수를 세는 전역 변수 선언
        global a # 문제의 수를 세는 전역 변수 선언
        if entry.get() == newEnglish[randomNum[a]]: # Entry에 입력받은 문자열이 답과 같다면
            messagebox.showinfo("결과", "정답입니다!") # 메시지를 띄우고
            result = open("out.csv", "a") # 결과를 out.csv 파일에 저장
            result.write(f"E, {newKorean[randomNum[a]]}, {entry.get()}, {newEnglish[randomNum[a]]}, O\n") # 시험 종류, 문제, 입력한 답, 정답, 정답여부 순으로 작성
            result.close() # 파일을 사용하고 난 뒤에는 close()를 호출하여 닫음
            correctEnglish += 1 # 맞춘 문제 +1
            a += 1 # 문제 수 +1
            question() # 문제 실행
        else: # 틀렸을 경우
            messagebox.showinfo("결과", f"오답입니다! 정답은 '{newEnglish[randomNum[a]]}'입니다!") # 답을 알려주는 메시지를 띄우고
            result = open("out.csv", "a") # 결과를 out.csv 파일에 저장
            result.write(f"E, {newKorean[randomNum[a]]}, {entry.get()}, {newEnglish[randomNum[a]]}, X\n") # 시험 종류, 문제, 입력한 답, 정답, 정답여부 순으로 작성
            result.close() # 파일을 사용하고 난 뒤에는 close()를 호출하여 닫음
            a += 1 # 문제 수 +1
            question() # 문제 실행

    # 정답 확인 후 다음 문제로 넘어가는 버튼 생성
    nextQuestion = Button(window, font=('D2 Coding', 12), text="다음 문제", bg='white', command=test)
    nextQuestion.pack(ipadx=8, ipady=8)
    window.mainloop()

# 한글 시험 보는 메소드 선언
def koreanTest():
    readFile = askopenfilename()  # 파일 탐색기로부터 파일 경로를 반환

    # 파일 종류에 따라 인코딩값 다르게 선언
    firstRead = open(readFile, 'rb').read()
    result = chardet.detect(firstRead)
    encodingValue = result['encoding']
    infile = open(readFile, "r", encoding=encodingValue)

    # 영어, 한글 리스트 선언 및 분할
    english = []
    korean = []
    for line in infile:
        line = line.rstrip()
        # try~except문을 이용하여 나뉘어 있는 문구에 따라 다르게 예외처리
        try:
            (e, k) = line.split(" ") # 공백을 기준으로 왼쪽은 e, 오른쪽은 k
        except:
            (e, k) = line.split(",") # 콤마를 기준으로 왼쪽은 e, 오른쪽은 k
        english.append(e) # e는 english의 요소로 추가
        korean.append(k) # k는 korean의 요소로 추가
    infile.close()  # 파일을 사용하고 난 뒤 close()를 호출하여 파일 닫기

    # 중복 단어 제거
    newEnglish = []
    newKorean = []
    for i in english:  # english 리스트에 있고
        if i not in newEnglish:  # newEnglish 리스트에 없다면
            newEnglish.append(i)  # newEnglish 리스트의 요소로 추가
    for i in korean:  # korean 리스트에 있고
        if i not in newKorean:  # newKorean 리스트에 없다면
            newKorean.append(i)  # newKorean 리스트의 요소로 추가

    # 한글 시험 창 구성
    window = Tk()
    window.title("한글 시험")
    window.geometry('500x400')
    window.resizable(False, False)

    # 문제 수를 나타내는 Label 선언
    count = Label(window, text="", font=('D2 Coding', 10))
    count.pack(pady=10)
    # 문제를 출력할 Label 선언
    label = Label(window, text="", borderwidth=2, width=35, height=3, bg='white', relief='solid', font=('D2 Coding', 12))
    label.pack(pady=50)
    # 답을 입력받을 Entry 선언
    entry = Entry(window, font=('D2 Coding', 12))
    entry.pack(ipadx=10, ipady=10, padx=10, pady=50)

    intList = list(range(0, len(newKorean)))  # 단어 개수 만큼의 정수 리스트
    randomNum = random.choice(intList, size=len(newKorean), replace=False)  # 비복원 추출

    # 문제 메소드 선언
    def question():
        global b # 전역 변수로 문제의 수를 카운트 하는 변수 b 선언
        global correctKorean # 전역 변수로 맞춘 한글 문제의 수를 카운트 하는 변수 correctKorean 선언
        if b == len(newKorean): # b가 newKorean의 길이와 같으면
            messagebox.showinfo("시험 종료", f"총 {len(newKorean)}문제 중 {correctKorean}문제를 맞추셨습니다!") # 결과창을 띄우고
            window.destroy() # 시험보는 창을 종료
            b = 0 # 재시험 가능하도록 b의 값을 0으로 초기화
            correctKorean = 0 # 재시험 가능하도록 correctKorean의 값을 0으로 초기화
        else:
            count.config(text=f"{b + 1}번 문제") # configuration을 이용하여 text의 내용이 변화될 수 있도록 함
            label.config(text=f"'{newEnglish[randomNum[b]]}'의 뜻은?") # configuration을 이용하여 text의 내용이 변화될 수 있도록 함
            entry.delete(0, END)

    question() # 문제 실행

    # 시험 결과를 판단하는 메소드 선언
    def test():
        global correctKorean # 맞춘 문제의 수를 세는 전역 변수 선언
        global b # 문제의 수를 세는 전역 변수 선언
        if entry.get() == newKorean[randomNum[b]]: # Entry에 입력받은 문자열이 답과 같다면
            messagebox.showinfo("결과", "정답입니다!") # 메시지를 띄우고
            result = open("out.csv", "a") # 결과를 out.csv 파일에 저장
            result.write(f"K, {newEnglish[randomNum[b]]}, {entry.get()}, {newKorean[randomNum[b]]}, O\n") # 시험 종류, 문제, 입력한 답, 정답, 정답여부 순으로 작성
            result.close() # 파일을 사용하고 난 뒤에는 close()를 호출하여 닫음
            correctKorean += 1 # 맞춘 문제 +1
            b += 1 # 문제 수 +1
            question() # 문제 실행
        else: # 틀렸을 경우
            messagebox.showinfo("결과", f"오답입니다! 정답은 '{newKorean[randomNum[b]]}'입니다!") # 답을 알려주는 메시지를 띄우고
            result = open("out.csv", "a") # 결과를 out.csv 파일에 저장
            result.write(f"K, {newEnglish[randomNum[b]]}, {entry.get()}, {newKorean[randomNum[b]]}, X\n") # 시험 종류, 문제, 입력한 답, 정답, 정답여부 순으로 작성
            result.close() # 파일을 사용하고 난 뒤에는 close()를 호출하여 닫음
            b += 1  # 문제 수 +1
            question() # 문제 실행

    # 정답 확인 후 다음 문제로 넘어가는 버튼 생성
    nextQuestion = Button(window, font=('D2 Coding', 12), text="다음 문제", bg='white', command=test)
    nextQuestion.pack(ipadx=8, ipady=8)
    window.mainloop()

# 기록을 확인하는 메소드 선언
def record():
    # 영어 시험 기록을 확인하는 메소드
    def englishRecord():
        # 공백 리스트 선언
        question = []
        yourAnswer = []
        correctAnswer = []
        correct = []

        infile = open("out.csv", "r") # 결과를 저장했던 out.csv파일을 읽어서
        for line in infile:
            line = line.rstrip() # 오른쪽 공백을 제거
            (t, q, yA, cA, c) = line.split(", ") # 콤마를 기준으로 t, q, yA, cA, c로 분할
            if t == 'E': # 시험 종류가 'E'라면 (영어 시험일 때)
                question.append(q) # q를 question의 요소로 추가
                yourAnswer.append(yA) # yA를 yourAnswer의 요소로 추가
                correctAnswer.append(cA) # cA를 correctAnswer의 요소로 추가
                correct.append(c) # c를 correct의 요소로 추가
        infile.close() # 파일을 사용하고 난 뒤에는 close()를 호출하여 닫음

        # 기록 확인을 위한 표 생성
        col = ['문제', '입력한 답', '정답', '정답여부'] # 열 요소
        ind = [] # 행 요소
        con = [] # 내용(데이터)
        for i in range(0, len(question)):
            ind.append(i + 1) # 문제 개수를 세기 위한 행 요소
        for i in range(0, len(question)):
            con.append([question[i], yourAnswer[i], correctAnswer[i], correct[i]]) # 데이터 구성
        table = pd.DataFrame(con, columns=col, index=ind) # pandas를 이용한 표 생성

        # 영어 시험 기록 확인 창 구성
        window = Tk()
        window.title("English Test Record")
        window.geometry('800x600')
        window.resizable(False, False)
        context = Text(window, font=('D2 Coding', 15))
        context.pack(padx=10, pady=10)
        context.insert(CURRENT, table)
        window.mainloop()

    # 한글 시험 기록 확인을 위한 메소드
    def koreanRecord():
        # 공백 리스트 선언
        question = []
        yourAnswer = []
        correctAnswer = []
        correct = []

        infile = open("out.csv", "r") # 결과를 저장했던 out.csv파일을 읽어서
        for line in infile:
            line = line.rstrip() # 오른쪽 공백을 제거
            (t, q, yA, cA, c) = line.split(", ") # 콤마를 기준으로 t, q, yA, cA, c로 분할
            if t == 'K': # 시험 종류가 'K'라면 (한글 시험일 때)
                question.append(q) # q를 question의 요소로 추가
                yourAnswer.append(yA) # yA를 yourAnswer의 요소로 추가
                correctAnswer.append(cA) # cA를 correctAnswer의 요소로 추가
                correct.append(c) # c를 correct의 요소로 추가
        infile.close() # 파일을 사용하고 난 뒤에는 close()를 호출하여 닫음

        # 기록 확인을 위한 표 생성
        col = ['문제', '입력한 답', '정답', '정답여부'] # 열 요소
        ind = [] # 행 요소
        con = [] # 내용(데이터)
        for i in range(0, len(question)):
            ind.append(i + 1) # 문제 개수를 세기 위한 행 요소
        for i in range(0, len(question)):
            con.append([question[i], yourAnswer[i], correctAnswer[i], correct[i]]) # 데이터 구성
        table = pd.DataFrame(con, columns=col, index=ind) # pandas를 이용한 표 생성

        # 한글 시험 기록 확인 창 구성
        window = Tk()
        window.title("한글 시험 기록")
        window.geometry('800x600')
        window.resizable(False, False)
        context = Text(window, font=('D2 Coding', 15))
        context.pack(padx=10, pady=10)
        context.insert(CURRENT, table)
        window.mainloop()

    # 기록 확인 창 구성
    window = Tk()
    window.title("기록 확인")
    window.geometry('600x400')
    window.resizable(False, False)
    label = Label(window, text='[Record]', font=('D2 Coding', 40))
    label.place(x=180, y=80)
    # '영어 시험 기록' 버튼을 누르면 englishRecord 메소드 호출
    button1 = Button(window, relief='solid', font=('D2 Coding', 20), text='영어 시험 기록', bg='white', command=englishRecord)
    button1.place(x=70, y=270)
    # '한글 시험 기록' 버튼을 누르면 koreanRecord 메소드 호출
    button2 = Button(window, relief='solid', font=('D2 Coding', 20), text='한글 시험 기록', bg='white', command=koreanRecord)
    button2.place(x=330, y=270)
    window.mainloop()

# 시작 메뉴 구성
window = Tk()
window.title('영어 단어 프로그램')
window.geometry('1000x600')
window.resizable(False, False)
label1 = Label(window, text='[English Word Program]', font=('D2 Coding', 50))
label1.place(x=130, y=50)
# '영어 시험' 버튼을 누르면 englishTest 메소드 호출
button1 = Button(window, relief='solid', font=('D2 Coding', 30), text='영어 시험', bg='white', command=englishTest)
button1.place(x=400, y=170)
# '한글 시험' 버튼을 누르면 koreanTest 메소드 호출
button2 = Button(window, relief='solid', font=('D2 Coding', 30), text='한글 시험', bg='white', command=koreanTest)
button2.place(x=400, y=270)
# '기록 확인' 버튼을 누르면 record 메소드 호출
button3 = Button(window, relief='solid', font=('D2 Coding', 30), text='기록 확인', bg='white', command=record)
button3.place(x=400, y=370)
# '종료' 버튼을 누르면 창 종료
button4 = Button(window, relief='solid', font=('D2 Coding', 30), text='종료', bg='white', command=window.destroy)
button4.place(x=440, y=470)

window.mainloop()