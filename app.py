from flask import Flask,request,jsonify,send_file
from flask_restx import Resource,Api
from flask_sqlalchemy import SQLAlchemy
from models import User,Role,db,Venue,Show,Show_Venue,Booking,UserRating
from flask_security import SQLAlchemyUserDatastore,Security,roles_required,auth_token_required
import bcrypt
import csv
from flask_cors import CORS
import os
import base64
from io import BytesIO
import datetime
from datetime import datetime
from werkzeug.utils import cached_property
from werkzeug.utils import secure_filename
from celery_worker import make_celery
import smtplib
import crontab
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from jinja2 import Template
from weasyprint import HTML
import uuid
from email import encoders
from celery.result import AsyncResult
import matplotlib.pyplot as plt
from flask_caching import Cache
import yaml,json


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket_database.sqlite3'
app.config['SECRET_KEY'] = 'onepieceisreal'
app.config['SECURITY_PASSWORD_SALT'] = 'onepieceisreal'
app.config['SQLALCHEMY_TRACK_MODIFICATONS'] = False
app.config['WTF_CSRF_ENABLED']=False
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER']='Authentication-Token'
app.config['SECURITY_TOKEN_AUTHENTICATION_KEY'] = 'token'
app.config['UPLOAD_FOLDER'] = ''
app.config['CELERY_BROKER_URL']='redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND']='redis://localhost:6379/0'
app.config['CACHE_TYPE']='RedisCache'
app.config['CACHE_REDIS_HOST']='localhost'
app.config['CACHE_REDIS_PORT']='6379'

SMTP_SERVER_HOST='localhost'
SMTP_SERVER_PORT='1025'
SENDER_ADDRESS='griss.harris@gmail.com'
SENDER_PASSWORD=''
db.init_app(app)
api = Api(app,title='My API', version='1.0', description='My API description', swagger=True) 
cache=Cache(app)
CORS(app, origins='http://localhost:8080',supports_credentials=True)
user_datastore=SQLAlchemyUserDatastore(db,User,Role)
app.security = Security(app, user_datastore)
celery = make_celery(app)


# @celery.task(name='generate_csv')
# def generate_csv(venues):
#     csv_filename = 'venues_details.csv'
#     venue_id=venues[0]
#     venue=Venue.query.filter(Venue.venue_id==venue_id).first()
#     books = Booking.query.filter(Venue.venue_id==venue.venue_id).all()
#     sum=0
#     for book in books:
#         for shows in venue.shows:
#             if book.show_id == shows.show_id:
#                 sum+=book.seats
#             with open(csv_filename, 'w', newline='') as csvfile:
#                 fieldnames = [venue.name , 'Number of Seats', 'Genre', 'Average Rating','Movie Price','No of Bookings']
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#             writer.writeheader()
#             writer.writerow({
#             'Theater Name': shows.name,
#             'Number of Seats': venue.capacity,
#             'Genre': shows.tags,
#             'Average Rating': shows.rating,
#             'Movie Price': shows.price,
#             'No of Bookings':sum,
#         })
#     return csv_filename
@celery.task(name='generate_csv')
def generate_csv(venues):
    csv_filename = 'venues_details.csv'
    venue_id = venues[0]
    venue = Venue.query.filter(Venue.venue_id == venue_id).first()
    books = Booking.query.filter(Venue.venue_id == venue.venue_id).all()
    sum = 0
    for book in books:
        for shows in venue.shows:
            if book.show_id == shows.show_id:
                sum += book.seats
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['Theater Name', 'Number of Seats', 'Genre', 'Average Rating', 'Movie Price', 'No of Bookings']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            'Theater Name': shows.name,
            'Number of Seats': venue.capacity,
            'Genre': shows.tags,
            'Average Rating': shows.rating,
            'Movie Price': shows.price,
            'No of Bookings': sum,
        })
    return csv_filename

@app.route('/download/<string:id>')
def download_file(id):
    res=celery.AsyncResult(id)
    csv_file=res.get()
    print(csv_file)
    return send_file(csv_file,as_attachment=True)

