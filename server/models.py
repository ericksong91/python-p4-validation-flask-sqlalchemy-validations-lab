from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self, key, name):
        if name:
            check = Author.query.filter(Author.name == name).first()
            if check:
                raise ValueError("Needs a Unique Name")
        else:
            raise ValueError("Needs a name")
        
        return name
    
    @validates('phone_number')
    def validate_phone(self, key, phone):
        if phone:
            check = Author.query.filter(Author.phone_number == phone).first()

            #Check duplicates
            if check:
                raise ValueError("Needs unique Phone Number")
            
            #check length
            if len(phone) != 10:
                raise ValueError("Phone number needs to be 10 digits long")
            elif not int(phone):
                raise ValueError("Phone number needs to be all digits")
        else:
            raise ValueError("Needs phone #")
            
        return phone


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('title')
    def title_clickbait(self, key, title):
        if title:
            click_bait = ["Won't Believe", "Secret", "Top", "Guess"]

            if not any(ele in title for ele in click_bait):
                raise ValueError("Isn't clickbait-y enough")
        else:
            raise ValueError("Needs title")

        return title
    @validates('content', 'summary')
    def post_length(self, key, body):
        if body:
            if key == "content":
                if len(body) < 250:
                    raise ValueError("Needs to be at least 250 characters")
            else:
                if len(body) > 250:
                    raise ValueError("Needs to be less than 250 characters")
        else:
            raise ValueError("Needs post")
        
        return body
    
    @validates('category')
    def post_category(self, key, category):
        if category == "Fiction" or category == "Non-Fiction":
           return category
        else:
             raise ValueError("Category needs to be Fiction or Non-Fiction")

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
