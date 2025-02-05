import datetime
import re

from bson import ObjectId
from flask import request, Flask, render_template, redirect, session
import os
import pymongo
import bcrypt

my_client = pymongo.MongoClient("mongodb://localhost:27017")
my_database = my_client["university_blog"]
room_owner_collection=my_database["room_owner"]
member_collection=my_database["member"]
admin_collection = my_database["admin"]
room_categories_collection = my_database["room_categories"]
room_collection = my_database["room"]
post_collection = my_database["post"]
polls_collection = my_database["polls"]

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PROFILES_PATH = APP_ROOT + "/static/profiles"
posted_files_image_path = APP_ROOT + "/static/posted_files/images"
posted_files_video_path = APP_ROOT + "/static/posted_files/video"

app.secret_key = "university"
admin_name = "admin"
password = "admin"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin")
def admin():
    return render_template("admin_login.html")


query = {}
count = admin_collection.count_documents(query)
if count == 0:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    query = {"username": "admin", "password": "admin","encrypt_password": hashed_password.decode('utf-8')}
    admin_collection.insert_one(query)


@app.route("/admin_login_action", methods=['post'])
def admin_login_action():
    name = request.form.get("name")
    password = request.form.get("password")
    if name == admin_name and password == password:
        session['role'] = 'admin'
        return redirect("/admin_home")
    else:
        return render_template("message.html", message="Invalid Admin Details")


@app.route("/room_owner")
def room_owner():
    return render_template("room_owner_login.html")


@app.route("/room_owner_registration")
def room_owner_registration():
    return render_template("room_owner_registration.html")


@app.route("/room_owner_registration_action", methods=['post'])
def room_owner_registration_action():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    address=request.form.get("address")
    city = request.form.get("city")
    state = request.form.get("state")
    zip_code = request.form.get("zip_code")
    query = {"email": email}
    count = room_owner_collection.count_documents(query)
    if count > 0:
        return render_template("message.html", message="Email Already Exists")
    query = {"phone": phone}
    count = room_owner_collection.count_documents(query)
    if count > 0:
        return render_template("message.html", message="Phone Number Already Exists")
    query = {"first_name": first_name, "last_name": last_name, "email": email, "phone": phone, "password": password, "address":address, "city" : city, "state": state, "zip_code": zip_code,'isLogged':False}
    room_owner_collection.insert_one(query)
    return render_template("admin_message.html", message=" Room Owner Added successfully")


@app.route("/room_owner_login_action", methods=['post'])
def room_owner_login_action():
    email = request.form.get("email")
    password = request.form.get("password")
    query = {"email": email, "password": password}
    count = room_owner_collection.count_documents(query)
    if count > 0:
        room_owner = room_owner_collection.find_one(query)
        if room_owner['isLogged']:
            session['room_owner_id'] = str(room_owner['_id'])
            session['role'] = 'room_owner'
            return redirect("/room_owner_home")
        else:
            session['role'] = 'room_owner'
            session["room_owner_id"] = str(room_owner['_id'])
            return render_template("change_room_owner_password.html")
    else:
        return render_template("message.html", message="Invalid  Room Owner Details")


@app.route("/change_room_owner_password_action", methods=['post'])
def change_room_owner_password_action():
    old_password = request.form.get("old_password")
    password = request.form.get("password")
    room_owner = room_owner_collection.find_one({"_id": ObjectId(session['room_owner_id'])})
    if room_owner['password'] != old_password:
        return render_template("message.html", message="Invalid Old Password...!")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    query = {"$set":{"password": password,"encrypt_password": hashed_password.decode('utf-8'), "isLogged": True}}
    room_owner_collection.update_one({"_id": ObjectId(session['room_owner_id'])}, query)
    session['room_owner_id'] = str(room_owner['_id'])
    session['role'] = 'room_owner'
    return redirect("/room_owner_home")


@app.route("/member")
def member():
    return render_template("member_login.html")


@app.route("/member_registration")
def member_registration():
    return render_template("member_registration.html")


@app.route("/member_registration_action", methods=['post'])
def member_registration_action():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    address = request.form.get("address")
    city = request.form.get("city")
    state = request.form.get("state")
    zip_code = request.form.get("zip_code")
    query = {"email": email}
    count = member_collection.count_documents(query)
    if count > 0:
        return render_template("message.html", message="Email Already Exists")
    query = {"phone": phone}
    count = member_collection.count_documents(query)
    if count > 0:
        return render_template("message.html", message="Phone Number Already Exists")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    query = {"first_name": first_name, "last_name": last_name, "email": email, "phone": phone, "password": password, "address": address, "city" : city, "state": state, "zip_code": zip_code,"encrypt_password": hashed_password.decode('utf-8')}
    member_collection.insert_one(query)
    return render_template("message.html", message=" Member Registered successfully")


