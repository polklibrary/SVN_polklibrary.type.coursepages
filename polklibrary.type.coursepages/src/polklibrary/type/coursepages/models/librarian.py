from plone import api
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.interface import directlyProvides
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

def librarian_vocab(context):
    try:
        voc = []
        brains = api.content.find(portal_type='polklibrary.type.staff.models.staff', sort_on='sortable_title')
        for brain in brains:
            voc.append(SimpleVocabulary.createTerm(brain.getPath(), brain.Title))
        return SimpleVocabulary(voc)
    except Exception as e:
        return []
directlyProvides(librarian_vocab, IContextSourceBinder)



class ILibrarian(model.Schema):

    title = schema.TextLine(
            title=u"Title",
            required=True,
        )
        
    location = schema.Choice(
            title=u"Select a staff member",
            required=False,
            source=librarian_vocab,
        )
        
    chat = schema.TextLine(
            title=u"LibraryH3lp ID",
            required=False,
        )
        
    libchat = schema.Text(
            title=u"LibChat Code",
            default=u" ",
            required=False,
        )
        
    resources = schema.List(
            title=u"List of faculty emails to be auto-assigned to this librarian (one email per line)",
            required=False,
            value_type=schema.TextLine()
        )
        
        