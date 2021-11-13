from datetime import datetime

from flask.globals import current_app
from blog import db,login_manger
from flask_login import UserMixin
from itsdangerous import BadSignature, SignatureExpired, TimedJSONWebSignatureSerializer
'''
放DB的地方 主要是放USER跟USER的POST

'''
@login_manger.user_loader#判斷是否login的東東
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def validate_confirm_token(self, token):
        """
        驗證回傳令牌是否正確，若正確則回傳True
        :param token:驗證令牌
        :return:回傳驗證是否正確，正確為True
        """
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)  # 驗證
        except SignatureExpired:
            #  當時間超過的時候就會引發SignatureExpired錯誤
            return False
        except BadSignature:
            #  當驗證錯誤的時候就會引發BadSignature錯誤
            return False
        return data
    def create_reset_token(self,expires_in=7200):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'reset_id': self.id})
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100),nullable=False)
    title = db.Column(db.String(100),nullable=False)
    rated = db.Column(db.Float,nullable=False)
    avg_cost = db.Column(db.Integer,nullable=False)



    
