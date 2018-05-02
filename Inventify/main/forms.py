from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Field

class ReviewForm(forms.Form):
    #name = forms.FieldType(label = 'label that will appear in front of field')
    title = forms.CharField(label = 'Title')   
    rating = forms.IntegerField(label = 'Rating')
    content = forms.CharField(label = 'Review body', widget=forms.widgets.Textarea())
    
    #hidden fields populated when page is loaded
    listing = forms.IntegerField(widget=forms.HiddenInput())
    author = forms.IntegerField(widget=forms.HiddenInput())
    
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('review_submit', 'Submit Review', css_class="btn-success"))

class addListForm(forms.Form):
    title = forms.CharField(label = "Title")
    helper = FormHelper()
    helper.add_input(Submit("add_list", "Add", css_class="btn-success"))
    helper.form_show_labels = False;
    helper.form_method = "POST"

class addElementForm(forms.Form):
    listingId = forms.IntegerField(widget=forms.HiddenInput())
    myListsId = forms.IntegerField(widget=forms.HiddenInput())

    #user = forms.IntegerField(widget=forms.HiddenInput())

    helper = FormHelper()
    helper.form_method = "POST"
    helper.add_input(Submit("add_element", "Add to List", css_class="btn-success"))
    
class EmailForm(forms.Form):
    from_email = forms.EmailField(required=True) #add username 
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('Send', ' Send', css_class="btn-success"))

    

#class filter(forms.Form):
    #Listingtype = bubble clicks. (V(enue) or S(ervice))
    #Location = dropdownMenu (strings)
    #Ratings = from to fields  (double)
    #Capacity = from to fields  (int)
    #Features = buttonClicks each type (boolean)
    #Hours = buttonClicks (boolean) & specifics (int & booleans)
    #button = Search. 

class filterBar(forms.Form):
    searchbar = forms.CharField(
        label = 'Search ',
        required = False,
        )
          
    listingType = forms.MultipleChoiceField(
        label='Type: ',
        choices =(
            ('V', 'Venue'), 
            ('S', 'Services')),                
        #initial = ''
        widget = forms.CheckboxSelectMultiple,
        required = False,
        )
   

    
    # location = forms.ChoiceField(
    #     label = 'Location',
    #     choices = (
    #         ('East_Mem', 'East Memphis'),
    #         ('West_Mem', 'West Memphis'), 
    #         ('Midtn', 'Midtown'),
    #         ('Nash', 'Nashville') 
    #         ),            
    #     widget = forms.RadioSelect, #make button unclickable too.
    #     required = False,
    #     )

    ratings = forms.ChoiceField(
        label = 'Average Rating: ',
        choices = (
            ('1', '1+' ),
            ('2', '2+'),
            ('3', '3+'),
            ('4', '4+')
            ),
        widget = forms.RadioSelect, #make button unclickable too.
        required = False,
        )

    features = forms.MultipleChoiceField(
        label = 'Amenities: ',
        choices = (
            ('CA', 'Catering available'), 
            ('OF', 'No outside food or beverages'),
            ('AA', 'Animals allowed'), 
            ('21', 'Age 21+'), 
            ('18', 'Age 18+'), 
            ('FF', 'Family-friendly'), 
            ('AP', 'Alcohol permitted'), 
            ('SP', 'Smoking permitted'), 
            ('VF', 'Vegan food available'), 
            ('VE', 'Vegetarian food available'), 
            ('SE', 'Sound equipment provided'), 
            ('OD', 'Outdoors'), 
            ('ID', 'Indoors'), 
            ('IO', 'Indoors and outdoors')
            ),
        widget = forms.CheckboxSelectMultiple,
        required = False,
        )
    

    helper = FormHelper()
    
    helper.form_class = 'form-horizontal' #horizontal or vertical
    
    helper.form_method = "POST"
    helper.add_input(Submit("Search", "Search", css_class="btn-success"))
