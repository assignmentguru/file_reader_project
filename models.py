from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FileModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), unique=True, nullable=False)
    checksum = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"FileModel(id={self.id}, file_path='{self.file_path}', checksum='{self.checksum}')"
