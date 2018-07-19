from plone import api
from plone.i18n.normalizer import idnormalizer
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from polklibrary.type.coursepages.utility import MailMe

import json


class CanvasView(BrowserView):

    template = ViewPageTemplateFile("canvas_view.pt")
    
    non_editor_roles = ['student', 'interpreter pre-semester', 'observers', 'interpreter semester']
    
    def __call__(self):
        self.message = None
        # TEST
        # getLibraryCanvasResources?custom_canvas_course_id=43943&context_title=Biology 101&custom_canvas_api_domain=uwosh.instructure.com&lis_person_contact_email_primary=hietpasd@uwosh.edu&lis_person_name_family=Hietpas&lis_person_name_given=David&roles=Instructor
    
        canvas_course_id = self.request.form.get('custom_canvas_course_id', 0)
        canvas_course_title = self.request.form.get('context_title', 0)
        canvas_role = self.request.form.get('roles', '').lower()
        canvas_firstname = self.request.form.get('lis_person_name_given', '')
        canvas_lastname = self.request.form.get('lis_person_name_family', '')
        canvas_email = self.request.form.get('lis_person_contact_email_primary', '')
        custom_canvas_domain = self.request.form.get('custom_canvas_api_domain', '')
        
        if 'uwosh.instructure.com' in custom_canvas_domain and canvas_course_id != 0:
            
            # print canvas_course_id
            # print canvas_role
            # print custom_canvas_domain
            # print canvas_firstname
            # print canvas_lastname
            self.custom_canvas_domain = custom_canvas_domain
            self.canvas_course_id = canvas_course_id
            self.canvas_course_title = canvas_course_title
            self.canvas_person_email = canvas_email
            self.canvas_person_name = canvas_firstname + " " + canvas_lastname
            self.canvas_role = canvas_role
            self.canvas_firstname = canvas_firstname
            self.canvas_lastname = canvas_lastname
            self.is_canvas_editor = canvas_role.lower() not in self.non_editor_roles
            
            # Handle Workflows
            if self.is_canvas_editor and 'form.submit' in self.request.form:
                self.workflow()
            
            # Setup Course Page
            course_page_brain =  self.get_course_page(canvas_course_id)
            subject_brain =  self.get_subject(canvas_course_title)
            self.course_page = None
            self.course_librarian = None
            self.librarian = None
            self.subject = None
            
            if subject_brain:
                self.subject = subject_brain.getObject()
            
            if course_page_brain:
                self.course_page = course_page_brain.getObject()
                self.librarian = self.get_librarian(self.course_page)
            
            self.requires_setup = self.is_canvas_editor and not self.course_page
            
            return self.template()
    
        return "None"

     
    def get_course_page(self, canvas_id):
        brains = api.content.find(portal_type='polklibrary.type.coursepages.models.page', resources=canvas_id)
        for brain in brains:
            if str(canvas_id) in brain.resources:
                return brains[0]
        return None

    def get_librarian(self, course_page):
        try:
            self.course_librarian = course_page.aq_parent
            return api.content.get(path=self.course_librarian.location)
        except:
            return None

    def get_subject(self, course_title):
        course_title = course_title.lower()
        subject_id = '^$#$&$%9JKSLDI' # random to produce miss

        if any(x in course_title for x in ['polk','art']):  # FOR TESTING
            subject_id = 'fine-arts' 
        if any(x in course_title for x in ['bio', 'chem', 'computer','test']):
            subject_id = 'stem'

        brains = api.content.find(portal_type='polklibrary.type.subjects.models.subject', id=subject_id)
        if brains:
            return brains[0]
        return None
    
    def get_disciplines(self):
        result = {}
        if self.subject:
            for i in self.subject.disciplines:
                result[i] = i
        return json.dumps(result)
    
    
    
    def workflow(self):
        print "WORKFLOW STARTED -------------------"
        
        librarian = None
        all_fail_email = True
        brains = api.content.find(portal_type='polklibrary.type.coursepages.models.librarian')
        for brain in brains:
            if self.canvas_person_email in brain.resources:
                librarian = brain.getObject()
                break
                
        plone_id = idnormalizer.normalize(self.canvas_course_title)
        
        if librarian:
            try:
                staff = api.content.get(path=librarian.location)
                obj = None
                
                brains = api.content.find(librarian, portal_type='polklibrary.type.coursepages.models.page', id=plone_id)
                if brains: # if exists, append new canvas id to list
                    obj = brains[0].getObject()
                    obj.resources.append(str(self.canvas_course_id))
                    obj.reindexObject()
                    print "OBJECT FOUND - ADDING INDEX"
                    self.message = "A previously create course page was found for this course and the assigned librarian will be contacting you shortly."
                    
                else: # if doesn't exist, add it
                    # obj = api.content.create(
                        # librarian, 
                        # type='polklibrary.type.coursepages.models.page', 
                        # id=plone_id,
                        # title=self.canvas_course_title, 
                        # resources=str(self.canvas_course_id)
                    # )
                    print "OBJECT NOT FOUND - CREATING"
                    self.message = "A course page has been created and your assigned librarian will be contacting you shortly."
                    
                all_fail_email = False #success
                    
                to_email = [staff.email]
                from_email = self.canvas_person_email
                subject = "Course Page Request: " + self.canvas_course_title
                body = "Canvas Course Instructor " + self.canvas_person_name + "\n"
                body += "Canvas Course ID: " + self.canvas_course_id + "\n"
                body += "Canvas Course Title: " + self.canvas_course_title + "\n"
                body += "Faculty Note: " + self.request.form.get('form.note','')+ "\n\n"
                body += "Here is the course page: " + obj.absolute_url()
                
                print "MAILING: " + subject + " " + from_email + " " + str(to_email) + " " + body
                #MailMe(subject, from_email, to_email, body)
                    
                
            except Exception as e:
                print "ERROR: " + str(e)

               
        if all_fail_email:
            self.message = "You do not have a librarian assigned to you.  We are assigning you a librarian best suited to this subject.  They will be contacting you shortly."
            
            print "NO AUTO ASSIGN FOUND - EMAILING"
            to_email = ['hietpasd@uwosh.edu']
            from_email = self.canvas_person_email
            subject = "Course Page Request: " + self.canvas_course_title
            body = "Canvas Course Instructor " + self.canvas_person_name + "\n"
            body += "Canvas Course ID: " + self.canvas_course_id + "\n"
            body += "Canvas Course Title: " + self.canvas_course_title + "\n"
            body += "Faculty Note: " + self.request.form.get('form.note','')+ "\n\n"
            body += "This appears to be a new faculty member.  No course page could be auto-assigned, please assign this faculty member to a librarian."
        
            print "MAILING: " + subject + " " + from_email + " " + str(to_email) + " " + body
            #MailMe(subject, from_email, to_email, body)
            
        
        
        
        
        
    @property
    def portal(self):
        return api.portal.get()
         