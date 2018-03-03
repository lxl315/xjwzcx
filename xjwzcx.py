from flask import Flask
import requests
import base64
from flask import render_template,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
import time,datetime
app = Flask(__name__)
app.debug = True
app.secret_key='lovexhy1314,./12312'
url = 'http://xj.122.gov.cn/m/publicquery/vio'
t = time.time()
class query(FlaskForm):
    cphm = StringField('车牌号码',validators=[DataRequired('车牌号码不能为空！')])
    fdjh = StringField('发动机号码',validators=[DataRequired('发动机号码不能为空！')])
    captcha = StringField('验证码',validators=[DataRequired('验证码不能为空！')])
    submit = SubmitField('查询')

@app.route('/',methods=['POST'])
def post():
    form = query()
    if form.validate_on_submit():
        cphm = form.cphm.data
        fdjh = form.fdjh.data
        captcha = form.captcha.data
        payload = {'hpzl': '02', 'hphm1b': cphm, 'hphm': '新'+cphm, 'fdjh': fdjh, 'captcha': captcha}
        headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                   'Referer': 'http://xj.122.gov.cn/views/inquiry.html?q=j'}
        r = requests.post(url,data=payload,headers=headers,cookies=cookie)
        data = r.json()
        return render_template('return.html',form=form,data=data)
    return render_template('index.html',form=form)
@app.route('/',methods=['GET'])
def index():
    global cookie
    form = query()
    r = requests.get("http://xj.122.gov.cn/captcha?nocache=" + str((round(t * 1000))))
    cookie = r.cookies.get_dict()
    print(cookie)
    img = base64.b64encode(r.content)
    img_string = img.decode('utf-8')
    img_url = ("data:image/jpg;base64," + img_string)
    return render_template('index.html',form=form,img_url=img_url)
if __name__ == '__main__':
    app.run()
