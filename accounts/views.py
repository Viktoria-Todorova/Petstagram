from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.forms import AppUserCreateForm, ProfileForm
from accounts.models import Profile
from pets.mixin import CheckUserIsOwner

UserModel = get_user_model()
# Create your views here.
def register(request: HttpRequest) -> HttpResponse:
    return render(request, 'accounts/register-page.html')
class RegisterAppUserView(CreateView):
    model = UserModel
    form_class = AppUserCreateForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('common:home')
def login(request: HttpRequest) -> HttpResponse:
    return render(request, 'accounts/login-page.html')

# def profile_details(request: HttpRequest,pk:int) -> HttpResponse:
#     return render(request, 'accounts/profile-details-page.html')

class ProfileDetailsView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'accounts/profile-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_likes"] = self.object.user.photo_set.annotate(
            num_likes=Count('like')
        ).aggregate(total_likes=Sum('num_likes')).get('total_likes') or 0

        context['total_pets'] = self.object.user.pet_set.count()
        context['total_photos']= self.object.user.photo_set.count()
        return context

# def profile_edit(request: HttpRequest,pk:int) -> HttpResponse:
#     return render(request, 'accounts/profile-edit-page.html')


from django.shortcuts import get_object_or_404

# form. We want the form to contain the first name, last name, date of birth and profile picture:
# Then, we will implement the profile edit view that will inherit from the UpdateView class:
# Next, we will refactor the code in the profile-edit-page.html template to implement the user form using the Django template language:
class ProfileEditView(LoginRequiredMixin, CheckUserIsOwner, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile-edit-page.html'

    def get_success_url(self) -> str:
        return reverse_lazy('accounts:details', kwargs={'pk': self.object.pk})
def profile_delete(request: HttpRequest,pk:int) -> HttpResponse:
    user =UserModel.objects.get(pk=pk)
    if request.user.is_authenticated and request.user.pk==user.pk:
        if request.method == "POST":
            user.delete()
            return redirect('common:home')
    else:
        return HttpResponseForbidden()

    return render(request, 'accounts/profile-delete-page.html')

