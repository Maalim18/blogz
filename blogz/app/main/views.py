from flask_login import login_required,current_user
from flask import render_template,request,redirect,url_for,abort
from ..models import  User,Blogs,Comments
from .forms import BlogForm,CommentForm,UpdateProfile
from .. import db, photos
from . import main




 

@main.route('/')
def index():

    message= "Welcome to Blogs!!"
    title= 'Blog-app'
    # blogs=Blogs.get_blogs()
    


    return render_template('index.html', message=message,title=title)

@main.route('/blogs')
def blog():

    message= "Welcome to blog Application!!"
    title= 'Blog app'
    new_blog = Blog.query.all()
    for blog in new_blog:
     blog=blog
     
     return render_template('blog.html', message=message,title=title,blog=blog)
  



@main.route('/blog/', methods = ['GET','POST'])
# @login_required
def new_blog():

   blog_form = BlogForm()

   if blog_form.validate_on_submit():
        
        blog= blog_form.blog.data
        title=blog_form.title.data

        # Updated pitchinstance
        new_blog = Blogs(title=title,blog= blog)
        db.session.add(new_blog)
        db.session.commit()


        title='New Blog'

        new_blog.save_blog()

        return redirect(url_for('main.index'))

   
   return render_template('blog.html',blog_form= blog_form)


@main.route('/categories/<cate>')
def category(cate):
    '''
    function to return the pitches by category
    '''
    category = blogs.get_blogs(cate)
    # print(category)
    title = f'{cate}'
    return render_template('categories.html',title = title, category = category)

@main.route('/comment/<int:pitch_id>', methods = ['POST','GET'])
@login_required
def comment(blog_id):
    form = CommentForm()
    pitch = Pitch.query.get(blog_id)
    all_comments = Comment.query.filter_by(blog_id = blog_id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        blog_id = blog_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,blog_id = blog_id)
        new_comment.save_c()
        return redirect(url_for('.comment', blog_id = pitch_id))
    return render_template('comment.html', form =form, blog= blog,all_comments=all_comments)



@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()

    return redirect(url_for('main.profile',uname=uname))   


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(author = uname).first()

    if user is None:
        
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(author = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.author))

    return render_template('profile/update.html',form =form)
 
   