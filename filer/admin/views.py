from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from .. import settings as filer_settings
from ..models import Clipboard, Folder, FolderRoot, tools
from .tools import AdminContext, admin_url_params_encoded, popup_status


class NewFolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ('name',)
        widgets = {
            'name': widgets.AdminTextInputWidget,
        }


@login_required
def make_folder(request, folder_id=None):
    if not folder_id:
        folder_id = request.GET.get('parent_id')
    if not folder_id:
        folder_id = request.POST.get('parent_id')
    if folder_id:
        try:
            folder = Folder.objects.get(id=folder_id)
        except Folder.DoesNotExist:
            raise PermissionDenied
    else:
        folder = None

    if (
        not request.user.is_superuser
        and folder is None
        and not filer_settings.FILER_ALLOW_REGULAR_USERS_TO_ADD_ROOT_FOLDERS
        or not request.user.is_superuser
        and folder is not None
        and not folder.has_add_children_permission(request)
    ):
        raise PermissionDenied
    if request.method == 'POST':
        new_folder_form = NewFolderForm(request.POST)
        if new_folder_form.is_valid():
            new_folder = new_folder_form.save(commit=False)
            if (folder or FolderRoot()).contains_folder(new_folder.name):
                new_folder_form._errors['name'] = new_folder_form.error_class(
                    [_('Folder with this name already exists.')])
            else:
                context = admin.site.each_context(request)
                new_folder.parent = folder
                new_folder.owner = request.user
                new_folder.save()
                return render(request, 'admin/filer/dismiss_popup.html', context)
    else:
        new_folder_form = NewFolderForm()

    context = admin.site.each_context(request)
    context.update({
        'opts': Folder._meta,
        'new_folder_form': new_folder_form,
        'is_popup': popup_status(request),
        'filer_admin_context': AdminContext(request),
    })
    return render(request, 'admin/filer/folder/new_folder_form.html', context)


@login_required
def paste_clipboard_to_folder(request):
    # TODO: cleanly remove Clipboard code if it is no longer needed
    return HttpResponseBadRequest('not implemented anymore')


@login_required
def discard_clipboard(request):
    # TODO: cleanly remove Clipboard code if it is no longer needed
    return HttpResponseBadRequest('not implemented anymore')


@login_required
def delete_clipboard(request):
    # TODO: cleanly remove Clipboard code if it is no longer needed
    return HttpResponseBadRequest('not implemented anymore')
