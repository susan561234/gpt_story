from flask import Flask, render_template, jsonify, request, url_for, redirect, make_response, session
import chaptgptget
import Image
from unidecode import unidecode
import voice
from concurrent.futures import ThreadPoolExecutor
import mongod
import datetime
import pandas as pd
import dash
from dash.dependencies import Input, Output
import uuid
from dash import html
from dash import dcc
from openai.error import RateLimitError
import mysqldatabase as md
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import timedelta
import os
import configparser



def story_split_start(story):
    if "故事名稱:" in story:
        story_split =  story.split("故事名稱:")
        story_split_1 = story_split[1].split("故事開頭:")
    elif "故事名稱：" in story:
        story_split =  story.split("故事名稱：")
        story_split_1 = story_split[1].split("故事開頭：")
    else:
        pass
    main_character = story_split[0]
    story_name = "<<" + story_split_1[0] + ">>"
    if "選項:1." in story:
        button = story.split("選項:1.")[1]
        story_notbutton = story_split_1[1].split("選項:1.")[0]
    elif "選項: 1." in story:
        button = story.split("選項: 1.")[1]
        story_notbutton = story_split_1[1].split("選項: 1.")[0]
    else:
        button = story.split("選項：1.")[1]
        story_notbutton = story_split_1[1].split("選項：1.")[0]
    button1 = button.split("2.")[0]
    button3 = button.split("3.")[1]  
    button2 = button[len(button1)+2:len(button)-len(button3)-2]
    return main_character, story_name,story_notbutton,button1,button2,button3
def story_split_item(updated_data):
    if "選項:1." in updated_data:
        button = updated_data.split("選項:1.")[1]
        story_notbutton = updated_data.split("選項:1.")[0][5:]
    elif "選項: 1." in updated_data:
        button = updated_data.split("選項: 1.")[1]
        story_notbutton = updated_data.split("選項: 1.")[0][5:]
    else:
        button = updated_data.split("選項：1.")[1]
        story_notbutton = updated_data.split("選項：1.")[0][5:]
    try:
        other_word = story_notbutton.split("故事內容")[0]
        if len(story_notbutton) != len(other_word):
            story_notbutton = story_notbutton.split("故事內容")[1][1:]
    except IndexError as e:
        print("IndexError",e)
        story_notbutton = story_notbutton.split("故事內容")[0]
    button1 = button.split("2.")[0]
    button3 = button.split("3.")[1]  
    button2 = button[len(button1)+2:len(button)-len(button3)-2]
    return story_notbutton,button1,button2,button3
def story_split_over(updated_data):
    updated_data = updated_data[5:]
    if "。" in updated_data:
        count = updated_data.split("。")
        if len(count) == 3:
            button_1 = count[0]
            button_2 = count[1]
            button_3 = count[2]
        elif  len(count) >3:
            button_1 = count[0]+count[1]
            button_2 = count[len(count)-2]
            button_3 = count[len(count)-1]
        elif len(count) <3:
            if len(count) == 2:
                button_1 = count[0]+count[1]
                button_2 = count[0]+count[1]
                button_3 = count[1]
            else :
                button_1 = count[0]+count[0]
                button_2 = count[0]+count[0]
                button_3 = count[0]
    return updated_data,button_1,button_2,button_3

def process_image_and_voice(main_character,story_notbutton,buttom1,buttom2,buttom3):
    image_url = Image.stable_diffusion_photo(main_character,story_notbutton,buttom1,buttom2,buttom3)
    voice.TTS(story_notbutton)
    return image_url
def image_voice(main_character,story_notbutton,button1,button2,button3):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(process_image_and_voice, main_character,story_notbutton,button1,button2,button3)
        image_url = future.result()
    return image_url
