from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo


def home(request):
    return render(request, "todo/home.html")


def signupuser(request):
    if request.method == "GET":
        return render(request, "todo/signupuser.html", {"form": UserCreationForm()})
    else:
        # Create a new user
        # password1 password2 username inspact HTML "name"
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"]
                )
                user.save()
                login(request, user)
                # user create send then to currenttodos page
                return redirect("currenttodos")

            except IntegrityError:  # ERROR when user name already been taken
                return render(
                    request,
                    "todo/signupuser.html",
                    {
                        "form": UserCreationForm(),
                        "error": "That username has already been taken. Please choose a new username",
                    },
                )

        else:
            return render(
                request,
                "todo/signupuser.html",
                {"form": UserCreationForm(), "error": "Passwords did not match"},
            )
            # Tell the user the passwords didn't match


def loginuser(request):
    if request.method == "GET":
        return render(request, "todo/loginuser.html", {"form": AuthenticationForm()})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "todo/loginuser.html",
                {
                    "form": AuthenticationForm(),
                    "error": "Username and password did not match",
                },
            )
        else:
            login(request, user)
            # user create send then to currenttodos page
            return redirect("currenttodos")


def logoutuser(request):
    if request.method == "POST":  # logout must be POST
        logout(request)
        return redirect("home")


def createtodo(request):
    if request.method == "GET":
        return render(request, "todo/createtodo.html", {"form": TodoForm()})

    else:  # when POST
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(
                commit=False
            )  # commit=False : create a new to do object and don't put it in the DB yet
            newtodo.user = request.user  # 確保新增的事件的user到與request user為同一個
            newtodo.save()  # put data to DB
            return redirect("currenttodos")  # 頁面導回currenttodos page
        except ValueError:  # title 超過長度 show error
            return render(
                request,
                "todo/createtodo.html",
                {"form": TodoForm(), "error": "Bad data passed in, Try again!"},
            )


def currenttodos(request):
    todos = Todo.objects.filter(
        user=request.user, datecompleted__isnull=True  # 如果datecompleted is null 就不show
    )  # filter 可以設定model要找的參數, model user = request user
    return render(request, "todo/currenttodos.html", {"todos": todos})


def viewtodo(request, todo_pk):  # 丟url.py設定的todo_pk到這
    # 從modle撈pk key資料需使用get_object_or_404
    # user=request.user 確保user只能更改自己的TODO 不然從URL更改ID就可以看到別人的資訊 並做update
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    # grap data form TodoForm
    if request.method == "GET":
        form = TodoForm(instance=todo)
        return render(request, "todo/viewtodo.html", {"todo": todo, "form": form})
    else:
        try:
            form = TodoForm(
                request.POST, instance=todo
            )  # 因為object已經存在 所以要根據instance=todo id 做update
            form.save()
            return redirect("currenttodos")
        except ValueError:
            return render(
                request,
                "todo/viewtodo.html",
                {"todo": todo, "form": form, "error": "Bad info"},
            )

