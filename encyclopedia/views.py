from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown

from . import util

class NewSearchForm(forms.Form):
    search = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'search', 'name':'q', 'placeholder':'Search Encyclopedia'}))

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
                "title": title.upper(),
                "form": NewSearchForm()
            })
        else:
            return render(request, "encyclopedia/noentry.html", {
                "form": NewSearchForm()
            })

def search(request):
    if request.method == "POST":
        # Get the form data from post
        form = NewSearchForm(request.POST)

        # Validate the form
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