def page_not_found(e):
  return render_template('404.html'), 404

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR ,'config.ini'))
app.config['SECRET_KEY']=config.get('flask', 'SECRET_KEY')
app.permanent_session_lifetime = timedelta(hours=1)
app.register_error_handler(404, page_not_found)
MD = md.User()
DB = mongod.DB()
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app1 = dash.Dash(__name__, server=app, url_base_pathname='/dash/',external_stylesheets=external_stylesheets)
@app.before_request
def before_request_func():
    global count1, count2, count3, df, count4, count5
    if request.path == '/dash/': 
        count1, count2, count3,count4 = DB.DB_find_style(pd.date_range(start='2023-05-18', periods=30))
        count5 = DB.DB_find_people(pd.date_range(start='2023-05-18', periods=30))
    df = pd.DataFrame({
        'date': pd.date_range(start='2023-05-18', periods=30),
        '科幻': count1,
        "魔法": count2,
        "童話": count3,
        "人數_over": count4,
        "人數_start": count5
    })

count1, count2, count3, count4 =DB.DB_find_style(pd.date_range(start='2023-05-18', periods=30))
count5 = DB.DB_find_people(pd.date_range(start='2023-05-18', periods=30))
df = pd.DataFrame({
        'date': pd.date_range(start='2023-05-18', periods=30),
        '科幻': count1,
        "魔法": count2,
        "童話": count3,
        "人數_over": count4,
        "人數_start": count5
    })
app1.layout = html.Div(
    [
        html.Div(
            [       
                html.P(children="統計圖表", className="header-description"),
                html.A('回主頁', href='/style', className="home-button"),
            ],
            className="header",
        ),
        html.Div([
            html.P(children="風格統計", className="graph-description"),
            html.H5("日期"),
            dcc.Dropdown(
                id='data',
                options=[{'label': i.strftime('%Y-%m-%d'), 'value': i} for i in df["date"]],
                value=df["date"][0]
            ),
            dcc.Graph(id='bar-plot1'),   
        ],
        className="graph1",
        ),
        html.Div([
            html.P(children="瀏覽統計", className="graph-description"),
            dcc.Graph(id='bar-plot2'),   
        ],
        className="graph2",
        ),
    ],
)

@app1.callback(
    Output('bar-plot1', 'figure'),
    Output('bar-plot2', 'figure'),
    [Input('data', 'value')]
)
def update_scatter_plot(selected_index):
    data = df[df['date'] == selected_index]
    fig1 = {
        'data': [
            {'x': ['科幻', '魔法', '童話'], 'y': [data['科幻'].values[0], data['魔法'].values[0], data['童話'].values[0]], 'type': 'bar', 'name': '次數'}
        ],
        'layout': {
            'title': '風格統計圖表',
            'xaxis': {'title': '風格類別'},
            'yaxis': {'title': '次數'}
        }
    }
    fig2 = {
        'data': [
            {'x': ['完成故事人數', '進入頁面人數'], 'y': [data['人數_over'].values[0], data['人數_start'].values[0]], 'type': 'bar', 'name': '人數'}
        ],
        'layout': {
            'title': '瀏覽統計圖表',
            'xaxis': {'title': '瀏覽類別'},
            'yaxis': {'title': '人數'}
        }
    }
    return fig1, fig2

@app.route('/',methods=['POST','GET'])
def index():
    return render_template('login.html')  
@app.route('/style', methods = ['POST', 'GET'])
def style():
    global option_count, ip, start_time, content , imgurl, story_generator,DB
    option_count = 0
    content = ""
    imgurl = dict()
    story_generator = chaptgptget.StoryGenerator()
    DB = mongod.DB()
    MD = md.User()
    if 'user_id' not in session:
        return redirect(url_for('login'))
    ip = request.remote_addr
    start_time = datetime.datetime.now()
    DB.DB_start(ip,session.get('user_id'),start_time,datetime.datetime.combine(start_time.date(), datetime.datetime.min.time()))
    return render_template('index.html', **locals())
