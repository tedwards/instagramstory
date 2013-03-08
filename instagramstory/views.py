import sys
## Include the lib dir so we can pickup nltk, instagram and their dependencies
sys.path.append("lib")

from django.shortcuts import render_to_response
from django.template import Context, RequestContext, loader
from instagram.client import InstagramAPI
import nltk
from nltk.corpus import wordnet

##Setup the instagram API client
clientID='7161200ec77b460284f7557296f7e3d2'
clientSecret='115c91e4a5ae43dba6dfc5d3c05e7b76'
api = InstagramAPI(client_id=clientID, client_secret=clientSecret)


def index(request):
    '''Return the main index page
    Output:
      story := a text string
    '''
    c = {}
    return render_to_response('index.html', c,
                              context_instance=RequestContext(request))


def chooseImages(request):
    '''Parse the story input for nouns and retrieve images from instagram.
    Display the images for selection by the user.
    Filtering for nouns should result in pictures relevant to the objects described
    in the users story.
    Input:
      story := a text string
    Output:
      story := a text string
      images := a dictionary with a list  of image urls as entries indexed by subject
    '''
    c={}
    c['story']=request.POST['story']
    c['images']={}
    ## Make a list of word tokens
    words = nltk.word_tokenize(c['story'])
    ## Tag each word with their grammar type
    tagged_words=nltk.pos_tag(words)
    ## Filter out anything that is not tagged as a noun
    nounCandidates = [ w for w,t in tagged_words if t=='NN' ]
    nouns=[]
    ## Since we are using a context free grammar, double check to make sure
    ## the main entry in wordnet for the word is a noun
    for aWord in nounCandidates:
        ## Check wordnet for the word as a noun
        synset=wordnet.synsets(aWord, pos='n')
        if len(synset):
            if synset[0].name.startswith(aWord) and not aWord in nouns:
                ## IFF we find the word in wordnet
                ## add the word once to list of nouns
                nouns.append(aWord)
    ## Find instagram images tagged for each noun
    ## We really ought to check for len(nouns)==0 and return an error
    for aWord in nouns:
        c['images'][aWord]=[]
        ## Search for images tagged as 'aWord' and hope you get something
        ## besides people taking pictures of themselves with their own phone
        media=api.tag_recent_media(tag_name=aWord)
        for aPic in media[0]:
            ## append each image to the images dictionary under the subject key
            c['images'][aWord].append(aPic.images['standard_resolution'].url)
            
    return render_to_response('chooseImages.html',c,
                              context_instance=RequestContext(request))

def viewResults(request):
    ''' Display the users story and selected images together
    Input:
        story := a text string
        subjectName** arguments containing an image url selected by the user
                      argument names are relative to the subject nouns in the story
    Output:
        story := a text string
        images: = 
    '''
    c={}
    c['images']={}
    for selectImage in request.POST.keys():
        if not selectImage in ('csrfmiddlewaretoken', 'story'):
            ## add any argument that was not the story or the csrf token
            ## as a selected image
            c['images'][selectImage]=request.POST[selectImage]
    c['story']=request.POST['story']
    return render_to_response('viewResults.html', c,
                              context_instance=RequestContext(request))
