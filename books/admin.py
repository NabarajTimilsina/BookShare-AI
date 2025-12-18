from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # What columns to display in list view
    list_display = ('title', 'author', 'uploaded_at', 'summary_preview', 'has_pdf')
    
    # Make columns clickable for editing
    list_display_links = ('title', 'author')
    
    # Add filters on the right sidebar
    list_filter = ('uploaded_at',)
    
    # Search box functionality
    search_fields = ('title', 'author', 'summary')
    
    # Actions dropdown (top of list)
    actions = ['approve_books', 'delete_selected']
    
    # How records are ordered
    ordering = ('-uploaded_at',)  # newest first
    
    # Fields to show in edit form (grouped nicely)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'summary')
        }),
        ('File Information', {
            'fields': ('pdf_file', 'uploaded_at'),
            'classes': ('collapse',)  # Collapsible section
        }),
    )
    
    # Read-only fields (can't edit)
    readonly_fields = ('uploaded_at',)
    
    # Custom columns
    def summary_preview(self, obj):
        """Show first 50 chars of summary"""
        return obj.summary[:50] + '...' if obj.summary else 'No summary'
    summary_preview.short_description = 'Summary Preview'
    
    def has_pdf(self, obj):
        """Checkmark if PDF exists"""
        return bool(obj.pdf_file)
    has_pdf.boolean = True
    has_pdf.short_description = 'Has PDF'
    
    # Custom actions
    def approve_books(self, request, queryset):
        """Custom action example - could send notifications, etc."""
        count = queryset.update()  # Placeholder for actual approval logic
        self.message_user(request, f'{count} books approved.')
    approve_books.short_description = 'Approve selected books'
