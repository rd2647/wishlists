"""
Models for Homepage_Schema

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Homepage_Schema(db.Model):
    """
    Class that represents a Homepage_Schema
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    email = db.Column(db.String(32))
    shared_with1 = db.Column(db.String(63))
    shared_with2 = db.Column(db.String(63))
    shared_with3 = db.Column(db.String(63))

    def __repr__(self):
        return "<Homepage_Schema %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a Homepage_Schema to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a Homepage_Schema to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a Homepage_Schema from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Homepage_Schema into a dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "shared_with1":self.shared_with1,
            "shared_with2":self.shared_with2,
            "shared_with3":self.shared_with3
        }

    def deserialize(self, data):
        """
        Deserializes a Homepage_Schema from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.id = data["id"]
            self.name = data["name"]
            self.email = data["email"]
            self.shared_with1 = data["shared_with1"]
            self.shared_with2 = data["shared_with2"]
            self.shared_with3 = data["shared_with3"]
        except KeyError as error:
            raise DataValidationError("Invalid Homepage_Schema: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Homepage_Schema: body of request contained" "bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Homepage_Schemas in the database """
        logger.info("Processing all Homepage_Schemas")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Homepage_Schema by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a Homepage_Schema by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_name(cls, name):
        """ Returns all Homepage_Schemas with the given name

        Args:
            name (string): the name of the Homepage_Schemas you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
    
    @classmethod
    def find_by_name(cls, id):
        """ Returns all Homepage_Schemas with the given name

        Args:
            name (string): the name of the Homepage_Schemas you want to match
        """
        logger.info("Processing name query for %s ...", id)
        return cls.query.filter(cls.id == id)