from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
import markdown2
from . import util

def index(request):
    """ Displays the list of all encyclopedia entries. """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    """ Retrieves and displays a specific encyclopedia entry.
        Converts Markdown to HTML before rendering.
    """
    content = util.get_entry(title)
    if content:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(content)
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })

def search(request):
    """ Handles search queries and displays relevant results.
        If an exact match exists, redirects to that entry.
    """
    query = request.GET.get("q", "").lower()
    entries = util.list_entries()
    results = [entry for entry in entries if query in entry.lower()]

    if query in map(str.lower, entries):
        return redirect(f"/wiki/{query}")

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })

def new_page(request):
    """ Allows users to create a new encyclopedia entry.
        Prevents duplicates and saves valid entries.
    """
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("content").strip()

        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "message": "This page already exists."
            })

        util.save_entry(title, content)
        return redirect(f"/wiki/{title}")

    return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    """ Enables users to edit existing entries. """
    content = util.get_entry(title)

    if request.method == "POST":
        new_content = request.POST.get("content").strip()
        util.save_entry(title, new_content)
        return redirect(f"/wiki/{title}")

    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    """ Redirects users to a randomly chosen entry. """
    entries = util.list_entries()
    if entries:
        random_title = random.choice(entries)
        return redirect(f"/wiki/{random_title}")
    return render(request, "encyclopedia/error.html", {
        "message": "No entries available!"
    })
