from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PageView(BrowserView):

    template = ViewPageTemplateFile("page.pt")
    
    def __call__(self):
        return self.template()

    @property
    def portal(self):
        return api.portal.get()
        