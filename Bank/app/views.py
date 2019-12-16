from flask import *
from flask_sqlalchemy import *
from app import app, db,login
from .models import User,Account
from .forms import UserForm
from flask_login import current_user, login_user,logout_user,login_required
from io import BytesIO

import random
import string
from PIL import Image, ImageFont, ImageDraw, ImageFilter


def rndColor():
    '''随机颜色'''
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def gene_text():
    '''生成4位验证码'''
    return ''.join(random.sample(string.ascii_letters+string.digits, 4))

def draw_lines(draw, num, width, height):
    '''划线'''
    for num in range(num):
        x1 = random.randint(0, width / 2)
        y1 = random.randint(0, height / 2)
        x2 = random.randint(0, width)
        y2 = random.randint(height / 2, height)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

def get_verify_code():
    '''生成验证码图形'''
    code = gene_text()
    # 图片大小120×50
    width, height = 120, 50
    # 新图片对象
    im = Image.new('RGB',(width, height),'white')
    # 字体
    font = ImageFont.truetype('app/static/fonts/arialbd.ttf', 40)
    # draw对象
    draw = ImageDraw.Draw(im)
    # 绘制字符串
    for item in range(4):
        draw.text((5+random.randint(-3,3)+23*item, 5+random.randint(-3,3)),
                  text=code[item], fill=rndColor(),font=font )
    # 划线
    draw_lines(draw, 2, width, height)
    # 高斯模糊
    im = im.filter(ImageFilter.GaussianBlur(radius=1.5))
    return im, code

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/code')
def get_code():
    image, code = get_verify_code()
    # 图片以二进制形式写入
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把buf_str作为response返回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    session['image'] = code
    return response

# Home page, login and register
@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home',id=current_user.id))
    if request.method == 'POST':
        name = request.form.get('user')
        pwd = request.form.get('pwd')
        if str(session.get('image')).lower() != request.form.get('verify').lower():
            flash('Wrong verify code.')
            pass
            return redirect('/')
        if all([name, pwd]):
            a = User.query.filter(User.name == name).first()
            if a:
                # 如果用户存在，判断密码是否正确
                if a.pwd == pwd:
                    # 其他页面用来判断用户到登录状态
                    login_user(a)
                    flash('Welcome!')
                    # 登录成功后跳转到首页
                    return redirect(url_for('home',id=a.id))
                else:
                    flash('Wrong password')
            else:
                flash('The account is invalid')
        else:
            flash('The information are not complete')
    return render_template("lo.html",
                           title="Bank of Wey")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form.get('user')
        pwd1 = request.form.get('pwd1')
        pwd2 = request.form.get('pwd2')
        code = request.form.get('code')
        email = request.form.get('email')
        if all([user, pwd1, pwd2, email]):
            if pwd1 == pwd2:
                if code == 'NMSL':
                    a = User()
                    a.name = user
                    a.pwd = pwd1
                    a.email = email
                    a.manager = True

                    db.session.add(a)
                    db.session.commit()

                    b=Account()
                    b.score = 1000
                    b.money = 100000
                    b.owner_id = a.id
                    db.session.add(b)
                    db.session.commit()

                    flash('Welcome Manager!!!')
                    redirect('/')
                else:
                    a = User()
                    a.name = user
                    a.pwd = pwd1
                    a.email = email
                    a.manager = False

                    db.session.add(a)
                    db.session.commit()

                    b = Account()
                    b.score = 1000
                    b.money = 10000
                    b.owner_id = a.id

                    db.session.add(b)
                    db.session.commit()

                    flash('Success!!!')
                    redirect('/')
            else:
                flash('The passwords are not same')
        else:
            flash('The information is not complete')
    return render_template('re.html',
                           title='Sign-up')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/home/<id>', methods=['GET', 'POST'])
@login_required
def home(id):
    if(current_user.id==int(id)):
        user = User.query.get(id)
        return render_template('home.html',
                                    obj=user,
                                    title="Home")
    else:
        return current_app.login_manager.unauthorized()

