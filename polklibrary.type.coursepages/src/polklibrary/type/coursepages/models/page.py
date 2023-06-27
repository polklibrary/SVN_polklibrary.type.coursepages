from plone import api
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.browser.edit import DefaultEditForm
from plone.app.textfield.value import RichTextValue
from zope.schema.interfaces import IContextAwareDefaultFactory
from zope.interface import alsoProvides, provider
from plone.autoform.interfaces import IFormFieldProvider


citation_choices = SimpleVocabulary([
    SimpleTerm(value=u'citation_apa', title=u'APA'),
    SimpleTerm(value=u'citation_mla', title=u'MLA'),
    SimpleTerm(value=u'citation_chicago', title=u'Chicago'),
])

@provider(IContextAwareDefaultFactory)
def default_apa_factory(context):
    if context.portal_type == 'polklibrary.type.coursepages.models.page':
        if context.aq_parent.citation_apa:
            return context.aq_parent.citation_apa.output
    if context.portal_type == 'polklibrary.type.coursepages.models.librarian':
        if context.citation_apa:
            return context.citation_apa.output
    return u"<p> </p>"

@provider(IContextAwareDefaultFactory)
def default_mla_factory(context):
    if context.portal_type == 'polklibrary.type.coursepages.models.page':
        if context.aq_parent.citation_mla:
            return context.aq_parent.citation_mla.output
    if context.portal_type == 'polklibrary.type.coursepages.models.librarian':
        if context.citation_mla:
            return context.citation_mla.output
    return u"<p> </p>"


@provider(IContextAwareDefaultFactory)
def default_chicago_factory(context):
    if context.portal_type == 'polklibrary.type.coursepages.models.page':
        if context.aq_parent.citation_chicago:
            return context.aq_parent.citation_chicago.output
    if context.portal_type == 'polklibrary.type.coursepages.models.librarian':
        if context.citation_chicago:
            return context.citation_chicago.output
    return u"<p> </p>"


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
          
          
    model.fieldset(
        'citations',
        label=u'Citations', 
        fields=['citation_ordering', 'citation_apa', 'citation_mla', 'citation_chicago'],
    )
        

    citation_ordering = schema.List(
            title=u"Citation Show/Hide and Ordering",
            required=False,
            value_type=schema.Choice(source=citation_choices),
        )
        
    citation_apa = RichText(
            title=u"APA Citation Guide",
            description=u"Delete all apa content and save to have it show original snippet again.",
            default_mime_type='text/structured',
            required=False, 
            defaultFactory=default_apa_factory,
            missing_value=u"",
        )
        
    citation_mla = RichText(
            title=u"MLA Citation Guide",
            description=u"Delete all mla content and save to have it show original snippet again.",
            default_mime_type='text/structured',
            required=False,
            defaultFactory=default_mla_factory,
            missing_value=u"",
        )
        
    citation_chicago = RichText(
            title=u"Chicago Citation Guide",
            description=u"Delete all chicago content and save to have it show original snippet again.",
            default_mime_type='text/structured',
            required=False,
            defaultFactory=default_chicago_factory,
            missing_value=u"",
        )
        
alsoProvides(IPage, IFormFieldProvider) # required for defaultFactory context.
        
        
        
    
class EditForm(DefaultEditForm):
    portal_type = 'polklibrary.type.coursepages.models.page'

    def __init__(self, context, request):
        DefaultEditForm.__init__(self,context, request)

        apa = u""
        if self.context.citation_apa:
            apa = self.context.citation_apa.output
        if apa == None or apa== u"<p> </p>" or apa == u"<p></p>" or apa == u"":
            if self.context.aq_parent.citation_apa:
                self.context.citation_apa = RichTextValue(self.context.aq_parent.citation_apa.output, 'text/plain', 'text/html')
            
        mla = u""
        if self.context.citation_mla:
            mla = self.context.citation_mla.output
        if mla == None or mla== u"<p> </p>" or mla == u"<p></p>" or mla == u"":
            if self.context.aq_parent.citation_mla:
                self.context.citation_mla = RichTextValue(self.context.aq_parent.citation_mla.output, 'text/plain', 'text/html')
            
            
        chicago = u""
        if self.context.citation_chicago:
            chicago = self.context.citation_chicago.output
        if chicago == None or chicago == u"<p> </p>" or chicago == u"<p></p>" or chicago == u"":
            if self.context.aq_parent.citation_chicago:
                self.context.citation_chicago = RichTextValue(self.context.aq_parent.citation_chicago.output, 'text/plain', 'text/html')
            
            
            