@app.route("/member_login_action",methods=['post'])
def member_login_action():
    email = request.form.get("email")
    password = request.form.get("password")
    query = {"email": email, "password": password}
    count = member_collection.count_documents(query)
    if count > 0:
          member = member_collection.find_one(query)
          session['role'] = 'member'
          session['member_id'] = str(member['_id'])
          return redirect("/member_home")
    else:
        return render_template("message.html", message="Invalid Email and Password")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")


@app.route("/room_categories")
def room_categories():
    message = request.args.get("message")
    if message==None:
        message = ""
    room_categories = room_categories_collection.find({})
    room_categories = list(room_categories)
    return render_template("room_categories.html",room_categories=room_categories,message=message)


@app.route("/room_categories_action")
def room_categories_action():
    category_name = request.args.get("category_name")
    query = {"category_name":category_name}
    count = room_categories_collection.count_documents(query)
    if count>0:
        return redirect("room_categories?message=Already added this category")
    else:
        room_categories_collection.insert_one(query)
        return redirect("room_categories?message=Room category added Successfully")


@app.route("/view_room_owners")
def view_room_owners():
    query={}
    keyword = request.args.get("keyword")
    if session["role"] == "admin":
        if keyword == None:
            keyword = ""
        if keyword == "":
            query = {}
        else:
            keyword2 = re.compile(".*" + str(keyword) + ".*", re.IGNORECASE)
            query = {"$or": [{"first_name": keyword2}, {"email": keyword2}, {"last_name": keyword2}, {"phone": keyword}]}
    room_owners=room_owner_collection.find(query)
    room_owners = list(room_owners)
    return render_template("view_room_owners.html",room_owners=room_owners)


@app.route("/add_room")
def add_room():
    room_categories=room_categories_collection.find({})
    room_categories = list(room_categories)
    room_owners = room_owner_collection.find({})
    room_owners = list(room_owners)
    return render_template("add_room.html",room_categories=room_categories,room_owners=room_owners)


@app.route("/add_room_action",methods=['post'])
def add_room_action():
    room_title = request.form.get("room_title")
    category_id = request.form.get("category_id")
    room_owner_id = request.form.get("room_owner_id")
    description = request.form.get("description")
    created_on = datetime.datetime.now()
    created_by = 'Admin'
    status = 'Room Created'
    query = {"room_title":room_title,"category_id":ObjectId(category_id),"room_owner_id":ObjectId(room_owner_id),"description":description,"created_on":created_on,"created_by":created_by,"status":status}
    room_collection.insert_one(query)
    return render_template("admin_message.html",message="Room Created Successfully")


@app.route("/view_room")
def view_room():
    query = {}
    rooms=room_collection.find(query)
    rooms = list(rooms)
    return render_template("view_room.html",rooms=rooms,get_room_owner_id_by_room=get_room_owner_id_by_room,get_room_category_id_by_room=get_room_category_id_by_room,get_room_member_id_by_room_member=get_room_member_id_by_room_member,get_is_in_room_by_room_id=get_is_in_room_by_room_id, get_is_in_room_by_room_id2=get_is_in_room_by_room_id2)


def get_room_owner_id_by_room(room_owner_id):
    query = {"_id": ObjectId(room_owner_id)}
    room_owner = room_owner_collection.find_one(query)
    return room_owner


def get_room_category_id_by_room(category_id):
    query = {"_id": ObjectId(category_id)}
    room_category = room_categories_collection.find_one(query)
    return room_category


def get_room_member_id_by_room_member(member_id):
    query = {"_id": ObjectId(member_id)}
    member = member_collection.find_one(query)
    return member


@app.route("/member_home")
def member_home():
    return render_template("member_home.html")


@app.route("/room_owner_home")
def room_owner_home():
    return render_template("room_owner_home.html")


@app.route("/send_room_join_request")
def send_room_join_request():
    member_id = session['member_id']
    room_id = request.args.get("room_id")
    status = 'Join Requested'
    joining_date = datetime.datetime.now()
    room_member = {"member_id":ObjectId(member_id),"status":status,"joining_date":joining_date}
    query = {"$push":{"room_members":room_member}}
    room_collection.update_one({"_id":ObjectId(room_id)},query)
    return redirect("/view_room")


