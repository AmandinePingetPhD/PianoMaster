from django.contrib import admin
from .models import PianoSheet, Musician, Note


class PianoSheetAdmin(admin.ModelAdmin):
    """Sheet_id read only auto-generation."""
    
    readonly_fields = ('sheet_id',)


class MusicianAdmin(admin.ModelAdmin):
    """User_id read only auto-generation."""

    readonly_fields = ('user_id',)


class NoteAdmin(admin.ModelAdmin):
    """Rating_id read only auto-generation."""

    readonly_fields = ('rating_id',)

admin.site.register(PianoSheet, PianoSheetAdmin)
admin.site.register(Musician, MusicianAdmin)
admin.site.register(Note, NoteAdmin)
