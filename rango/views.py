from django.shortcuts import render
from rango.forms import CategoryForm
from rango.models import Category
from rango.models import Page
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse


def index(request):
    # build dictionairy to pass to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    # return a rendered response to send to client using a shortcut
    # request parameter is the template
    return render(request, 'rango/index.html', context=context_dict)
    # return HttpResponse("Rango says hey there partner! <a href='/rango/about/'>About</a>")


def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Zander'}
    return render(request, 'rango/about.html', context=context_dict)
    # return HttpResponse('Rango says here is the about page. <a href="/rango/">Index</a>')


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        # see if the category slug exists to work on, .get raises doesnotexist exp
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages

        context_dict['category'] = category
    except Category.DoesNotExist:
        # if no slug in category
        # do nothing
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/range/')
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug': category_name_slug}))
            else:
                print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
