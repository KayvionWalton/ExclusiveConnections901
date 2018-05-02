from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
from django.db.models import Q
from main.forms import *
from main.models import *
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect


# Create your views here.


def get_username(current_user): #if we end up needing another piece of info for every page, add it to context up here
    context = {}
    #check if user is logged in, add username to context
    if current_user.is_authenticated:
        context['username'] = current_user.username
    else:
        context['username'] = 'Guest'
    return context

def home(request): 
    current_user = request.user
    context = get_username(current_user)
    
    listings_list = Listing.objects.all()
    listing_attributes = ListingAttribute.objects.all()    
    
    #Filter Bar Form.
    if request.method == "POST":
        filter_form = filterBar(request.POST)
        if filter_form.is_valid():
            #Search Bar
            searchbar = filter_form.cleaned_data['searchbar']
            if not searchbar:
                filter_name = Listing.objects.all()
            context['searchbar'] = searchbar
            filter_name = Listing.objects.filter(name__icontains = searchbar)
            
            #TYPE
            listingType = filter_form.cleaned_data['listingType']
            if not listingType:
                filter_type = filter_name
            else:
                listingType = str(listingType)
                listingType = listingType.strip('[\']')
                filter_type = filter_name.filter(listing_type = listingType)
                context['listingType'] = listingType #for testing        

             #RATINGS
            ratings = filter_form.cleaned_data['ratings']
            if not ratings:
                ratings = 0
            ratings = int(ratings)    
            context['ratings'] = ratings #for testing            
            filter_ratings = filter_type.filter(average_rating__gte = ratings)

           ##FEATURES
            features = filter_form.cleaned_data['features']
            #filter_features = filter_ratings
            if not features:
                filter_features = filter_ratings            
            context['features'] = features
            if len(features) >= 1:
                filter_features = filter_ratings.filter(listingattribute__type='null')
                for feature in features:
                    feature = str(feature)
                    feature = feature.strip('[\']')
                    filter_features = filter_ratings.filter(listingattribute__type = feature) | filter_features            
            #pass the filtered results to paginator.           
            listings_list=filter_features.order_by('id').distinct()      #only distinct elements (bc of features.)   
            listingsfound = len(listings_list)
            context['search_results'] = listingsfound
            context['filter_form'] = filter_form #Put at end of filterBar form
    else:
        filter_form = filterBar()
        context['filter_form'] = filter_form

    #fix paginator.
    paginator = Paginator(listings_list, 6) #https://docs.djangoproject.com/en/1.11/topics/pagination/
    
    page = request.GET.get('page')
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)
    context['listings'] = listings
    context ['attributes'] = listing_attributes

    return render(request, 'main/home.html', context)

    
