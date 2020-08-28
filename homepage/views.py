from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from homepage.forms import LoginForm, SignupForm, AddTicketForm
from homepage.models import MyUser, Ticket


@login_required
def index(request):
    new_tickets = Ticket.objects.filter(status="NE")
    in_progress_tickets = Ticket.objects.filter(status="IP")
    done_tickets = Ticket.objects.filter(status="DO")
    invalid_tickets = Ticket.objects.filter(status="IN")
    return render(request, "index.html", {
        "new_tickets": new_tickets,
        "in_progress_tickets": in_progress_tickets,
        "done_tickets": done_tickets,
        "invalid_tickets": invalid_tickets,
        "tickets": [new_tickets, in_progress_tickets, done_tickets, invalid_tickets],
    })


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get(
                "username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse("homepage")))

    form = LoginForm()
    return render(request, "generic_form.html", {"form": form, "title": "Login"})


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = MyUser.objects.create_user(
                username=data.get("username"),
                password=data.get("password"),
                display_name=data.get("display_name")
            )
        login(request, new_user)
        return HttpResponseRedirect(reverse("homepage"))

    form = SignupForm()
    return render(request, "generic_form.html", {"form": form, "title": "Signup"})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


@login_required
def add_ticket(request):
    if request.method == "POST":
        form = AddTicketForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_filed = request.user
            # if obj.status == 'DO':
            #     obj.user_completed = request.user
            #     obj.save()
            obj.save()
        return HttpResponseRedirect(reverse("homepage"))

    form = AddTicketForm()
    return render(request, "generic_form.html", {"form": form})


@login_required
def ticket(request, ticket_id):
    ticket = Ticket.objects.filter(id=ticket_id).first()
    return render(request, "ticket.html", {"ticket": ticket})


@ login_required
def user(request, user_id):
    tickets_assigned = Ticket.objects.filter(user_assigned=user_id)
    tickets_filed = Ticket.objects.filter(user_filed=user_id)
    tickets_completed = Ticket.objects.filter(user_completed=user_id)
    return render(request, "user.html", {
        "user_id": user_id,
        "tickets_assigned": tickets_assigned,
        "tickets_filed": tickets_filed,
        "tickets_completed": tickets_completed,
    })


def ticket_edit_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":
        form = AddTicketForm(request.POST, instance=ticket)
        form.save()
        return HttpResponseRedirect(reverse("ticket", args=[ticket.id]))

    form = AddTicketForm(instance=ticket)
    return render(request, "generic_form.html", {"form": form})


def assign_ticket(request, ticket_id):
    ticket = Ticket.objects.filter(id=ticket_id).update(
        user_assigned=request.user, status="IP")
    return HttpResponseRedirect(reverse("ticket", args=[ticket_id]))


def set_status_done(request, ticket_id):
    ticket = Ticket.objects.filter(id=ticket_id).update(
        user_assigned=None,
        user_completed=request.user,
        status="DO"
    )
    return HttpResponseRedirect(reverse("ticket", args=[ticket_id]))


def set_status_invalid(request, ticket_id):
    ticket = Ticket.objects.filter(id=ticket_id).update(
        user_assigned=None,
        user_completed=None,
        status="IN"
    )
    return HttpResponseRedirect(reverse("ticket", args=[ticket_id]))
