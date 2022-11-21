from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Equipement,Animal

# Create your views here.

def post_list(request):
    animaux = Animal.objects.all()
    return render(request, 'blog/post_list.html', {'animaux':animaux})

def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    if request.method == "POST":
        form = MoveForm(request.POST, instance=animal)
    else:
        form = MoveForm()

    if form.is_valid():
        ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        ancien_lieu.disponibilite = "libre"
        ancien_lieu.save()
        form.save()
        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        nouveau_lieu.disponibilite = "occupé"
        nouveau_lieu.save()
        animal.save()
        return redirect('animal_detail', id_animal=id_animal)
    return render(request,
                'blog/animal_detail.html',
                {'animal': animal, 'lieu': animal.lieu, 'form': form})
