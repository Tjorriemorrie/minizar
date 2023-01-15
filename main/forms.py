from crispy_forms import layout
from crispy_forms.helper import FormHelper
from django import forms
from django.urls import reverse
from django.utils.timezone import now

from main.models import Game


class GameStatusForm(forms.ModelForm):
    class Meta:
        fields = ['status']
        model = Game

    def __init__(self, *args, **kwargs):
        """Create fields dynamically."""
        # self._add_dynamic_fields()
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'row row-cols-lg-auto g-3 align-items-center'
        self.helper.attrs = {'hx-post': reverse('hxg_status', args=[self.instance.id])}
        # self.helper.layout = layout.Layout(
        #     layout.Fieldset(
        #         '',
        #         layout.Field('status', label_class='col-form-label'),
        #     ),
        #     layout.Submit('submit', 'save status', css_class='btn btn-secondary'),
        # )
        self.helper.add_input(layout.Submit('submit', 'update status'))

    def save(self, commit=True):
        if 10 <= self.cleaned_data['status'] < 19:
            self.instance.started_at = now()
            self.instance.ended_at = None
        if 20 <= self.cleaned_data['status']:
            self.instance.ended_at = now()
        return super().save(commit)

    # def _add_dynamic_fields(self):
    #     d = self.state.data
    #     s = self.state.to_play
    #     fields = {}  # type: Dict[str, Any]
    #     for k, v in self.prev_data.items():
    #         fields[k] = forms.CharField(widget=forms.HiddenInput, initial=v)
    #     fields['units'] = forms.CharField(widget=forms.HiddenInput, initial=True)
    #
    #     disableds = {}
    #     movements = {}
    #     links = d['map'][self.prev_data['trgt']]['links']
    #     # add rebel base space units as well if target/adjacent system
    #     if s == c.REBEL and not d['map'][c.SYSTEM_REBEL_BASE]['revealed']:
    #         base_link = d['map'][c.SYSTEM_REBEL_BASE]['system_key']
    #         if base_link == self.prev_data['trgt'] or base_link in links:
    #             links.append(c.SYSTEM_REBEL_BASE)
    #     for link_key in links:
    #         system = d['map'][link_key]
    #
    #         # cannot move units from another system that has a leader in it
    #         nc_ldrs = [l for l in system['leaders'][s] if l['ring'] not in c.CAPTURED_RINGS]
    #         if nc_ldrs:
    #             continue
    #
    #         for terrain in [c.TERRAIN_SPACE, c.TERRAIN_GROUND]:
    #             for ix, unit in enumerate(system[terrain][s]):
    #                 suffix = f'(cap={unit["capacity"]})'
    #                 suffix = unit['transport'] and '(T)' or suffix
    #                 suffix = unit['immobile'] and '(immobile)' or suffix
    #                 bf_key = f'{link_key}_{terrain}_{ix}'
    #                 bf_lbl = f'{system["name"]}: {unit["name"]} {suffix}'
    #                 if unit['immobile']:
    #                     disableds[bf_key] = forms.BooleanField(
    #                         required=False, initial=False, label=bf_lbl, disabled=True)
    #                 else:
    #                     movements[bf_key] = forms.BooleanField(
    #                         required=False, initial=True, label=bf_lbl)
    #     if not movements:
    #         fields = {'fail': forms.CharField(label='', disabled=True, initial='No units can be moved')}
    #     else:
    #         fields.update(disableds)
    #         fields.update(movements)
    #     self.base_fields = fields
    #     self.movements = movements  # saved for simulation
