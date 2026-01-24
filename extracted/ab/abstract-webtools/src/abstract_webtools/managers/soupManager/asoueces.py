text = """{"title": "NoviSoul
        novissbm@gmail.com", "href": "http://www.youtube.com/signin?authuser=0&next=%2Fwatch%3Fv%3DEaIYRM1yrM4&action_handle_signin=true", "description": ""},
  {"title": "Sign in", "href": "https://accounts.google.com/ServiceLogin?continue=http%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26hl%3Den_GB%26next%3D%252Fwatch%253Fv%253DEaIYRM1yrM4%26nomobiletemp%3D1&uilel=3&service=youtube&passive=true&hl=en_GB", "description": ""},
  {"title": "Sign up", "href": "http://www.youtube.com/signup?next=%2Fwatch%3Fv%3DEaIYRM1yrM4", "description": ""},
  {"title": "9:58


    
 

Physics of Free Energy Deviceby Eugene Jeong        
        
336,881 views", "href": "http://www.youtube.com/watch?v=EB-jWfzkz_E", "description": ""},
  {"title": "4:49


    
 

[www.witts.ws] Self-Running 40kW (40,000 Watt) Fuelless Generator (1 of 3)by wits2014        
        
488,638 views", "href": "http://www.youtube.com/watch?v=LFu-s6ZmGyE", "description": ""},
  {"title": "2:33


    
 

Free Energy - Evidence of military antigravity technologyby DoubleMarkez        
        
390,020 views", "href": "http://www.youtube.com/watch?v=qljY-YfFaPc", "description": ""},
  {"title": "15:01


    
 

APEX 2013   SSBM L10   Shroomed VS CT EMP Mew2Kingby Jason AxelrodRecommended for you", "href": "http://www.youtube.com/watch?v=pc7v49k5FhY", "description": ""},
  {"title": "161
            
            
              videos
            
          
        
      
          
              
          
          
              
          
      
    
      
        
          
Play all
        
      
  
washby dle3276", "href": "http://www.youtube.com/watch?v=AmcSt5hU4qA&list=PL4517CA6C6244A844", "description": ""},
  {"title": "10:31


    
 

Pyramid Magnet - free energy - english subtitleby MrTermsof        
        
616,081 views", "href": "http://www.youtube.com/watch?v=pMbHswNoGWM", "description": ""},
  {"title": "4:11


    
 

My all new newman motor 1.(TheDaftman)by theDaftman        
        
1,147,470 views", "href": "http://www.youtube.com/watch?v=dL4B_DNBtvc", "description": ""},
  {"title": "2:18


    
 

Is there free energy in magnets?by aetherix01        
        
371,642 views", "href": "http://www.youtube.com/watch?v=vrn5B9a8aOk", "description": ""},
  {"title": "3:00


    
 

The Most Dangerous Video On The Internet  - Trevor Paglenby killuminati63        
        
585,755 views", "href": "http://www.youtube.com/watch?v=9xEuhEHDJM8", "description": ""},
  {"title": "2:18


    
 

Free Energy - Magnet Motorby ATBootstrap        
        
358,641 views", "href": "http://www.youtube.com/watch?v=hfkwCE3BeBs", "description": ""},
  {"title": "2:38


    
 

100% free energy generator is easy to buildby LifeHack2012        
        
238,092 views", "href": "http://www.youtube.com/watch?v=GEUyhhMEs7U", "description": ""},
  {"title": "3:41


    
 

5KW free energy –±–µ—Å—Ç–æ–ø–ª–∏–≤–Ω—ã–π –≥–µ–Ω–µ—Ä–∞—Ç–æ—Ä Kapanadze –ö–∞–ø–∞–Ω–∞–¥–∑–µby Alexander Frolov        
        
488,213 views", "href": "http://www.youtube.com/watch?v=uxQ99R4gOWY", "description": ""},""".split('\n')
sources = ' '.join([te for te in text if te])
while True:
    if '  ' in sources:
        sources = sources.replace('  ',' ').replace('\t',' ')
    else:
        break
sources = sources.replace('}, {','},{').replace('},{','},\n{')
input(sources)


