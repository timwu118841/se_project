import re
from flask import render_template, url_for, flash, redirect
from flask.globals import request
from sqlalchemy.orm import Session
from blog import app,db,bycrypt
from blog.forms import RegistrationForm, LoginForm,ResetPasswordFormEmail,FormResetPassword,RestuarantForm
from blog.model import User, Restaurant
from flask_login import login_user, current_user,logout_user
from blog.sendmail import send_mail
from werkzeug.utils import secure_filename
import base64 as b
'''
就是route的地方
'''

@app.route("/",methods=['GET','POST'])



@app.route("/home",methods=['GET','POST'])
def home():
    
    
            
        
    
    
    return render_template('index.html')
    
@app.route("/layer2",methods=['GET','POST'])
def layer2():
    
    if request.method=='POST':
        
        if request.form['submit_button']=="後門":
                title=Restaurant.query.filter(Restaurant.location=="中央後門").all()
                return render_template('layer2card.html',data=title)

        elif request.form['submit_button']=="宵夜街":
            title=Restaurant.query.filter(Restaurant.location=="宵夜街").all()
            return render_template('layer2card.html',data=title)
        elif request.form['submit_button']=="校內":
            title=Restaurant.query.filter(Restaurant.location=="校內").all()
            return render_template('layer2card.html',data=title)
        elif request.form['submit_button']=="市區":
            title=Restaurant.query.filter(Restaurant.location=="市區").all()
            return render_template('layer2card.html',data=title)
        
        if request.form['submit_button']=="101中央後門":
           
            title=Restaurant.query.filter(
                Restaurant.money>=100,
                Restaurant.money<300,
                Restaurant.location == '中央後門'
                
            ).all()
          
            return render_template('layer2card.html',data=title)
            
        else:
            title=Restaurant.query.all()
            return render_template('layer2card.html',data=title)

     
        
            
    
@app.route("/r_sumit",methods=['GET','POST'])
def sumit():
    form = RestuarantForm()

    if form.validate_on_submit(): 
            image_data= request.files[form.image.name].read()
            Dimage_data= b.b64encode(image_data)
           
            
            restaurant = Restaurant(title=form.title.data,money=form.money.data,tele=form.tele.data,image=Dimage_data
                                ,location=form.location.data,description=form.description.data)
           
            db.session.add(restaurant)
         
            db.session.commit()
            flash('成功新增餐廳')
            return redirect(url_for('home'))
    print(form.errors)    
    return render_template('r_sumit.html',form=form)
        
    


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/forget", methods=['GET','POST'])
def resetpassword():
    if not current_user.is_anonymous:
        return redirect(url_for('home'))
    form=ResetPasswordFormEmail()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token=user.create_reset_token()
            send_mail(sender='@GMAIL.COM',  #  發送者
                      recipients=[user.email],
                      subject='Reset Your Password',
                      template='resetemail',
                      mailtype='html',
                      user=current_user,
                      token=token)
            flash('請檢查你的電子信箱')
            return render_template('index.html')
    return render_template('forgetpassword.html',form=form)

@app.route("/resetpassword/<token>",methods=['GET','POST'])
def reset_password_recieve(token):
    
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    form = FormResetPassword()

    if form.validate_on_submit():
        user = User()
        data = user.validate_confirm_token(token)
        if data:
            
            user = User.query.filter_by(id=data.get('reset_id')).first()
            #  驗證
            if user:
                hashed_password= bycrypt.generate_password_hash(form.password.data).decode('utf-8')
                user.password = hashed_password
                db.session.commit()
                flash('更改成功')
                return redirect(url_for('login'))
            else:
                flash('沒有這個信箱')
                return redirect(url_for('login'))
        else:
            flash('驗證過期')
            return redirect(url_for('login'))
    return render_template('resetpassword.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password= bycrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'成功建立帳號搂, {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
            user=User.query.filter_by(email=form.email.data).first()
            if user and bycrypt.check_password_hash(user.password,form.password.data):
                login_user(user)
                flash('登入成功')
                return redirect(url_for('home'))
            else:
                flash('登入失敗')
    return render_template('login.html', title='Login', form=form)
  
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))