def listing_page(request):
    current_user = request.user
    context = get_username(current_user)
    

    listing = request.GET.get('listing') #pulls listing ID from POST
    listing = Listing.objects.get(id = listing) #fetches from DB
    
    context['listing_attributes'] = ListingAttribute.objects.filter(listing=listing)    

    
    #gets the listing id and adds it to the list.

    if current_user.is_authenticated:
        getLists = UserList.objects.filter(owner = current_user.id)
        context['getLists'] = getLists
        addElementForm
        context['current_user'] = current_user


    
    #    add_to = ListElements(listing = listing, parent_list = 1 )
    #    add_to.save()
    current_reviews = Review.objects.filter(listing = listing) #gathers all its reviews
    if current_user.is_authenticated:
        reviewed = current_reviews.filter(author = current_user) #fetches review (if exists) of current user
    else:
        reviewed = False
    if not reviewed:    
        if request.method == 'POST':
            #get all the data and insert
            form = ReviewForm(request.POST)
            if form.is_valid():
                #pull data from form
                temp_title = form.cleaned_data['title']
                temp_content = form.cleaned_data['content']
                temp_rating = form.cleaned_data['rating']
                temp_listing = form.cleaned_data['listing']
                temp_listing = Listing.objects.get(id = temp_listing)
                temp_author = form.cleaned_data['author']
                temp_author = User.objects.get(id = temp_author)            

                                #create new Review row
                new_review = Review(title=temp_title, content=temp_content, rating=temp_rating, listing=temp_listing, author=temp_author)
                new_review.save()
                    
                #update average review score for listing
                current_reviews = Review.objects.filter(listing = listing)
                total = 0
                for item in current_reviews:
                    total += item.rating
                average_score = total/len(current_reviews)
                listing.average_rating = average_score
                listing.save()
                form = ReviewForm(initial = {'author':current_user.id, 'listing': listing.id}) #prepopulates hidden fields of review form w/ user and listing data
                context['form'] = form
                
        else:
            form = ReviewForm(initial = {'author':current_user.id, 'listing': listing.id}) #prepopulates hidden fields of review form w/ user and listing data
            context['form'] = form
    else:
        if request.method == 'POST':
            #get all the data and insert
            form = ReviewForm(request.POST)
            if form.is_valid():
                #pull data from form
                temp_title = form.cleaned_data['title']
                temp_content = form.cleaned_data['content']
                temp_rating = form.cleaned_data['rating']
                #temp_listing = form.cleaned_data['listing']
                #temp_listing = Listing.objects.get(id = temp_listing)
                #temp_author = form.cleaned_data['author']
                #temp_author = User.objects.get(id = temp_author)            

              
                current_reviews.filter(author=current_user).update(title=temp_title, content=temp_content, rating=temp_rating)
                context['form'] = form

                #update average review score for listing
                current_reviews = Review.objects.filter(listing = listing)
                total = 0
                for item in current_reviews:
                    total += item.rating
                average_score = total/len(current_reviews)
                listing.average_rating = average_score
                listing.save()
                form = ReviewForm(initial = {'author':current_user.id, 'listing': listing.id}) #prepopulates hidden fields of review form w/ user and listing data
                context['form'] = form
        else:
            reviewed = current_reviews.get(author = current_user)
            form = ReviewForm(initial = {'author':current_user.id, 'listing': listing.id, 'title': reviewed.title, 'content': reviewed.content, 'rating': reviewed.rating}) #prepopulates hidden fields of review form w/ user and listing data
            context['form'] = form
        
                
    current_reviews = Review.objects.filter(listing = listing) #gathers all its reviews
    if current_user.is_authenticated:
        reviewed = current_reviews.filter(author = current_user) #fetches review (if exists) of current user
        if reviewed:
            context['user_reviewed'] = True
            reviewed = current_reviews.get(author = current_user) 
            context['curr_user_review'] = reviewed
        else:
            context['user_reviewed'] = False
    else:
        context['user_reviewed'] = False
    
    context['reviews'] = current_reviews
    context['listing'] = listing
    context['name'] = listing.name
    context['address'] = listing.address
    context['capacity'] = listing.capacity
    context['description']=listing.description
    if listing.phone_number:
        phone_num = listing.phone_number
        phone_num = '-'.join((phone_num[:3],phone_num[3:6],phone_num[6:]))
        context['phone_num'] = phone_num
  

    return render(request, 'main/venuePage.html', context)
    