@app.route("/accept_room_request")
def accept_room_request():
    room_id = request.args.get("room_id")
    member_id = request.args.get("member_id")
    query1 = {"_id": ObjectId(room_id),'room_members.member_id':ObjectId(member_id)}
    query2 = {"$set":{"room_members.$.status":"Accepted"}}
    room_collection.update_one(query1, query2)
    return redirect("/view_rooms_by_room_owner")


@app.route("/reject_room_request")
def reject_room_request():
    room_id = request.args.get("room_id")
    member_id = request.args.get("member_id")
    query1 = {"_id": ObjectId(room_id),'room_members.member_id':ObjectId(member_id)}
    query2 = {"$set":{"room_members.$.status":"Rejected"}}
    room_collection.update_one(query1, query2)
    return redirect("/view_rooms_by_room_owner")


@app.route("/block_member")
def block_member():
    room_id = request.args.get("room_id")
    member_id = request.args.get("member_id")
    query1 = {"_id": ObjectId(room_id),'room_members.member_id':ObjectId(member_id)}
    query2 = {"$set":{"room_members.$.status":"Blocked"}}
    room_collection.update_one(query1, query2)
    return redirect("/view_rooms_by_room_owner")


@app.route("/un_block_member")
def un_block_member():
    room_id = request.args.get("room_id")
    member_id = request.args.get("member_id")
    print(room_id)
    print(member_id)
    query1 = {"_id": ObjectId(room_id),'room_members.member_id':ObjectId(member_id)}
    query2 = {"$set":{"room_members.$.status":"Accepted"}}
    room_collection.update_one(query1, query2)
    return redirect("/view_rooms_by_room_owner")


@app.route("/view_rooms_by_room_owner")
def view_rooms_by_room_owner():
    if session['role']=="room_owner":
        room_owner_id = session['room_owner_id']
        # query = {"room_owner_id":ObjectId(room_owner_id)}
        query={}
    elif session['role']=='admin':
        query ={}
    rooms = room_collection.find(query)
    rooms = list(rooms)
    return render_template("view_rooms_by_room_owner.html", rooms=rooms,get_room_owner_id_by_room=get_room_owner_id_by_room,get_room_category_id_by_room=get_room_category_id_by_room,get_room_member_id_by_room_member=get_room_member_id_by_room_member,str=str)


@app.route("/view_requests")
def view_requests():
    room_id = request.args.get("room_id")
    query = {"_id": ObjectId(room_id)}
    rooms = room_collection.find_one(query)
    return render_template("view_requests.html",room=rooms,get_room_member_id_by_room_member=get_room_member_id_by_room_member)


@app.route("/goto_my_room")
def goto_my_room():
    room_id = request.args.get("room_id")
    query ={"room_id":ObjectId(room_id)}
    posts = post_collection.find(query)
    posts=list(posts)
    print(posts)
    return render_template("goto_my_room.html",room_id=room_id,posts=posts,get_like_count=get_like_count,get_comment_count=get_comment_count,get_posted_by_post=get_posted_by_post,get_member_by_post=get_member_by_post,get_room_by_room_id=get_room_by_room_id)


def get_like_count(post_id):
    post = post_collection.find_one({"_id":ObjectId(post_id)})
    if "likes" in post:
        count = len(post['likes'])
        return count
    else:
         count =0
         return count


def get_comment_count(post_id):
    post = post_collection.find_one({"_id":ObjectId(post_id)})
    if "comments" in post:
        count = len(post['comments'])
        return count
    else:
        count =0
        return count


def get_posted_by_post(room_owner_id):
    room_owner = room_owner_collection.find_one({"_id": ObjectId(room_owner_id)})
    return room_owner


def get_member_by_post(member_id):
    member = member_collection.find_one({"_id": ObjectId(member_id)})
    return member


@app.route("/add_post")
def add_post():
    room_id = request.args.get("room_id")
    return render_template("add_post.html",room_id=room_id)


