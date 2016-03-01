from plone import api
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


class IPage(model.Schema):

    title = schema.TextLine(
            title=u"Title",
            required=True,
        )

    body = RichText(
            title=u"Course Page",
            default_mime_type='text/structured',
            required=False,
            default=u"",
        )
        
    resources = schema.List(
            title=u"Add to D2L (provide one ID on each line)",
            required=False,
            value_type=schema.TextLine()
        )
        
        

        
        