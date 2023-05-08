from django.shortcuts import render, redirect
from django import forms
import markdown2
import random
from . import util
import markdown2




# Form Class
class NewForm(forms.Form):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "input", "placeholder": "Title"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Page Body"}), required=True)


# Function to check all possible string combos in order to get correct entry
def string_combo(name):
    # Check all possible string combinations
    name = name.lower()
    page_entry = util.get_entry(name)

    if not page_entry:
        name = name.upper()
        page_entry = util.get_entry(name)

    if not page_entry:
        name = name.capitalize()
        page_entry = util.get_entry(name)

    return name


# Index route
def index(request):
    # if request is post then user is searching, we need to check if page exists
    if request.method == "POST":
        data = request.POST
        q = data.get("q")

        # Check all possible string combinations
        q = string_combo(q)

        # If exists then we redirect to the page
        if util.get_entry(q):
            return redirect(page, q)

        # Otherwise we redirect to search route
        else:
            return redirect(search, q)

    # If user uses GET then display page
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


# Add page route to show a requested page with called <name>
def page(request, name):
    # Check all possible string combinations
    name = string_combo(name)
    page_entry = util.get_entry(name)

    if not page_entry:
        return render(request, "encyclopedia/apology.html")

    else:
        content = markdown2.markdown(page_entry)
        return render(request, "encyclopedia/page.html", {
            'entry': name,
            'content': content
        })

# Search route for a requested <search> that is not exactly a page that exists
def search(request, s):
    # Search current pages that are similar to the search prompt
    entries = util.list_entries()
    matches = []
    for entry in entries:
        if s.lower() in entry.lower():
            matches.append(entry)

    return render(request, "encyclopedia/search.html", {
        'matches': matches
    })


# New Page route
def new(request):
    # Display page creation if user is acessing
    if request.method == 'GET':
        return render(request, "encyclopedia/new.html", {
            'form': NewForm()
        })

    # Submit form and check if page exists
    else:
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            title = title.capitalize()
            content = form.cleaned_data["content"]
            page_entry = util.get_entry(title)
            if page_entry:
                return render(request, "encyclopedia/page_exists.html", {
                })
            else:
                util.save_entry(title, content)
                return redirect(page, title)


# Edit page route
def edit(request, name):
    # Display page edit
    if request.method == 'GET':
        page_entry = util.get_entry(name)
        return render(request, "encyclopedia/edit.html", {
            'entry': name.capitalize(),
            'form': NewForm(initial={'title':name, 'content':page_entry})
        })

    # If user submits a change then update
    else:
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect(page, title)


# Def Random Page
def random_page(request):
    entries = util.list_entries()
    rand = random.choice(entries)
    return redirect(page, rand)
