from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown
from os import path
import random

from . import util

# A class for Search Page
class NewSearchForm(forms.Form):
    search = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'search', 'name':'q', 'placeholder':'Search Encyclopedia', "autocomplete":"off"}))

# Shows the main page with links
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

# /wiki/title should renders the contents of that encyclopedia entry
def wiki_entry(request, title):
        markdowner = Markdown()
        if util.get_entry(title):
            return render(request, "encyclopedia/wiki_entry.html", {
                "content": markdowner.convert(util.get_entry(title)),
                "title": title,
                "form": NewSearchForm()
            })
        else:
            return render(request, "encyclopedia/noentry.html", {
                "form": NewSearchForm()
            })

# Adds a search functionality
def search(request):
    if request.method == "POST":
        # Get the form data from post
        form = NewSearchForm(request.POST)

        # Validate the form automatically
        if form.is_valid():

            # Save the data of input field into a variable search
            search = form.cleaned_data["search"]

            # If the data inside input field mathces any encyclopedia entry, redirect to that entry's page
            if util.get_entry(search):
                return HttpResponseRedirect(reverse("wiki_entry", args=[search]))

            substrings = []
            # If the query field does not match, find all substrings with that query and display them
            for sub in util.list_entries():
                if search.lower() in sub.lower():
                    substrings.append(sub)

            # Display the index page with search results
            return render(request, "encyclopedia/index.html", {
                "entries": substrings,
                "form": NewSearchForm()
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "form": form
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

# Creates a new page
def new_page(request):
    if request.method == "POST":

        # Get the form data
        form = request.POST

        # Validate the form manually
        if not form["text-title"]:
            return render(request, "encyclopedia/new_page.html", {
                "no_title": "N",
                "form": NewSearchForm(),
                "invalidTitle": "is-invalid"
            })
        if not form["text-content"]:
            return render(request, "encyclopedia/new_page.html", {
                "no_content": "T",
                "form": NewSearchForm(),
                "invalidContent": "is-invalid"
            })

        # If the title already exists the error message appears and the same form is seen
        if form["text-title"] in util.list_entries():
            return render(request, "encyclopedia/new_page.html", {
                "title_exists": "E",
                "title": form["text-title"],
                "content": form["text-content"],
                "invalidTitle": "is-invalid",
                "form": NewSearchForm()
            })
        
        # Saves the entry with h1 title
        textContent = "# " + form["text-title"] + "\n" + form["text-content"]
        util.save_entry(form["text-title"], textContent)

        return HttpResponseRedirect(reverse("wiki_entry", args=[form["text-title"]]))

    return render(request, "encyclopedia/new_page.html", {
        "form": NewSearchForm()
    })

# Edits the created page
def edit_page(request, title):
    if request.method == "POST":
        
        # Get the form data
        form = request.POST

        # Validate the form manually
        if not form["text-title"]:
            return render(request, "encyclopedia/new_page.html", {
                "no_title": "N",
                "content": form["text-content"],
                "form": NewSearchForm(),
                "invalidTitle": "is-invalid"
            })
        if not form["text-content"]:
            return render(request, "encyclopedia/new_page.html", {
                "no_content": "T",
                "title": form["text-title"],
                "form": NewSearchForm(),
                "invalidContent": "is-invalid"
            })

        # Replaces the entry
        util.save_entry(form["text-title"], form["text-content"])

        return HttpResponseRedirect(reverse("wiki_entry", args=[form["text-title"]]))

    return render(request, "encyclopedia/edit_page.html",{
        "title": title,
        "content": util.get_entry(title),
        "form": NewSearchForm()
    })

# Goes to a random page
def random_page(request):
    random_value = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("wiki_entry", args=[random_value]))
