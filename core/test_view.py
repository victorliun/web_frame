# from core.app import web
from werkzeug.exceptions import HTTPException, NotFound
from jinja2 import Environment, FileSystemLoader
import os
from db import db
from werkzeug.utils import redirect
from werkzeug.wrappers import Request, Response
# import pdb

template_path = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = Environment(loader=FileSystemLoader(template_path),autoescape=True)

def render_template(template_name, **context):
    t = jinja_env.get_template(template_name)
    return Response(t.render(context), mimetype='text/html')

def on_short_link_details(request, short_id):
    query = "SELECT * from url_short where id=%d" %int(short_id)
    # pdb.set_trace()
    db.execute("SELECT * from url_short where id=%d" %int(short_id))
    link_target = db.fetchone()
    if link_target is None:
        raise NotFound()
    click_count = int(link_target[2])
    return render_template('short_link_details.html',
        link_target=link_target[1],
        short_id=link_target[0],
        click_count=click_count+1
    )

def on_follow_short_link(request, short_id):
    db.execute("SELECT * from url_short where id=%s" %short_id)
    link_target = db.fetchone()
    if link_target is None:
        raise NotFound()
    db.execute("UPDATE url_short SET count=%d where id=%d "%(link_target[2]+1, link_target[0]))
    db.con.commit()
    return redirect(link_target[1])

def insert_url(url):
    db.execute("SELECT id from url_short where url='%s'" %url)
    if db.rowcount():
        return db.fetchone()[0]
    db.execute("INSERT INTO url_short(url, count) VALUES('%s',0)" %url)
    db.con.commit()
    return db.cursor.lastrowid

def on_new_url(request):
    error = None
    url = ''
    if request.method == 'POST':
        url = request.form['url']
        if not url.startswith("http"):
            error = 'Please enter a valid URL'
        else:
            short_id = insert_url(url)
            print short_id
            return redirect('/%s+' % short_id)
    return render_template('new_url.html', error=error, url=url)
