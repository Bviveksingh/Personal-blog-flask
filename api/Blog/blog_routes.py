from flask import Blueprint,request,jsonify,make_response
from flask_jwt_extended import jwt_required
from api import db
from api.Blog.blog_model import Blog
from api.Tag.tag_model import Tag

blogs= Blueprint('blogs',__name__)

@blogs.route('/blogs',methods=["GET"])
def get_all_blogs():
    blogs= Blog.query.all()
    serialized_data = []
    for blog in blogs:
        serialized_data.append(blog.serialize)

    return jsonify({"all_blogs": serialized_data})

@blogs.route('/blog/<int:id>',methods=["GET"])
def get_single_blog(id):
    blog = Blog.query.filter_by(id=id).first_or_404()
    serialized_blog = blog.serialize
    serialized_blog["tags"] = []

    for tag in blog.tags:
        serialized_blog["tags"].append(tag.serialize)

    return jsonify({"single_blog": serialized_blog})    

@blogs.route('/delete_blog/<int:id>', methods=["DELETE"])
@jwt_required
def delete_blog(id):
    blog = Blog.query.filter_by(id=id).first()
    db.session.delete(blog)
    db.session.commit()

    return jsonify("Blog was deleted"),200

@blogs.route('/update_blog/<int:id>', methods=["PUT"])
@jwt_required
def update_blog(id):
    data = request.get_json()
    blog=Blog.query.filter_by(id=id).first_or_404()

    blog.title = data["title"]
    blog.content=data["content"]
    blog.feature_image=data["feature_image"]

    updated_blog = blog.serialize

    db.session.commit()
    return jsonify({"blog_id": blog.id})



@blogs.route('/add_blog',methods=["POST"])
@jwt_required
def create_blog():
    data = request.get_json()

    new_blog=Blog(title=data["title"],content=data["content"],feature_image=data["feature_image"])

    for tag in data["tags"]:
        present_tag=Tag.query.filter_by(name=tag).first()
        if(present_tag):
            present_tag.blogs_associated.append(new_blog)
        else:
            new_tag =Tag(name=tag)
            new_tag.blogs_associated.append(new_blog)
            db.session.add(new_tag)
            

    db.session.add(new_blog)
    db.session.commit()

    blog_id = getattr(new_blog, "id")
    return jsonify({"id": blog_id})
    
    