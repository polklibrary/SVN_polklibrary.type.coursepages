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
            default=u"<p>Please provide course specific content.</p>",
        )
        
    resources = schema.List(
            title=u"LMS Course ID (provide one ID on each line)",
            required=False,
            value_type=schema.TextLine()
        )
        
    show_subject_resources = schema.Bool(
            title=u"Show Subject Resources",
            required=False,
            default=True,
            missing_value=True,
        )
        
        
    show_search_atuw = schema.Bool(
            title=u"Show Search@UW",
            required=False,
            default=True,
            missing_value=True,
        )
        
# @indexer(IPage)
# def make_searchable(object, **kwargs):
    # import re
    # portal_transforms = api.portal.get_tool(name='portal_transforms')
    # data = portal_transforms.convertTo('text/plain', object.body.output, mimetype='text/structured')
    # text = data.getData()
    # urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', object.body.output)
    # return [object.title, object.description, text] + urls
        
        
        
        
        