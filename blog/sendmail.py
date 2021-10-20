from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from blog import mail,app


def send_mail(sender, recipients, subject, template, mailtype='html', **kwargs):
 
    app = current_app._get_current_object()
    msg = Message(subject,
                  sender=sender,
                  recipients=recipients)
    if mailtype == 'html':
        msg.html = render_template(template + '.html', **kwargs)
    elif mailtype == 'txt':
        msg.body = render_template(template + '.txt', **kwargs)
    elif mailtype == 'body':
        msg.body = template

    #  使用多線程
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_async_email(app, msg):
    """
  
    """
    with app.app_context():
        mail.send(msg)