@app.route("/add_post_action",methods=['post'])
def add_post_action():
    room_id = request.form.get("room_id")
    title = request.form.get("title")
    image = request.files.get("image")
    video = request.files.get("video")
    description = request.form.get("description")
    if image.filename != "":
        path = posted_files_image_path + "/" + image.filename
        image.save(path)
    if video.filename != "":
        path2 = posted_files_video_path + "/" + video.filename
        video.save(path2)
    if session['role'] == 'room_owner':
        room_owner_id = session['room_owner_id']
        query = {"title":title,"image":image.filename,"video":video.filename,"description":description,"room_id":ObjectId(room_id),"room_owner_id":ObjectId(room_owner_id),"status":'Posted'}
    else:
        member_id = session['member_id']
        query = {"title":title,"image":image.filename,"video":video.filename,"description":description,"room_id":ObjectId(room_id),"member_id":ObjectId(member_id),"status":'Posted'}
    post_collection.insert_one(query)
    return redirect("/goto_my_room?room_id=" + room_id)


@app.route("/get_comments")
def get_comments():
    post_id = request.args.get("post_id")
    query = {"_id":ObjectId(post_id)}
    post = post_collection.find_one(query)
    return render_template("get_comments.html",post_id=post_id,post=post,get_room_owner_id_by_comments=get_room_owner_id_by_comments,get_member_id_by_comments=get_member_id_by_comments)


@app.route("/get_comment_action")
def get_comment_action():
    post_id = request.args.get("post_id")
    comment = request.args.get("comment")
    commented_on = datetime.datetime.now()
    if session['role']=='room_owner':
        room_owner_id = session['room_owner_id']
        comments = {"commented_on": commented_on,"comment":comment,"room_owner_id":ObjectId(room_owner_id)}
        query = {"$push": {"comments": comments}}
    if session['role']=='member':
        member_id = session['member_id']
        comments = {"commented_on": commented_on,"comment":comment,"member_id":ObjectId(member_id)}
        query = {"$push": {"comments": comments}}
    post_collection.update_one({"_id": ObjectId(post_id)}, query)
    return redirect("/get_comments?post_id="+post_id)


def get_room_owner_id_by_comments(room_owner_id):
    query = {"_id": ObjectId(room_owner_id)}
    room_owner = room_owner_collection.find_one(query)
    return room_owner


def get_member_id_by_comments(member_id):
    query = {"_id": ObjectId(member_id)}
    member = member_collection.find_one(query)
    return member


@app.route("/add_like")
def add_like():
    post_id = request.args.get('post_id')
    query = {"_id":ObjectId(post_id)}
    post = post_collection.find_one(query)
    if session['role'] == 'member':
        member_id = session['member_id']
        if 'likes' in post:
            query = {'_id': ObjectId(post_id), "likes.member_id":  ObjectId(member_id)}
            count = post_collection.count_documents(query)
            if count==0:
                query = {"member_id": ObjectId(member_id),"liked_on":datetime.datetime.now()}
                post_collection.update_one({'_id': ObjectId(post_id)}, {'$push': {'likes': query}})
        else:
            query = {"member_id": ObjectId(member_id), "liked_on": datetime.datetime.now()}
            post_collection.update_one({'_id': ObjectId(post_id)}, {'$push': {'likes': query}})
    elif session['role'] == 'room_owner':
        room_owner_id = session['room_owner_id']
        if 'likes' in post:
            query = {'_id': ObjectId(post_id), "likes.room_owner_id":  ObjectId(room_owner_id)}
            count = post_collection.count_documents(query)
            if count==0:
                query = {"room_owner_id": ObjectId(room_owner_id),"liked_on":datetime.datetime.now()}
                post_collection.update_one({'_id': ObjectId(post_id)}, {'$push': {'likes': query}})
        else:
            query = {"room_owner_id": ObjectId(room_owner_id), "liked_on": datetime.datetime.now()}
            post_collection.update_one({'_id': ObjectId(post_id)}, {'$push': {'likes': query}})
    return {"message":"liked"}


@app.route("/poll")
def poll():
    room_id = request.args.get("room_id")
    query = {"room_id":ObjectId(room_id)}
    polls = polls_collection.find(query)
    return render_template("poll.html",get_is_answer_poll_id=get_is_answer_poll_id,get_poll_count_by_poll_id2=get_poll_count_by_poll_id2,room_id=room_id,polls=polls,get_poll_count_by_poll_id=get_poll_count_by_poll_id,get_submitted_count_by_poll_id=get_submitted_count_by_poll_id)


@app.route("/add_poll")
def add_poll():
    room_id = request.args.get("room_id")
    return render_template("add_poll.html",room_id=room_id)


@app.route("/add_poll_action")
def add_poll_action():
    question = request.args.get("question")
    room_id = request.args.get("room_id")
    if session['role'] == "room_owner":
        room_owner_id = session['room_owner_id']
        query={"question": question,"room_id":ObjectId(room_id),"room_owner_id":ObjectId(room_owner_id)}
    elif session['role'] == "member":
            member_id = session['member_id']
            query={"question": question,"room_id":ObjectId(room_id),"member_id":ObjectId(member_id)}
    polls_collection.insert_one(query)
    return redirect("/poll?room_id="+room_id)


