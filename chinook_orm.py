from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

class Album(Base):
    __tablename__ = 'Album'
    AlbumId = Column(Integer, primary_key=True)
    Title = Column(String, nullable=False)
    ArtistId = Column(Integer, ForeignKey('Artist.ArtistId'), nullable=False)
    artist = relationship("Artist")

class Artist(Base):
    __tablename__ = 'Artist'
    ArtistId = Column(Integer, primary_key=True)
    Name = Column(String)

class Customer(Base):
    __tablename__ = 'Customer'
    CustomerId = Column(Integer, primary_key=True)
    FirstName = Column(String, nullable=False)
    LastName = Column(String, nullable=False)
    Company = Column(String)
    Address = Column(String)
    City = Column(String)
    State = Column(String)
    Country = Column(String)
    PostalCode = Column(String)
    Phone = Column(String)
    Fax = Column(String)
    Email = Column(String, nullable=False)
    SupportRepId = Column(Integer, ForeignKey('Employee.EmployeeId'))
    support_rep = relationship("Employee")

class Employee(Base):
    __tablename__ = 'Employee'
    EmployeeId = Column(Integer, primary_key=True)
    LastName = Column(String, nullable=False)
    FirstName = Column(String, nullable=False)
    Title = Column(String)
    ReportsTo = Column(Integer, ForeignKey('Employee.EmployeeId'))
    BirthDate = Column(DateTime)
    HireDate = Column(DateTime)
    Address = Column(String)
    City = Column(String)
    State = Column(String)
    Country = Column(String)
    PostalCode = Column(String)
    Phone = Column(String)
    Fax = Column(String)
    Email = Column(String)
    manager = relationship("Employee", remote_side=[EmployeeId])

class Genre(Base):
    __tablename__ = 'Genre'
    GenreId = Column(Integer, primary_key=True)
    Name = Column(String)

class Invoice(Base):
    __tablename__ = 'Invoice'
    InvoiceId = Column(Integer, primary_key=True)
    CustomerId = Column(Integer, ForeignKey('Customer.CustomerId'), nullable=False)
    InvoiceDate = Column(DateTime, nullable=False)
    BillingAddress = Column(String)
    BillingCity = Column(String)
    BillingState = Column(String)
    BillingCountry = Column(String)
    BillingPostalCode = Column(String)
    Total = Column(Numeric(10, 2), nullable=False)
    customer = relationship("Customer")

class InvoiceLine(Base):
    __tablename__ = 'InvoiceLine'
    InvoiceLineId = Column(Integer, primary_key=True)
    InvoiceId = Column(Integer, ForeignKey('Invoice.InvoiceId'), nullable=False)
    TrackId = Column(Integer, ForeignKey('Track.TrackId'), nullable=False)
    UnitPrice = Column(Numeric(10, 2), nullable=False)
    Quantity = Column(Integer, nullable=False)
    invoice = relationship("Invoice")
    track = relationship("Track")

class MediaType(Base):
    __tablename__ = 'MediaType'
    MediaTypeId = Column(Integer, primary_key=True)
    Name = Column(String)

class Playlist(Base):
    __tablename__ = 'Playlist'
    PlaylistId = Column(Integer, primary_key=True)
    Name = Column(String)

class PlaylistTrack(Base):
    __tablename__ = 'PlaylistTrack'
    PlaylistId = Column(Integer, ForeignKey('Playlist.PlaylistId'), primary_key=True)
    TrackId = Column(Integer, ForeignKey('Track.TrackId'), primary_key=True)
    playlist = relationship("Playlist")
    track = relationship("Track")

class Track(Base):
    __tablename__ = 'Track'
    TrackId = Column(Integer, primary_key=True)
    Name = Column(String, nullable=False)
    AlbumId = Column(Integer, ForeignKey('Album.AlbumId'))
    MediaTypeId = Column(Integer, ForeignKey('MediaType.MediaTypeId'), nullable=False)
    GenreId = Column(Integer, ForeignKey('Genre.GenreId'))
    Composer = Column(String)
    Milliseconds = Column(Integer, nullable=False)
    Bytes = Column(Integer)
    UnitPrice = Column(Numeric(10, 2), nullable=False)
    album = relationship("Album")
    media_type = relationship("MediaType")
    genre = relationship("Genre")

