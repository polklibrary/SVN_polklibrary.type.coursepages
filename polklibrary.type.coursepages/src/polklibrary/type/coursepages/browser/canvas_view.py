from plone import api
from plone.i18n.normalizer import idnormalizer
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from polklibrary.type.coursepages.utility import MailMe
import json, logging

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

logger = logging.getLogger("Plone")
cp_logger = setup_logger('CoursePages', 'var/coursepages.log')


class CanvasView(BrowserView):

    template = ViewPageTemplateFile("canvas_view.pt")
    
    # SUBJECT RULE MAP
    # NOTE: Some targets are missing ending letters to prevent conflicts.  Example:  data communicatio != communication
    BUSINESS = ['business',' economics','economy','marketing','finance','financial','accounting','information systems','human resource',
        'audit','tax','taxation','fraud','cost management','operations management','organizational behavior','independent study','risk management',
        'managing','strategic management','consulting','banking','markets','trade','monetary','industrial organization','time series analysis','econometric',
        'real estate','investment','security analysis','endowment','actuarial science','insurance','digital future','networking hardware',
        'virtualization technologies','systems analysis','data communicatio','agile','c#','e-commerce','technology innovation','software design',
        'mobile application','planning systems','engineering project management','change management','entrepreneurship','global management','employee',
        'occupational safety','compensation management','benefits','project execution','sales','retail management','consumer behavior','sales management',
        'product management','purchasing behavior','supply chain','manufacturing','procurement','quality management'
    ]
    COMMUNICATION = ['communication','public speaking','speech communication','interpersonal speech','speech','rhetoric','public advocacy','interviewing',
        'oral interpretation','effective listening','argumentation','debate','speaking','prison exchange','gender and discourse','persuasion','participation',
        'training and development','public address','criticism'
    ]
    ENGLISH = ['english','foreign language','composition','literature','writing','perspectives','shakespeare','speaking globally','writers','novel','romanticism',
        'linguistics','story','wbis','literary','connect','poetry','mythology','chaucer','drama','methods of research','fiction','grammer'
    ]
    EDUCATION = ['education','school','psychology','disabilities','special ed','teaching','adolescent','k-12','k12','instruction','lesson plans','ed leadership',
        'spec ed','pupil','curriculum','prof development','professional development','higher ed','decision making','learning','trad ed','community engagement',
        'program development','applied research','superintendency','theoretical foundations','systematic inequity','hr management','pe major',
        'swimming','dance','aquatics','motor development','pe/ape','prek-12','prek',
        'kindergarden','daycare','sport','wellness','nutrition','human sexuality','health','classroom','cpr','aed','first aid','death and dying','interpersonal',
        'intervention','literacy','childhood','skillful practice','foundational knowledge','adolescence','american sign','sign language','deaf','youth',
        'children','behavior management','birth','family'
    ]
    FINE_ARTS = ['polk','test','studio art','drawing','arts','dimensional design','2d','3d',' art ','art ',' art','art:','creation','memorial','figure','experience mapping','graphic',
        'typograpy','watercolor','photography','printmaking','lithography','serigraphy','intaglio','relief','art metal','sculpture','ceramics','painting','paint','animation',
        'fabrication','responsive objects','studio','topics in art','art history','ancient art','medieval art','gothic art','architecture','baroque','dutch and flemish',
        'art of india','european art','contemporary','american art','greek and roman art','museum','exhibition design','woodworking','developmental art','visual identity','branding',
        'design intership','music','convocation','aural skills','applied study','ensemble','piano','voice','diction','instuments','instumental','vocal','composition','conducting',
        'form and analysis','midi','applied lessons','chamber','recital','instrumentation','instrument','opera','theater','theatre','pedagogy','chore','choral','keyboard','keybd',
        'pianist','symphonic','symphony','orchest',' song','strings','string','rythme','private lesson','studio','audio','costume','set design','lighting and sound',
        'acting studio','directing','culture and style','intro to acting','introduction to acting','play analysis','musical','drama','creative process','history of styles','scene shop',
        'comedy','playwright','stage','props','makeup','screen','entertainment','design/tech','jazz'
    ]
    GOV_LAW = ['government','criminal','intro to law', 'introduction to law', 'constitutional law','administrative law','international law','judicial','environmental law','justice',
        'correctional','police','policing','crime','investigation','guilt','courts','violence','criminology','terrorism','homeland security','human behavior','social issues','human services',
        'public admin','public policy','intergovernmental','public sector','leadership and ethics','non-profit','pub admin','nonprofit','human resources','hr','fire and emergency','fire & emergency',
        'fesa','faea','faer','municipal','bureaucracy','economic development','health care management','health care administration','health care policy','public budgeting','military',
        'basic leadership','advanced leadership','us army','u.s. army','cadet','rotc','officer','ferm','emergency','fire prevention','community risk'
    ]
    # HISTORY IS LAST DUE TO MANY CONFLICTS
    HISTORY = ['history','historical','civilization','migration','great depression','ancient greece','middle ages','roman','reformation','renaissance','europe','nationalism','modernism',
        'revolution','american cities','culture and society','imperial','world war','wars','nazi','reich','holocaust','nuclear america','globalization','twentieth century','ancient',
        'democracy','republic','communism','middle ages','medieval','middle east','african american','philosphopy','elementary logic','symbolic logic','cognitive science','theory of knowledge',
        'biomedical ethics','ethical issues','ethical problems','existentialism','climate justice','human nature','religion','religious','bible','testament','hebrew','christ','catholic',
        'judaism','hindu','budda','buddhism','islam','muslim','catholicism','jesus','letters to paul','buddhist','mystical','cults','sects'
    ]
    INTERDISCIPLINARY = ['wg stds','liberal studies','international studies','international issues','international negotiation','diplomatic','diplomacy','women','feminist','feminism',
        'gender studies','lgbtq','lgbtq+','queer','transexual','asexual','masculinity','sexuality','diversity','inclusion','inclusive','african american studies'
    
    ]
    NURSING = ['nurs','nursing','medicine','medical','health','physiology','evidence-based practice','ethical care','pharm','pharmacy','drugs','childbearing','obstetrics','clinical',
        'children and adolescents','nutrition','pathophysiology','informatics','aging','therapeutic','caring','human anatomy','kinesiology','biomechanics','motor learning',
        'exercise','resistance training','recreation','leisure','adventure','activities','fitness'
    ]
    PSYCHOLOGY = ['psychology','psych','abnormal behavior','research methods','abnormal behav','principles of learning','personality','autism','counseling','professional identity',
        'career development','contextual diagnosis','social and cultural foundations','trauma','neuroscience','mental health','student affairs','student development'
    ]
    SOCIAL_SCIENCES = ['anthrophology','anthro','archaeology','language in culture','ethnographic','osteology','human evolution','race and human','sociology','intercultural',
        'ethnicity','social statistics','soc. theory','social stratification','social control','social research','geography','geo','gis','environment','natural resource','natural hazards',
        'urban planning','political','poli sci','polisci','pol sci','politics','government and politics','civic','democratic','social justice','soc just','rhetorical criticism',
        'social work','geog','soil','conservation','weather','wisconsin','meteorology','climatology','water resource','cartography','population and environment'
    ]
    # LOWER DOWN LIST due to BIO
    STEM = ['biology','biological concepts','bio','microbi','neurobio','bacteri','animal behavior','virology','mycology','ornithology','ichtyology','entomology','ecology','immunology'
    'microscopy','hematology','parasitology','freshwater invertebrates','genetics','ecosystems','biotechnology','ecosphere','human physiology','epidemiology','living systems',
    'plant taxonomy','rt block','physics','astronomy','astro','stars','galaxies','universe','solar system','energy','engineering','astrophysics','electronic circuits','physical optics',
    'stellar structure','digital instrumentation','electricity','quantum','geology','earth','dinosaurs','reptiles','mineralogy','lithology','petrology','paleontology','stratigraphy',
    'geomorphology','mineral','geophysics','tectonics','oceanography','glacial','hydrogeology','geochemistry','computer science','object oriented','java','computer architecture','assembly language',
    'programming','data structures','algorithms','software engineering','computing ethics','operating systems','computing','compilers','computer','database systems','web design','networking and data',
    'mobile application','web development','agile','math','mathematics','algebra','trigonometry','statistics','number systems','calculas','geometry','data explorations','propbability','topology',
    'differential equations','chemistry','chem','biochem','biochemistry','general organic','organic chemistry','biophysical','inorganic',
    
    ]
    SUSTAINABILITY = ['sustainable','sustainability','energy and facilities management','environmental','environment science','nature writing','env studies','physical geography','climate'
        'ecology','population problems'
    ]
    
    
    NON_EDITOR_ROLES = ['student', 'interpreter pre-semester', 'observers', 'interpreter semester', 'learner', 'students']
    
    def __call__(self):
        self.message = None
        
        canvas_course_id = self.request.form.get('custom_canvas_course_id', 0)
        canvas_course_title = self.request.form.get('context_title', 0)
        canvas_role = self.request.form.get('roles', '').lower()
        canvas_firstname = self.request.form.get('lis_person_name_given', '')
        canvas_lastname = self.request.form.get('lis_person_name_family', '')
        canvas_email = self.request.form.get('lis_person_contact_email_primary', '')
        custom_canvas_domain = self.request.form.get('custom_canvas_api_domain', '')
        
        if ('uws.instructure.com' in custom_canvas_domain or 'uwosh.instructure.com' in custom_canvas_domain or 'uwosh.test.instructure.com' in custom_canvas_domain or 'uwosh.beta.instructure.com' in custom_canvas_domain) and canvas_course_id != 0:
            
            self.custom_canvas_domain = custom_canvas_domain
            self.canvas_course_id = canvas_course_id
            self.canvas_course_title = canvas_course_title
            self.canvas_person_email = canvas_email
            self.canvas_person_name = canvas_firstname + " " + canvas_lastname
            self.canvas_role = canvas_role
            self.canvas_firstname = canvas_firstname
            self.canvas_lastname = canvas_lastname
            self.is_canvas_editor = canvas_role.lower() not in self.NON_EDITOR_ROLES
            
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
    
        return "Access denied.  Access to this LTI is only accessible from a uwosh instructure domain.  To get an exception added please contact librarytechnology@uwosh.edu."

     
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

        if any(x in course_title for x in self.BUSINESS):
            subject_id = 'business-economics'
        elif any(x in course_title for x in self.COMMUNICATION):
            subject_id = 'communication-media'
        elif any(x in course_title for x in self.EDUCATION):
            subject_id = 'education'
        elif any(x in course_title for x in self.ENGLISH):
            subject_id = 'english-foreign-languages'
        elif any(x in course_title for x in self.FINE_ARTS): 
            subject_id = 'fine-arts' 
        elif any(x in course_title for x in self.GOV_LAW):
            subject_id = 'government-law-human-services'
        elif any(x in course_title for x in self.INTERDISCIPLINARY):
            subject_id = 'interdisciplinary'
        elif any(x in course_title for x in self.NURSING):
            subject_id = 'nursing-allied-health'
        elif any(x in course_title for x in self.PSYCHOLOGY):
            subject_id = 'psychology-counseling'
        elif any(x in course_title for x in self.SOCIAL_SCIENCES):
            subject_id = 'social-sciences'
        elif any(x in course_title for x in self.SUSTAINABILITY):
            subject_id = 'sustainability'
        elif any(x in course_title for x in self.STEM): # SECOND TO BOTTOM DUE TO BIO
            subject_id = 'stem'
        elif any(x in course_title for x in self.HISTORY):  # LAST DUE TO HISTORY BEING OVER MANY GROUPS
            subject_id = 'history-philosophy-religion'
        
        
        brains = api.content.find(portal_type='polklibrary.type.subjects.models.subject', id=subject_id)
        if brains:
            cp_logger.info("FOUND: " + str(course_title) + brains[0].Title) # FOUND
            return brains[0]
            
        cp_logger.info("MISS: " + str(course_title)) # MISS
        return None
    
    def get_disciplines(self):
        result = {}
        if self.subject:
            for i in self.subject.disciplines:
                result[i] = i
        return json.dumps(result)
        
        
    def workflow(self):   
        librarian_count = 0
        librarian = None
        all_fail_email = True
        brains = api.content.find(portal_type='polklibrary.type.coursepages.models.librarian')
        for brain in brains:
            if brain.resources:
                if self.canvas_person_email in brain.resources:
                    librarian_count+=1
                    if not librarian:
                        librarian = brain.getObject()
                
        plone_id = idnormalizer.normalize(self.canvas_course_title)
        
        # Distance education workflow
        if self.request.form.get('form.online','').lower() == 'yes':
            all_fail_email = False #success
            
            to_email = ['onlinelearning@uwosh.edu',self.canvas_person_email,'librarytechnology@uwosh.edu']
            from_email = [self.canvas_person_email]
            subject = "Course Page Request: " + self.canvas_course_title
            body = "This is an online course, please contact the instructor for information." + str(librarian_count) + "<br/><br/>"
            body += "Canvas Course Instructor: " + self.canvas_person_name + "<br/>"
            body += "Canvas Course ID: " + self.canvas_course_id + "<br/>"
            body += "Canvas Course Title: " + self.canvas_course_title + "<br/>"
            body += "Canvas Online Course: " + self.request.form.get('form.online','') + "<br/>"
            body += "Instructor Note: " + self.request.form.get('form.note','')+ "<br/>"
            
            MailMe(subject, from_email, to_email, body)
        
        # Standard workflow
        elif librarian and librarian_count == 1:
            try:
                staff = api.content.get(path=librarian.location)
                obj = None
                
                brains = api.content.find(librarian, portal_type='polklibrary.type.coursepages.models.page', id=plone_id)
                if brains: # if exists, append new canvas id to list
                    obj = brains[0].getObject()
                    obj.resources.append(self.canvas_course_id)
                    
                    obj.reindexObject()
                    self.message = "A previously created course page was found for this course and the assigned librarian will be contacting you shortly."
                    
                else: # if doesn't exist, add it
                    obj = api.content.create(
                        librarian, 
                        type='polklibrary.type.coursepages.models.page', 
                        id=plone_id,
                        title=self.canvas_course_title, 
                    )
                    obj.resources=[]
                    obj.resources.append(self.canvas_course_id)
                    with api.env.adopt_roles(roles=['Manager']): # publish empty page
                        api.content.transition(obj=obj, transition='publish')
                    
                    obj.reindexObject()
                    self.message = "A course page has been created and your assigned librarian will be contacting you shortly."
                    
                all_fail_email = False #success
                    
                to_email = [staff.email, self.canvas_person_email, 'librarytechnology@uwosh.edu']
                from_email = [self.canvas_person_email]
                subject = "Course Page Request: " + self.canvas_course_title
                body = "Here is the course page: " + obj.absolute_url() + "<br/><br/>"
                body += "Canvas Course Instructor: " + self.canvas_person_name + "<br/>"
                body += "Canvas Course ID: " + self.canvas_course_id + "<br/>"
                body += "Canvas Course Title: " + self.canvas_course_title + "<br/>"
                body += "Canvas Online Course: " + self.request.form.get('form.online','') + "<br/>"
                body += "Instructor Note: " + self.request.form.get('form.note','')+ "<br/>"
                
                MailMe(subject, from_email, to_email, body)
                    
                
            except Exception as e:
                logger.info("Course Page Standard Workflow")
                logger.exception(e)

       # Catch all workflow
        if all_fail_email:
            self.message = "You do not have a librarian assigned to you.  We are assigning you a librarian best suited to this subject.  They will be contacting you shortly."
            
            to_email = ['libraryinstruction@uwosh.edu', self.canvas_person_email, 'librarytechnology@uwosh.edu']
            from_email = [self.canvas_person_email]
            subject = "Course Page Request: " + self.canvas_course_title
            body = "This appears to be a new faculty member.  No course page could be auto-assigned, please assign this faculty member to a librarian. <br/><br/>"
            body += "Canvas Course Instructor: " + self.canvas_person_name + "<br/>"
            body += "Canvas Course ID: " + self.canvas_course_id + "<br/>"
            body += "Canvas Course Title: " + self.canvas_course_title + "<br/>"
            body += "Canvas Online Course: " + self.request.form.get('form.online','') + "<br/>"
            body += "Instructor Note: " + self.request.form.get('form.note','')+ "<br/>"
        
            MailMe(subject, from_email, to_email, body)

            
    @property
    def portal(self):
        return api.portal.get()
         