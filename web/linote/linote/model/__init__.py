"""The application's model objects"""
from sqlalchemy import orm
from sqlalchemy.schema import Table
from sqlalchemy.schema import Column

from linote.model import meta

from sqlalchemy.databases.mysql import MSTinyInteger as Tinyint
from sqlalchemy.databases.mysql import MSSmallInteger as Smallint
from sqlalchemy.databases.mysql import MSInteger as Integer
from sqlalchemy.databases.mysql import MSBigInteger as BigInteger
from sqlalchemy.databases.mysql import MSDouble as Double
#from sqlalchemy.databases.mysql import MSBlob as Blob
#from sqlalchemy.databases.mysql import MSDate as Date
#from sqlalchemy.databases.mysql import MSDateTime as Datetime
from sqlalchemy.databases.mysql import MSNVarChar as Varchar
from sqlalchemy.databases.mysql import MSNChar as Char
from sqlalchemy.databases.mysql import MSText as Text


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #
    meta.Session.configure(bind=engine)
    meta.engine = engine


## Non-reflected tables may be defined and mapped at module level
note_table = Table(
    "note",
    meta.metadata,
    Column("guid", Char(length=32), primary_key=True, nullable=False),
    Column("active", Tinyint(unsigned=True), nullable=False, default=0),
    Column("updated", BigInteger(unsigned=True), nullable=False, default=0),
    Column("created", BigInteger(unsigned=True), nullable=False, default=0),
    Column("deleted", BigInteger(unsigned=True), nullable=False, default=0),
    Column("updateSequenceNum", Integer(unsigned=True), nullable=False,
           default=0),
    Column("contentLength", Integer(unsigned=True), nullable=False,
           default=0),
    Column("contentHash", Char(length=32), nullable=False),
    Column("notebookGuid", Char(length=32), nullable=False, default=''),
    Column("title", Varchar(length=230), nullable=False, default=''),
    Column("content", Text(), nullable=False, default=''),
)


tag_table = Table(
    "tag",
    meta.metadata,
    Column("guid", Char(length=32), primary_key=True, nullable=False),
    Column("name", Varchar(length=32), nullable=False, default=''),
    Column("parentGuid", Char(length=32), nullable=False, default=''),
    Column("updateSequenceNum", Integer(unsigned=True), nullable=False,
           default=0),
)


note_tag_table = Table(
    "note_tag",
    meta.metadata,
    Column("id", Integer(unsigned=True), primary_key=True,
           autoincrement=True, nullable=False, default=0),
    Column("nid", Char(length=32), nullable=False, default=''),
    Column("tid", Char(length=32), nullable=False, default=''),
)


data_table = Table(
    "data",
    meta.metadata,
    Column("bodyHash", Char(length=32), primary_key=True,
           nullable=False, default=''),
    Column("size", Integer(unsigned=True), nullable=False, default=0),
    Column("body", Text(), nullable=False, default=0),
)

resource_table = Table(
    "resource",
    meta.metadata,
    Column("guid", Char(length=32), primary_key=True,
           nullable=False, default=''),
    Column("noteGuid", Char(length=32), nullable=False, default=''),
    Column("data", Integer(unsigned=True), nullable=False, default=''),
    Column("mime", Varchar(length=32), nullable=False, default=''),
    Column("width", Smallint(unsigned=True), nullable=False, default=0),
    Column("height", Smallint(unsigned=True), nullable=False, default=0),
    Column("duration", Smallint(unsigned=True), nullable=False, default=0),
    Column("active", Tinyint(unsigned=True), nullable=False, default=0),
    Column("updateSequenceNum", Integer(unsigned=True), nullable=False,
           default=0),
    Column("data", Varchar(length=32), nullable=False, default=''),
    Column("recognition", Varchar(length=32), nullable=False, default=''),
    Column("alternateData", Varchar(length=32), nullable=False, default=''),
)


resource_attribute_table = Table(
    "resource_attribute",
    meta.metadata,
    Column("id", Integer(unsigned=True), primary_key=True,
           autoincrement=True, nullable=False, default=0),
    Column("sourceURL", Varchar(length=1024), nullable=False, default=''),
    Column("timestamp", Integer(unsigned=True), nullable=False, default=0),
    Column("latitude",  Double(), nullable=False, default=0),
    Column("longitude",  Double(), nullable=False, default=0),
    Column("altitude",  Double(), nullable=False, default=0),
    Column("cameraMake",  Varchar(length=64), nullable=False, default=''),
    Column("cameraModel",  Varchar(length=64), nullable=False, default=''),
    Column("clientWillIndex",  Tinyint(unsigned=True), nullable=False,
           default=0),
    Column("recoType",  Varchar(length=64), nullable=False, default=''),
    Column("fileName",  Varchar(length=256), nullable=False, default=''),
    Column("attachment",  Tinyint(unsigned=True), nullable=False, default=''),
    Column("applicationData",  Integer(unsigned=True), nullable=False,
           default=0),
)


resource_resource_attribute_table = Table(
    "resource_resource_attribute",
    meta.metadata,
    Column("id", Integer(unsigned=True), primary_key=True,
           autoincrement=True, nullable=False, default=0),
    Column('rid', Char(length=32), nullable=False, default=''),
    Column('raid', Integer(unsigned=True), nullable=False, default=0),
)