@app.route('/<int:venue_id>/trigger_job/celery')
def trigger_celery_job(venue_id):
    venue=Venue.query.filter(Venue.venue_id==venue_id).first()
    venues=[]
    venues.append(venue.venue_id)
    filename=generate_csv.delay(venues)
    return {
        "Task_id":filename.id,
        "Task_state":filename.state,
        "Task_result":filename.result
    }
@app.route('/status/<string:id>')
def check_status(id):
    res = celery.AsyncResult(id)
    print(res.id)
    print(res.status)
    if res.failed():
        print(res.traceback)
        return {
            "Task_id": res.id,
            "Task_state": res.state,
            "Traceback": res.traceback,
        }
    else:
        return {
            "Task_id": res.id,
            "Task_state": res.state,
        }





def format_message(template_file,data={}):
    with open(template_file) as file_:
        template=Template(file_.read())
        return template.render(data=data)
    
def create_pdf_report(data):
    print(data)
    message=format_message('MonthlyPdfReport.html',data=data)
    html=HTML(string=message)
    file_name=str(uuid.uuid4())+".pdf"
    print(file_name)
    html.write_pdf(target=file_name)
    return file_name

def send_message(to_address,subject,message,attachment_file=None):
    msg=MIMEMultipart()
    msg['From']=SENDER_ADDRESS
    msg['To']=to_address
    msg['Subject']=subject
    if attachment_file:
        filename, data = attachment_file 
        part = MIMEBase("application", "octet-stream")
        part.set_payload(data)
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={filename}")
        msg.attach(part)
    msg.attach(MIMEText(message,"html"))
    s=smtplib.SMTP(host=SMTP_SERVER_HOST,port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True


@celery.task()
def send_remainder_via_email():
    users=User.query.all()
    message=None
    for user in users:
        if not  user.is_admin:
            if user.last_login.date() == datetime.today().date():
                message=format_message('Reminder.html',data=user.username)
                send_message(to_address=user.email,
                    subject="User Reminder",
                    message=message)


@celery.task()
def send_monthly_reports():
    users=User.query.all()
    book=Booking.query.all()
    venues=Venue.query.all()
    venue_list = []  # Create an empty list to hold venue dictionaries
    for venue in venues:
        venue_json = {
        'id': venue.venue_id,
        'name': venue.name,
        'place': venue.place,
        'location': venue.location,
        'capacity': venue.capacity,
        'shows': []
        }
        if venue.shows:
            for shows in venue.shows:
                show_json = {
                'id': shows.show_id,
                'name': shows.name,
                'rating': shows.rating,
                'price': shows.price,
                'show_time': shows.show_time, 
                'image_file': shows.image_file,
                'tags': shows.tags
                }
                venue_json['shows'].append(show_json)
        venue_list.append({'venue': venue_json})
    for user in users:
        if not  user.is_admin:
            print(user.username)
            book_list=[]
            for books in book:
                if books.user_id == user.id:
                    print(books.user_id,user.id)
                    booking={
                    "user_id":books.user_id,
                    "id":books.booking_id,
                    "venue_id":books.venue_id,
                    "show_id":books.show_id,
                    "seats":books.seats,
                    }
                    book_list.append({"books":booking})
            data={"id":user.id,
            "username":user.username,
                "email":user.email,
                "venues":venue_list,
                "books":book_list
            }
            if user.report=='pdf':
                pdf_file_name = create_pdf_report(data)  
                with open(pdf_file_name, "rb") as pdf_file:
                    send_message(to_address=user.email,
                        subject="Monthly Report",
                        message="Hi user,Here is your Monthly Report for your last months activities.",
                        attachment_file=(pdf_file_name, pdf_file.read()))
            elif user.report=='html':
                temp_file=format_message('MonthlyReport.html',data=data)
                send_message(to_address=user.email,
                subject="Monthly Report", 
                message=temp_file,attachment_file=None)     
    return "report"





@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(crontab(hour=18, minute=30), send_remainder_via_email.s(), name='every day evening')


    sender.add_periodic_task(crontab(0, 0, day_of_month='1'), send_monthly_reports.s(), name='1st Day of every month')

    # sender.add_periodic_task(30.0, send_monthly_reports.s(), name='1st Day of every month')











class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        print(username)
        password = data.get('password')
        user = user_datastore.find_user(username=username)
        print(user.username)
        if user:
            if not user.is_admin:
                user.last_login = datetime.now()
                db.session.commit()
                hashed_password = user.password.encode('utf-8')
                is_password_valid = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
                if is_password_valid:
                    token = user.get_auth_token()  
                    return jsonify({"message": "User Successfully Logged In", "id": user.id, "token": token})
                else:
                    return jsonify("Invalid password")
            elif user.is_admin:
                user.last_login = datetime.now()
                db.session.commit()
                print(user)
                hashed_password = user.password.encode('utf-8')
                is_password_valid = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
                if is_password_valid:
                    token = user.get_auth_token()  
                    print(token)
                    return jsonify({"message": "Admin Successfully Logged In", "id": user.id, "token": token})
                else:
                    return jsonify("Invalid password")
        else:
            return jsonify("NOT USER!!!!!")        

class UserAPI(Resource):
    @roles_required('user')
    @auth_token_required
    @cache.cached(timeout=50)
    def get(self, id=None):
        user = user_datastore.find_user(id=id)
        print(user.roles)
        if user:
            user_json = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            return jsonify(user_json)
        else:
            return jsonify(message="User not found"), 404  
    def post(self):
        data=request.get_json()
        username=data.get('username')
        password=data.get('password')
        email=data.get('email')
        report=data.get('reportType')
        user_role = user_datastore.find_or_create_role(name='user',description='user has access')
        user=user_datastore.create_user(
        username=username,
        password= bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        email=email,
        active=True,
        report=report,
        roles=[user_role],
        is_admin=False
        )
        db.session.commit()
        return jsonify("User Successfully Registered")
   
class AdminAPI(Resource):
    @roles_required('admin')
    @auth_token_required
    @cache.cached(timeout=50)
    def get(self, id=None):
        admin = user_datastore.find_user(id=id)
        print(admin.roles)
        if admin:
            admin_json = {
                'id': admin.id,
                'username': admin.username,
                'email': admin.email,
            }
            return jsonify(admin_json)
        else:
            return jsonify(message="User not found"), 404
    
class VenueAPI(Resource):
    @cache.cached(timeout=50)
    def get(self, venue_id=None):
        if venue_id is None:
           venues = Venue.query.all()
        else:
           venues = Venue.query.filter(Venue.venue_id == venue_id).all()

        if not venues:
            return jsonify({'message': 'No venues found'}), 404
        venue_list = []
        for venue in venues:
            venue_json = {
                'id': venue.venue_id,
                'name': venue.name,
                'place': venue.place,
                'location': venue.location,
                'capacity': venue.capacity,
                'shows':[]
            }
            if venue.shows:
                for shows in venue.shows:
                    show_json={
                        'id': shows.show_id,
                        'name': shows.name,
                         'rating': shows.rating,
                        'price': shows.price,
                        'show_time': shows.show_time, 
                        'image_file':shows.image_file,
                        'tags':shows.tags
                    }
                    venue_json['shows'].append(show_json)
            venue_list.append(venue_json)
        return jsonify(venue_list)
    
    @roles_required('admin')
    def post(self):
        data=request.get_json()
        name = data.get('venue_name')
        print(name)
        place = data.get('venue_place')
        location = data.get('venue_location')
        capacity = data.get('venue_capacity')
        sho = Venue(name=name, place=place, location=location, capacity=capacity)
        try:
            db.session.add(sho)
            db.session.commit()
        except:
            return jsonify({'message': 'An error occurred while adding the venue'})
        return jsonify({"message":"Venue successfully created"})

    @roles_required('admin')
    def put(self, venue_id):
        venue = Venue.query.filter(Venue.venue_id == venue_id).first()
        data=request.get_json()
        name = data.get('name')
        place = data.get('place')
        location = data.get('location')
        capacity = data.get('capacity')
        try:
            venue.name = name
            venue.place = place
            venue.location = location
            venue.capacity = capacity
            db.session.commit()
        except:
            return {'message': 'An error occurred while updating the venue'}, 500
        return jsonify({"message":"Venue successfully updated"})

    

    @roles_required('admin')
    def delete(self, venue_id):
        venue = Venue.query.filter(Venue.venue_id == venue_id).first()
        if venue is None:
            return jsonify({"message":"Venue not found"}),404
        for sh in venue.shows:
            show = Show_Venue.query.filter(Show_Venue.show_id == sh.show_id).all()
            for shows in show:
                db.session.delete(shows)
            db.session.commit()
        db.session.delete(venue)
        db.session.commit()
        return "", 200

class ShowAPI(Resource):
    def get(self, show_id=None):
        if show_id is None:
            show = Venue.query.all()
        else:
            show = Show.query.filter(Show.show_id == show_id).scalar()
        show_list = []
        show_json = {
            'id': show.show_id,
            'name': show.name,
            'rating':show.rating,
            'price': show.price,
            'tags': show.tags,
            'show_time':show.show_time,
            'image_file':show.image_file,
            'venues':[]
            }
        if show.venues:
            for venue in show.venues:
                venue_json={
                    'id': venue.venue_id,
                    'name': venue.name,
                    'place': venue.place,
                    'location': venue.location,
                    'capacity': venue.capacity,
                }
                show_json['venues'].append(venue_json)
            show_list.append(show_json)
        return jsonify(show_list)
    @roles_required('admin')
    def post(self, venue_id):
        venue = Venue.query.filter(Venue.venue_id == venue_id).first()
        name = request.form.get('name')
        print(name)
        rating = request.form.get('rating')
        print(rating)
        tags = request.form.get('tags')
        print(tags)
        showtime = request.form.get('show_time')
        print(showtime)
        if showtime:
            try:
                show_time = datetime.fromisoformat(showtime)
            except ValueError:
                print('error')
                return jsonify({'message': 'Invalid datetime format'}), 400
        price = request.form.get('ticketprice')
        print(price)
        file = request.files['image_file']
        print(file)
        filename = secure_filename(file.filename)
        if file:
            file.save(os.path.join('templates/src/assets/images', filename))
        show = Show(name=name, rating=rating, tags=tags, show_time=show_time, price=price, image_file=filename)
        print(show)
        db.session.add(show)
        venue.shows.append(show)
        db.session.commit()
        return jsonify({'message': 'Show successfully created'})

    
    def put(self,venue_id, show_id):
        show = Show.query.filter(Show.show_id == show_id).first()
        venue=Venue.query.filter(Venue.venue_id == venue_id).first()
        name = request.form['name']
        rating = request.form['rating']
        tags = request.form['tags']
        time = request.form['show_time']
        print(time)
        try:
            show_time = datetime.datetime.fromisoformat(time)
        except ValueError:
            return {'message': 'Invalid datetime format'}, 400
        price = request.form['ticketprice']
        print(price)
        file = request.files['image_file']
        filename = secure_filename(file.filename)
        print(filename)
        if file:
            file.save(os.path.join('templates/src/assets/images', filename))
        try:
            show.name = name
            show.rating = rating
            show.tags = tags
            show.show_time = show_time
            show.price = price
            db.session.commit()
        except:
            return {'message': 'An error occurred while updating the show'}, 500
        return jsonify({'message': 'Show successfully updated'})

    
    def delete(self,venue_id, show_id):
        show = Show.query.filter(Show.show_id==show_id).first()
        
        if show is None:
            return jsonify({'message':'Show Not Found'}),400
        showv = Show_Venue.query.filter(Show_Venue.show_id == show_id).all()
        # Venue=Venue.query.filter(Venue.venue_id==venue_id).first()
        for sho in showv:
            print(sho.show_id)
            db.session.delete(sho)
        # db.session.delete(show)
        db.session.commit()
        return "", 200

class BookingAPI(Resource):
    @auth_token_required
    @roles_required('user')
    @cache.cached(timeout=50)
    def get(self,id):
        book=Booking.query.filter(Booking.user_id==id).all()
        user= User.query.filter(User.id==id)
        book_list=[]
        for books in book:
            book_json={
                "id":books.booking_id,
                "user_id":books.user_id,
                "venue_id":books.venue_id,
                "show_id":books.show_id,
                "seats":books.seats
            }
            book_list.append(book_json)
        return jsonify(book_list)
    @roles_required('user')
    def post(self,id, venue_id, show_id):
        user = User.query.filter(User.id == id).first()
        show= Show.query.filter(Show.show_id == show_id).first()
        venue=Venue.query.filter(Venue.venue_id == venue_id).first()
        user_id=user.id
        show_id = show.show_id
        venue_id=venue.venue_id
        data=request.get_json()
        seat=data.get('seats')
        print(seat)
        if show.venues:
            for venue in show.venues:
                if venue.venue_id ==venue_id:
                    capacity=venue.capacity
        print(type(capacity),type(seat))
        print(seat)
        capacity=str(int(capacity)-seat)
        venue.capacity=capacity
        print(seat)
        con=Booking(user_id=user_id,show_id=show_id,seats=seat,venue_id=venue_id)
        db.session.add(con)
        db.session.commit()
        return jsonify({'message':'Successfulllly Boooked'})

class SearchAPI(Resource):
    @auth_token_required
    @roles_required('user')
    def post(self):
        data = request.get_json()
        ser = data.get('query')
        if ser is not None:
            query = "%" + ser + "%"
            venue_search = Venue.query.filter(Venue.location.like(query)).all()
            print(venue_search)
            show_search = Show.query.filter(Show.tags.like('%' + ser + '%')).all()
            print(show_search)
            if venue_search:
                id = venue_search[0].venue_id 
            elif show_search:
                for show in show_search:
                    id = show.show_id 
            else:
                id = None 

        return jsonify({"id": id, "message": "search is successful"})

class RatingAPI(Resource):
    def post(self,id,show_id):
        data=request.get_json()
        rating=data.get('rating')
        user=User.query.filter(User.id==id).first()
        show=Show.query.filter(Show.show_id==show_id).first()
        rate=UserRating(user_id=user.id,show_id=show.show_id,rating=rating)
        db.session.add(rate)
        db.session.commit()
        return jsonify({"message":'Show is rated','rating':rating})




class SummaryAPI(Resource):
    @cache.cached(timeout=50)
    def get(self):
        x = []
        y = []
        img=BytesIO()
        Book = Booking.query.all()
        for book in Book:
            show = book.show_id
            shows = Show.query.filter_by(show_id=show)
            for sho in shows:
                x.append(sho.name)
                y.append(book.seats)
        plt.bar(x, y)
        plt.xlabel('shows')
        plt.ylabel('seats')
        plt.title('show_summary')
        plt.savefig(img,format='png')
        plt.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        return jsonify(plot_url)
    



class LogoutAPI(Resource):
    @auth_token_required
    @cache.cached(timeout=50)
    def post(self):
        return jsonify(message="Logged out")


api.add_resource(SummaryAPI,'/api/generate_summary')
api.add_resource(RatingAPI,'/api/post/<int:id>/<int:show_id>/rating')
api.add_resource(SearchAPI,'/api/search')
api.add_resource(BookingAPI,'/api/<int:id>/get/bookings','/api/post/book/<int:id>/<int:venue_id>/<int:show_id>')
api.add_resource(ShowAPI,'/api/<int:show_id>/get/show','/api/<int:venue_id>/post/show','/api/<int:venue_id>/<int:show_id>/put/show','/api/<int:venue_id>/<int:show_id>/delete/show') 
api.add_resource(VenueAPI,'/api/get/venue','/api/post/venue','/api/<int:venue_id>/put/venue','/api/<int:venue_id>/delete/venue')
api.add_resource(UserAPI, '/api/<int:id>/user','/api/user')
api.add_resource(AdminAPI,'/api/<int:id>/admin')
api.add_resource(LoginAPI,'/api/login')
api.add_resource(LogoutAPI,'/api/logout')


# with open('swagger.json', 'r') as json_file:
#     swagger_data = json.load(json_file)

# yaml_data = yaml.dump(swagger_data, default_flow_style=False)

# with open('swagger.yaml', 'w') as yaml_file:
#     yaml_file.write(yaml_data)



if __name__=='__main__':
    with app.app_context():    
        db.create_all()
        celery = make_celery(app)
    app.run(debug=True)
    