from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    #build dictionairy to pass to the template engine.
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    #return a rendered response to send to client using a shortcut
    #request parameter is the template
    return render(request, 'rango/index.html',context=context_dict)
    #return HttpResponse("Rango says hey there partner! <a href='/rango/about/'>About</a>")
def about(request):
    return HttpResponse('Rango says here is the about page. <a href="/rango/">Index</a>')