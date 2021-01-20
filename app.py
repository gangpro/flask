from flask import Flask, render_template, request     # Flask import
import random
import requests
app = Flask(__name__)       # app 초기화 과정


@app.route("/")  # Decorator  # route 디렉토리로 들어오면 hello world를 출력시킬거란 의미
def hello():
    return "Hello World!"


@app.route('/hello')
def hello_new():
    return "Hello? Hello! New World!"


@app.route('/greeting/<string:name>')
def greeting(name):     # name이라는 변수를 받겠다라는 의미
    return f'반갑습니다! {name}님!'


@app.route('/cube/<int:num>')
def cube(num):
    result = num ** 3  # 3제곱이라는 의미(num*num*num 같다.)
    return str(result)  # return은 string 값을 가져오기 때문에 위와 return result만 하면 타입 오류가 발생한다. 그래서 str(return)을 해야한다.


@app.route('/lunch/<int:person>')
def lunch(person):
    # menu라는 리스트를 만들고
    # 사람 수 만큼 랜덤 아이템을 뽑아서 반환
    menu = ['짜장면', '짬뽕', '짬짜면', '삼선고추짬뽕', '복짬면', '탕수육']
    order = random.sample(menu, person)
    return f'{order} 주문할게요!'


@app.route('/html')
def html():
    return '''
    <h1>Happy Hacking!</h1>
    <p>즐겁게 코딩합시다 :)</p>
    '''


@app.route('/html_file')
def html_file():
    return render_template('html_file.html')  # import render_template 해야 사용 가능


@app.route('/hi/<string:name>')
def hi(name):
    return render_template('/hi.html', name=name)


@app.route('/cube_new/<int:number>')
def cube_new(number):
    # 계산
    result = number ** 3
    return render_template('/cube_new.html', result=result, number=number)

# Fake naver
@app.route('/naver')
def naver():
    return render_template('naver.html')


# ex 사용자 로그인 페이지 같은 곳, 값을 넣어서 보내는 곳
@app.route('/send')
def send():
    return render_template('send.html')


# send에서 작성한 것을 receive로 받는다.
@app.route('/receive')
def receive():
    username = request.args.get('username')
    message = request.args.get('message')
    return render_template('receive.html', username=username, message=message)


# 사용자의 uersname과 password를 input으로 받는다.
# form action을 통해 login_check로 redirect한다.
@app.route('/login')
def login():
    return render_template('login.html')


# 사용자의 입력이 admin / admin123이 맞는지 확인한다.
# 맞으면 '환영합니다.' 아니면 '관리자가 아닙니다'
# 라고 출력한다.
@app.route('/login_check')
def login_check():
    username = request.args.get('username')
    password = request.args.get('password')

    if username == 'admin' and password == 'admin123':
        message = '환영합니다.'
    else:
        message = '관리자가 아닙니다.'

    return render_template('login_check.html', message=message)


# 사용자의 로또 input을 받는다.
# lotto_result로 받는다.
@app.route('/lotto_check')
def lotto_check():
    return render_template('lotto_check.html')


@app.route('/lotto_result')
def lotto_result():
    # lotto_check에서 보낸 lotto_round input을 받는다.
    lotto_round = request.args.get('lotto_round')
    numbers = [int(num) for num in lotto_round.split()]
    print(lotto_round)  # 10 23 29 33 37 40

    # 동행복권 사이트에서 1회차 로또 당첨 번호를 JSON으로 가져온다.
    url = 'https://dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=1'
    response = requests.get(url)  # Response [200] : '응답을 잘 받았다'라는 의미
    print(response.json())  # {'totSellamnt': 3681782000, 'returnValue': 'success', 'drwNoDate': '2002-12-07', 'firstWinamnt': 0, 'drwtNo6': 40, 'drwtNo4': 33, 'firstPrzwnerCo': 0, 'drwtNo5': 37, 'bnusNo': 16, 'firstAccumamnt': 863604600, 'drwNo': 1, 'drwtNo2': 23, 'drwtNo3': 29, 'drwtNo1': 10}
    json = response.json()
    drwNo = json[f'drwNo']  # 제 n 회
    bnusNo = json[f'bnusNo']  # 보너스 넘버

    # 방법 1
    # winner = []
    # for i in range(1, 7):
    #     winner.append(json[f'drwtNo{i}'])
    # print('winner : ', winner)  # winner :  [10, 23, 29, 33, 37, 40]

    # 방법 2
    winner = [json[f'drwtNo{i}'] for i in range(1, 7)] # 당첨번호



    # 번호 당첨 여부 확인하기
    if len(numbers) != 6:
        result = '번호의 수가 6개가 아닙니다!'
    else:
        matched = len(set(winner) & set(numbers))
        if matched == 6:
            result = '1등 당첨을 축하드립니다.'
        elif matched == 5:
            if json['bnusNo'] in numbers:
                result = '2등 당첨을 축하드립니다.'
            else:
                result = '3등 당첨을 축하드립니다.'
        elif matched == 4:
            result = '4등 당첨을 축하드립니다.'
        elif matched == 3:
            result = '5등 당첨을 축하드립니다.'
        else:
            result = '낙첨 되었습니다.'

    return render_template('/lotto_result.html', winner=winner, numbers=numbers, drwNo=drwNo, bnusNo=bnusNo, result=result)


# python name.py로 설정할 수 있도록 설정방법
# app.py 파일이 'python app.py'로 시작되었을 때
# 서버를 시작하겠다 라는 의미.
if __name__ == '__main__':
    app.run(debug=True)
    # 서버가 실행이 되어있는동안 수정이 되면 자동으로 재시작을 하겠다 라는 의미

# 방법 1. 모듈로 실행 : flask run
# 방법 2. 직접 실행(코드작성해야함) : python app.py


