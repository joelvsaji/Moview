from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import*
from .forms import*
from django.db.models import Avg
# Create your views here.

# def home(request):
#     query=request.GET.get("title")
#     a=None
#     if query:
#         a=Movie.objects.filter(name__icontains=query)
#     else:
#         a=Movie.objects.all()
    
#     return render(request, 'index.html',{"a":a})

def home(request):
    query = request.GET.get("title")
    movies = None
    
    if query:
        movies = Movie.objects.filter(name__icontains=query)
    else:
        movies = Movie.objects.all()
    
    # Annotate each movie with its average rating
    movies_with_avg = movies.annotate(
        avg_rating=Avg('review__rating')
    ).order_by('name')
    
    # Round the average ratings
    for movie in movies_with_avg:
        movie.avg_rating = round(movie.avg_rating or 0, 2)
    
    return render(request, 'index.html', {"a": movies_with_avg})

def details(request,id):
    b=Movie.objects.get(id=id)
    review=Review.objects.filter(movie=id).order_by("-comment")

    average = review.aggregate(Avg("rating"))["rating__avg"]
    if average == None:
        average = 0
    average= round(average, 2)
    return render(request, 'details.html',{"b":b,"review":review,"average":average})

def add_movies(request):  
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method=="POST":
                form=MovieForm(request.POST or None)
                if form.is_valid():
                    data=form.save(commit=False)
                    data.save()
                    return redirect("moviewapp:home")
            else:
                form=MovieForm()
            return render(request,'addmovies.html',{"form":form, "controller":"Add Movies"})
        # if they are not admin
        else:
            return redirect("moviewapp:home")
    # if they are not loggin    
    return redirect("accounts:login")

def edit_movies(request,id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            movie=Movie.objects.get(id=id)
            if request.method=="POST":
                form=MovieForm(request.POST or None,instance=movie)
                if form.is_valid():
                    data=form.save(commit=False)
                    data.save()
                    return redirect("moviewapp:details",id)
            else:
                form=MovieForm(instance=movie)
            return render(request,'addmovies.html',{"form":form, "controller":"Edit Movies"})
        # if they are not admin
        else:
            return redirect("moviewapp:home")
    # if they are not loggin    
    return redirect("accounts:login")

def delete_movies(request,id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            movie=Movie.objects.get(id=id)
            movie.delete()
            return redirect('moviewapp:home')
        # if they are not admin
        else:
            return redirect("moviewapp:home")
    # if they are not loggin    
    return redirect("accounts:login")

def add_review(request,id):
    if request.user.is_authenticated:
        movie=Movie.objects.get(id=id)
        if request.method=="POST":
            form=ReviewForm(request.POST or None)
            if form.is_valid():
                data=form.save(commit=False)
                data.comment=request.POST["comment"]
                data.rating=request.POST["rating"]
                data.user=request.user
                data.movie=movie
                data.save()
                return redirect("moviewapp:details",id)
        else:
            form=ReviewForm()
        return render(request,"details.html",{"form":form})
    else:
        return redirect("accounts:login")
    

def edit_review(request,movie_id,review_id):
    if request.user.is_authenticated:
        movie=Movie.objects.get(id=movie_id)
        review=Review.objects.get(movie=movie,id=review_id)
        if request.user==review.user:
            if request.method=="POST":
                form=ReviewForm(request.POST,instance=review)
                if form.is_valid():
                    data=form.save(commit=False)
                    if (data.rating>10) or (data.rating<0):
                        error="Out of range. Please select rating from 0 to 10."
                        return render(request,'editreview.html',{"error":error,"form":form})
                    else:
                        data.save()
                        return redirect("moviewapp:details",movie_id)
            else:
                form=ReviewForm(instance=review)
            return render(request,"editreview.html",{"form":form})
        else:
            return redirect("moviewapp:details",movie_id)
    else:
        return redirect("accounts:login")
    

def delete_review(request,movie_id,review_id):
    if request.user.is_authenticated:
        movie=Movie.objects.get(id=movie_id)
        review=Review.objects.get(movie=movie,id=review_id)
        if request.user==review.user:
            review.delete()
        return redirect("moviewapp:details",movie_id)
    else:
        return redirect("accounts:login")