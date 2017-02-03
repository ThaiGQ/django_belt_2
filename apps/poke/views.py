from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count
from .models import User, Poke

# Create your views here.
def index(request):
    user = User.objects.get(id = request.session["logged_in_user"])
    all_users = User.objects.exclude(id = user.id)
    poked = Poke.objects.filter(being_poked = user).values("person_poking").annotate(num_poked = Count("being_poked")).order_by("-num_poked")
    print poked
    all_pokes = Poke.objects.values("being_poked").annotate(all_poked = Count("being_poked"))
    # print all_pokes
    people_poking = Poke.objects.filter(being_poked = user).order_by("person_poking_id")
    poking_id = set()
    unique_pokers = []
    for person in people_poking:
        if person.person_poking_id not in poking_id:
            unique_pokers.append(person)
            poking_id.add(person.person_poking_id)
    people_poking = len(unique_pokers)
    # print people_poking
    context = {
        "user": user,
        "all_users": all_users,
        "poked": poked,
        "all_pokes": all_pokes,
        "people_poking": people_poking
        }
    return render(request, "poke/index.html", context)

def poke(request, pokee_id):
    poker = User.objects.get(id = request.session["logged_in_user"])
    pokee = User.objects.get(id = pokee_id)
    print poker.first_name
    print pokee.first_name
    poked = Poke.objects.create(person_poking = poker, being_poked = pokee)
    print "*"*50
    print poked.being_poked.id
    return redirect(reverse("poke:main"))
