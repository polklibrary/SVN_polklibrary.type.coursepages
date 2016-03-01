from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class LibrarianView(BrowserView):

    template = ViewPageTemplateFile("librarian.pt")
    
    def __call__(self):
        return self.template()

    def get_member(self):
        return api.content.get(path=self.context.location)
        
    def get_course_pages(self):
        return api.content.find(context=self.context, depth=1, portal_type='polklibrary.type.coursepages.models.page', sort_on='sortable_title')
        
    @property
    def portal(self):
        return api.portal.get()
        