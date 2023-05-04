from django.contrib import admin
from django.urls import reverse


class PrimitivePermissionAwareModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # we don't have a "add" permission... but all adding is handled
        # by special methods that go around these permissions anyway
        # TODO: reactivate return False
        return False

    def has_change_permission(self, request, obj=None):
        return bool(
            hasattr(obj, 'has_edit_permission')
            and obj.has_edit_permission(request)
            or not hasattr(obj, 'has_edit_permission')
        )

    def has_delete_permission(self, request, obj=None):
        # we don't have a specific delete permission... so we use change
        return self.has_change_permission(request, obj)

    def _get_post_url(self, obj):
        """
        Needed to retrieve the changelist url as Folder/File can be extended
        and admin url may change
        """
        # Code from django ModelAdmin to determine changelist on the fly
        opts = obj._meta
        return reverse(
            f'admin:{opts.app_label}_{opts.model_name}_changelist',
            current_app=self.admin_site.name,
        )
