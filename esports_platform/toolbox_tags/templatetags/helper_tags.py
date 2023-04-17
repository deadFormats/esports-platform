from django import forms
from django import template
from django.forms import BoundField
from django.template.loader import get_template
from django.utils.safestring import mark_safe 


register = template.Library()


BULMA_COLUMN_COUNT = 1


@register.simple_tag
def render_cdn_link(cdn_link):
    html_tag = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/brands.min.css">'
    return mark_safe(cdn_link)


@register.filter
def bulma(element):
    markup_classes = {
        'label': '',
        'value': '',
        'single-value': ''
    }

    return render(element, markup_classes)



@register.filter
def add_input_classes(field):
    if not is_checkbox(field) and not is_multiple_checkbox(field) and not is_radio(field) and not is_file(field):
        field_classes = field.field.widget.attrs.get("class", '')
        field_classes += " control"
        field.field.widget.attrs['class'] = field_classes


def render(element, markup_classes):
    if isinstance(element, BoundField):
        add_input_classes(element)
        template = get_template("bulma/forms/field.html")
        context = {
            'field': element,
            'classes': markup_classes,
            'form': element.form
        }
    else:
        has_management = getattr(element, 'management_form', None)
        if has_management:
            for form in element.forms:
                for field in form.visible_fields():
                    add_input_classes(field)

            template = get_template('bulma/forms/formset.html')
            context = {
                'formset': element,
                'classes': markup_classes
            }
        else:
            for field in element.visible_fields():
                add_input_classes(field)

            template = get_template('bulma/forms/form.html')
            context = {
                'form': element,
                'classes': markup_classes
            }

    return template.render(context)



@register.filter
def widget_type(field):
    return type(field.field.widget)


@register.filter
def is_select(field):
    return widget_type(field) == forms.Select 


@register.filter
def is_select_multiple(field):
    return widget_type(field) == forms.SelectMultiple


@register.filter
def is_textarea(field):
    return widget_type(field) == forms.Textarea


@register.filter
def is_input(field):
    widgets = [
        forms.TextInput,
        forms.NumberInput,
        forms.EmailInput,
        forms.PasswordInput,
        forms.URLInput
    ]

    for widget in widgets:
        if widget_type(field) == widget:
            return True 
        
    else:
        return False
    

@register.filter
def is_checkbox(field):
    return widget_type(field) == forms.CheckboxInput


@register.filter
def is_checkbox_multiple(field):
    return widget_type(field) == forms.CheckboxSelectMultiple 


@register.filter
def is_radio(field):
    return widget_type(field) == forms.RadioSelect


@register.filter
def is_file(field):
    return widget_type(field) == forms.FileInput


@register.filter
def add_class(field, css_class):
    if len(field.errors) > 0:
        css_class += ' is-danger'
    field_classes = field.field.widget.attrs.get('class', '')
    field_classes += f' {css_class}'
    return field.as_widget(attrs={'class': field_classes})


@register.filter
def bulma_message(tag):
    return {
        'error': 'danger'
    }.get(tag, tag)