def sign_up(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() #saving form creates User object in db
            return render(request, 'main/sign_up_success.html')
        else:
            return redirect('home')
    else:
        form = UserCreationForm() #built-in django.contrib.auth form; need to make crispy form to take additional data beyond username and pw
        context = {'form': form} #send form to front-end in dictionary
        return render(request, 'main/sign_up.html', context)
        
def log_out(request):
    logout(request)
    return redirect('home')

def normalize(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    query = None # Query to search for every search term        
    terms = normalize(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['title', 'body',])
        found_entries = Entry.objects.filter(entry_query).order_by('-pub_date')
    return render_to_response('search/search_results.html', {'query_string': query_string, 'found_entries':found_entries}, context_instance=RequestContext(request))


def user_page(request):
    current_user = request.user
    context = get_username(current_user)
    context['userId'] = current_user.id   

    #myList = UserList.objects.all() #delete.
    context["allLists"] = UserList.objects.all()  #To display all of the current lists from everyone
    userId = current_user.id
    myLists = UserList.objects.filter(owner = userId)
    context["myLists"] = myLists    #displays all the lists for the current user.
    

    elements = ListElements.objects.all()
    context["elements"] = elements
    p_list = Listing.objects.all()
    context['list_elements'] = p_list




    #listings = Listing.objects.filter(id = elements.parent_list) #doesn't work...
    #context["listings"] = listings

    #filter(parent_list = list_id)
    #list_id = UserList.objects.get(id = myLists.id )

    if request.method == "POST":
        list_form = addListForm(request.POST)
        if list_form.is_valid():
                    #pull data from form
            title = list_form.cleaned_data['title']

            new_list = UserList(owner=current_user, title=title)
            new_list.save()
            list_form = addListForm()
            context['list_form'] = list_form
    else:
        list_form = addListForm()
        context['list_form'] = list_form
#is probably right, gives error either way, but adds it to the db?? -SE
        
    return render(request, 'main/userPage.html', context)

def confirmationPage(request):
    current_user = request.user
    context = get_username(current_user)

    listing = request.GET.get('listing') #pulls listing ID from POST
    listing = Listing.objects.get(id = listing) #fetches from DB
    context["listing"] = listing

    #list id from the url that i make on the html. 
    list_id = request.GET.get('list_id') #pulls listing ID from POST
    list_id = UserList.objects.get(id = list_id) #fetches from DB
    
    if ListElements.objects.filter(parent_list =list_id, listing = listing).exists():
        context['error'] = 'That listing is already part of that list.'
        return render(request, 'main/error_page.html', context)
    else:
        new_element = ListElements(listing=listing , parent_list=list_id)
        new_element.save()
        return render(request, 'main/confirmationPage.html', context)

# def filterBar(request):
#     listing = Listing.objects.all()
#     context['listing'] = listing
#     attributes = ListingAttribute.objects.all()
#     context['attributes'] = attributes
#     hours = Hours.objects.all()
#     context['hours'] = hours

#     #figure out if i need a form or not. 
#     #probably will tho.

#     return render(request, 'main/home.html', context)

def delete_list(request):
    user_list = request.GET.get('user_list')
    list_object = UserList.objects.get(id = user_list)
    if list_object.owner == request.user:
        list_object.delete()
        return redirect(user_page)
    else:
        context = get_username(current_user)
        context['error'] = "You cannot delete another user's list."

        return render(request, 'main/error_page.html', context)
        
def delete_list_item(request):
    list_item = request.GET.get('list_item')
    parent_list = request.GET.get('parent')
    list_item_object = ListElements.objects.get(id=list_item)
    parent_object = UserList.objects.get(id=parent_list)
    
    current_user = request.user
    context = get_username(current_user)
    
    if parent_object.owner == current_user:
        list_item_object.delete()
        return redirect(user_page)
    else:
        context['error'] = "You cannot delete from another user's list."
        return render(request, 'main/error_page.html', context)
    
def emailView(request):
    context = {}
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            from_email = form.cleaned_data['from_email']
            #temp_email = User.objects.get(id = temp_email)
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['message']            
            context['email_form'] = form        

            new_email = Email(email=from_email, title=subject, content=content)
            new_email.save()
            return render(request, 'main/success.html', context)

    else:
        form = EmailForm(request.POST)
        context['email_form'] = form      
          
    return render(request, "main/email.html", context)

#else:
#    form = ReviewForm(initial = {'author':current_user.id, 'listing': listing.id}) #prepopulates hidden fields of review form w/ user and listing data
#    context['form'] = form


def successView(request):
    return HttpResponse('Success! Thank you for your message.')
    
def delete_review(request):
    user_review = request.GET.get('id')
    source = request.GET.get('source')
    user_review = Review.objects.get(id = user_review)
    if user_review.author == request.user:
        user_review.delete()
        return redirect('/view_listing?listing=' + str(source))
    else:
        context = get_username(current_user)
        context['error'] = "You cannot delete another user's review."
        return render(request, 'main/error_page.html', context)