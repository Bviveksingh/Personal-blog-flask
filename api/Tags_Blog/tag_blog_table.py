from api import db

tag_blog = db.Table('tag_blog',
    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id'), primary_key=True),
    db.Column('blog_id', db.Integer,db.ForeignKey('blog.id'),primary_key=True)
)   