@app.route("/room_owner_poll_submit_action")
def room_owner_poll_submit_action():
    poll_id = request.args.get("poll_id")
    room_id = request.args.get("room_id")
    poll = request.args.get("poll")
    if session['role'] == 'room_owner':
        room_owner_id = session['room_owner_id']
        query = {"_id":ObjectId(poll_id)}
        polls_collection.find_one(query)
        answers = {"room_owner_id": ObjectId(room_owner_id),"poll":poll}
        query = {"$push":{"answers": answers}}
        polls_collection.update_one({"_id": ObjectId(poll_id)},query)
        return redirect("/poll?room_id=" + room_id)
    elif session['role'] == 'member':
        member_id = session['member_id']
        query = {"_id": ObjectId(poll_id)}
        polls_collection.find_one(query)
        answers = {"member_id": ObjectId(member_id),"poll":poll}
        query = {"$push":{"answers":answers}}
        polls_collection.update_one({"_id":ObjectId(poll_id)},query)
        return redirect("/poll?room_id="+room_id)


def get_poll_count_by_poll_id(poll_id):
    query = {"_id": ObjectId(poll_id)}
    polls = polls_collection.find_one(query)
    count = 0
    if 'answers' in polls:
        for answer in polls['answers']:
            if answer['poll']=='yes':
                count = count+1
    return count

def get_poll_count_by_poll_id2(poll_id):
    query = {"_id": ObjectId(poll_id)}
    polls = polls_collection.find_one(query)
    count = 0
    if 'answers' in polls:
        for answer in polls['answers']:
            if answer['poll'] == 'no':
                count = count + 1
    return count


def get_is_answer_poll_id(poll_id):
    member_id = session['member_id']
    count = polls_collection.count_documents({"_id":poll_id, "answers.member_id":ObjectId(member_id)})
    if count==0:
        return False
    else:
        return True



def get_submitted_count_by_poll_id(poll_id):
    poll = polls_collection.find_one({"_id": ObjectId(poll_id)})
    if "answers" in poll:
        count = len(poll['answers'])
        return count
    else:
         count =0
         return count


def get_is_in_room_by_room_id(room_id):
    member_id = session['member_id']
    query= {"_id":room_id, "room_members.member_id": ObjectId(member_id),"room_members.status": { "$ne": "Rejected"}}
    count = room_collection.count_documents(query)
    if count == 0:
        return False
    else:
        return True

def get_is_in_room_by_room_id2(room_id):
    member_id = session['member_id']
    query={"_id":room_id, "room_members.member_id": ObjectId(member_id), "room_members.status": "Accepted"}
    count = room_collection.count_documents(query)
    if count == 0:
        return False
    else:
        return True


def get_is_room_request_status_accepted_by_room_id(room_id):
    member_id = session['member_id']
    count = room_collection.count_documents({"_id":room_id, "room_members.member_id": ObjectId(member_id),"status":'Accepted'})
    if count == 0:
        return False
    else:
        return True


@app.route("/block_post")
def block_post():
    room_id = request.args.get("room_id")
    post_id = request.args.get("post_id")
    status = 'Blocked'
    query1 = {"_id": ObjectId(post_id)}
    query2 = {"$set": {"status": status}}
    post_collection.update_one(query1, query2)
    return redirect("/goto_my_room?room_id="+room_id)


@app.route("/edit_category")
def edit_category():
    category_id = request.args.get("category_id")
    query = {"_id":ObjectId(category_id)}
    category = room_categories_collection.find_one(query)
    return render_template("edit_category.html",category=category,category_id=category_id)


@app.route("/edit_category_action")
def edit_category_action():
    category_id = request.args.get("category_id")
    category_name = request.args.get("category_name")
    query1 = {"_id": ObjectId(category_id)}
    query2 = {"$set": {"category_name": category_name}}
    room_categories_collection.update_one(query1, query2)
    return redirect("/room_categories")


def get_room_by_room_id(room_id):
    query={"_id":ObjectId(room_id)}
    room =room_collection.find_one(query)
    return room


@app.route("/back_to_room")
def back_to_room():
    room_id = request.args.get("room_id")
    return redirect("/goto_my_room?room_id="+room_id)


app.run(debug=True)