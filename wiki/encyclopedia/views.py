from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django import forms

import markdown2
import random
from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Enter Your Page Title:")
    content = forms.CharField(label="Enter Your Content (Markdown format):", widget=forms.Textarea,)

class EditForm(forms.Form):
    content = forms.CharField(label="Edit Your Content (Markdown format):", widget=forms.Textarea,)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def edit(request):
    # retrieve the entry 
    entry = request.POST.get('editpage')
    loaded = util.get_entry(entry)

    # error message if no entry can be found
    if (loaded == None):
        return HttpResponse("This entry does not exist!")
    
    # load the edit page, prepopulated with edit data
    else:
        prepop = {'content': loaded}
        form = EditForm(prepop)

        return render(request, "encyclopedia/edit.html", {
            "entry": entry,
            "form": form
        })


def edited(request):
        # create a form instance and populate it with data from the request:
        form = EditForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # access the form data
            title = request.POST.get('title')
            content = form.cleaned_data['content']
        
            # need to save content and title to an md file with title as file name.
            util.save_entry(title, content)
            address = "wiki/"+ title
            return redirect(address)
        
        return redirect('/')



def load_entry(request, entry):
    # retrieve the entry entered into the URL (if it exists)
    loaded = util.get_entry(entry)

    # error message if no entry can be found
    if (loaded == None):
        return HttpResponse("This entry does not exist!")
    
    # load the entry page by converting the marked down file into a HTML page
    else:
        
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "loaded": markdown2.markdown(loaded)
        })


def newpage(request):
    if request.method == 'GET':
        form = NewPageForm()
        return render(request, "encyclopedia/newpage.html", {
            "form": form
        })
    else:
        # create a form instance and populate it with data from the request:
        form = NewPageForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # access the form data
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            #check title is not already being used
            if title in util.list_entries():
                return HttpResponse("This Title is already taken! Please select another name for your Title")
        
            else:
                # need to save content and title to an md file with title as file name.
                util.save_entry(title, content)
                address = "wiki/"+ title
                return redirect(address)
        
        return redirect('/')


def random_page(request):
    
    random_entry = random.choice(util.list_entries())
    address = "wiki/"+ random_entry
    return redirect(address)



def results(request):

    #retrieve search query from submitted form
    query = request.POST.get('q')

    #retrieve list of all encyclopedia entries
    full_list = util.list_entries()

    #check if query exactly matches an entry and load that page
    if query in full_list:
        loaded = util.get_entry(query)
        return render(request, "encyclopedia/entry.html", {
            "entry": query,
            "loaded": markdown2.markdown(loaded)
        })
    
    #find entries that contain query string and return those as search results
    else:
        results=[]
        for entry in full_list:
            if query in entry:
                results.append(entry)
        
        return render(request, "encyclopedia/results.html", {
        "results": results
    })