@app.route('/mod/<id>',methods=['GET','POST'])
@login_required
def mod(id):
    user = User.query.get(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        ed = user
        ed.name = form.name.data
        ed.email = form.email.data
        ed.pwd = form.pwd.data
        db.session.commit()
        flash("Successfully modified")
    return render_template('modify.html',
                           title='Account Management',
                           obj=user,
                           form=form)

@app.route('/view/<id>',methods=['GET','POST'])
@login_required
def view(id):
    if (current_user.id == int(id)):
        infos = User.query.all()
        man = User.query.get(id)
        return render_template('view_all.html',
                               infos=infos,
                               obj=man)
    else:
        return current_app.login_manager.unauthorized()

@app.route('/select/<id>',methods=['GET','POST'])
@login_required
def select(id):
    if (current_user.id == int(id)):
        obj = User.query.get(id)
        return render_template('select.html',
                               obj=obj)
    else:
        return current_app.login_manager.unauthorized()

@app.route('/respond',methods=['POST'])
@login_required
def search():
    data = json.loads(request.data)  # Transfer the string to dict
    response = data.get('response')  # Get the data from front end
    s = User.query.all()  # The list of all tasks
    list = '<table class="table table-striped">' \
               '<tr><th>ID</th><th>Name</th><th>Email</th>' \
               '<th>Deposit</th><th>Loan</th><th>Credit Score</th></tr>'

    for info in s:  # Each line in the list
        if response in info.name:  # To orient the tasks containing inputting words
            list = list + '<tr><th>' + str(info.id) + '</th><th>' + str(info.name) + '</th><th>' + str(info.email) + \
                '</th><th>' + str(info.account.money) + '</th><th>' + str(info.account.loan)+"</th><th>"\
                   + str(info.account.score) + '</th></tr><br>'
            list = list + '</table>'
    return json.dumps({'status': 'OK', 'response': list})

#Delete the task
@app.route('/delete/<id>',methods=['GET','POST'])
@login_required
def delete_task(id):
    if (current_user.id == int(id)):
        target = User.query.get(id)
        db.session.delete(target)
        db.session.commit()
        return redirect('/view/1')
    else:
        return current_app.login_manager.unauthorized()

@app.route('/save',methods=['POST'])
@login_required
def save():
    data = json.loads(request.data)
    response = data.get('in')

    data2 = json.loads(request.data)
    user = data2.get('user')

    if (response.isdigit()):
        OBJ = User.query.get(user)
        OBJ.account.money = OBJ.account.money+float(response)
        db.session.commit()
        return json.dumps({'status': 'OK'})

@app.route('/withdraw',methods=['POST'])
@login_required
def withdraw():
    data = json.loads(request.data)
    response = data.get('out')

    data2 = json.loads(request.data)
    user = data2.get('user')

    if (response.isdigit()):
        OBJ = User.query.get(user)
        OBJ.account.money = OBJ.account.money - float(response)
        db.session.commit()
        return json.dumps({'status': 'OK'})

@app.route('/loan/<id>',methods=['GET','POST'])
@login_required
def loan(id):
    if (current_user.id == int(id)):
        obj = User.query.get(id)
        return render_template('loan.html',
                               obj=obj,
                               info=obj)
    else:
        return current_app.login_manager.unauthorized()

@app.route('/loan_in',methods=['POST'])
@login_required
def loan_in():
    data = json.loads(request.data)
    loan = data.get('in')

    data2 = json.loads(request.data)
    user = data2.get('user')

    obj = User.query.get(user)

    if(loan.isdigit() and float(loan) < 0.4*(obj.account.money-obj.account.loan)):
        obj.account.loan = obj.account.loan + float(loan)
        db.session.commit()
        return json.dumps({'status': 'OK'})

@app.route('/loan_back',methods=['POST'])
@login_required
def loan_back():
    data = json.loads(request.data)
    back = data.get('back')

    data2 = json.loads(request.data)
    user = data2.get('user')

    obj = User.query.get(user)

    if(back.isdigit() and  float(back)<=obj.account.loan and float(back)>=0):
        obj.account.loan = obj.account.loan - float(back)
        obj.account.money = obj.account.money - float(back)
        db.session.commit()
        return json.dumps({'status': 'OK'})

@app.route('/trans/<id>',methods=['GET','POST'])
@login_required
def trans(id):
    if (current_user.id == int(id)):
        user = User.query.get(id)

        return render_template('exchange.html',
                               obj=user,
                               title="Exchange")
    else:
        return current_app.login_manager.unauthorized()

@app.route('/filter',methods=['POST'])
@login_required
def filter():
    data = json.loads(request.data)
    email = data.get('email')

    all = User.query.all()
    list = ""

    for single in all:
        if email in single.email:
            list = list + '<li ><a onclick=\'getValue(event)\' href=\'#\'>' + str(single.name) + ' : ' + str(single.email) + "</a></li>"

    return json.dumps({'status': 'OK', 'response': list})


@app.route('/trans/exchange',methods=['POST'])
@login_required
def exchange():
    data = json.loads(request.data)
    email = data.get('email')

    data2 = json.loads(request.data)
    user = data2.get('from')

    data3 = json.loads(request.data)
    money = data3.get('money')

    me = User.query.get(user)
    you = User.query.filter_by(email=email).first()

    if(money.isdigit() and float(money) <= me.account.money):
        me.account.money = me.account.money - float(money)
        you.account.money = you.account.money + float(money)
        db.session.commit()
        return json.dumps({'status': 'OK'})

