from plone import api
from plone.indexer.decorator import indexer
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
            title=u"LMS Course ID (provide one ID on each line)",
            required=False,
            value_type=schema.TextLine()
        )
        
        
@indexer(IPage)
def make_searchable(object, **kwargs):
    import re
    portal_transforms = api.portal.get_tool(name='portal_transforms')
    data = portal_transforms.convertTo('text/plain', object.body.output, mimetype='text/structured')
    text = data.getData()
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', object.body.output)
    return [object.title, object.description, text] + urls
        
        
        
        
        