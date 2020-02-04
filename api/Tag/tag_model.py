from api import db

class Tag(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    @property
    def serialize(self):
        return {
        'id': self.id,
        'name': self.name     
        }