note_resource_table = Table(
    "note_resource",
    meta.metadata,
    Column("id", Integer(unsigned=True), primary_key=True,
           autoincrement=True, nullable=False, default=0),
    Column("nid", Char(length=32), nullable=False, default=''),
    Column("rid", Char(length=32), nullable=False, default=''),
)

note_attribute_table = Table(
    "note_attribute",
    meta.metadata,
    Column("id", Integer(unsigned=True), primary_key=True,
           autoincrement=True, nullable=False, default=0),
    Column("subjectDate", Integer(unsigned=True), nullable=False, default=0),
    Column("latitude", Double(), nullable=False, default=0),
    Column("longitude", Double(), nullable=False, default=0),
    Column("altitude", Double(), nullable=False, default=0),
    Column("author", Varchar(length=64), nullable=False, default=""),
    Column("source", Varchar(length=64), nullable=False, default=""),
    Column("sourceURL", Varchar(length=1024), nullable=False, default=""),
    Column("sourceApplication", Varchar(length=64), nullable=False,
           default=""),
    Column("shareDate", Integer(unsigned=True), nullable=False,
           default=0),
    Column("reminderOrder", BigInteger(unsigned=True), nullable=False,
           default=0),
    Column("reminderDoneTime", Integer(unsigned=True), nullable=False,
           default=0),
    Column("reminderTime", Integer(unsigned=True), nullable=False, default=0),
    Column("placeName", Varchar(length=64), nullable=False, default=''),
    Column("contentClass", Varchar(length=64), nullable=False, default=''),
    Column("applicationData", Varchar(length=256), nullable=False, default=''),
    Column("lastEditedBy", Varchar(length=32), nullable=False, default=''),
    Column("classifications", Varchar(length=256), nullable=False, default=''),
    Column("creatorId", Integer(unsigned=True), nullable=False, default=0),
    Column("lastEditorId", Integer(unsigned=True), nullable=False, default=0),
)


note_note_attribute_table = Table(
    "note_note_attribute",
    meta.metadata,
    Column("id", Integer(unsigned=True), primary_key=True,
           autoincrement=True, nullable=False, default=0),
    Column("nid", Char(length=32), nullable=False, default=0),
    Column("naid", Integer(unsigned=True), nullable=False, default=0),
)


lazymap_table = Table(
    "lazymap",
    meta.metadata,
    Column("id", Integer(unsigned=True), primary_key=True,
           autoincrement=True, nullable=False, default=0),
    Column("keysOnly", Varchar(length=256), nullable=False, default=''),
    Column("fullMap", Varchar(length=512), nullable=False, default=''),
)


#binascii.b2a_hex(md5('1').digest())

#class Foo(object):
#    pass
#
#orm.mapper(Foo, foo_table)


## Classes for reflected tables may be defined here, but the table and
## mapping itself must be done in the init_model function
#reflected_table = None
#
#class Reflected(object):
#    pass


notebook_table = Table(
    "notebook",
    meta.metadata,
    Column("guid", Char(length=32), primary_key=True, nullable=False),
    Column("name", Varchar(length=64), nullable=False, default=''),
    Column("updateSequenceNum", Integer(unsigned=True), nullable=False,
           default=0),
    Column("defaultNotebook", Tinyint(unsigned=True), nullable=False,
           default=0),
    Column("serviceCreated", Integer(unsigned=True), nullable=False,
           default=0),
    Column("serviceUpdated", Integer(unsigned=True), nullable=False,
           default=0),
    Column("publishing", Integer(unsigned=True), nullable=False,
           default=0),
    Column("published", Tinyint(unsigned=True), nullable=False,
           default=0),
    Column("stack", Varchar(length=64), nullable=False,
           default=''),
    #sharedNotebookIds   list<i64>
    #sharedNotebooks list<SharedNotebook>
    #businessNotebook    BusinessNotebook
    #contact User
    #restrictions    NotebookRestrictions
)

publishing_table = Table(
    "publishing",
    meta.metadata,
    Column("id", Integer(unsigned=True), primary_key=True,
           autoincrement=True, nullable=False, default=0),
    Column("uri", Varchar(length=1024), nullable=False, default=""),
    Column("order", Tinyint(unsigned=True), nullable=False, default=0),
    Column("ascending", Tinyint(unsigned=True), nullable=False, default=0),
    Column("publicDescription", Varchar(length=256), nullable=False,
           default=0),
)


class Note(object):
    pass


class Tag(object):
    pass


class NoteTag(object):
    pass


class NoteAttribute(object):
    pass


class NoteNoteAttribute(object):
    pass


class Data(object):
    pass


class Resource(object):
    pass


class ResourceAttribute(object):
    pass


class ResourceResourceAttribute(object):
    pass


orm.mapper(Note, note_table)
orm.mapper(Tag, tag_table)
orm.mapper(NoteTag, note_tag_table)
orm.mapper(NoteAttribute, note_attribute_table)
orm.mapper(NoteNoteAttribute, note_note_attribute_table)
orm.mapper(Data, data_table)
orm.mapper(Resource, resource_table)
orm.mapper(ResourceAttribute, resource_attribute_table)
orm.mapper(ResourceResourceAttribute, resource_resource_attribute_table)
