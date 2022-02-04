var Canvas = {

    POLK_ROOT : 'https://library.uwosh.edu/',
    POLK_WS_ROOT : 'https://library.uwosh.edu/',

    construct : function() {
        $('a').attr('target','_blank'); // make links open new tabs
        this.retrieve_db_information();
        this.telephone_format();
    },
    
    telephone_format : function() {
        $('.pat-telephone').each(function(){
            var text = $.trim($(this).text());
            text = text.replace(/(\d{3})(\d{3})(\d{4})/, "$1-$2-$3");
            $(this).text(text);
        });
    },
    
    retrieve_db_information : function(){
        $.getJSON(Canvas.POLK_WS_ROOT + 'getResearchDatabase', function(data){
            DB.dynamic_construct(data);
        });
    }


}

var DB = {
    
    construct : function(){
        this.subject_legend();
    },
        
    dynamic_construct : function(data){
        var self = this;
        for (var i in data){
            var result = data[i];
            
            var d = $('body').find('.pat-db-info-desc[data-desc-id="' + result.getId + '"]');
            $(d).attr('data-safe','1');
            
            var e = $('body').find('.pat-db-info[data-id="' + result.getId + '"]');
            $(e).attr('data-safe','1');
            if (result.message_type == 'Warning')
                $(e).before(self.create('WARN', 'Information Notice!', result.getURL + '/dbinfo'));
            if (result.message_type == 'Trial')
                $(e).before(self.create('TRIAL', 'Trial Information Available', result.getURL + '/dbinfo'));
            if (result.tutorial != '') {
                $(e).before(self.create('INFO', 'Tutorial Available', result.tutorial));
            }
            $(e).attr('href', result.getURL);
            self.disciplines(result, e);
        };
        
        $('.pat-db-info:not([data-safe])').hide(); // no db in A-Z list, hide it, it was removed
        $('.pat-db-info-desc:not([data-safe])').hide(); // no db in A-Z list, hide it, it was removed
    },
    
    
    create : function(type, title, link) {
        var icons = {
            'INFO' : '/++theme++uwosh/images/icons/help-128.png',
            'WARN' : '/++theme++uwosh/images/icons/warning-128.png',
            'TRIAL' : '/++theme++uwosh/images/icons/trial-128.png',
        }
        
        var img = $('<img>').addClass('db-icon-' + type).attr('alt', type).attr('title', title).attr('src', Canvas.POLK_ROOT + icons[type]);
        var a = $('<a>').addClass('db-info').attr('href', link).append(img);
        return a;
    },
    
    
    subject_legend : function(){
        if (typeof SubjectDisciplines !== 'undefined') {
            for (var i in SubjectDisciplines){
                var e = $('#subject-legend li[data-discipline="0"]').eq(0);
                $(e).attr('data-discipline', SubjectDisciplines[i]);
                $(e).find('div').html(SubjectDisciplines[i]).css('display','inline');
            }
        }
    },
    
    disciplines : function(db, e) {
        
        if (typeof SubjectDisciplines !== 'undefined') {
            
            for (var i in db.disciplines){
                var discipline = db.disciplines[i];
                var key = $('#subject-legend li[data-discipline="' + discipline + '"]').eq(0);
                if (key) {
                    var img = $(key).find('img').attr({'title': discipline, 'alt': discipline}).clone();
                    $('#content-core .content-subject').find(e).after(img);
                }
                
            }
        }
        
    },
    
    
    
}



var Accordians = {
    
    construct : function(){
        $('#content-core .accordion-header-on').each(function(){
            $(this).nextUntil('#content-core .accordion-end, #content-core .accordion-header-on, #content-core .accordion-header-off').wrapAll('<div class="accordion-body-on"></div>');
        });
        $('#content-core .accordion-header-off').each(function(){
            $(this).nextUntil('#content-core .accordion-end, #content-core .accordion-header-on, #content-core .accordion-header-off').wrapAll('<div class="accordion-body-off"></div>');
        });
        
        this.events();
    },
    
    events : function(){
        $('#content-core .accordion-header-on').click(function(){
            $(this).toggleClass('accordion-open');
            $(this).next('.accordion-body-on').slideToggle(333);
        });
    }
    
}




$(document).ready(function(){
    DB.construct();
    Canvas.construct();
    Accordians.construct();
});