@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')  
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('login_name')
    password = data.get('login_pass11')
    users_list = MD.get_users_list()
    password_confim = MD.get_password(username)
    if not all([username, password]):
        return jsonify({"message": "少填寫一項"}), 400
    if username not in users_list[0] or not check_password_hash(password_confim.decode("utf-8"), password):
        return jsonify({"message": "帳號密碼錯誤"}), 400
    session['user_id'] = username
    session.permanent = True
    return jsonify({"message": "登入成功"}), 200
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    print(data)
    username = data.get('login_name')
    password = data.get('login_pass11')
    confirm_password = data.get('login_pass12')
    email = data.get('u_email')
    sex = data.get('u_sex')
    users_list = MD.get_users_list()
    if not all([username, password, confirm_password, email]):
        return jsonify({"message": "Missing required fields"}), 400

    if password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400

    if username in users_list:
        return jsonify({"message": "Username already exists"}), 400
    hashed_password = generate_password_hash(password)
    MD.insert_user(username,hashed_password,email,sex,)
    return jsonify({"message": "Registration successful"}), 200



@app.route('/teammember', methods = ['POST', 'GET'])
def teammember():
    return render_template('teammember.html')
@app.route('/submit_score', methods=['POST'])
def submit_score():
    global score
    score = request.form.get('score')
    story_id = MD.get_story_id(userid,story_name)
    MD.insert_score(story_id,userid,score)
    MD.logout()
    return 'Score received' 
@app.route('/start', methods = ['POST', 'GET'])
def start():
    global story_name, imgurl, content, image_url, main_character, style
    try:
        story = story_generator.generate_story_beginning(style)
        main_character, story_name,story_notbutton,button1,button2,button3 = story_split_start(story)
    except Exception as e:
        print(f"An error occurred: {e}")
        return redirect(url_for("index"))
    
    content += story_notbutton
    image_url = image_voice(main_character,story_notbutton,button1,button2,button3)
    imgurl["first"] = image_url
    image_url1 = image_url[0] 
    return render_template('test1.html',story=story_notbutton,button1=button1,button2=button2,button3=button3,image_url=image_url1,story_name=story_name,option_count=option_count)

@app.route('/update_story', methods=['POST'])
def update_story():
    global option_count, content, image_url, main_character, userid
    button_value = request.form.get('buttonValue')
    content += button_value#上次所選的選項
    try:
        updated_data, option_count = story_generator.generate_story_item(button_value, option_count)
    except Exception as e:
        print(f"An error occurred: {e}")
        response = {
            'redirect': 404
        }
        return jsonify(response)
    print(updated_data, option_count)
    if option_count == 4:
        updated_data,button_1,button_2,button_3 = story_split_over(updated_data)
        content += updated_data
        image_url = image_voice(main_character,updated_data,button_1,button_2,button_3)
        imgurl["final"] = image_url
        image_url1 = image_url[0]
        response = {
            'story': updated_data,
            'image_url': image_url1,
            'redirect': option_count
        }
        userid = MD.get_user_id(session.get('user_id'))
        MD.insert_story(userid,start_time,datetime.datetime.now(),style,story_name,content)
        DB.DB_over(ip,start_time,datetime.datetime.now(),datetime.datetime.combine(datetime.datetime.now().date(), datetime.datetime.min.time()),style,story_name,content,imgurl)
        return jsonify(response)
    try:
        story_notbutton,button1,button2,button3 = story_split_item(updated_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        response = {
            'redirect': 404
        }
        return jsonify(response)
    
    image_url = image_voice(main_character,story_notbutton,button1,button2,button3)
    if option_count==1:
        imgurl["second"] = image_url
    elif option_count==2:
        imgurl["third"] = image_url
    else:
        imgurl["fourth"] = image_url
    content += story_notbutton
    image_url1 = image_url[0]
    response = {
        'story': story_notbutton,
        'image_url': unidecode(image_url1),
        'button1': button1,
        'button2': button2,
        'button3': button3,
        'option_count': str(option_count),
    }
    return jsonify(response)

@app.route('/redirect')
def redirectToHello():
    global style
    style = request.args.get('style')
    return redirect(url_for('start'))

@app.route('/get_image_url', methods=["POST",'GET'])
def get_image_url():
    global  image_url
    click_count = request.form.get('click_count', 0, type=int)
    click_count = click_count%4
    image_url01 = image_url[click_count]
    return jsonify({'imageUrl': image_url01})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=False)