# Create an engine and a session
engine = create_engine('sqlite:///Chinook.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Update the merge_if_not_exists function
def merge_if_not_exists(session, instance):
    primary_key = list(instance.__class__.__table__.primary_key.columns.keys())[0]
    existing_instance = session.query(instance.__class__).filter_by(**{primary_key: instance.__dict__[primary_key]}).first()
    if not existing_instance:
        session.merge(instance)
        print(f"Inserted: {instance}")
    else:
        print(f"Already exists: {instance}")

# Insert data with checks for existing records
artist1 = Artist(ArtistId=1, Name='AC/DC')
artist2 = Artist(ArtistId=2, Name='Accept')
merge_if_not_exists(session, artist1)
merge_if_not_exists(session, artist2)

album1 = Album(AlbumId=1, Title='For Those About To Rock We Salute You', ArtistId=1)
album2 = Album(AlbumId=2, Title='Balls to the Wall', ArtistId=2)
merge_if_not_exists(session, album1)
merge_if_not_exists(session, album2)

genre1 = Genre(GenreId=1, Name='Rock')
genre2 = Genre(GenreId=2, Name='Jazz')
merge_if_not_exists(session, genre1)
merge_if_not_exists(session, genre2)

media_type1 = MediaType(MediaTypeId=1, Name='MPEG audio file')
media_type2 = MediaType(MediaTypeId=2, Name='Protected AAC audio file')
merge_if_not_exists(session, media_type1)
merge_if_not_exists(session, media_type2)

track1 = Track(TrackId=1, Name='For Those About To Rock (We Salute You)', AlbumId=1, MediaTypeId=1, GenreId=1, Composer='Angus Young, Malcolm Young, Brian Johnson', Milliseconds=343719, Bytes=11170334, UnitPrice=0.99)
track2 = Track(TrackId=2, Name='Balls to the Wall', AlbumId=2, MediaTypeId=2, GenreId=1, Composer='U. Dirkschneider, W. Hoffmann, H. Frank, P. Baltes, S. Kaufmann, G. Hoffmann', Milliseconds=342562, Bytes=5510424, UnitPrice=0.99)
merge_if_not_exists(session, track1)
merge_if_not_exists(session, track2)

employee1 = Employee(EmployeeId=1, LastName='Adams', FirstName='Andrew', Title='General Manager', BirthDate='1962-02-18', HireDate='2002-08-14', Address='11120 Jasper Ave NW', City='Edmonton', State='AB', Country='Canada', PostalCode='T5K 2N1', Phone='+1 (780) 428-9482', Fax='+1 (780) 428-3457', Email='andrew@chinookcorp.com')
employee2 = Employee(EmployeeId=8, LastName='Callahan', FirstName='Laura', Title='IT Staff', ReportsTo=6, BirthDate='1968-01-09', HireDate='2004-03-04', Address='923 7 ST NW', City='Lethbridge', State='AB', Country='Canada', PostalCode='T1H 1Y8', Phone='+1 (403) 467-3351', Fax='+1 (403) 467-8772', Email='laura@chinookcorp.com')
merge_if_not_exists(session, employee1)
merge_if_not_exists(session, employee2)

customer1 = Customer(CustomerId=1, FirstName='Luís', LastName='Gonçalves', Company='Embraer - Empresa Brasileira de Aeronáutica S.A.', Address='Av. Brigadeiro Faria Lima, 2170', City='São José dos Campos', State='SP', Country='Brazil', PostalCode='12227-000', Phone='+55 (12) 3923-5555', Fax='+55 (12) 3923-5566', Email='luisg@embraer.com.br', SupportRepId=3)
customer2 = Customer(CustomerId=59, FirstName='Puja', LastName='Srivastava', Address='3,Raj Bhavan Road', City='Bangalore', Country='India', PostalCode='560001', Phone='+91 080 22289999', Email='puja_srivastava@yahoo.in', SupportRepId=3)
merge_if_not_exists(session, customer1)
merge_if_not_exists(session, customer2)

invoice1 = Invoice(InvoiceId=1, CustomerId=2, InvoiceDate='2021-01-01', BillingAddress='Theodor-Heuss-Straße 34', BillingCity='Stuttgart', BillingCountry='Germany', BillingPostalCode='70174', Total=1.98)
invoice2 = Invoice(InvoiceId=412, CustomerId=58, InvoiceDate='2025-12-22', BillingAddress='12,Community Centre', BillingCity='Delhi', BillingCountry='India', BillingPostalCode='110017', Total=1.99)
merge_if_not_exists(session, invoice1)
merge_if_not_exists(session, invoice2)

invoice_line1 = InvoiceLine(InvoiceLineId=1, InvoiceId=1, TrackId=2, UnitPrice=0.99, Quantity=1)
invoice_line2 = InvoiceLine(InvoiceLineId=1000, InvoiceId=185, TrackId=2565, UnitPrice=0.99, Quantity=1)
merge_if_not_exists(session, invoice_line1)
merge_if_not_exists(session, invoice_line2)

playlist1 = Playlist(PlaylistId=1, Name='Music')
playlist2 = Playlist(PlaylistId=18, Name='On-The-Go 1')
merge_if_not_exists(session, playlist1)
merge_if_not_exists(session, playlist2)

playlist_track1 = PlaylistTrack(PlaylistId=1, TrackId=3402)
playlist_track2 = PlaylistTrack(PlaylistId=1, TrackId=985)
merge_if_not_exists(session, playlist_track1)
merge_if_not_exists(session, playlist_track2)

session.commit()
