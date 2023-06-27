from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PageView(BrowserView):

    template = ViewPageTemplateFile("page.pt")
    
    def __call__(self):
        return self.template()


    @property
    def get_citations(self):
    
        output = u""
        if hasattr(self.context, 'citation_ordering'):
            if self.context.citation_ordering:
                for citation_id in self.context.citation_ordering:
                    if hasattr(self.context, citation_id):
                        citation = getattr(self.context, citation_id, None)
                        if citation:
                            if citation.raw:
                                output += citation.raw + "<br />"
        return output


    @property
    def portal(self):
        return api.portal.get()
        