from django.shortcuts import render
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki_entry(request, title):
        markdowner = Markdown()
        if util.get_entry(title):
            return render(request, "encyclopedia/wiki.html", {
            "content": markdowner.convert(util.get_entry(title)),
            "title": title.upper()
            })
        else:
            return render(request, "encyclopedia/error.html")
    


