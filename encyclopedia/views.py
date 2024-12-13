from django.shortcuts import render, redirect
from . import util
from django import forms
import random
from wiki import settings
import os


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "found": True, 
    })


def page(request, name):
    if name.isspace():
        return index(request)
    name = util.cut_spaces(name)     # get rid of the spaces at the end
    entry = util.get_entry(name)     # get the file name 
    if entry is None:                # if the file not found, make the list of all entries that contain the name as a substring and return
        all_entries = util.list_entries()          
        returned_list = [element for element in all_entries if name.lower() in element.lower()]
        if returned_list:
            return render(request, "encyclopedia/index.html", {
                "title": name,
                "entries": returned_list,
                "found": False,
            })
        return render(request, 'encyclopedia/error.html', {      # if returned list is emptry, return the error page 
            'title': name
        })
    return render(request, 'encyclopedia/page.html', {    # if the file name was found, return the direct path to the file page 
        'title': name,
        'entry': util.get_html(entry),
        'text': entry,
    })


def search(request):
    if request.method == 'POST':
        query = request.POST.get('xui')
    if query == '':
        return index(request)
    return page(request, query)


def random_entry(request):
    all_entries = util.list_entries()
    random_entry = random.choice(all_entries)
    return redirect('page', name=random_entry)


class NewPageForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)
    edit = forms.BooleanField(required=False, initial=False)


def new(request, POST=True, unfilled=False): 
    if request.method == 'POST' and POST:
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            edit = True
        return render(request, 'encyclopedia/new.html', {
            'title': title,
            'text': text,
            'edit': edit,
        })
    if not unfilled:
        return render(request, 'encyclopedia/new.html', {
            'edit': False
        })
    else:
        return render(request, 'encyclopedia/new.html', {
            'edit': False,
            'unfilled': True
        })


def create_page(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            edit = form.cleaned_data['edit']
            if util.get_entry(title) != None and (not edit):       # if the file already exists and it is not being edited, return error page                        
                return render(request, 'encyclopedia/creating_error.html', {'title': title.capitalize()})
            entries_directory = os.path.join(settings.BASE_DIR, 'entries')
            file_path = os.path.join(entries_directory, f'{title}.md')
            with open(file_path, 'w') as file:
                file.write(text)
            return redirect(page, name=title)
        else:
            return new(request, False, True)
        
